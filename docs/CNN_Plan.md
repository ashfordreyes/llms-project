dat# Blowing Snow Detection — Roadmap

This is a step-by-step roadmap, not an implementation plan. Work through it one
step at a time, in order, and revisit/revise earlier steps as you learn things
from later ones. Nothing here is a commitment to build all of it — several
steps (especially 11) are explicitly optional stretch goals.

## 0. Overview & goals

Three goals, in priority order:

1. **Localize** blowing snow in a frame — not just "is it snowing," but
   *where* in the frame it's happening.
2. **Disambiguate** blowing snow from other precipitation/conditions by
   cross-referencing a weather-observations JSON API (e.g. a 40°F sunny
   reading makes "blowing snow" implausible regardless of what the pixels
   show).
3. *(Stretch)* **Estimate snow depth** by measuring how obscured known-height
   fences are in the frame.

Simplifying assumption: the camera is a **single fixed webcam** — no pan,
tilt, or zoom. This matters a lot for later steps (augmentation, model
choice) because the background is static and framing never changes.

## 1. Data collection pipeline

Before any modeling, you need frames landing on disk on a schedule, paired
with weather data from the same moment:

- Capture cadence — e.g. every N minutes, adjustable per season (blowing snow
  events may warrant tighter sampling in winter).
- Storage layout — something like `raw/YYYY/MM/DD/HHMMSS.jpg` plus a small
  sidecar (or manifest row, see step 3) recording the exact capture
  timestamp.
- At capture time, also pull the weather API's current observation and store
  it alongside the image (nearest-timestamp match). Do this **from day one**
  — backfilling paired weather data later is harder than capturing it live.
- Decide retention (keep everything indefinitely vs. downsample after N
  months) — not urgent, but worth deciding before disk fills up.

## 2. Weather API integration & feature engineering

Once you know the API, figure out which fields are actually useful as model
features:

- Temperature, precipitation type/probability, wind speed & gust, visibility,
  cloud cover — the obvious ones for the "is it plausibly snowing" question.
- Sun elevation / time-of-day — useful both as a weather feature and as a
  hint for the "can a CNN learn when it's sunny" question in step 7.
- Decide normalization/encoding now conceptually (e.g. z-score continuous
  fields, one-hot categorical fields like precip type) — the actual encoding
  code comes later, once step 7's model is being built.

## 3. Raw dataset organization

This answers "do I need a dataset processor first?" — yes, but for
**organizing/indexing**, not for pixel-level preprocessing:

- Keep raw captured frames immutable. Never overwrite or destructively edit
  them.
- Maintain a manifest (a CSV or SQLite table is enough at this scale) linking
  image path ↔ capture timestamp ↔ weather snapshot ↔ label status
  (unlabeled / labeled / skipped).
- This manifest is what a labeling tool, a training script, and an
  evaluation script will all read from — build it once, reuse it everywhere.

## 4. Labeling approach

This replaces the old fixed-ROI approach. The core idea: **don't build a
custom labeler** — use an existing tool, and label *masks*, not boxes.

- Why masks instead of a bounding box per image: blowing snow is a diffuse,
  irregular plume, and a fixed box (even redrawn per image) still forces an
  axis-aligned rectangle onto a shape that isn't one. A pixel mask captures
  the actual extent, is still fully flexible per image, and gives you a
  head start on the fence-occlusion idea in step 11 (also a pixel-level
  visibility problem on the same static background).
- Practically: use an existing open-source annotation tool (e.g. Label
  Studio or CVAT) to draw freeform polygons or boxes per image — whichever
  is faster for you day-to-day. Export as COCO-style JSON.
- Write one small script whose only job is: read the exported annotations,
  rasterize each into a binary mask image aligned to the source frame. This
  is the one piece of "labeling infra" you actually build yourself, and it's
  small.
- You do not need to decide the full labeling workflow now — start by
  labeling a small batch by hand and see how the tool feels before
  committing to a volume.

