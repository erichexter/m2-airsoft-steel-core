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

def _newest(comp, n_before):
    """The body a feature just made.

    Do NOT use feature.bodies.item(0): in a direct-design document that hands back
    the component's FIRST body, not the new one. It looks correct only while the
    component is empty, which is how it went unnoticed until several parts started
    sharing one. New bodies are appended, so take the last."""
    n = comp.bRepBodies.count
    if n <= n_before:
        raise RuntimeError('feature produced no new body')
    return comp.bRepBodies.item(n - 1)

def extrude_region(comp, x0, x1, region, axis='x'):
    pr = sketch_region_yz(comp, x0, region, axis)
    ei = comp.features.extrudeFeatures.createInput(
        pr, f.FeatureOperations.NewBodyFeatureOperation)
    ei.setDistanceExtent(False, c.ValueInput.createByReal((x1 - x0)/10.0))
    n0 = comp.bRepBodies.count
    comp.features.extrudeFeatures.add(ei)
    return _newest(comp, n0)

def loft_regions(comp, stations, axis='x'):
    """stations = [(smm, region), ...] -> lofted body"""
    li = comp.features.loftFeatures.createInput(f.FeatureOperations.NewBodyFeatureOperation)
    for (x, r) in stations:
        li.loftSections.add(sketch_region_yz(comp, x, r, axis))
    li.isSolid = True
    n0 = comp.bRepBodies.count
    comp.features.loftFeatures.add(li)
    return _newest(comp, n0)

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

def sphere(centre, radius):
    """radius in mm."""
    return tbm().createSphere(
        c.Point3D.create(centre[0]/10., centre[1]/10., centre[2]/10.), radius/10.)

def dome(x, z, y_centre, radius, sign=1.0):
    """A rivet head. The sphere centre sits *inside* the panel, so unioning it
    leaves only the spherical cap standing proud - which is what a round-head
    rivet actually is. y_centre is given as |Y|."""
    return sphere((x, sign * y_centre, z), radius)

def revolve_profile(comp, plane, pts3d, axis_p0, axis_p1, smooth=True):
    """A true surface of revolution. pts3d are model-space points tracing the
    OUTER profile; axis_p0/axis_p1 are two points on the axis, in the same plane.
    Closing the profile back along the axis gives the end faces.

    Use this rather than a stack of cone segments: a 44-segment stack renders as
    visible rings and reads as knurling, which is exactly what these turned parts
    are not."""
    sk = comp.sketches.add(plane); sk.isLightBulbOn = False
    col = c.ObjectCollection.create()
    for p in pts3d:
        col.add(sk.modelToSketchSpace(c.Point3D.create(p[0]/10.0, p[1]/10.0, p[2]/10.0)))
    lines = sk.sketchCurves.sketchLines
    if smooth:
        crv = sk.sketchCurves.sketchFittedSplines.add(col)
        p_start, p_end = crv.startSketchPoint, crv.endSketchPoint
    else:
        segs = [lines.addByTwoPoints(col.item(i), col.item(i+1)) for i in range(col.count-1)]
        p_start, p_end = segs[0].startSketchPoint, segs[-1].endSketchPoint
    a0 = sk.modelToSketchSpace(c.Point3D.create(axis_p0[0]/10.0, axis_p0[1]/10.0, axis_p0[2]/10.0))
    a1 = sk.modelToSketchSpace(c.Point3D.create(axis_p1[0]/10.0, axis_p1[1]/10.0, axis_p1[2]/10.0))
    l1 = lines.addByTwoPoints(p_end, a1)
    axl = lines.addByTwoPoints(a1, a0)
    lines.addByTwoPoints(a0, p_start)
    if sk.profiles.count == 0:
        raise RuntimeError('revolve profile did not close')
    best, ba = None, -1
    for pr in sk.profiles:
        a = pr.areaProperties(f.CalculationAccuracy.LowCalculationAccuracy).area
        if a > ba: ba, best = a, pr
    ri = comp.features.revolveFeatures.createInput(
        best, axl, f.FeatureOperations.NewBodyFeatureOperation)
    ri.setAngleExtent(False, c.ValueInput.createByReal(2 * 3.14159265358979))
    n0 = comp.bRepBodies.count
    comp.features.revolveFeatures.add(ri)
    return _newest(comp, n0)

