# Side_L1 (rear side panel) as native geometry.
#
# Five stepped tiers rather than the donor's continuous draft - the M2's side
# plate is stamped sheet with stepped panels, and straight steps read closer to
# the real gun than a smooth taper does. Rivet heads and fastener holes are real
# cylinders. The charging-handle slot stays a polygon (it is rectangular).
import adsk.core as c, adsk.fusion as f
BT = f.BooleanTypes
T = tbm()

M3_X = (-525.10, -460.10, -285.70)
M3_Z = (8.00, -24.00)

# (region, |Y| inner, |Y| outer)
TIERS = [(L1_T1, 25.85, 30.00),
         (L1_T2, 30.00, 34.50),
         (L1_T3, 34.50, 37.50),
         (L1_T4A, 37.50, 40.75),
         (L1_T4B, 37.50, 40.75),
         (L1_T5, 40.75, 46.50)]

# (disc list, |Y| inner, |Y| outer)
DISCS = [(L1_D2, 30.00, 32.50),    # d2.9 studs on the upper panel
         (L1_D3, 34.50, 37.60),    # the two rivet rows, 16 heads
         (L1_D4, 37.50, 40.00),
         (L1_D5, 40.75, 46.00)]

BOSS = (-293.80, -29.60, 19.00, 46.50, 61.50)   # x, z, dia, |Y| in, |Y| out


def build_side1(name, sign):
    occ = None
    for o in root.occurrences:
        if o.name.startswith(name): occ = o
    if occ is None:
        occ = root.occurrences.addNewComponent(c.Matrix3D.create()); occ.component.name = name
    comp = occ.component
    for b in list(comp.bRepBodies): b.deleteMe()
    cleanup(comp)

    segs = []
    for reg, a, b in TIERS:
        segs.append(extrude_region(comp, sign*a, sign*b, reg, 'y'))
    for i, b in enumerate(segs):
        print('  tier %d: faces=%-3d vol=%7.2f solid=%s' % (i, b.faces.count, b.volume, b.isSolid))

    acc = T.copy(segs[0])
    for b in segs[1:]:
        T.booleanOperation(acc, T.copy(b), BT.UnionBooleanType)

    for lst, a, b in DISCS:
        for (x, z, dia) in lst:
            T.booleanOperation(acc, cyl((x, sign*a, z), (x, sign*b, z), dia), BT.UnionBooleanType)

    x, z, dia, a, b = BOSS
    T.booleanOperation(acc, cyl((x, sign*a, z), (x, sign*b, z), dia), BT.UnionBooleanType)

    # d8 bosses bridging to the tube face, at the M3 positions
    for xx in M3_X:
        for zz in M3_Z:
            T.booleanOperation(acc, cyl((xx, sign*25.40, zz), (xx, sign*25.85, zz), 8.0),
                               BT.UnionBooleanType)

    # fastener holes right through
    for xx in M3_X:
        for zz in M3_Z:
            T.booleanOperation(acc, cyl((xx, sign*24.0, zz), (xx, sign*48.0, zz), 3.40),
                               BT.DifferenceBooleanType)
    # local recesses in the outer tiers
    for (x2, z2, d2) in L1_C4:
        T.booleanOperation(acc, cyl((x2, sign*37.0, z2), (x2, sign*41.5, z2), d2), BT.DifferenceBooleanType)
    for (x2, z2, d2) in L1_C3:
        T.booleanOperation(acc, cyl((x2, sign*34.0, z2), (x2, sign*38.0, z2), d2), BT.DifferenceBooleanType)
    # the single small rivet hole in the plate
    T.booleanOperation(acc, cyl((-468.0, sign*30.1, 40.10), (-468.0, sign*27.8, 40.10), 1.40),
                       BT.DifferenceBooleanType)

    for b in list(comp.bRepBodies): b.deleteMe()
    nb = comp.bRepBodies.add(acc); nb.name = name.replace('_Native', '_native')
    cleanup(comp)
    return nb


nb = build_side1('Side_L1_Native', -1.0)
report(nb, 'SIDE_L1', 331.48)
