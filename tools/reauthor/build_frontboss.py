# FrontBoss (front sight assembly and its mount) as native geometry.
#
# Six prismatic runs along X. The rear face is a set of twelve plain rectangular
# standoff ribs; the front carries the sight hood and post.
import adsk.core as c, adsk.fusion as f
BT = f.BooleanTypes
T = tbm()

# Two separate things happen between X 7.9 and X 8.75, and collapsing them into one
# run put an 18 mm slab of phantom flange on each side: the wide flange ENDS at
# X 7.90 (|Y| drops 44.78 -> 30.00), and the window only opens at X 8.75. They need
# their own runs.
RUNS = [(FB_RIBS, -13.35, -3.00),
        (FB_B,     -3.00,  0.00),
        (FB_C,      0.00,  3.50),
        (FB_D,      3.50,  7.90),
        (FB_D2,     7.90,  8.75),
        (FB_E,      8.75, 19.00),
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
# Fill the gap across the ENTIRE rib run (X -13.35..-3.0), not just around the
# bore: the donor ear is solid from Z 43.6 right up to 66.8 with nothing but the
# round hole in it. Filling only +/-3.6 about the bore left a 2.4 mm slot running
# out of it at X -5.40..-3.00.
for (ey0, ey1) in EARS:
    T.booleanOperation(acc, box(-13.35, -3.00, ey0, ey1, 59.0, 66.0), BT.UnionBooleanType)
T.booleanOperation(acc, cyl((PIN_X, -34.0, PIN_Z), (PIN_X, 34.0, PIN_Z), PIN_DIA),
                   BT.DifferenceBooleanType)

# The opening between the inner ears does not stop dead at the rib run - it tapers
# shut over X -3.4..-2.0 (7.3 mm tall at -3.2, 4.4 at -2.5, gone by -2.0). FB_B is
# solid across that span, so the gap was being closed off a millimetre early.
T.booleanOperation(acc, T.copy(extrude_region(comp, -18.0, 18.0,
    {'outer': [(66.50, -3.50), (59.20, -3.50), (62.85, -2.00)],
     'holes': [], 'net': 0.5 * 7.30 * 1.50}, 'y')), BT.DifferenceBooleanType)

# countersunk screw hole low on the front face, both sides: d5.96 countersink
# closing to a d1.5 pilot by |Y| 28
# The front mounting hole is a BLIND countersunk pilot, one per side - NOT a
# through hole. Measured on the donor: d5.96 at the |Y| 30.0 face closing to d1.4
# by |Y| 28.0 and bottoming at 27.8. Drilling it straight through, as the first
# attempt did, cut a slot clean across the part and through the window behind it.
SCR_X, SCR_Z = 14.72, -38.20
SCR_FACE, SCR_TIP = 30.05, 27.80
SCR_CSK, SCR_PILOT = 5.96, 1.40
for sy in (-1.0, 1.0):
    T.booleanOperation(acc, cyl((SCR_X, sy*SCR_FACE, SCR_Z), (SCR_X, sy*28.0, SCR_Z),
                                SCR_CSK, SCR_PILOT), BT.DifferenceBooleanType)
    T.booleanOperation(acc, cyl((SCR_X, sy*28.0, SCR_Z), (SCR_X, sy*SCR_TIP, SCR_Z),
                                SCR_PILOT), BT.DifferenceBooleanType)

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

# The scallop in the bottom edge is a CIRCLE - R 8.00 about (X 1.00, Z -33.40),
# least-squares fit to the donor outline at 0.00 mm - cut through the two walls at
# |Y| 25.8..30.0. The prismatic runs approximated it with a four-step staircase.
#
# Fill the band beside it in the walls, then cut the real cylinder. Filling first is
# what makes this work: trimming the staircase back to the arc without filling just
# splits the part, because the staircase corners are load-bearing in this
# reconstruction.
SCALLOP_X, SCALLOP_Z, SCALLOP_R = 1.00, -33.40, 8.00
for (wy0, wy1) in ((-30.0, -25.8), (25.8, 30.0)):
    T.booleanOperation(acc, box(3.0, 9.2, wy0, wy1, -41.6, -25.2), BT.UnionBooleanType)
T.booleanOperation(acc, cyl((SCALLOP_X, -50.0, SCALLOP_Z), (SCALLOP_X, 50.0, SCALLOP_Z),
                            SCALLOP_R * 2), BT.DifferenceBooleanType)

nb = finish_part(comp, KEEP, acc, PART)
report(nb, 'FRONTBOSS', 108.08)
