# Sacrificial mouse-ear pads for the two long rear side panels.
#
# WHY THESE PARTS NEED THEM
# PR-11 and PR-12 are 295.6mm long. PLA contracts about 0.4% as it cools, so the part
# tries to shrink ~1.2mm along its length - 0.6mm at each end - and that force peels the
# end corners off the bed. Adhesion is not losing because the glue is weak; it is losing
# because peel at a corner loads a very small area.
#
# WHY A NORMAL BRIM WILL NOT DO IT
# The design deliberately sits at the bed limit: BUILD-NOTES puts the seam at X -265
# because "max forward is X -260.6 before Side_1 exceeds the 300mm bed". At 295.6mm on a
# 300mm bed there is about 1.1mm of margin at each end - nowhere near enough for a brim
# in the direction that matters, which is the direction the part is contracting.
#
# So the pads grow SIDEWAYS instead. Across the part there is 165mm of spare bed, so a
# pad can extend 10mm past the edge in Z while adding only 1mm in X. It still resists the
# lifting moment at the corner, which is the whole job.
#
# These are print aids, not design geometry. They are unioned onto a COPY and written to
# stl/print-aids/, so the fitted model stays clean and nothing downstream sees them.
import adsk.core as c, adsk.fusion as f, os
BT = f.BooleanTypes
T = tbm()

PAD_R = 10.0          # mm
# Two layers at the 0.3mm layer height this is printed at. NOT one, and not a nominal
# 0.2-0.25: a pad thinner than the layer height either vanishes at slice time or gets
# rounded up unpredictably, and a single 0.3 layer tears instead of snapping when you
# pull it off. Re-check this if the layer height changes.
PAD_T = 0.60
# How far a pad may stand past the part's own end.
#
# ZERO, and that is not a safety margin - it is a hard requirement.
#
# The first version used 1.0, which read as conservative against 1.1mm of bed margin.
# It made the part 297.6mm and Creality Print refused to place it at all: "Nothing to
# be sliced ... no object is fully inside the print volume". The slicer agent bracketed
# it by scaling the real mesh - 297.6 rejected, 296.1 rejected, 294.6 slices - while
# PR-18 at 295.6 slices and a featureless box at 297.6 also slices. So the usable
# envelope for real geometry is tighter than the nominal 300 and tighter than for a
# plain bounding box.
#
# At 0 the pads sit tangent to the part's ends and the footprint stays exactly 295.6mm,
# unchanged from the plain part. Nothing is lost by this: the bond the pads add comes
# from the half-disc that overhangs the part SIDEWAYS in Z, which is untouched.
X_PROUD = 0.0

# part, mating axis, bed-face coordinate, outboard direction, corner points of the
# contact patch as (along-X, across) - measured off the exported mesh, not guessed.
PARTS = [
    ('PR-11-Side-Rear-L', 'y', 25.400, +1.0,
     [(-560.60, -66.90), (-560.60, 68.20), (-273.60, -65.50), (-265.00, 43.65)]),
    ('PR-12-Side-Rear-R', 'y', -25.400, -1.0,
     [(-560.60, -66.90), (-560.60, 68.20), (-274.85, -66.90), (-265.00, 43.65)]),
]

OUT = r'C:\Users\eric\Documents\3dprint\m2-airsoft-steel-core\stl\print-aids'
if not os.path.isdir(OUT):
    os.makedirs(OUT)


def find_body(name):
    for occ in root.allOccurrences:
        if occ.name.split(':')[0].startswith('00_Ref'):
            continue
        for b in occ.component.bRepBodies:
            if b.name == name:
                return occ.component, b
    return None, None


em = des.exportManager
for (name, axis, face, outb, corners) in PARTS:
    comp, b = find_body(name)
    if b is None:
        print('%-22s ! not found' % name)
        continue

    xs = [p[0] for p in corners]
    x_lo, x_hi = min(xs), max(xs)
    acc = T.copy(b)
    v0 = acc.volume

    for (px, pz) in corners:
        # push the pad inboard so it stands at most X_PROUD past the end of the part
        if abs(px - x_lo) < abs(px - x_hi):
            cx = px + (PAD_R - X_PROUD)
        else:
            cx = px - (PAD_R - X_PROUD)
        p0 = (cx, face, pz)
        p1 = (cx, face + outb * PAD_T, pz)
        T.booleanOperation(acc, cyl(p0, p1, PAD_R * 2), BT.UnionBooleanType)

    if acc.shells.count != 1 or not acc.isSolid:
        print('%-22s ! %d shells - SKIPPED' % (name, acc.shells.count))
        continue

    bb = acc.boundingBox
    span_x = (bb.maxPoint.x - bb.minPoint.x) * 10.0
    span_z = (bb.maxPoint.z - bb.minPoint.z) * 10.0

    tmp = comp.bRepBodies.add(acc)
    tmp.name = name + '-ears'
    path = os.path.join(OUT, name + '-ears.stl')
    o = em.createSTLExportOptions(tmp, path)
    o.meshRefinement = f.MeshRefinementSettings.MeshRefinementHigh
    o.isBinaryFormat = True
    em.execute(o)
    tmp.deleteMe()

    print('%-22s +%.3f cm3 of pad, footprint %.1f x %.1f mm  (bed 300: %s)'
          % (name, acc.volume - v0, span_x, span_z,
             'FITS with %.1fmm to spare' % (300.0 - span_x) if span_x <= 300.0 else 'TOO BIG'))
