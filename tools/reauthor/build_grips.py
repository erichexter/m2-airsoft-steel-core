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
REAR_BOSS = (-645.5, -628.0, 34.80)   # x0, x1, dia - round, on the centre axis

COMPONENT, PART = '40_Print_Grip', 'PR-31-Spade-Grips'
comp, KEEP = begin_part(root, COMPONENT, PART)
cleanup(comp)

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

# The rear of the spine is a round boss, not the square end the plan sections give.
rx0, rx1, rdia = REAR_BOSS
keep = box(rx1, -520.0, -90.0, 90.0, -90.0, 90.0)
T.booleanOperation(keep, cyl((rx0, 0.0, 0.0), (rx1, 0.0, 0.0), rdia), BT.UnionBooleanType)
T.booleanOperation(acc, keep, BT.IntersectionBooleanType)
print('  after rear boss trim: %.2f' % acc.volume)

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
