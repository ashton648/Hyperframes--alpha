"""Alpha Sports Medicine back print: 'connected issues, connective tissues'.
Text is converted to vector outlines (Rubik ExtraBold, OFL) so the SVGs are print-ready."""
import math, random
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen

W = 1200
NAVY, BLUE, LBLUE, ORANGE = "#0B2545", "#1F6FD1", "#5AB0FF", "#F7801E"
font = TTFont("fonts/rubik-latin-800-normal.woff2")
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

CAP = font["OS/2"].sCapHeight / UPM  # cap height as a fraction of font size

def layout():
    size = 900 / width("CONNECTIVE", 1)        # one size for all four words
    cap, lead = CAP * size, 0.30 * size
    b1 = 130 + cap + 15                         # CONNECTED
    b2 = b1 + lead + cap                        # ISSUES,
    cy = b2 + 96                                # squiggle, tucked under the words
    b3 = cy + 80 + cap                          # CONNECTIVE
    b4 = b3 + lead + cap                        # TISSUES
    b5 = b4 + 105                               # brand line
    return size, (b1, b2), cy, (b3, b4), b5, b5 + 125

def build(fg, bg):
    size, (b1, b2), cy, (b3, b4), b5, h = layout()
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {h:.0f}" width="{W}" height="{h:.0f}">']
    if bg:
        o.append(f'<rect width="100%" height="100%" fill="{bg}"/>')
    blue = LBLUE if fg == "#FFFFFF" else BLUE
    # wonky, bouncy top words
    o.append(text_paths("CONNECTED", 600, b1, size, lambda i, c: blue, wobble=1.0, seed=7))
    o.append(text_paths("ISSUES,", 600, b2, size, lambda i, c: blue, wobble=1.0, seed=3))
    # tangle -> smooth line, ending in a little dot
    d = squiggle(170, 1000, cy)
    x_end, y_end = (float(v) for v in d.rsplit(' L', 1)[1].split(','))
    o.append(f'<path d="{d}" fill="none" stroke="{ORANGE}" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/>')
    o.append(f'<circle cx="{x_end + 30:.1f}" cy="{y_end:.1f}" r="13" fill="{ORANGE}"/>')
    # calm, tidy bottom words
    o.append(text_paths("CONNECTIVE", 600, b3, size, lambda i, c: fg))
    o.append(text_paths("TISSUES", 600, b4, size, lambda i, c: fg))
    # small brand line, letter-spaced
    o.append(text_paths("ALPHA SPORTS MEDICINE", 600, b5, 34, lambda i, c: blue, tracking=0.18))
    o.append('</svg>')
    return "\n".join(o)

if __name__ == "__main__":
    open("back-print-navy-shirt.svg", "w").write(build("#FFFFFF", None))
    open("back-print-white-shirt.svg", "w").write(build(NAVY, None))
    open("_prev_navy.svg", "w").write(build("#FFFFFF", NAVY))
    open("_prev_white.svg", "w").write(build(NAVY, "#FFFFFF"))
