# Make the tube-mating face of each screwed skin genuinely flat, so it can be the bed face.
#
# THE PROBLEM
# The panels were given a 0.4mm clearance gap to the tube, and because a screw pulled
# across that gap would just flex a 3mm shell, every fastener got a d8 boss on the
# panel's INNER face to bridge it (BUILD-NOTES, "SKIN FASTENING").
#
# But the inner face is the face these parts are printed on - visible side up, so the
# outside can be ironed. So the part lands on the bed sitting on nothing but those
# bosses. Measured with tools/bedcheck.js before this script:
#
#   PR-13-Side-Front-L    2.46 cm2 on the bed,  216.69 cm2 floating 0.45mm above it
#   PR-12-Side-Rear-R     2.46 cm2 on the bed,  334.91 cm2 floating 0.45mm
#   PR-15-Top-Deck        2.46 cm2 on the bed,  105.91 cm2 floating 0.35mm
#
# 2.46 cm2 is exactly six bosses: 6 * (d8 disc - d3.4 hole). So 98% of the face is
# held in the air by six small pads, and the slicer supports all of it.
#
# THE FIX
# Fill the gap. Take the d-thick layer of panel just outboard of the main inner face,
# translate it inboard by d, and union it back on. That drops the main face down flush
# with the bosses, which is where the tube is anyway - so the panel now beds on the
# steel across its whole area instead of on six pads, which is also the better joint.
#
# Translating along the mating axis leaves in-plane positions untouched, so the layer
# already carries the d3.4 clearance holes and they stay open. No re-drilling.
#
# The bosses are absorbed and become flush. They are no longer doing anything, but
# removing them separately would be extra cuts for no gain.
import adsk.core as c, adsk.fusion as f
BT = f.BooleanTypes
T = tbm()

# part, mating axis, which end of it faces the tube
PARTS = [
    ('PR-11-Side-Rear-L',  'y', 'min'),
    ('PR-12-Side-Rear-R',  'y', 'max'),
    ('PR-13-Side-Front-L', 'y', 'min'),
    ('PR-14-Side-Front-R', 'y', 'max'),
    ('PR-15-Top-Deck',     'z', 'min'),
    ('PR-18-Bottom-Rear',  'z', 'max'),
]
AXIS_I = {'x': 0, 'y': 1, 'z': 2}
NEAR = 2.0          # mm: how far from the extreme plane to look for the main face


def find_body(name):
    for occ in root.allOccurrences:
        for b in occ.component.bRepBodies:
            if b.name == name:
                return occ.component, b
    return None, None


def planes_near_face(body, ai, inb):
    """Planar faces perpendicular to the mating axis, as {coord_mm: area_mm2}."""
    out = {}
    for fa in body.faces:
        g = fa.geometry
        if not isinstance(g, c.Plane):
            continue
        n = g.normal
        comp = (n.x, n.y, n.z)[ai]
        if abs(comp) < 0.999:                     # not perpendicular to the axis
            continue
        s = round(((g.origin.x, g.origin.y, g.origin.z)[ai]) * 10.0, 3)   # cm -> mm
        out[s] = out.get(s, 0.0) + fa.area * 100.0                        # cm2 -> mm2
    return out


