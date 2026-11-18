"""Alpha Sports Medicine back print: 'connected issues, connective tissues'.
Text is converted to vector outlines (Fredoka SemiBold, OFL) so the SVGs are print-ready."""
import math, random
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen

W, H = 1200, 1020
NAVY, BLUE, LBLUE, ORANGE = "#0B2545", "#1F6FD1", "#5AB0FF", "#F7801E"
font = TTFont("fonts/fredoka-latin-600-normal.woff2")
gs, cmap, UPM = font.getGlyphSet(), font.getBestCmap(), font["head"].unitsPerEm

def width(text, size):
    return sum(gs[cmap[ord(c)]].width for c in text) * size / UPM

def text_paths(text, cx, baseline, size, colours, wobble=0.0, seed=1):
    """One <path> per glyph; wobble adds a playful bounce/tilt to each letter."""
    rnd = random.Random(seed)
    s = size / UPM
    x = cx - width(text, size) / 2
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
        x += g.width * s
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

def build(fg, bg):
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">']
    if bg:
        o.append(f'<rect width="100%" height="100%" fill="{bg}"/>')
    blue = LBLUE if bg != "#FFFFFF" and fg == "#FFFFFF" else BLUE
    # wonky, slightly jumbled top line
    l1 = "connected issues,"
    o.append(text_paths(l1, 600, 260, 1000 / width(l1, 1), lambda i, c: blue, wobble=1.0, seed=7))
    # tangle -> smooth line, ending in a little dot
    d = squiggle(170, 1030, 450)
    x_end, y_end = (float(v) for v in d.rsplit(' L', 1)[1].split(','))
    x_end += 30
    o.append(f'<path d="{d}" fill="none" stroke="{ORANGE}" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/>')
    o.append(f'<circle cx="{x_end:.1f}" cy="{y_end:.1f}" r="13" fill="{ORANGE}"/>')
    # calm, tidy bottom line with the orange "t"
    l2 = "connective tissues"
    o.append(text_paths(l2, 600, 700, 1000 / width(l2, 1),
                        lambda i, c: ORANGE if i == l2.index("t", 11) else fg, wobble=0.0))
    # small brand line
    l3 = "alpha sports medicine"
    o.append(text_paths(l3, 600, 880, 46, lambda i, c: blue))
    o.append('</svg>')
    return "\n".join(o)

if __name__ == "__main__":
    open("back-print-navy-shirt.svg", "w").write(build("#FFFFFF", None))
    open("back-print-white-shirt.svg", "w").write(build(NAVY, None))
    open("_prev_navy.svg", "w").write(build("#FFFFFF", NAVY))
    open("_prev_white.svg", "w").write(build(NAVY, "#FFFFFF"))
