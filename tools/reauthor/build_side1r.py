# Side_R1 (rear side panel, right) as native geometry.
#
# Same stepped-tier treatment as the left panel, but the right side has no
# charging-handle slot and no d19 boss. It carries the d6 pin drift hole, a
# long raised bracket on the top edge, and conical rivet heads.
import adsk.core as c, adsk.fusion as f
BT = f.BooleanTypes
T = tbm()

M3_X = (-525.10, -460.10, -285.70)
M3_Z = (8.00, -24.00)

# Two rivet rows, generated arithmetically - reading them back off the mesh
# missed one head and gave slightly different diameters row to row.
RIVET_ROWS = [(-55.50, -541.84, 36.852, 8),
              ( 56.30, -541.84, 28.298, 8)]

TIERS = [(R1_T1A, 25.85, 28.40),
         (R1_T1B, 28.40, 30.00),
         (R1_T2,  30.00, 33.00),
         (R1_T3A, 33.00, 34.50),
         (R1_T3B, 33.00, 34.50)]

# The raised bracket on the top edge reads as three round pads on a flat bar,
# not the wavy outline the mesh traces. Built that way it is four primitives.
BRACKET_PADS = (-345.30, -329.10, -312.30)
BRACKET_Z = 57.90
BRACKET_BAR = (-351.30, -307.00, 55.40, 60.40)   # x0, x1, z0, z1


def build_side1r(name, sign):
    occ = None
    for o in root.occurrences:
        if o.name.startswith(name): occ = o
    if occ is None:
        occ = root.occurrences.addNewComponent(c.Matrix3D.create()); occ.component.name = name
    comp = occ.component
    for b in list(comp.bRepBodies): b.deleteMe()
    cleanup(comp)

    segs = [extrude_region(comp, sign*a, sign*b, reg, 'y') for reg, a, b in TIERS]
    for i, b in enumerate(segs):
        print('  tier %d: faces=%-3d vol=%7.2f solid=%s' % (i, b.faces.count, b.volume, b.isSolid))

    acc = T.copy(segs[0])
    for b in segs[1:]:
        T.booleanOperation(acc, T.copy(b), BT.UnionBooleanType)

    bx0, bx1, bz0, bz1 = BRACKET_BAR
    T.booleanOperation(acc, box(bx0, bx1, sign*34.50, sign*46.20, bz0, bz1), BT.UnionBooleanType)
    for x in BRACKET_PADS:
        T.booleanOperation(acc, cyl((x, sign*34.50, BRACKET_Z), (x, sign*46.20, BRACKET_Z), 12.0),
                           BT.UnionBooleanType)
    # The tier beneath the bracket stops at X -334.4, which is exactly where the top
    # cover begins. Past that the bracket overhangs the cover's skirt, so its underside
    # has to start outboard of it - the donor does the same thing.
    T.booleanOperation(acc, box(-334.4, -300.0, sign*34.50, sign*34.95, 44.0, 70.0),
                       BT.DifferenceBooleanType)

    # conical rivet heads: d9.6 at the tier face tapering to d6.4
    for (z, x0, pitch, n) in RIVET_ROWS:
        for i in range(n):
            x = x0 + pitch * i
            T.booleanOperation(acc, cyl((x, sign*34.50, z), (x, sign*37.40, z), 9.90, 6.40),
                               BT.UnionBooleanType)

    for (x, z, dia) in R1_D2:
        T.booleanOperation(acc, cyl((x, sign*30.00, z), (x, sign*33.00, z), dia), BT.UnionBooleanType)

    for xx in M3_X:
        for zz in M3_Z:
            T.booleanOperation(acc, cyl((xx, sign*25.40, zz), (xx, sign*25.85, zz), 8.0),
                               BT.UnionBooleanType)
            T.booleanOperation(acc, cyl((xx, sign*24.0, zz), (xx, sign*48.0, zz), 3.40),
                               BT.DifferenceBooleanType)

    # d6 pin drift hole and the small hole above it, right through
    for (x, z, dia) in R1_CUT:
        T.booleanOperation(acc, cyl((x, sign*24.0, z), (x, sign*48.0, z), dia), BT.DifferenceBooleanType)

    for b in list(comp.bRepBodies): b.deleteMe()
    nb = comp.bRepBodies.add(acc); nb.name = name.replace('_Native', '_native')
    cleanup(comp)
    return nb


nb = build_side1r('Side_R1_Native', +1.0)
report(nb, 'SIDE_R1', 207.00)
