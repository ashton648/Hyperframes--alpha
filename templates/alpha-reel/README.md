# Alpha reel template

Brand template for Alpha Sports Medicine Instagram reels, saved from the "Compare the Pair" reel
(`videos/compare-the-pair`, final video in `final/`).

- `frame.md`: brand colours, Montserrat type scale, and component styles (captions, name tags,
  info cards, split-screen divider, end card). Copy into a new project as `frame.md`.
- `storyboard-skeleton.md`, `brief-skeleton.md`, `recipe.json`: the HyperFrames recipe
  (`alpha-reel` v1).
- `assets/alpha-logo.png`: transparent logo. `assets/gsap.min.js`: local GSAP (the CDN is blocked
  in the cloud environment).

To start a new reel, ask Claude: "make another alpha-reel". It scaffolds a project, adopts this
recipe (`media-use/scripts/recipe.mjs use --name alpha-reel`), and asks only what's new.

Palette: navy `#002E6B` · orange `#F15F2E` · cream `#FEF1E1` · white. Clinics: Newport ·
Ascot Vale · Bacchus Marsh · Hawthorn. Handle: @alphasportsmed.
