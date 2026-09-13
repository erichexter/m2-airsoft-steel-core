# Top1 (top deck strip) as native geometry. Constant-width plate, Y +/-25.8,
# with a raised crown, a tall centre block, ramped ends and six blind M3 holes.
import adsk.core as c, adsk.fusion as f
BT = f.BooleanTypes
T = tbm()

occ = None
for o in root.occurrences:
    if o.name.startswith('Top1_Native'): occ = o
if occ is None:
    occ = root.occurrences.addNewComponent(c.Matrix3D.create()); occ.component.name = 'Top1_Native'
comp = occ.component
for b in list(comp.bRepBodies): b.deleteMe()
cleanup(comp)

segs = [
    extrude_region(comp, -560.6, -552.6, PA),   # rear end, deep underside notch
    extrude_region(comp, -552.6, -535.0, PB),   # shallower notch
    extrude_region(comp, -535.0, -382.5, PC),   # main run with the crown
    extrude_region(comp, -382.5, -334.3, PG),   # plain plate to the front
    extrude_region(comp, -495.0, -432.5, PE),   # tall centre walls
    extrude_region(comp, -482.5, -442.5, PD),   # + the bridge between them
]
for i, b in enumerate(segs):
    print('  seg %d: faces=%-3d vol=%7.2f solid=%s' % (i, b.faces.count, b.volume, b.isSolid))

acc = T.copy(segs[0])
for b in segs[1:]:
    T.booleanOperation(acc, T.copy(b), BT.UnionBooleanType)

# ramp the ends of the tall block down to the crown - straight slopes, cut as
# triangular prisms in the XZ plane and swept across the full width
front = extrude_region(comp, -30.0, 30.0,
    {'outer': [(71.2, -495.0), (96.5, -495.0), (96.5, -482.5)], 'holes': [], 'net': 0.5*25.3*12.5}, 'y')
rear = extrude_region(comp, -30.0, 30.0,
    {'outer': [(71.2, -432.5), (96.5, -432.5), (96.5, -442.5)], 'holes': [], 'net': 0.5*25.3*10.0}, 'y')
T.booleanOperation(acc, T.copy(front), BT.DifferenceBooleanType)
T.booleanOperation(acc, T.copy(rear), BT.DifferenceBooleanType)

# Six d8 bosses standing 0.35 mm proud of the underside at the fastener positions -
# the same bridging bosses the side panels carry, landing the deck on the tube.
# The first pass missed them and left the part 0.35 mm short in Z.
for x in (-526.7, -413.5, -356.9):
    for y in (18.0, -18.0):
        T.booleanOperation(acc, cyl((x, y, 30.15), (x, y, 30.50), 8.0), BT.UnionBooleanType)

# six blind d3.40 fastening holes, up through the boss from the underside
for x in (-526.7, -413.5, -356.9):
    for y in (18.0, -18.0):
        T.booleanOperation(acc, cyl((x, y, 30.10), (x, y, 51.0), 3.40), BT.DifferenceBooleanType)

for b in list(comp.bRepBodies): b.deleteMe()
nb = comp.bRepBodies.add(acc); nb.name = 'Top1_native'
cleanup(comp)
report(nb, 'TOP1', 472.87)
