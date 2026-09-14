# Render the documentation images straight out of the model, so they cannot drift
# from the geometry. Colour-codes by class for the shots, then puts the model's
# appearance back exactly as it was.
import adsk.core as c, adsk.fusion as f, os

IMG = r'C:\Users\eric\Documents\3dprint\m2-airsoft-steel-core\docs\img'
os.makedirs(IMG, exist_ok=True)
vp = app.activeViewport
ORI = {'iso':  c.ViewOrientations.IsoTopRightViewOrientation,
       'isoL': c.ViewOrientations.IsoTopLeftViewOrientation,
       'left': c.ViewOrientations.LeftViewOrientation}

RESTORE_TO = 'Steel - Satin'
DOC_COLOURS = {'ST': 'Opaque(79,122,170)',    # steel you weld  - blue
               'HW': 'Opaque(204,153,51)',    # hardware you buy - brass
               'PR': 'Opaque(204,204,204)'}   # printed         - light grey

def _app(name):
    for a in des.appearances:
        if a.name == name: return a
    return None

def paint(by_class):
    for occ in root.occurrences:
        if occ.name.split(':')[0].startswith('00_Ref'): continue
        for b in occ.component.bRepBodies:
            nm = DOC_COLOURS.get(b.name[:2]) if by_class else RESTORE_TO
            a = _app(nm)
            if a: b.appearance = a

def show(spec):
    for occ in root.occurrences:
        nm = occ.name.split(':')[0]
        on = nm in spec
        occ.isLightBulbOn = on
        want = spec.get(nm)
        for b in occ.component.bRepBodies:
            b.isLightBulbOn = on and (want is None or b.name in want)

def shot(fname, spec, ori='iso', w=1500, h=780):
    show(spec)
    cam = vp.camera
    cam.viewOrientation = ORI[ori]; cam.isFitView = True
    vp.camera = cam
    adsk.doEvents(); vp.fit(); adsk.doEvents()
    p = os.path.join(IMG, fname + '.png')
    vp.saveAsImageFile(p, w, h)
    print('  %-34s %7d B' % (fname, os.path.getsize(p) if os.path.exists(p) else -1))

ALL_BUILD = {'10_Steel_Core': None, '11_Steel_Weldments': None, '20_Print_Receiver': None,
             '30_Print_Barrel': None, '40_Print_Grip': None, '50_Print_Charging': None,
             '60_Print_Trigger': None, '70_Print_Engine': None}
STEEL = {'10_Steel_Core': None, '11_Steel_Weldments': None}

ASSEMBLY = [
  ('01-assembly',        dict(ALL_BUILD, **{'00_Ref_PolarStar_F2': None}), 'iso', 1600, 700),
  ('02-steel-core',      STEEL, 'iso', 1600, 700),
  ('03-steel-core-side', STEEL, 'left', 1600, 560),
  ('04-receiver-skins',  {'20_Print_Receiver': None}, 'iso', 1500, 780),
  ('05-trigger-group',   {'60_Print_Trigger': None}, 'iso', 1200, 900),
  ('06-charging-handle', {'50_Print_Charging': None}, 'iso', 1400, 800),
  ('07-barrel-mount',    {'30_Print_Barrel': None,
                          '11_Steel_Weldments': ('ST-04-Barrel-Plate','ST-05-Barrel-Socket',
                                                 'HW-01-Barrel-EMT-1in')}, 'iso', 1500, 700),
  ('08-grip-backplate',  {'40_Print_Grip': None, '60_Print_Trigger': None,
                          '11_Steel_Weldments': ('ST-02-Backplate','ST-03-Backplate-Boss-L',
                                                 'ST-03-Backplate-Boss-R')}, 'isoL', 1300, 900),
  ('09-engine-cradle',   {'70_Print_Engine': None, '00_Ref_PolarStar_F2': None,
                          '10_Steel_Core': None}, 'iso', 1500, 700),
]

def parts_list():
    out = []
    for occ in root.occurrences:
        nm = occ.name.split(':')[0]
        if nm.startswith('00_Ref'): continue
        for b in occ.component.bRepBodies:
            if b.name[:2] in ('PR','ST','HW'): out.append((nm, b.name))
    return sorted(out, key=lambda t: t[1])

def finish():
    paint(False)
    show(dict(ALL_BUILD, **{'00_Ref_PolarStar_F2': None}))
    cam = vp.camera; cam.viewOrientation = ORI['iso']; cam.isFitView = True
    vp.camera = cam
    adsk.doEvents(); vp.fit()
