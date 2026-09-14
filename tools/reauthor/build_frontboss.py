# FrontBoss (front sight assembly and its mount) as native geometry.
#
# Six prismatic runs along X. The rear face is a set of twelve plain rectangular
# standoff ribs; the front carries the sight hood and post.
import adsk.core as c, adsk.fusion as f
BT = f.BooleanTypes
T = tbm()

RUNS = [(FB_RIBS, -13.35, -3.00),
        (FB_B,     -3.00,  0.00),
        (FB_C,      0.00,  3.50),
        (FB_D,      3.50,  8.00),
        (FB_E,      8.00, 19.00),
        (FB_F,     19.00, 24.80)]

COMPONENT, PART = '20_Print_Receiver', 'PR-17-Front-Sight-Boss'
comp, KEEP = begin_part(root, COMPONENT, PART)
cleanup(comp)

segs = []
for regs, x0, x1 in RUNS:
    for r in regs:
        segs.append(extrude_region(comp, x0, x1, r))
print('  %d segments' % len(segs))

acc = T.copy(segs[0])
for b in segs[1:]:
    T.booleanOperation(acc, T.copy(b), BT.UnionBooleanType)

# TRANSVERSE HOLES — these run side to side along Y, and a reconstruction stacked
# from YZ sections physically cannot represent one: each X run captures a different
# chord of the circle and extrudes it prismatically, so a round bore comes out as a
# stack of stepped slots. The first pass missed them entirely and left only those
# stepped slivers. Cut them as real cylinders instead.
#
# The pin bore passes through four Y bands at X -9: the outer ears at |Y| 22.35..30
# and the inner ribs at |Y| 18..19.18. The steel hinge tab interleaves in the gap
# between them, which is why the bore has to line up with it exactly.
PIN_X, PIN_Z, PIN_DIA = -9.00, 62.50, 6.65
# The hinge ears are built as separate rib slabs stopping at Z 59.4 and resuming at
# Z 65.7, so the pin bore was never a hole at all - it was the SQUARE GAP between
# two slabs. Fill that gap across the bore's footprint in each ear, then drill it
# round. The four ears sit at these Y bands (measured off the donor at X -9).
EARS = ((-30.00, -22.35), (-19.18, -18.00), (18.00, 19.18), (22.35, 30.00))
for (ey0, ey1) in EARS:
    T.booleanOperation(acc, box(PIN_X - 3.6, PIN_X + 3.6, ey0, ey1, 59.0, 66.0),
                       BT.UnionBooleanType)
T.booleanOperation(acc, cyl((PIN_X, -34.0, PIN_Z), (PIN_X, 34.0, PIN_Z), PIN_DIA),
                   BT.DifferenceBooleanType)

# countersunk screw hole low on the front face, both sides: d5.96 countersink
# closing to a d1.5 pilot by |Y| 28
SCR_X, SCR_Z, SCR_PILOT, SCR_CSK = 14.72, -38.20, 1.50, 5.96
T.booleanOperation(acc, cyl((SCR_X, -34.0, SCR_Z), (SCR_X, 34.0, SCR_Z), SCR_PILOT),
                   BT.DifferenceBooleanType)
for sy in (-1.0, 1.0):
    T.booleanOperation(acc, cyl((SCR_X, sy*30.2, SCR_Z), (SCR_X, sy*27.9, SCR_Z),
                                SCR_CSK, SCR_PILOT), BT.DifferenceBooleanType)

# Domed bosses on both outer faces. These are round-head rivets exactly like the
# ones on the side panels — fitted to a sphere off the donor at R 3.34 about
# |Y| 28.95, deviation 0.02–0.07 mm. Missing them was why this part looked wrong:
# with no dome covering the view, the thin internal slots behind them at |Y| 17
# showed straight through and read as a jagged striped square.
BOSS_DOMES = ((-0.97, 62.82), (14.83, 58.32), (14.50, 38.90))
BOSS_YC, BOSS_R = 28.95, 3.38
# The bosses are round-head rivet domes, and a reconstruction stacked from YZ
# sections cannot hold one: each X run catches a different chord and extrudes it,
# stacking into a staircase that reads as a striped square. Worse, FB_B is sampled
# at X -2 which is *inside* a boss footprint, so its outline carries the boss's
# |Y| 32.1 right across the section.
#
# Nothing lives outboard of |Y| 30 above Z 48 except the two upper bosses, so clip
# that off; clear a d12 column for the lower one; then add all six as real domes.
for sy in (-1.0, 1.0):
    T.booleanOperation(acc, box(-20.0, 30.0, sy*30.0, sy*60.0, 48.0, 100.0),
                       BT.DifferenceBooleanType)
T.booleanOperation(acc, cyl((14.50, -30.0, 38.90), (14.50, -42.0, 38.90), 12.0),
                   BT.DifferenceBooleanType)
T.booleanOperation(acc, cyl((14.50,  30.0, 38.90), (14.50,  42.0, 38.90), 12.0),
                   BT.DifferenceBooleanType)
for (bx, bz) in BOSS_DOMES:
    for sy in (-1.0, 1.0):
        T.booleanOperation(acc, dome(bx, bz, BOSS_YC, BOSS_R, sy), BT.UnionBooleanType)

nb = finish_part(comp, KEEP, acc, PART)
report(nb, 'FRONTBOSS', 108.08)
