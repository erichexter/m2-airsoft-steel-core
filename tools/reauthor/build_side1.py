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

# Rivet heads are ROUND-HEAD rivets - spherical domes, not flat-topped cylinders.
# Each group was fitted to r^2 = R^2 - (Y - Yc)^2 off the donor mesh; every one
# came back a true sphere to within 0.25 mm. (|Y| centre, radius, positions)
RIVET_ROWS = [(-55.50, -541.84, 36.852, 8),
              ( 56.30, -541.84, 28.298, 8)]
DOMES = [(28.953, 3.380, [(x, z) for (x, z, _d) in L1_D2]),
         (35.554, 4.394, [(x, z) for (x, z, _d) in L1_D4])]
RIVET_DOME = (33.546, 4.219)

# the two big studs are a domed head sitting on a shallow conical pad
STUDS = [(x, z) for (x, z, _d) in L1_D5]
STUD_DOME = (41.630, 4.550)
STUD_PAD = (40.75, 42.65, 18.70, 15.40)   # |Y| in, |Y| out, dia in, dia out

# d18.98 constant, flat-ended at |Y| 62.25 - measured to the last full section.
# The first pass stopped it at 61.50 and left the left panel 0.8 mm short of the
# donor, the same truncation as the right panel's bracket dome.
BOSS = (-293.80, -29.60, 18.98, 44.47, 62.25)   # x, z, dia, |Y| in, |Y| out
BOSS_CHAMFER = 1.50


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

    for (yc, R, pts) in DOMES:
        for (x, z) in pts:
            T.booleanOperation(acc, dome(x, z, yc, R, sign), BT.UnionBooleanType)
    yc, R = RIVET_DOME
    for (z, x0, pitch, n) in RIVET_ROWS:
        for i in range(n):
            T.booleanOperation(acc, dome(x0 + pitch*i, z, yc, R, sign), BT.UnionBooleanType)
    pa, pb, pda, pdb = STUD_PAD
    syc, sR = STUD_DOME
    for (x, z) in STUDS:
        T.booleanOperation(acc, cyl((x, sign*pa, z), (x, sign*pb, z), pda, pdb), BT.UnionBooleanType)
        T.booleanOperation(acc, dome(x, z, syc, sR, sign), BT.UnionBooleanType)

    x, z, dia, a, b = BOSS
    # Full diameter up to the chamfer, then a 1.5 mm x 45 deg bevel on the rim so the
    # spigot ends like every other feature that stands proud, rather than as a raw
    # flat-ended cylinder. The donor leaves it square; this is a deliberate change.
    T.booleanOperation(acc, cyl((x, sign*a, z), (x, sign*(b - BOSS_CHAMFER), z), dia),
                       BT.UnionBooleanType)
    T.booleanOperation(acc, cyl((x, sign*(b - BOSS_CHAMFER), z), (x, sign*b, z),
                                dia, dia - 2*BOSS_CHAMFER), BT.UnionBooleanType)

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
    # The small inset recesses have a SPHERICAL interior (fits to 0.15 mm), not a
    # flat bottom - the same domed treatment as the rivet heads, cut inwards.
    for (x2, z2, _d2) in L1_C3:
        T.booleanOperation(acc, sphere((x2, sign*37.28, z2), 2.95), BT.DifferenceBooleanType)
    # the single small rivet hole in the plate
    T.booleanOperation(acc, cyl((-468.0, sign*30.1, 40.10), (-468.0, sign*27.8, 40.10), 1.40),
                       BT.DifferenceBooleanType)

    # A dome is a whole sphere; its far hemisphere sits inside the panel and can
    # break out through the inboard face. Clip everything back to the tube face.
    T.booleanOperation(acc, box(-600.0, -250.0, sign*25.40, sign*90.0, -90.0, 90.0),
                       BT.IntersectionBooleanType)

    for b in list(comp.bRepBodies): b.deleteMe()
    nb = comp.bRepBodies.add(acc); nb.name = name.replace('_Native', '_native')
    cleanup(comp)
    return nb


nb = build_side1('Side_L1_Native', -1.0)
report(nb, 'SIDE_L1', 331.48)
