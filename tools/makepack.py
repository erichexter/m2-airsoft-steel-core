#!/usr/bin/env python3
"""Build the downloadable print pack.

    python tools/makepack.py <version>        e.g. python tools/makepack.py v1.1

Emits dist/M2-steel-core-print-pack-<version>.zip containing the 18 printed STLs,
both tube-template PDFs, the licence and a generated README.

WHY THIS EXISTS AS A RELEASE ASSET AND NOT A FILE IN THE REPO
The STLs live in Git LFS, and two of the obvious ways to fetch them - "Code ->
Download ZIP" and raw.githubusercontent.com - hand back 131-byte pointer files
instead of models. A release asset is served directly, so one link works with no
git-lfs, no clone and no way to end up holding pointers.

Which is also why this script REFUSES to build if it finds a pointer in its own
inputs: a pack built on a machine that cloned without git-lfs would be 5 KB of text
wearing .stl extensions, and would look completely fine until someone sliced it.
"""
import os
import re
import sys
import zipfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LFS_MAGIC = b'version https://git-lfs'

TEMPLATES = [
    ('tube-template/M2_tube_wrap.pdf', 'templates/M2_tube_wrap.pdf'),
    ('tube-template/M2_tube_wrap_letter.pdf', 'templates/M2_tube_wrap_letter.pdf'),
]


def read(rel):
    """Read a repo file, refusing LFS pointers."""
    path = os.path.join(ROOT, rel)
    with open(path, 'rb') as fh:
        data = fh.read()
    if data.startswith(LFS_MAGIC):
        sys.exit('REFUSING TO BUILD: %s is a Git LFS pointer, not the real file.\n'
                 'Run "git lfs install && git lfs pull" and try again.' % rel)
    return data


def part_table():
    """Name, faces and cm3 for the printed parts, taken from the catalogue so the
    pack cannot drift from docs/PARTS.md."""
    md = read('docs/PARTS.md').decode('utf-8')
    rows = re.findall(r'\|\s*`(PR-[\w-]+)`\s*\|\s*([\d,]+)\s*\|\s*([\d.]+)\s*\|', md)
    return [(n, int(f.replace(',', '')), float(v)) for n, f, v in rows]


