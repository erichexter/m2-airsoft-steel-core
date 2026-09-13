# Video pipeline

Builds a narrated walkthrough from the Fusion model. The render frames and the
finished mp4 are **not** committed — they are ~1 GB and ~70 MB respectively.

```
narration.md   the script; each "## NN_name" block becomes one VO clip
tts.js         renders each block to vo/NN_name.mp3 via ElevenLabs
build.sh       frames + vo -> M2_steel_core.mp4
```

## Running it

1. **Render frames from Fusion.** Seven sequences at 1920×1080, written to
   `<work>/hero`, `steel`, `section`, `ch`, `trig`, `barrel`, `explode`.
   Driven by `Viewport.saveAsImageFile` in a loop — see the build notes for the
   camera paths. `hero` and `steel` must share the same camera path, because the
   reveal crossfades one into the other.
2. `ELEVENLABS_API_KEY=... node tts.js [voiceId]` — default voice is Roger
   (`CwhRBWXzGAHq8TQ4Fs17`), conversational American, which suits a maker video.
3. `bash build.sh`

## How the timing works

There is no separate edit. **Each video segment is built to the exact duration of
its narration clip**, so the cut always lands on the sentence. Change a line of
narration, re-run `tts.js`, re-run `build.sh`, and the picture re-times itself.

Drift is about 0.2 s across three minutes — each segment rounds up to a 24 fps
frame boundary. Not worth correcting.

## Gotchas

- Sequences that travel linearly (`section`, `barrel`, `explode`) are built
  **ping-ponged** (forward then reversed) so they loop seamlessly when stretched
  to fill a narration block. Turntables loop naturally and are not ping-ponged.
- `drawtext` on Windows needs the font path escaped as `C\:/Windows/Fonts/...`.
  Avoid apostrophes **and colons** in title text — both terminate the filter
  string. A subtitle reading "1:1 scale" fails to parse; "full scale" works.
- Mesh-derived bodies (jacket, grip, handle) carry **face-level** appearances that
  override `body.appearance`, so they cannot be recoloured in bulk. Iterating
  20k faces to fix that hangs Fusion. This is why the metal/plastic story is told
  by hiding the printed parts rather than by colour-coding them.
