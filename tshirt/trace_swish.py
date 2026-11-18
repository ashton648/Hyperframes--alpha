"""Trace the orange alpha swish from the Alpha Sports Medicine logo PNG into an SVG path."""
import numpy as np, potrace
from PIL import Image

im = np.array(Image.open("alpha-logo-white.png").convert("RGBA")).astype(int)
r, g, b, a = im[..., 0], im[..., 1], im[..., 2], im[..., 3]
mask = (a > 128) & (r > 180) & (g < 160) & (b < 120)        # orange pixels only
ys, xs = np.nonzero(mask)
x0, x1, y0, y1 = xs.min(), xs.max() + 1, ys.min(), ys.max() + 1
mask = mask[y0:y1, x0:x1]
paths = potrace.Bitmap(~mask).trace(turdsize=20, alphamax=1.0, opticurve=True, opttolerance=0.2)

parts = []
for curve in paths:
    s = curve.start_point
    parts.append(f"M{s.x:.1f},{s.y:.1f}")
    for seg in curve.segments:
        if seg.is_corner:
            parts.append(f"L{seg.c.x:.1f},{seg.c.y:.1f}L{seg.end_point.x:.1f},{seg.end_point.y:.1f}")
        else:
            parts.append(f"C{seg.c1.x:.1f},{seg.c1.y:.1f} {seg.c2.x:.1f},{seg.c2.y:.1f} {seg.end_point.x:.1f},{seg.end_point.y:.1f}")
    parts.append("Z")
w, h = x1 - x0, y1 - y0
open("alpha-swish.path", "w").write(f"{w} {h}\n" + "".join(parts))
print(w, h, len(paths))
