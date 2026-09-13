# Hatch (top cover) as native geometry: straight-line prismatic runs, a lofted
# transition at each step in width, plus hinge knuckles and the rear sight dome.
import adsk.core as c, adsk.fusion as f
BT = f.BooleanTypes
T = tbm()

occ = None
for o in root.occurrences:
    if o.name.startswith('Hatch_Native'): occ = o
if occ is None:
    occ = root.occurrences.addNewComponent(c.Matrix3D.create()); occ.component.name = 'Hatch_Native'
comp = occ.component
for b in list(comp.bRepBodies): b.deleteMe()
cleanup(comp)

M, FF, FT = MAIN[0], FRONT_FULL[0], FRONT_T[0]
N16, RL = NOSE16[0], REAR_LUG[0]

segs = []
segs.append(extrude_region(comp, -333.0, -119.0, M))      # main run, 214 mm
segs.append(loft_regions(comp, [(-119.0, M), (-108.0, FF)]))   # widen to the front block
segs.append(extrude_region(comp, -108.0, -101.0, FF))
segs.append(extrude_region(comp, -101.0,  -40.0, FT))     # underside opening
segs.append(extrude_region(comp,  -40.0,  -32.0, FF))
segs.append(loft_regions(comp, [(-32.0, FF), (-16.0, N16)]))   # nose taper
segs.append(extrude_region(comp, -16.0, -12.0, N16))
for r in NOSE10:
    segs.append(extrude_region(comp, -12.0, -4.4, r))     # nose + front sight aperture
for i, b in enumerate(segs):
    print('  seg %d: faces=%-3d vol=%7.2f solid=%s' % (i, b.faces.count, b.volume, b.isSolid))

acc = T.copy(segs[0])
for b in segs[1:]:
    T.booleanOperation(acc, T.copy(b), BT.UnionBooleanType)

# hinge knuckles: rounded ribs on the +Y deck, r 3.47 about (Y 24.5, Z 67.03)
for (x0, x1) in ((-314.0, -308.0), (-260.0, -253.0), (-205.0, -198.0)):
    T.booleanOperation(acc, cyl((x0, 24.5, 67.03), (x1, 24.5, 67.03), 6.94), BT.UnionBooleanType)

# rear sight base: a truncated pyramid, which is what the donor actually is -
# a trapezoid in both elevations, not a dome.
sight = loft_regions(comp, [(67.5, rect(-231.0, -206.0, -24.75, 2.0)),
                            (74.0, rect(-222.0, -215.0, -14.5, -8.3))], 'z')
print('  sight: faces=%d vol=%.2f' % (sight.faces.count, sight.volume))
T.booleanOperation(acc, T.copy(sight), BT.UnionBooleanType)

# rear latch lug on the -Y side
T.booleanOperation(acc, cyl((-331.0, -33.5, 54.8), (-320.0, -33.5, 54.8), 8.54), BT.UnionBooleanType)
T.booleanOperation(acc, box(-333.0, -318.0, -45.0, -34.9, 50.75, 58.85), BT.IntersectionBooleanType) \
    if False else None

# Hinge-tab clearance. The steel tabs are 1/8in plate at Y +/-19.18..22.35 with an
# arc top of r8 about the hinge pin at (X -9, Z 62.5). The donor cover is SOLID
# through that corridor - it cannot close. Cutting an r8.5 arc about the same pin
# gives clearance at every angle of swing, not just when shut.
for (y0, y1) in ((18.90, 22.65), (-22.65, -18.90)):
    slot = box(-21.0, -4.0, y0, y1, 43.0, 62.5)
    T.booleanOperation(slot, cyl((-9.0, y0, 62.5), (-9.0, y1, 62.5), 17.0), BT.UnionBooleanType)
    T.booleanOperation(acc, slot, BT.DifferenceBooleanType)

for b in list(comp.bRepBodies): b.deleteMe()
nb = comp.bRepBodies.add(acc); nb.name = 'Hatch_native'
cleanup(comp)
report(nb, 'HATCH', 516.81)
