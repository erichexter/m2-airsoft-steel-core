# Grip_Assembly (spade grips) as native geometry.
#
# Two handgrips, each an exact body of revolution about a vertical axis at
# (X -613.81, Y +/-62.23) - first-hit radius agrees to 0.006 mm across 48 rays,
# so they are turned, not knurled. Built as cone stacks through the measured
# radius profile, the same way as the barrel jacket and the CH knob.
#
# The frame is a stack of horizontal plan sections. An earlier attempt extruded
# the fore-aft SIDE profile across the full width and trimmed it against one plan
# section per half; that came out 10% light, because the spine's plan changes
# shape the whole way up - it is not a slab with a constant outline.
import adsk.core as c, adsk.fusion as f
BT = f.BooleanTypes
T = tbm()

GRIP_X, GRIP_Y = -613.81, 62.23
# Buffer tube, measured off the donor: a true cylinder r 17.389 (spread 0.015 mm
# over 64 rays) from X -642.17 forward, chamfered back to r 13.741 at the end face.
BUF_END_X, BUF_CHAMFER_X, BUF_JOIN_X = -645.20, -642.17, -626.00
BUF_DIA, BUF_END_DIA = 34.78, 27.48

COMPONENT, PART = '40_Print_Grip', 'PR-31-Spade-Grips'
comp, KEEP = begin_part(root, COMPONENT, PART)
cleanup(comp)

# Stack the plan sections as prisms. Lofting between them instead was tried, to
# smooth the terrace at each band boundary, and it was worse on every measure:
# -6.1% on volume against -2.0% (a loft cuts the corner where a mid-band prism
# averages it), two shells instead of one, two new clashes into the deck and the
# bottom rail, and 415 NURBS faces where the prisms give planes. The visible
# stepping is the honest cost of a construction that is other-wise more accurate.
acc = None
nseg = 0
for (z0, z1, regions) in BANDS:
    for r in regions:
        b = T.copy(extrude_region(comp, z0, z1, r, 'z'))
        nseg += 1
        if acc is None:
            acc = b
        else:
            T.booleanOperation(acc, b, BT.UnionBooleanType)
print('  frame: %d banded plan sections, vol %.2f' % (nseg, acc.volume))

# The buffer tube is a PLAIN CYLINDER. Earlier this was made by intersecting the
# plan-section stack with a cylinder, which left the stack's stepped approximation
# showing through instead of a clean turned part. Cut the stack off behind the
# frame and add the real thing: d34.78 measured to 0.015 mm across 64 rays, with a
# chamfered end and a wedge slot across the face.
#
# Do this BEFORE the handgrips are added - they reach back to X -629.7, so a blanket
# cut behind X -628 is only safe while they are not there yet.
T.booleanOperation(acc, box(-700.0, -628.0, -95.0, 95.0, -95.0, 95.0), BT.DifferenceBooleanType)
T.booleanOperation(acc, cyl((BUF_CHAMFER_X, 0.0, 0.0), (BUF_JOIN_X, 0.0, 0.0), BUF_DIA),
                   BT.UnionBooleanType)
T.booleanOperation(acc, cyl((BUF_END_X, 0.0, 0.0), (BUF_CHAMFER_X, 0.0, 0.0),
                            BUF_END_DIA, BUF_DIA), BT.UnionBooleanType)
# wedge slot across the end face: 3.3 mm at the face, closing to nothing at X -643.45
slot = extrude_region(comp, -25.0, 25.0,
    {'outer': [(1.65, BUF_END_X - 0.2), (-1.65, BUF_END_X - 0.2), (0.0, -643.45)],
     'holes': [], 'net': 0.5 * 3.3 * abs(-643.45 - (BUF_END_X - 0.2))}, 'y')
T.booleanOperation(acc, T.copy(slot), BT.DifferenceBooleanType)
print('  buffer tube: d%.2f cylinder + chamfer + end slot -> %.2f cm3' % (BUF_DIA, acc.volume))

for sy in (+1.0, -1.0):
    pts = [(GRIP_X + r, sy * GRIP_Y, z) for (z, r) in GRIP]
    hg = revolve_profile(comp, plane_at(comp, 'y', sy * GRIP_Y), pts,
                         (GRIP_X, sy * GRIP_Y, GRIP[0][0]), (GRIP_X, sy * GRIP_Y, GRIP[-1][0]))
    print('  handgrip: revolve faces=%d vol=%.2f solid=%s' % (hg.faces.count, hg.volume, hg.isSolid))
    T.booleanOperation(acc, T.copy(hg), BT.UnionBooleanType)

# The mounting tongue reaches into the receiver, where the backplate and the tube
# already are. Relieve it against the steel so the grip actually seats - the donor
# has no material in that corridor either.
# Match on the catalogue prefixes, not hard-coded body names: renaming the model
# once made these lookups miss silently and the relief cuts quietly did nothing.
# 0.25 mm severed the thin mounting tongue into its own shell; 0.05 is enough to
# stop faces landing exactly coincident (which tessellates non-manifold) without
# cutting anything free.
RELIEF_CLEARANCE = 0.05
RELIEVE = ('ST-01-Core-Tube', 'ST-02-Backplate',
           'ST-03-Backplate-Boss-L', 'ST-03-Backplate-Boss-R')
relieved = 0
for occ2 in root.allOccurrences:
    if occ2.name.split(':')[0] not in ('10_Steel_Core', '11_Steel_Weldments'): continue
    for sb in occ2.bRepBodies:
        if sb.name not in RELIEVE: continue
        try:
            relieve(acc, sb, RELIEF_CLEARANCE); relieved += 1
        except Exception as e:
            print('  ! relief against %s failed: %s' % (sb.name, str(e)[:50]))
print('  after steel relief: %.2f cm3  (%d bodies)' % (acc.volume, relieved))

# The butterfly trigger sits between the handgrips and pivots through about 5.5 deg
# on the pin at (X -552, Z 1). Relieve against its SWEPT path, not just where it
# rests, or it fouls partway through the pull. Near-coincident rotated copies cannot
# be unioned (ASM_EDGECOIN_PROBLEM), so subtract each position on its own.
import math
PIVOT_X, PIVOT_Z = -552.0, 1.0
swept = 0
for occ2 in root.allOccurrences:
    if occ2.name.split(':')[0] != '60_Print_Trigger': continue
    for sb in occ2.bRepBodies:
        if sb.name.startswith('HW-'):
            try: T.booleanOperation(acc, T.copy(sb), BT.DifferenceBooleanType)
            except: pass
            continue
        for deg in (0.0, 1.5, 3.0, 4.5, 6.0):
            tb = T.copy(sb)
            if deg:
                m = c.Matrix3D.create()
                m.setToRotation(math.radians(deg), c.Vector3D.create(0, 1, 0),
                                c.Point3D.create(PIVOT_X/10.0, 0.0, PIVOT_Z/10.0))
                T.transform(tb, m)
            try:
                T.booleanOperation(acc, tb, BT.DifferenceBooleanType); swept += 1
            except: pass
print('  after trigger sweep relief: %.2f cm3  (%d bodies)' % (acc.volume, swept))
before = acc.shells.count
drop_debris(acc)
if acc.shells.count != before:
    print('  dropped %d debris shell(s) left by the relief cuts' % (before - acc.shells.count))

nb = finish_part(comp, KEEP, acc, PART)
report(nb, 'GRIP_ASSEMBLY', 337.40)