print('%-24s %8s %8s %6s   %s' % ('part', 'boss', 'face', 'gap', 'result'))
done = 0
for (name, axis, side) in PARTS:
    comp, body = find_body(name)
    if body is None:
        print('%-24s  ! not found' % name)
        continue

    ai = AXIS_I[axis]
    inb = -1.0 if side == 'min' else 1.0          # direction pointing at the tube

    pl = planes_near_face(body, ai, inb)
    if not pl:
        print('%-24s  ! no planar faces on the mating axis' % name)
        continue

    # P: the plane furthest toward the tube - the bosses.
    P = min(pl) if side == 'min' else max(pl)
    # F: of the planes within NEAR of P, the one with the most area - the panel face.
    near = {s: a for s, a in pl.items() if abs(s - P) <= NEAR}
    F = max(near, key=lambda s: near[s])
    d = abs(F - P)

    if d < 1e-3:
        print('%-24s %8.3f %8.3f %6.3f   already flat' % (name, P, F, d))
        continue

    bb = body.boundingBox
    lo = (bb.minPoint.x * 10, bb.minPoint.y * 10, bb.minPoint.z * 10)
    hi = (bb.maxPoint.x * 10, bb.maxPoint.y * 10, bb.maxPoint.z * 10)

    # The d-thick layer of panel sitting just OUTBOARD of the main face.
    band = [list(lo), list(hi)]
    if side == 'min':
        band[0][ai], band[1][ai] = F, F + d
    else:
        band[0][ai], band[1][ai] = F - d, F

    acc = T.copy(body)
    layer = T.copy(body)
    T.booleanOperation(layer,
                       box(band[0][0] - 1, band[1][0] + 1,
                           band[0][1] - 1 if ai != 1 else band[0][1],
                           band[1][1] + 1 if ai != 1 else band[1][1],
                           band[0][2] - 1 if ai != 2 else band[0][2],
                           band[1][2] + 1 if ai != 2 else band[1][2]),
                       BT.IntersectionBooleanType)

    vec = [0.0, 0.0, 0.0]
    vec[ai] = inb * d / 10.0                      # mm -> cm
    m = c.Matrix3D.create()
    m.translation = c.Vector3D.create(*vec)
    T.transform(layer, m)

    v0 = acc.volume
    T.booleanOperation(acc, layer, BT.UnionBooleanType)
    gained = acc.volume - v0

    if acc.shells.count != 1 or not acc.isSolid:
        print('%-24s %8.3f %8.3f %6.3f   ! %d shells, solid=%s - SKIPPED'
              % (name, P, F, d, acc.shells.count, acc.isSolid))
        continue

    body.deleteMe()
    nb = comp.bRepBodies.add(acc)
    nb.name = name
    print('%-24s %8.3f %8.3f %6.3f   +%.2f cm3, %d faces, 1 shell'
          % (name, P, F, d, gained, nb.faces.count))
    done += 1

print('\n%d of %d parts flattened' % (done, len(PARTS)))

# ---------------------------------------------------------------------------
# Phase 2: the strips that fit BETWEEN the side panels have to follow them in.
#
# The top and bottom strips ran out to |Y| 25.80, butting against the side panels'
# inner faces at 25.85 with 0.05 clearance. Phase 1 moved those faces to 25.40 - the
# tube wall - so the strips now overlap the panels by 0.40 each side. Verified as
# caused by phase 1 and not pre-existing: every one of those intersections lies
# entirely inside the 0.45mm band that phase 1 added.
#
# Bring the strips in to match, keeping the same 0.05 clearance. The tube is 50.8
# wide, so at |Y| 25.35 a strip now spans the tube's full width and stops just shy of
# the panel beside it - which is what "fits between the side panels" was always
# supposed to mean.
TRIM = ['PR-15-Top-Deck', 'PR-18-Bottom-Rear',
        'PR-19-Bottom-Front-L', 'PR-19-Bottom-Front-R']
HALF = 25.35

print('')
for name in TRIM:
    comp, body = find_body(name)
    if body is None:
        print('%-24s  ! not found' % name)
        continue
    bb = body.boundingBox
    y0, y1 = bb.minPoint.y * 10, bb.maxPoint.y * 10
    if y0 >= -HALF - 1e-3 and y1 <= HALF + 1e-3:
        print('%-24s already within +/-%.2f' % (name, HALF))
        continue
    acc = T.copy(body)
    v0 = acc.volume
    T.booleanOperation(acc, box(bb.minPoint.x * 10 - 1, bb.maxPoint.x * 10 + 1,
                                -HALF, HALF,
                                bb.minPoint.z * 10 - 1, bb.maxPoint.z * 10 + 1),
                       BT.IntersectionBooleanType)
    if acc.shells.count != 1 or not acc.isSolid:
        print('%-24s ! %d shells after trim - SKIPPED' % (name, acc.shells.count))
        continue
    body.deleteMe()
    nb = comp.bRepBodies.add(acc)
    nb.name = name
    print('%-24s Y %.2f..%.2f -> +/-%.2f   -%.2f cm3, %d faces'
          % (name, y0, y1, HALF, v0 - acc.volume, nb.faces.count))
