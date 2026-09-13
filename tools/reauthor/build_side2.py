# Side_L2 / Side_R2 (forward side panels) as native geometry.
#
# Layered plate, normal to Y. Inner face sits 0.45 mm off the tube and is bridged
# by six d8 bosses at the M3 positions. Two tiers of raised panel on the outside,
# the outermost chamfered. Holes are cut as real cylinders, not snapped polygons.
import adsk.core as c, adsk.fusion as f
BT = f.BooleanTypes
T = tbm()

# hole pattern, measured off the donor (mm)
M3_X   = (-242.40, -122.90, -63.10)
M3_Z   = (8.00, -24.00)
BIG    = (-115.98, 0.00, 7.52)          # x, z, dia
RIVETS = [(-169.55 + 18.306 * i, -39.80) for i in range(9)]

# Y stations, given as distances from the centre plane; sign flips for the R panel
PLATE_IN, PLATE_OUT = 25.85, 30.00
RIBA0_OUT, RIBA1_OUT = 38.00, 40.50
RIBB_OUT, TIP_OUT = 44.00, 49.09
BOSS_IN = 25.40


def build_side2(name, sign, rear_panel=True, boss=False):
    occ = None
    for o in root.occurrences:
        if o.name.startswith(name): occ = o
    if occ is None:
        occ = root.occurrences.addNewComponent(c.Matrix3D.create()); occ.component.name = name
    comp = occ.component
    for b in list(comp.bRepBodies): b.deleteMe()
    cleanup(comp)

    def Y(a, b):
        """Extrusion limits at |Y| = a..b, on the correct side."""
        return (sign * a, sign * b)

    tiers = [(PLATE, PLATE_IN, PLATE_OUT),
             (RIBA0, PLATE_OUT, RIBA0_OUT),
             (RIBB0, RIBA0_OUT, RIBB_OUT),
             (RIBB1, RIBA0_OUT, RIBB_OUT)]
    # the rear raised panel is on the LEFT only; the right carries a conical boss
    # in roughly the same place instead
    if rear_panel:
        tiers.insert(2, (RIBA1, PLATE_OUT, RIBA1_OUT))
    segs = []
    for reg, a, b in tiers:
        y0, y1 = Y(a, b)
        segs.append(extrude_region(comp, y0, y1, reg, 'y'))

    # chamfered outer tips of the outermost tier
    for reg, tip in ((RIBB0, TIP0), (RIBB1, TIP1)):
        segs.append(loft_regions(comp, [(sign * RIBB_OUT, reg), (sign * TIP_OUT, tip)], 'y'))

    for i, b in enumerate(segs):
        print('  seg %d: faces=%-3d vol=%7.2f solid=%s' % (i, b.faces.count, b.volume, b.isSolid))

    acc = T.copy(segs[0])
    for b in segs[1:]:
        T.booleanOperation(acc, T.copy(b), BT.UnionBooleanType)

    # right-hand conical boss at X -222.7, Z 31.0 - two straight cone segments
    if boss:
        T.booleanOperation(acc, cyl((-222.7, sign*29.5, 31.0), (-222.7, sign*33.0, 31.0), 19.1, 8.3),
                           BT.UnionBooleanType)
        T.booleanOperation(acc, cyl((-222.7, sign*33.0, 31.0), (-222.7, sign*35.2, 31.0), 8.3, 4.0),
                           BT.UnionBooleanType)

    # d8 bosses bridging the gap to the tube, at the M3 positions
    yb0, yb1 = sign * BOSS_IN, sign * PLATE_IN
    for x in M3_X:
        for z in M3_Z:
            T.booleanOperation(acc, cyl((x, yb0, z), (x, yb1, z), 8.0), BT.UnionBooleanType)

    # fastener holes, right through the plate and its boss
    yh0, yh1 = sign * 24.0, sign * 31.0
    for x in M3_X:
        for z in M3_Z:
            T.booleanOperation(acc, cyl((x, yh0, z), (x, yh1, z), 3.40), BT.DifferenceBooleanType)
    T.booleanOperation(acc, cyl((BIG[0], yh0, BIG[1]), (BIG[0], yh1, BIG[1]), BIG[2]),
                       BT.DifferenceBooleanType)

    # Rivet detail: SPHERICAL dimples in the exposed outer face, R 3.125 about
    # |Y| 31.035 - a d5.9 opening 2.1 mm deep. The first pass read the diameter
    # deep inside the dimple and cut d1.50 pin holes instead, which is wrong in
    # both size and shape.
    for (x, z) in RIVETS:
        T.booleanOperation(acc, sphere((x, sign * 31.035, z), 3.125), BT.DifferenceBooleanType)

    for b in list(comp.bRepBodies): b.deleteMe()
    nb = comp.bRepBodies.add(acc); nb.name = name.replace('_Native', '_native')
    cleanup(comp)
    return nb


nbL = build_side2('Side_L2_Native', -1.0, rear_panel=True,  boss=False)
report(nbL, 'SIDE_L2', 136.23)
nbR = build_side2('Side_R2_Native', +1.0, rear_panel=False, boss=True)
report(nbR, 'SIDE_R2', 124.12)
