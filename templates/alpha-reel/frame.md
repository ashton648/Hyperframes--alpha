---
version: alpha
name: Alpha Sports Medicine — Reel Frame
description: >
  Brand frame for Alpha Sports Medicine Instagram reels (9:16, 1080×1920). Navy ground, orange
  accent, cream wedge; Montserrat throughout (900 display, 700 labels). Real gym footage carries
  the story; navy cards, orange tags and burned-in captions sit on top; navy end cards close.
unit: the frame — 1080×1920 (Instagram Reels) primary
principle: brand colours are sacred · footage first · one CTA per reel

colors:
  navy: "#002E6B"
  navy-deep: "#00214F"
  orange: "#F15F2E"
  orange-text-on-light: "#D15228"
  orange-text-on-cream: "#D4512A"
  cream: "#FEF1E1"
  white: "#FFFFFF"
  dim-overlay: "rgba(0, 33, 79, 0.62)"

typography:
  display:    { fontFamily: "Montserrat", px: 112, weight: 900, lineHeight: 0.98, tracking: "-0.035em", upper: true }
  headline:   { fontFamily: "Montserrat", px: 84, weight: 900, lineHeight: 1.0, tracking: "-0.03em", upper: true }
  chip:       { fontFamily: "Montserrat", px: 68, weight: 900, tracking: "-0.01em", upper: true }
  name-tag:   { fontFamily: "Montserrat", px: 56, weight: 900, tracking: "0.06em", upper: true }
  caption:    { fontFamily: "Montserrat", px: 50, weight: 800, lineHeight: 1.18 }
  card-value: { fontFamily: "Montserrat", px: 38, weight: 900, lineHeight: 1.08, upper: true }
  body:       { fontFamily: "Montserrat", px: 38, weight: 700, lineHeight: 1.3 }
  label:      { fontFamily: "Montserrat", px: 26, weight: 700, tracking: "0.14em", upper: true }
  kicker:     { fontFamily: "Montserrat", px: 34, weight: 700, tracking: "0.16em", upper: true }

spacing:
  edge-x: "90px"
  card-gap: "18px"
  safe-top: "220px"
  safe-bottom: "1570px"   # keep key content above Instagram's caption/UI zone

components:
  caption:
    style: "white text on {colors.navy} pill, 12px radius, 8px solid {colors.orange} drop under"
    placement: "centred, top 1420px, max-width 940px"
  name-tag:
    style: "white on {colors.orange}, 8px radius"
  info-card:
    style: "{colors.navy} card, 14px radius; {colors.orange} tracked label over white 900 value; round mark at right"
    marks: "✗ = {colors.orange} circle + white cross · ✓ = {colors.cream} circle + {colors.navy} tick (SVG, not glyphs)"
  chip:
    style: "{colors.navy} block, white 900 text, keyword in {colors.orange}, 8px {colors.orange} bottom border"
  divider:
    style: "8px {colors.orange} vertical rule at x=536 for split-screen comparisons"
  dim:
    style: "{colors.dim-overlay} + grayscale backdrop over the half not in focus"
  stamp:
    style: "{colors.orange-text-on-light} 900 text on near-white, 10px orange border, rotated −7°"
  end-card:
    ground: "{colors.navy}, cream wedge rotated −12° across the bottom"
    order: "logo → display headline (key words in orange) → orange rule → kicker + headline offer → orange CTA button → clinics → @alphasportsmed in orange"
    clinics: "Newport · Ascot Vale · Bacchus Marsh · Hawthorn"
  logo: "assets/alpha-logo.png (white wordmark + orange alpha mark, transparent)"
---

## Overview

Alpha reels are real training footage dressed with confident, clinical-but-cheeky graphics. The
navy is the brand's authority; orange is the voice — tags, keywords, CTAs. Cream appears as
the end-card wedge and on tick marks only.

## Rules

- Montserrat only (bundled 400/700/900). No second typeface.
- Footage scenes: never a full navy wash — overlays are cards, tags, captions and dims.
- Captions burned in for every voiceover line (sound-off viewing).
- Orange text on white/cream uses the darker text oranges for contrast; pure `#F15F2E` is for fills and text on navy.
- One call to action per reel, on the navy end card; current default is "link in bio".
- iPhone footage is often HDR (HLG): tone-map to SDR bt709 before building, and render with `--sdr`.
- Voiceover: deadpan, understated — the team's own recorded voice preferred.
