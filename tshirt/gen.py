import math
W, H = 1200, 1430
NAVY, BLUE, LBLUE, ORANGE = "#0B2545", "#1F6FD1", "#5AB0FF", "#F7801E"

def strand(i, n, x0, x1, cy, phase, amp, spread_end, spread_mid, crimp_k):
    pts = []
    steps = 240
    off = (i - (n-1)/2) / ((n-1)/2)  # -1..1
    for s in range(steps+1):
        x = x0 + (x1-x0)*s/steps
        t = (x - (x0+x1)/2) / ((x1-x0)/2)          # -1..1
        spread = spread_mid + (spread_end-spread_mid)*(t*t)
        a = amp * (0.35 + 0.65*t*t)                 # crimp relaxes at the pinch
        y = cy + off*spread + a*math.sin(crimp_k*x/100 + phase + i*0.55)
        pts.append((x, y))
    return "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts)

def build(fg, bg, shirt_label):
    out = []
    out.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">')
    if bg:
        out.append(f'<rect width="100%" height="100%" fill="{bg}"/>')
    out.append('<style>.d{font-family:"Inter Display","Inter",sans-serif;font-weight:900;}'
               '.s{font-family:"Inter",sans-serif;font-weight:700;letter-spacing:9px;}</style>')
    # header
    out.append(f'<line x1="150" y1="150" x2="295" y2="150" stroke="{ORANGE}" stroke-width="4"/>')
    out.append(f'<line x1="905" y1="150" x2="1050" y2="150" stroke="{ORANGE}" stroke-width="4"/>')
    out.append(f'<text class="s" x="600" y="160" font-size="28" fill="{fg}" text-anchor="middle">ALPHA SPORTS MEDICINE</text>')
    # fibre bundle
    cy, n = 370, 13
    blues = [BLUE, LBLUE, fg]
    for i in range(n):
        d = strand(i, n, 110, 1090, cy, 0.0, 14, 125, 16, 3.2)
        col = blues[i % 3]
        op = 0.95 if col != fg else 0.55
        out.append(f'<path d="{d}" fill="none" stroke="{col}" stroke-opacity="{op}" stroke-width="5" stroke-linecap="round"/>')
    # orange strand weaving across the bundle
    pts = []
    for s in range(301):
        x = 110 + 980*s/300
        t = (x-600)/490
        spread = 16 + 108*t*t
        y = cy + spread*math.sin(x/62) + 6*math.sin(x/9)
        pts.append((x, y))
    d = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    out.append(f'<path d="{d}" fill="none" stroke="{bg or NAVY}" stroke-width="16" stroke-linecap="round"/>')
    out.append(f'<path d="{d}" fill="none" stroke="{ORANGE}" stroke-width="8" stroke-linecap="round"/>')
    # junction node at the pinch
    out.append(f'<circle cx="600" cy="{cy}" r="34" fill="{bg or NAVY}" stroke="{ORANGE}" stroke-width="7"/>')
    out.append(f'<circle cx="600" cy="{cy}" r="13" fill="{ORANGE}"/>')
    for x in (160, 1040):
        out.append(f'<circle cx="{x}" cy="{cy}" r="7" fill="{ORANGE}"/>')
    # typography: outlined "issues" -> solid "tissues"
    o = f'fill="none" stroke="{LBLUE if fg == '#FFFFFF' else BLUE}" stroke-width="4"'
    lines = [("CONNECTED", 631.25, "out"), ("ISSUES,", 393.9, "out"), ("CONNECTIVE", 663.28, "solid"), ("TISSUES", 432.97, "solid")]
    y, gaps = 590, [0, 38, 80, 38]
    for (w, m, style), g in zip(lines, gaps):
        fs = 980/m*100
        y += g + 0.727*fs
        attrs = o if style == "out" else f'fill="{fg}"'
        txt = w
        if w == "CONNECTIVE": txt = f'CONNECT<tspan fill="{ORANGE}">IVE</tspan>'
        if w == "TISSUES": txt = f'<tspan fill="{ORANGE}">T</tspan>ISSUES'
        out.append(f'<text class="d" x="600" y="{y:.0f}" font-size="{fs:.1f}" text-anchor="middle" {attrs}>{txt}</text>')
    out.append(f'<line x1="540" y1="{y+55:.0f}" x2="660" y2="{y+55:.0f}" stroke="{ORANGE}" stroke-width="6" stroke-linecap="round"/>')
    out.append('</svg>')
    return "\n".join(out)

open("back-print-navy-shirt.svg", "w").write(build("#FFFFFF", None, "navy"))
open("back-print-white-shirt.svg", "w").write(build(NAVY, None, "white"))
open("_prev_navy.svg", "w").write(build("#FFFFFF", NAVY, "navy"))
open("_prev_white.svg", "w").write(build(NAVY, "#FFFFFF", "white"))
