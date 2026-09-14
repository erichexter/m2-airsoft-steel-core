# Apply the naming convention to the live model: rename components, rename and
# regroup bodies, and drop the dead ones.
import adsk.core as c, adsk.fusion as f

def occ_by_base(root, base):
    for o in root.occurrences:
        if o.name.split(':')[0] == base: return o
    return None

def ensure(root, name):
    o = occ_by_base(root, name)
    if o is None:
        o = root.occurrences.addNewComponent(c.Matrix3D.create())
        o.component.name = name
    return o

# 1. new grouping components
for nm in NEW_COMPONENTS:
    ensure(root, nm)

# 2. rename existing components
renamed = 0
for old, new in COMPONENTS.items():
    o = occ_by_base(root, old)
    if o is None: continue
    try:
        o.component.name = new; renamed += 1
    except Exception as e:
        print('  ! component %s -> %s: %s' % (old, new, str(e)[:60]))
print('components renamed: %d' % renamed)

# 3. rename + move bodies
moved = skipped = 0
for occ in list(root.allOccurrences):
    for b in list(occ.bRepBodies):
        spec = BODIES.get(b.name)
        if spec is None:
            continue
        new_name, target = spec[0], spec[1]
        if len(spec) > 2 and spec[2] == 'HAND':
            bb = b.boundingBox
            cy = (bb.minPoint.y + bb.maxPoint.y) * 5.0
            new_name += '-R' if cy < 0 else '-L'      # negative Y = right
        try:
            b.name = new_name
        except Exception as e:
            print('  ! rename %s: %s' % (b.name, str(e)[:60])); continue
        if target:
            dest = ensure(root, target)
            if occ.component != dest.component:
                try:
                    b.moveToComponent(dest)
                    moved += 1
                except Exception as e:
                    skipped += 1
                    print('  ! move %s -> %s: %s' % (new_name, target, str(e)[:60]))
print('bodies moved: %d   (move failed: %d)' % (moved, skipped))

# 4. drop the dead components
for nm in list(DROP_COMPONENTS) + list(EMPTIED):
    o = occ_by_base(root, nm)
    if o is None: continue
    if o.bRepBodies.count == 0 or nm in DROP_COMPONENTS:
        try:
            o.deleteMe(); print('  dropped %s' % nm)
        except Exception as e:
            print('  ! could not drop %s: %s' % (nm, str(e)[:60]))

print()
print('--- result ---')
for occ in sorted(root.occurrences, key=lambda o: o.name):
    print('%-26s %d body(ies)' % (occ.name.split(':')[0], occ.bRepBodies.count))
    for b in sorted(occ.component.bRepBodies, key=lambda x: x.name):
        print('     %-32s %6d f  %8.2f cm3' % (b.name, b.faces.count, b.volume))
n = len(root.bRepBodies)
if n: print('root-level bodies still loose: %d' % n)
