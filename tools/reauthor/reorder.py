# Put the browser in catalogue order.
#
# Fusion lists occurrences in CREATION order and exposes no way to reorder them -
# NamedViews has no index setter and neither does Occurrence. The only lever is
# creation order itself, so: rename the existing components out of the way, create
# fresh ones in the order you want, move the bodies across, delete the empties.
import adsk.core as c, adsk.fusion as f

SKIP = ('00_Ref_FCU',)          # holds child occurrences, not bodies - leave it put

def identity(m):
    a = m.asArray()
    want = (1,0,0,0, 0,1,0,0, 0,0,1,0, 0,0,0,1)
    return all(abs(x - y) < 1e-9 for x, y in zip(a, want))

# refuse to run if any component we MOVE BODIES OUT OF is transformed - the move
# would shift the geometry. Skipped components are left exactly where they are, so
# their transform does not matter.
bad = [o.name for o in root.occurrences
       if o.name.split(':')[0] not in SKIP and not identity(o.transform)]
if bad:
    print('ABORT - these occurrences are not at identity: %s' % bad)
else:
    # tidy: scratch sketches and planes left by the build scripts
    n_sk = 0
    for o in root.occurrences:
        for s in list(o.component.sketches): s.deleteMe(); n_sk += 1
        for p in list(o.component.constructionPlanes): p.deleteMe(); n_sk += 1
    if n_sk: print('removed %d leftover sketches/planes' % n_sk)

    plan = []
    for o in root.occurrences:
        nm = o.name.split(':')[0]
        if nm in SKIP: continue
        plan.append((nm, o.isLightBulbOn))
    plan.sort(key=lambda t: t[0])
    print('rebuilding %d components in order' % len(plan))

    # free up the names
    old = {}
    for o in root.occurrences:
        nm = o.name.split(':')[0]
        if nm in SKIP: continue
        o.component.name = '~old~' + nm
        old[nm] = o

    # create fresh, in order, and migrate
    moved = 0
    for nm, vis in plan:
        new = root.occurrences.addNewComponent(c.Matrix3D.create())
        new.component.name = nm
        src = old[nm]
        for b in list(src.bRepBodies):
            b.moveToComponent(new)
            moved += 1
        new.isLightBulbOn = vis
    print('moved %d bodies' % moved)

    for nm, o in old.items():
        if o.bRepBodies.count == 0:
            o.deleteMe()
        else:
            print('  ! %s still holds %d bodies - left in place' % (nm, o.bRepBodies.count))

    print()
    print('browser order now:')
    for i in range(root.occurrences.count):
        o = root.occurrences.item(i)
        print('  %2d  %-26s %2d bodies  %s' % (i, o.name.split(':')[0], o.bRepBodies.count,
                                               'shown' if o.isLightBulbOn else 'hidden'))
