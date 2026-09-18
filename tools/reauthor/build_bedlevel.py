# Bed levelling test artifact, as native geometry, so it is visible in Fusion.
#
# tools/bedlevel.js IS THE SOURCE OF TRUTH for stl/test/bed-level-squares.stl. This
# script exists so the thing can be seen and measured in the model too; it builds the
# same shape from the same numbers. If you change one, change the other - the constants
# below are duplicated deliberately and there is nothing keeping them in step.
#
# TWO THINGS ABOUT WHERE IT LIVES, both deliberate:
#
# 1. It goes in a 00_Ref_* component. Every clash and audit script in this repo skips
#    that prefix, so the artifact cannot contaminate them. Without that, a 290mm square
#    would intersect the tube and most of the skins and every interference check would
#    come back garbage.
#
# 2. It is parked at Z -400, well clear of the gun, which bottoms out at Z -92 at the
#    pintle tabs. Even with the checks excluding it, having it lying through the middle
#    of the assembly makes every render and section useless.
import adsk.core as c, adsk.fusion as f
BT = f.BooleanTypes
T = tbm()

H = 0.30          # one layer at 0.3mm - see bedlevel.js for why this is not 0.2
W = 1.20          # two 0.6mm beads
FRAMES = [290, 230, 170, 110, 50]
CENTRE = 20
KEY = 10
PARK_Z = -400.0   # out of the way of the gun

COMPONENT, PART = '00_Ref_Test_Artifacts', 'RF-90-Bed-Level-Squares'
comp, KEEP = begin_part(root, COMPONENT, PART)
cleanup(comp)

acc = None


def add(b):
    global acc
    if acc is None:
        acc = b
    else:
        T.booleanOperation(acc, b, BT.UnionBooleanType)


for s in FRAMES:
    o = s / 2.0
    i = o - W
    # A ring as four bars. Unlike the STL generator this CAN overlap at the corners,
    # because a boolean union resolves it into one clean shell - the STL version had to
    # build a proper annulus by hand precisely because it has no boolean available.
    add(box(-o, o, -o, -i, PARK_Z, PARK_Z + H))
    add(box(-o, o, i, o, PARK_Z, PARK_Z + H))
    add(box(-o, -i, -i, i, PARK_Z, PARK_Z + H))
    add(box(i, o, -i, i, PARK_Z, PARK_Z + H))

add(box(-CENTRE / 2, CENTRE / 2, -CENTRE / 2, CENTRE / 2, PARK_Z, PARK_Z + H))
add(box(-130, -130 + KEY, -130, -130 + KEY, PARK_Z, PARK_Z + H))

nb = finish_part(comp, KEEP, acc, PART)
print('%s: %d faces, %d shells, %.3f cm3, parked at Z %.0f'
      % (PART, nb.faces.count, nb.shells.count, nb.volume, PARK_Z))
bb = nb.boundingBox
print('  spans X %.1f..%.1f  Y %.1f..%.1f  Z %.2f..%.2f'
      % (bb.minPoint.x * 10, bb.maxPoint.x * 10, bb.minPoint.y * 10,
         bb.maxPoint.y * 10, bb.minPoint.z * 10, bb.maxPoint.z * 10))