## 5. Preprocessing & augmentation pipeline (training-time)

This is the direct answer to "do I need to change hue/contrast/colors first":
**no, not as a first pass over raw images.** That kind of transform belongs
in the training data loader, applied on-the-fly, not as a destructive
one-time edit to stored frames. Reasons:

- Raw frames stay reusable — if you change your augmentation strategy later,
  you don't need to re-capture or re-derive anything.
- Labels stay aligned to the untouched raw pixels.

When you get to actually training (step 8), the loader-side pipeline will
look roughly like: brightness/contrast/hue jitter (to cover lighting changes
across the day), normalization, resize. Because the camera is fixed, skip
aggressive geometric augmentation (random crops/rotations that a moving
camera would need) — it would misalign the frame relative to what the model
should be learning about that specific static scene.

## 6. Train/val/test split strategy

Don't split randomly — split by time (contiguous date ranges) so
near-duplicate consecutive frames (e.g. two frames 5 minutes apart during the
same snow event) don't leak across splits and inflate apparent accuracy.

Also worth deciding once you have a labeled set: blowing snow is likely rare
relative to total frames, so note this as a class-imbalance problem to
address later (weighted sampling or a weighted loss) — not something to
solve before you have data to look at.

## 7. Model architecture

A first sketch, to revisit once steps 1–6 produce real data:

- Small U-Net-style encoder-decoder (PyTorch) taking the image and outputting
  a per-pixel blowing-snow probability mask.
- A small MLP branch encoding the weather features from step 2, fused with
  the image branch before a final decision — so the network doesn't have to
  re-derive "is it sunny/warm" purely from pixels when you can just tell it.
- On "can a CNN learn when it's sunny": yes, coarsely, from brightness and
  shadow cues in a fixed-framing scene — but fusing real weather-API data is
  strictly more reliable than relying on the network to infer it, which is
  exactly why step 2's fusion matters more than pushing the vision model
  harder.

Treat this as a starting hypothesis, not a locked-in architecture — the
right level of complexity will depend on how much labeled data step 4
actually produces.

## 8. Training loop

Once there's a labeled dataset and a model sketch: a standard PyTorch
training script — Dice + BCE loss for the mask output, checkpointing, basic
logging. Not worth designing in detail until steps 1–7 are further along.

## 9. Evaluation

Metrics worth tracking once a model exists:

- Pixel-level IoU/Dice for mask quality.
- Frame-level precision/recall/F1 for "is snow blowing" as a yes/no signal
  derived from the mask.
- A weather-disagreement report — frames where the model says snow but the
  weather API says implausible, and vice versa — useful for manually
  spot-checking failure modes rather than trusting either signal blindly.

## 10. Inference/deployment

Once a model is trained: run it on new incoming frames alongside their
paired weather JSON, threshold the output mask, and decide what the output
means downstream (e.g. % of frame covered by the mask as a rough severity
signal). Revisit this only after step 9 shows the model is worth deploying.

## 11. Phase 2 (stretch, optional): snow depth via fence occlusion

Not part of the core classifier — a separate, later problem that happens to
reuse the same static-camera assumption and segmentation tooling from steps
4–7. Sketch only:

- Segment/track the known fence geometry in the frame (static, so this is a
  one-time or rarely-updated reference, not something re-detected every
  frame).
- Measure the visible fence height in pixels vs. the known real-world fence
  height.
- Convert the obscured fraction into an estimated snow depth.

This is an occlusion/visibility-estimation problem, distinct from blowing-
snow detection — don't start it until the core classifier (steps 0–10) is
working and you actually want depth estimates.

## 12. Documenting decisions

As real decisions get made while working through the steps above (e.g. "why
masks over boxes," "why fuse weather data instead of relying on the CNN"),
record them as ADRs in `docs/adr/` using the existing template
(`docs/adr/template.md`) rather than editing this roadmap to also serve as a
decision log. This roadmap describes the plan; the ADRs describe why the
plan changed as you actually build it.