def main():
    version = sys.argv[1] if len(sys.argv) > 1 else 'dev'

    stls = sorted(f for f in os.listdir(os.path.join(ROOT, 'stl'))
                  if f.startswith('PR-') and f.endswith('.stl'))
    if not stls:
        sys.exit('no PR-*.stl found in stl/')

    parts = part_table()
    by_name = {n: (f, v) for n, f, v in parts}
    missing = [s for s in stls if s[:-4] not in by_name]
    if missing:
        sys.exit('not in docs/PARTS.md: %s' % ', '.join(missing))

    total_cm3 = sum(by_name[s[:-4]][1] for s in stls)

    lines = []
    for s in stls:
        faces, vol = by_name[s[:-4]]
        lines.append('  %-34s %8.2f cm3' % (s, vol))
    listing = '\n'.join(lines)

    readme = README.format(version=version, count=len(stls), listing=listing,
                           total=total_cm3, kg=total_cm3 * 1.24 / 1000.0)

    os.makedirs(os.path.join(ROOT, 'dist'), exist_ok=True)
    out = os.path.join(ROOT, 'dist', 'M2-steel-core-print-pack-%s.zip' % version)
    with zipfile.ZipFile(out, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        z.writestr('README.txt', readme)
        z.writestr('LICENSE.txt', read('LICENSE'))
        for s in stls:
            z.writestr('print/' + s, read('stl/' + s))
        for arc, rel in TEMPLATES:
            z.writestr(arc, read(rel))

    size = os.path.getsize(out)
    print('%s' % os.path.relpath(out, ROOT))
    print('  %d printed parts, %.0f cm3 (~%.1f kg PLA solid)' % (len(stls), total_cm3,
                                                                total_cm3 * 1.24 / 1000.0))
    print('  %d entries, %.1f MB' % (len(stls) + len(TEMPLATES) + 2, size / 1048576.0))


README = """M2 BROWNING - STEEL CORE CONVERSION - PRINT PACK {version}
=========================================================================

A 1:1 airsoft replica built around a welded steel core. The printed parts in here
are NON-STRUCTURAL SKINS - every load path runs through the steel tube. Printing
these alone does not get you a gun; it gets you the cosmetic shell for one.

Full build notes, the steel cut list, the STEP files and the Fusion source:
https://github.com/erichexter/m2-airsoft-steel-core


WHAT IS IN HERE
---------------
print/              {count} printed parts, ready to slice
tube-template/      1:1 cutting template for the 2x3 steel core tube
LICENSE.txt         CC BY-NC-SA 4.0


THE PRINTED PARTS
-----------------
{listing}

{total:.0f} cm3 total - about {kg:.1f} kg of PLA at 100% infill, considerably less in
practice. All are closed, single-shell, correctly oriented meshes with zero open
edges. Two need a word of warning:

  PR-16-Top-Cover     329.9 mm long. It does NOT fit a 300 mm bed axis-aligned.
                      Laid diagonally it is a 294 mm footprint - 5.7 mm of margin.

  PR-31-Spade-Grips   Reports 3 non-manifold edges in some checkers. They are three
                      2 mm verticals where the trigger clearance slot cuts through
                      the spine and the cut surface meets itself. The part has no
                      holes and is one closed shell. Slicers handle it.

L and R are the PHYSICAL sides of the gun, standing behind it and firing forward.


THE TUBE TEMPLATE
-----------------
The tube's perimeter unrolled flat, for marking it out by hand. Generated from the
model, not transcribed.

  M2_tube_wrap.pdf          one sheet, 619.52 x 273.53 mm - for a plotter
  M2_tube_wrap_letter.pdf   the same drawing tiled across 6 letter pages

CHECK THE SCALE BEFORE YOU CUT ANYTHING. Every sheet carries a 100 mm calibration
bar. Measure it. If it is not 100 mm, the print was scaled and every dimension
downstream is wrong - reprint at 100% / "Actual size", never "Fit to page".

On a plotter: 24" roll is 610 mm, which is 9.5 mm too narrow to take the sheet
across the roll - plot it along the roll instead, or use 36" or A1.

Letter version: trim on the grey corner crop marks, overlap 12 mm, tape.

Wrap it around the tube with the paper flush to the BREECH end and the seam down
the BOTTOM face centreline. It closes on itself at 243.53 mm.

Reading it:
  solid black       cut these
  red dashed        corner tangents - where the tube's radii begin. FOLD LINES,
                    NOT CUTS. They also tell you when a cut crosses a corner.
  grey dashed       the wrap boundary
  grey verticals    every 50 mm, labelled with the model's X coordinate

Three things that surprise people:
  - The air line hole sits ON the seam. It appears as two half-circles, one at
    each edge of the sheet. They join when wrapped.
  - The belt slot and the top opening are ONE aperture. No web between them.
  - The locating tabs are material to LEAVE, not remove. Cut around them.


LICENCE AND CREDIT
------------------
This pack is licensed CC BY-NC-SA 4.0 - see LICENSE.txt.

The cosmetic skin geometry is DERIVED FROM:

    M2 Browning 0.50 cal Machine Gun (1:1 Scale) by HappyBattleSheep
    https://www.thingiverse.com/thing:7248430
    Licensed CC BY (Creative Commons - Attribution)

Keep that credit if you fork or redistribute this. CC BY is not share-alike, so
this derivative may carry the more restrictive CC BY-NC-SA above; that applies to
the original contributions here and cannot revoke anyone's rights to
HappyBattleSheep's work, which remains available under CC BY from the link above.

The steel core, weldments, engine cradle, tooling and documentation are original.

This is a REPLICA of a firearm for airsoft use. It does not and cannot fire live
ammunition. Check your local law before building, transporting or displaying it.
"""


if __name__ == '__main__':
    main()
