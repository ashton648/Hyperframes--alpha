"""Alpha Sports Medicine back print: 'connected issues, connective tissues'.
Text is converted to vector outlines (Fredoka SemiBold, OFL) so the SVGs are print-ready."""
import math, random
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen

W = 1200
NAVY, BLUE, LBLUE, ORANGE = "#0B2545", "#1F6FD1", "#5AB0FF", "#F7801E"
font = TTFont("fonts/fredoka-latin-600-normal.woff2")
gs, cmap, UPM = font.getGlyphSet(), font.getBestCmap(), font["head"].unitsPerEm

def width(text, size, tracking=0.0):
    return sum(gs[cmap[ord(c)]].width for c in text) * size / UPM + tracking * size * (len(text) - 1)

def text_paths(text, cx, baseline, size, colours, wobble=0.0, seed=1, tracking=0.0):
    """One <path> per glyph; wobble adds a playful bounce/tilt to each letter."""
    rnd = random.Random(seed)
    s = size / UPM
    x = cx - width(text, size, tracking) / 2
    out = []
    for i, c in enumerate(text):
        g = gs[cmap[ord(c)]]
        dy = wobble * 14 * math.sin(i * 1.3) + rnd.uniform(-1, 1) * wobble * 6
        rot = rnd.uniform(-1, 1) * wobble * 9
        if c != " ":
            pen = SVGPathPen(gs)
            g.draw(TransformPen(pen, (s, 0, 0, -s, x, baseline + dy)))
            gx = x + g.width * s / 2
            out.append(f'<path d="{pen.getCommands()}" fill="{colours(i, c)}" '
                       f'transform="rotate({rot:.1f} {gx:.1f} {baseline - size*0.3:.1f})"/>')
        x += g.width * s + tracking * size
    return "\n".join(out)

def squiggle(x0, x1, cy):
    """A tangled scribble that relaxes into a calm wave: issues -> healthy tissue."""
    pts, n = [], 1400
    for k in range(n + 1):
        u = k / n
        t = u * 30 * math.pi
        fade = max(0.0, 1 - u / 0.55) ** 1.2                 # loops shrink then vanish
        r = 58 * fade * (0.75 + 0.25 * math.sin(t * 0.37))   # uneven loops = messy knot
        x = x0 + (x1 - x0) * u - r * math.sin(t)
        y = cy + r * math.cos(t) * 0.9 + 22 * math.sin(u * 3.2 * math.pi) * (0.3 + 0.7 * u)
        pts.append((x, y))
    return "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts)

CAP = 0.70  # Fredoka cap height as a fraction of font size

def layout():
    l1, l2, l3 = "CONNECTED ISSUES,", "CONNECTIVE TISSUES", "ALPHA SPORTS MEDICINE"
    s1, s2, s3 = 1000 / width(l1, 1), 1000 / width(l2, 1), 34
    b1 = 130 + CAP * s1 + 15            # top line baseline
    cy = b1 + 84                        # squiggle centre, tucked right under the words
    b2 = cy + 76 + CAP * s2             # bottom line sits just under the squiggle
    b3 = b2 + 95                        # small brand line
    return (l1, s1, b1), cy, (l2, s2, b2), (l3, s3, b3), b3 + 115

def build(fg, bg):
    (l1, s1, b1), cy, (l2, s2, b2), (l3, s3, b3), h = layout()
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {h:.0f}" width="{W}" height="{h:.0f}">']
    if bg:
        o.append(f'<rect width="100%" height="100%" fill="{bg}"/>')
    blue = LBLUE if fg == "#FFFFFF" else BLUE
    # wonky, bouncy top line
    o.append(text_paths(l1, 600, b1, s1, lambda i, c: blue, wobble=1.0, seed=7))
    # tangle -> smooth line, ending in a little dot
    d = squiggle(150, 1020, cy)
    x_end, y_end = (float(v) for v in d.rsplit(' L', 1)[1].split(','))
    o.append(f'<path d="{d}" fill="none" stroke="{ORANGE}" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/>')
    o.append(f'<circle cx="{x_end + 30:.1f}" cy="{y_end:.1f}" r="13" fill="{ORANGE}"/>')
    # calm, tidy bottom line
    o.append(text_paths(l2, 600, b2, s2, lambda i, c: fg))
    # small brand line, letter-spaced
    o.append(text_paths(l3, 600, b3, s3, lambda i, c: blue, tracking=0.18))
    o.append('</svg>')
    return "\n".join(o)

if __name__ == "__main__":
    open("back-print-navy-shirt.svg", "w").write(build("#FFFFFF", None))
    open("back-print-white-shirt.svg", "w").write(build(NAVY, None))
    open("_prev_navy.svg", "w").write(build("#FFFFFF", NAVY))
    open("_prev_white.svg", "w").write(build(NAVY, "#FFFFFF"))
