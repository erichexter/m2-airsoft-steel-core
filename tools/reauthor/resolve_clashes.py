# Clear the four remaining skin interferences.
#
# Found by pairwise-intersecting the eight receiver skins against all 210 bodies. All
# four predate the mating-face flattening - confirmed by checking that each overlap
# extends outside the 0.45mm band that work added - so they have been sitting in the
# model since the skins were first cut.
#
#   PR-11 <-> PR-13          34.6 mm3   lengthwise seam at X -265
#   PR-12 <-> PR-14          37.6 mm3   the same seam, other side
#   PR-12 <-> trigger pin    20.1 mm3   panel fouls the d4 pivot - blocks assembly
#   PR-15 <-> spade grips     6.6 mm3   deck corner into the grip spine
#
# Two solids cannot share space whatever the intent, so "it is probably a lap joint"
# is not a defence: a lap still needs clearance cut into one side of it. The rule used
# here is that the part which is easier to reprint and less load-bearing gives way -
# the front panel yields to the rear one, the skin yields to the hardware.
#
# CLEARANCE is deliberately larger than the 0.05 used between a strip and a panel.
# These are not faces meant to bed together; they are places where two parts were
# accidentally occupying the same space, and a printed part wants room at a joint it
# has to be slid into.
import adsk.core as c, adsk.fusion as f
BT = f.BooleanTypes
T = tbm()

CLEARANCE = 0.20        # mm cut into the yielding part, on every axis

# (part that gives way, part it must clear)
PAIRS = [
    ('PR-13-Side-Front-L', 'PR-11-Side-Rear-L'),
    ('PR-14-Side-Front-R', 'PR-12-Side-Rear-R'),
    ('PR-12-Side-Rear-R',  'HW-03-Trigger-Pin-4mm'),
    ('PR-15-Top-Deck',     'PR-31-Spade-Grips'),
    # Found only when the check was widened from the eight skins to ALL EIGHTEEN
    # printed parts. The front sight boss runs back to X -13.4 and the hinge tabs
    # forward to X 0, so it sits down over both of them. Steel that is already welded
    # into the tube does not yield; the printed part does. The relief is at the boss's
    # X-min end, well away from the face it prints on.
    ('PR-17-Front-Sight-Boss', 'ST-07-Hinge-Tab-L'),
    ('PR-17-Front-Sight-Boss', 'ST-07-Hinge-Tab-R'),
]


def find_body(name):
    for occ in root.allOccurrences:
        if occ.name.split(':')[0].startswith('00_Ref'):
            continue
        for b in occ.component.bRepBodies:
            if b.name == name:
                return occ.component, b
    return None, None


print('%-22s %-24s %10s   %s' % ('yields', 'to', 'overlap', 'result'))
for (yielding, fixed) in PAIRS:
    comp, yb = find_body(yielding)
    _, fb = find_body(fixed)
    if yb is None or fb is None:
        print('%-22s %-24s  ! body not found' % (yielding, fixed))
        continue

    probe = T.copy(yb)
    T.booleanOperation(probe, T.copy(fb), BT.IntersectionBooleanType)
    overlap = probe.volume * 1000.0
    if overlap <= 0.5:
        print('%-22s %-24s %10.1f   already clear' % (yielding, fixed, overlap))
        continue

    acc = T.copy(yb)
    v0 = acc.volume
    relieve(acc, fb, CLEARANCE)
    before = acc.shells.count
    drop_debris(acc)
    dropped = before - acc.shells.count

    if acc.shells.count != 1 or not acc.isSolid:
        print('%-22s %-24s %10.1f   ! %d shells, solid=%s - SKIPPED'
              % (yielding, fixed, overlap, acc.shells.count, acc.isSolid))
        continue

    check = T.copy(acc)
    T.booleanOperation(check, T.copy(fb), BT.IntersectionBooleanType)
    left = check.volume * 1000.0

    yb.deleteMe()
    nb = comp.bRepBodies.add(acc)
    nb.name = yielding
    print('%-22s %-24s %10.1f   -%.2f cm3, %d faces, %.3f mm3 left%s'
          % (yielding, fixed, overlap, v0 - acc.volume, nb.faces.count, left,
             ', dropped %d debris' % dropped if dropped else ''))
