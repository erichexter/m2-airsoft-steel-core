# Helpers for reauthoring donor skins as native geometry.
# All external dimensions are mm; the Fusion API is cm.
import adsk.core as c, adsk.fusion as f

# axis: which coordinate the section plane is normal to. 'x' -> section is (y,z),
# 'y' -> (z,x), 'z' -> (x,y) - matching the slicer's U/V convention.
_BASE = {'x': 'yZConstructionPlane', 'y': 'xZConstructionPlane', 'z': 'xYConstructionPlane'}
_UV   = {'x': (1, 2), 'y': (2, 0), 'z': (0, 1)}

def plane_at(comp, axis, smm):
    ci = comp.constructionPlanes.createInput()
    ci.setByOffset(getattr(comp, _BASE[axis]), c.ValueInput.createByReal(smm/10.0))
    p = comp.constructionPlanes.add(ci); p.isLightBulbOn = False
    return p

def plane_at_x(comp, xmm):
    return plane_at(comp, 'x', xmm)

def _pt(axis, smm, u, v):
    xyz = [0.0, 0.0, 0.0]
    iu, iv = _UV[axis]
    iw = {'x': 0, 'y': 1, 'z': 2}[axis]
    xyz[iw] = smm/10.0; xyz[iu] = u/10.0; xyz[iv] = v/10.0
    return c.Point3D.create(*xyz)

def _add_loop(sk, xmm, pts, axis='x'):
    col = c.ObjectCollection.create()
    for (u, v) in pts:
        col.add(sk.modelToSketchSpace(_pt(axis, xmm, u, v)))
    n = col.count
    lines = sk.sketchCurves.sketchLines
    for i in range(n):
        lines.addByTwoPoints(col.item(i), col.item((i+1) % n))

def sketch_region_yz(comp, xmm, region, axis='x'):
    """One sketch holding a region's outer loop and its holes. Returns the profile
    whose area matches the region's net area (so holes are excluded, not selected)."""
    sk = comp.sketches.add(plane_at(comp, axis, xmm)); sk.isLightBulbOn = False
    sk.isComputeDeferred = True
    _add_loop(sk, xmm, region['outer'], axis)
    for h in region.get('holes', []):
        _add_loop(sk, xmm, h, axis)
    sk.isComputeDeferred = False
    target = region['net'] / 100.0          # mm2 -> cm2
    best, err = None, 1e9
    for pr in sk.profiles:
        a = pr.areaProperties(f.CalculationAccuracy.MediumCalculationAccuracy).area
        if abs(a - target) < err:
            err, best = abs(a - target), pr
    if best is None:
        raise RuntimeError('no profile at x=%.2f' % xmm)
    if err > 0.02 * max(target, 1.0):
        print('   ! profile at x=%.1f off by %.2f cm2 (want %.2f)' % (xmm, err, target))
    return best

def extrude_region(comp, x0, x1, region, axis='x'):
    pr = sketch_region_yz(comp, x0, region, axis)
    ei = comp.features.extrudeFeatures.createInput(
        pr, f.FeatureOperations.NewBodyFeatureOperation)
    ei.setDistanceExtent(False, c.ValueInput.createByReal((x1 - x0)/10.0))
    return comp.features.extrudeFeatures.add(ei).bodies.item(0)

def loft_regions(comp, stations, axis='x'):
    """stations = [(smm, region), ...] -> lofted body"""
    li = comp.features.loftFeatures.createInput(f.FeatureOperations.NewBodyFeatureOperation)
    for (x, r) in stations:
        li.loftSections.add(sketch_region_yz(comp, x, r, axis))
    li.isSolid = True
    return comp.features.loftFeatures.add(li).bodies.item(0)

# --- temporary-BRep primitives (mm in, cm out) -------------------------------
def tbm(): return f.TemporaryBRepManager.get()

def box(x0, x1, y0, y1, z0, z1):
    bb = c.OrientedBoundingBox3D.create(
        c.Point3D.create((x0+x1)/20.0, (y0+y1)/20.0, (z0+z1)/20.0),
        c.Vector3D.create(1,0,0), c.Vector3D.create(0,1,0),
        abs(x1-x0)/10.0, abs(y1-y0)/10.0, abs(z1-z0)/10.0)
    return tbm().createBox(bb)

def cyl(p0, p1, d, d2=None):
    return tbm().createCylinderOrCone(
        c.Point3D.create(p0[0]/10., p0[1]/10., p0[2]/10.), d/20.,
        c.Point3D.create(p1[0]/10., p1[1]/10., p1[2]/10.), (d if d2 is None else d2)/20.)

def cleanup(comp):
    for s in list(comp.sketches): s.deleteMe()
    for p in list(comp.constructionPlanes): p.deleteMe()

def report(body, name, donor_vol=None):
    kinds = {}
    for fc in body.faces:
        k = fc.geometry.objectType.split('::')[-1]; kinds[k] = kinds.get(k,0)+1
    bb = body.boundingBox
    print('%s: faces=%d vol=%.2f solid=%s shells=%d %s' % (
        name, body.faces.count, body.volume, body.isSolid, body.shells.count, kinds))
    print('   bbox X %.2f..%.2f  Y %.2f..%.2f  Z %.2f..%.2f' % (
        bb.minPoint.x*10, bb.maxPoint.x*10, bb.minPoint.y*10, bb.maxPoint.y*10,
        bb.minPoint.z*10, bb.maxPoint.z*10))
    if donor_vol:
        print('   vs donor %.2f cm3  ->  %+.1f%%' % (donor_vol, 100*(body.volume-donor_vol)/donor_vol))

def rect(u0, u1, v0, v1):
    """A rectangular region ready for sketch_region_yz / loft_regions."""
    return {'outer': [(u0, v0), (u1, v0), (u1, v1), (u0, v1)],
            'holes': [], 'net': abs((u1-u0)*(v1-v0))}
