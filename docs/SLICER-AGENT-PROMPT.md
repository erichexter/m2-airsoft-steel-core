# Prompt for an agent on the slicer machine

Copy everything below the line into an agent running on the machine that has Creality
Print (or OrcaSlicer) installed. It is self-contained — it assumes no knowledge of this
repo or of the conversation that produced it.

---

I need you to slice some 3D-printed parts for a Creality **K1 Max** and prepare them for
printing. **Do not start a physical print** — prepare the plates, save the project/G-code,
and tell me what you did so I can review and start it myself.

## Printer and process

- Creality K1 Max, build volume 300 × 300 × 300 mm — **confirm which plate is fitted; do
  not trust the slicer profile's plate type, it says textured on a machine running smooth PEI**
- **0.6 mm nozzle, 0.3 mm layer height**
- PLA
- These are non-structural cosmetic panels — **do not print solid.** 3–4 walls and
  light infill (10–15% gyroid) is plenty. Total across all parts is ~3.5 litres of
  material, so infill choice matters a lot.

## Getting the files

The models are in a public GitHub repo. **They are stored in Git LFS**, which means two of
the obvious download routes silently return 131-byte text pointers instead of models:

- ❌ "Code → Download ZIP" — gives pointers
- ❌ `raw.githubusercontent.com/...` — gives a pointer
- ✅ `https://github.com/erichexter/m2-airsoft-steel-core/raw/main/<path>` — real file
- ✅ the release assets below — real files

**A pointer file is ~131 bytes of text starting `version https://git-lfs`. If a download is
that size, that is what happened — do not feed it to the slicer.**

Easiest: get the whole pack from the latest release, which is served directly and has no
LFS problem:

```
https://github.com/erichexter/m2-airsoft-steel-core/releases/latest
```

Download `M2-steel-core-print-pack-v1.4.zip` (or whatever the newest is) and unzip. The 18
parts are in `print/`.

**Then replace two of them.** `PR-11` and `PR-12` in that pack are the plain versions; use
these instead, which have sacrificial corner pads added:

```
https://github.com/erichexter/m2-airsoft-steel-core/raw/main/stl/print-aids/PR-11-Side-Rear-L-ears.stl
https://github.com/erichexter/m2-airsoft-steel-core/raw/main/stl/print-aids/PR-12-Side-Rear-R-ears.stl
```

Verify each downloaded STL is hundreds of KB, not 131 bytes, before slicing.

## Orientation — the most important instruction here

Every panel must be laid **inner (tube-mating) face DOWN on the bed, visible face UP.**
The parts were specifically reworked so that face is flat; printing them on any other face
throws that away and needs support everywhere. The correct face is the one listed:

| file | put this face on the bed | footprint |
|---|---|---|
| `PR-11-Side-Rear-L-ears` | **Y min** | 298 × 155 mm |
| `PR-12-Side-Rear-R-ears` | **Y max** | 298 × 155 mm |
| `PR-13-Side-Front-L` | **Y min** | 271 × 99 mm |
| `PR-14-Side-Front-R` | **Y max** | 271 × 99 mm |
| `PR-15-Top-Deck` | **Z min** | 226 × 51 mm |
| `PR-18-Bottom-Rear` | **Z max** | 296 × 51 mm |
| `PR-17-Front-Sight-Boss` | **X max** | — |

"Y min face on the bed" means rotate the part so the face at its lowest Y coordinate is
touching the plate. After orienting, confirm the part's flat face really is coplanar with
the bed — most slicers have a "place on face" tool; use it and pick that face.

For the parts not listed, pick the orientation with the largest flat face and the least
overhang.

## Two things that will go wrong if you ignore them

**`PR-16-Top-Cover` is 329.9 mm long and will NOT fit the 300 mm bed axis-aligned.**
Rotate it **45° about Z** — that gives **272.7 × 272.4 mm, 13.6 mm of margin per side**,
which is room for a 10 mm brim. The slicer will not work this out for you. If it still
will not fit, stop and tell me rather than scaling it.

**`PR-11` and `PR-12` with their pads are 297.6 mm across a 300 mm bed — 1.2 mm clear at
each end.** Centre them deliberately and confirm nothing is off the plate or inside any
exclusion zone. Print each of these **alone on the plate.**

## Settings

These address a real bed-adhesion failure on this exact machine — the long panels were
peeling their end corners off the plate. PLA contracts ~0.4% cooling, so a 296 mm part
shrinks ~1.2 mm along its length and levers its corners up.

Apply in this order of importance:

1. **Auxiliary / side fan OFF for the first ~10 layers.** The K1 Max stock PLA profile runs
   it hard and it blows straight across a 296 mm first layer. Biggest single lever.
2. **Part cooling fan 0% for layers 1–3**, then ramp to normal.
3. **First layer 30–50 mm/s** with reduced first-layer acceleration. Stock profiles are far
   faster and that is real shear on a marginally attached part.
4. **Bed 60 °C.** Tell me to let it soak 5+ minutes before starting.
5. **Brim on `PR-13` / `PR-14`** — they have 14 mm of spare bed. **No brim on `PR-11` /
   `PR-12`** — there is no room, which is exactly why those two have built-in corner pads
   instead.
6. Slight negative Z-offset if the profile allows — at 0.6/0.3 an under-squished first
   layer still looks acceptable.

Keep the enclosure **closed**. Chamber heat helps against warping here, even though stock
PLA profiles often suggest opening it.

## What to give me back

- One project/plate per part (or a sensible grouping), saved where I can find it
- Estimated time and filament per part
- Confirmation of which face ended up on the bed for each one
- Anything that did not fit, sliced oddly, or needed a judgement call

Do not send anything to the printer or to a cloud account. Stop and report.
