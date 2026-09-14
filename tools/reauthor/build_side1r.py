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


def build_side1r(comp_name, part, sign):
    comp, keep = begin_part(root, comp_name, part)
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
    # domed rivet on the centre pad, standing proud of the bracket face. Truncating
    # the part at |Y| 46.2 lopped this off and left the panel 3.5 mm short of the
    # donor's 49.7 - it is the whole reason the right panel's Y extent was wrong.
    T.booleanOperation(acc, dome(BRACKET_PADS[1], BRACKET_Z, 44.529, 5.138, sign),
                       BT.UnionBooleanType)
    # The tier beneath the bracket stops at X -334.4, which is exactly where the top
    # cover begins. Past that the bracket overhangs the cover's skirt, so its underside
    # has to start outboard of it - the donor does the same thing.
    T.booleanOperation(acc, box(-334.4, -300.0, sign*34.50, sign*34.95, 44.0, 70.0),
                       BT.DifferenceBooleanType)

    # Round-head rivets: spherical domes. Fitted off the donor at centre |Y| 33.525,
    # R 4.223 - the same rivet the left panel carries, to within 0.005 mm.
    for (z, x0, pitch, n) in RIVET_ROWS:
        for i in range(n):
            T.booleanOperation(acc, dome(x0 + pitch*i, z, 33.525, 4.223, sign), BT.UnionBooleanType)

    # the six studs on the middle tier are domes too, in two sizes
    for (x, z, dia) in R1_D2:
        yc, R = (28.346, 5.269) if dia > 6.0 else (28.966, 3.360)
        T.booleanOperation(acc, dome(x, z, yc, R, sign), BT.UnionBooleanType)

    for xx in M3_X:
        for zz in M3_Z:
            T.booleanOperation(acc, cyl((xx, sign*25.40, zz), (xx, sign*25.85, zz), 8.0),
                               BT.UnionBooleanType)
            T.booleanOperation(acc, cyl((xx, sign*24.0, zz), (xx, sign*48.0, zz), 3.40),
                               BT.DifferenceBooleanType)

    # d6 pin drift hole and the small hole above it, right through
    for (x, z, dia) in R1_CUT:
        T.booleanOperation(acc, cyl((x, sign*24.0, z), (x, sign*48.0, z), dia), BT.DifferenceBooleanType)

    # the two small inset recesses on the middle tier - spherical interior, R 3.00
    # about |Y| 34.01. These were missed entirely on the first pass.
    for z in (24.016, -21.900):
        T.booleanOperation(acc, sphere((-545.57, sign*34.01, z), 3.00), BT.DifferenceBooleanType)

    # A dome is a whole sphere; its far hemisphere sits inside the panel and can
    # break out through the inboard face. Clip everything back to the tube face.
    T.booleanOperation(acc, box(-600.0, -250.0, sign*25.40, sign*90.0, -90.0, 90.0),
                       BT.IntersectionBooleanType)

    return finish_part(comp, keep, acc, part)


nb = build_side1r('20_Print_Receiver', 'PR-11-Side-Rear-L', +1.0)
report(nb, 'SIDE_R1', 207.00)
