# CH_Handle (charging handle) as native geometry.
#
# The knob is an exact body of revolution about the Y axis at (X -286.80,
# Z 48.875) - first-hit radius agrees to 0.008 mm across 64 rays at every
# station, so it is turned, not sculpted. Built as a stack of cone segments
# through the measured radius profile, exactly like the barrel jacket.
import adsk.core as c, adsk.fusion as f
BT = f.BooleanTypes
T = tbm()

AXIS_X, AXIS_Z = -286.80, 48.875     # the knob's axis of revolution
BOSS = (-293.60, -8.02, 19.00, -71.0, -48.5)   # x, z, dia, y0, y1

COMPONENT, PART = '50_Print_Charging', 'PR-41-CH-Handle'
comp, KEEP = begin_part(root, COMPONENT, PART)
cleanup(comp)

# knob: one true revolve of the measured radius profile
pts = [(AXIS_X, y, AXIS_Z + r) for (y, r) in KNOB]
knob = revolve_profile(comp, plane_at(comp, 'x', AXIS_X), pts,
                       (AXIS_X, KNOB[0][0], AXIS_Z), (AXIS_X, KNOB[-1][0], AXIS_Z))
acc = T.copy(knob)
print('  knob: revolve, faces=%d vol=%.2f solid=%s' % (knob.faces.count, knob.volume, knob.isSolid))

# mounting plate, then the flat arm that clamps to the carrier
plate = extrude_region(comp, -58.0, -48.0, CH_BODY, 'y')
arm = extrude_region(comp, -48.0, -38.0, CH_ARM, 'y')
print('  plate: faces=%d vol=%.2f   arm: faces=%d vol=%.2f' % (
    plate.faces.count, plate.volume, arm.faces.count, arm.volume))
T.booleanOperation(acc, T.copy(plate), BT.UnionBooleanType)
T.booleanOperation(acc, T.copy(arm), BT.UnionBooleanType)

bx, bz, bd, by0, by1 = BOSS
T.booleanOperation(acc, cyl((bx, by0, bz), (bx, by1, bz), bd), BT.UnionBooleanType)

# four d8 blind pockets for the captive nuts, entered from the outboard face
for (x, z, dia) in CH_POCKETS:
    T.booleanOperation(acc, cyl((x, -37.9, z), (x, -47.0, z), dia), BT.DifferenceBooleanType)

nb = finish_part(comp, KEEP, acc, PART)
report(nb, 'CH_HANDLE', 116.17)
