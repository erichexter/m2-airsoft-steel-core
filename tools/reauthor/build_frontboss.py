# FrontBoss (front sight assembly and its mount) as native geometry.
#
# Six prismatic runs along X. The rear face is a set of twelve plain rectangular
# standoff ribs; the front carries the sight hood and post.
import adsk.core as c, adsk.fusion as f
BT = f.BooleanTypes
T = tbm()

RUNS = [(FB_RIBS, -13.35, -3.00),
        (FB_B,     -3.00,  0.00),
        (FB_C,      0.00,  3.50),
        (FB_D,      3.50,  8.00),
        (FB_E,      8.00, 19.00),
        (FB_F,     19.00, 24.80)]

COMPONENT, PART = '20_Print_Receiver', 'PR-17-Front-Sight-Boss'
comp, KEEP = begin_part(root, COMPONENT, PART)
cleanup(comp)

segs = []
for regs, x0, x1 in RUNS:
    for r in regs:
        segs.append(extrude_region(comp, x0, x1, r))
print('  %d segments' % len(segs))

acc = T.copy(segs[0])
for b in segs[1:]:
    T.booleanOperation(acc, T.copy(b), BT.UnionBooleanType)

nb = finish_part(comp, KEEP, acc, PART)
report(nb, 'FRONTBOSS', 108.08)