def part_component(root, name):
    """Get-or-create a named grouping component."""
    for o in root.occurrences:
        if o.name.split(':')[0] == name: return o.component
    o = root.occurrences.addNewComponent(c.Matrix3D.create())
    o.component.name = name
    return o.component

def begin_part(root, comp_name, part_name):
    """Start a build. Several parts now share a component, so remove only the
    previous version of THIS part and remember what else was already there."""
    comp = part_component(root, comp_name)
    for b in list(comp.bRepBodies):
        if b.name == part_name: b.deleteMe()
    return comp, set(b.name for b in comp.bRepBodies)

def finish_part(comp, keep, body, part_name):
    """Drop the scratch bodies this build created (never its neighbours), add the
    finished part under its catalogue name, and clear the sketches."""
    for b in list(comp.bRepBodies):
        if b.name not in keep: b.deleteMe()
    nb = comp.bRepBodies.add(body)
    nb.name = part_name
    cleanup(comp)
    return nb

def relieve(acc, tool, clearance=0.25):
    """Subtract `tool` with a little clearance around it.

    Cutting a printed part against steel with ZERO clearance leaves faces exactly
    coincident, which tessellates into non-manifold edges - and leaves a part that
    is a press fit at best. Subtracting the tool plus six axis-offset copies
    thickens the cut by `clearance` on every axis-aligned face, which is what the
    steel faces mostly are."""
    t = tbm()
    t.booleanOperation(acc, t.copy(tool), f.BooleanTypes.DifferenceBooleanType)
    d = clearance / 10.0
    for vec in ((d,0,0), (-d,0,0), (0,d,0), (0,-d,0), (0,0,d), (0,0,-d)):
        cp = t.copy(tool)
        m = c.Matrix3D.create()
        m.translation = c.Vector3D.create(*vec)
        t.transform(cp, m)
        try:
            t.booleanOperation(acc, cp, f.BooleanTypes.DifferenceBooleanType)
        except:
            pass
    return acc

def drop_debris(acc, max_debris_mm3=200.0):
    """Delete stray shells left behind by relief cuts.

    Slicing a thin feature can leave a wafer a couple of tenths thick floating
    free. It is still 'solid' and still one body, but it is three shells, and a
    slicer sees three objects. Cut away anything whose bounding box is smaller
    than max_debris_mm3."""
    t = tbm()
    for _ in range(12):
        if acc.shells.count <= 1: return acc
        worst, worst_v = None, None
        for sh in acc.shells:
            bb = sh.boundingBox
            v = ((bb.maxPoint.x-bb.minPoint.x) * (bb.maxPoint.y-bb.minPoint.y) *
                 (bb.maxPoint.z-bb.minPoint.z)) * 1000.0     # cm3 -> mm3
            if worst_v is None or v < worst_v: worst, worst_v = bb, v
        if worst_v is None or worst_v > max_debris_mm3:
            return acc                                       # nothing small enough
        pad = 0.001
        cut = t.createBox(c.OrientedBoundingBox3D.create(
            c.Point3D.create((worst.minPoint.x+worst.maxPoint.x)/2,
                             (worst.minPoint.y+worst.maxPoint.y)/2,
                             (worst.minPoint.z+worst.maxPoint.z)/2),
            c.Vector3D.create(1,0,0), c.Vector3D.create(0,1,0),
            (worst.maxPoint.x-worst.minPoint.x)+pad,
            (worst.maxPoint.y-worst.minPoint.y)+pad,
            (worst.maxPoint.z-worst.minPoint.z)+pad))
        try:
            t.booleanOperation(acc, cut, f.BooleanTypes.DifferenceBooleanType)
        except:
            return acc
    return acc

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
