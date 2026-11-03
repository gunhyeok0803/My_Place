"""Top-down map of an SPZ file (x right, z down) with a 0.5 m grid, to pick cleanup boundaries."""
import sys
import numpy as np
from PIL import Image, ImageDraw
import spz

src, out = sys.argv[1], sys.argv[2]
keep_path = sys.argv[3] if len(sys.argv) > 3 else None
x0, x1, z0, z1, px = -4.5, 3.5, -4.0, 4.0, 110          # metres, pixels per metre
s = spz.read(src)
p, a = spz.positions(s), spz.alphas(s)
col = s['blocks']['color'].astype(np.float64)
rgb = np.clip(0.5 + 0.28209 * ((col / 255.0 - 0.5) / 0.15), 0, 1)
m = (a > 0.25) & (p[:, 1] > -1.0) & (p[:, 1] < 1.6)
if keep_path:
    m &= np.load(keep_path)
order = np.argsort(p[m, 1])                                   # draw low first, high last
P, RGB = p[m][order], rgb[m][order]
W, H = int((x1 - x0) * px), int((z1 - z0) * px)
img = np.full((H, W, 3), 18, np.uint8)
u = ((P[:, 0] - x0) * px).astype(int); v = ((P[:, 2] - z0) * px).astype(int)
ok = (u >= 0) & (u < W) & (v >= 0) & (v < H)
img[v[ok], u[ok]] = (RGB[ok] * 255).astype(np.uint8)
im = Image.fromarray(img); d = ImageDraw.Draw(im)
for gx in np.arange(np.ceil(x0 * 2) / 2, x1 + 1e-6, 0.5):
    X = int((gx - x0) * px); d.line([(X, 0), (X, H)], fill=(60, 90, 80) if gx % 1 else (90, 160, 140))
    if gx % 1 == 0: d.text((X + 2, 2), f'x{gx:g}', fill=(160, 220, 200))
for gz in np.arange(np.ceil(z0 * 2) / 2, z1 + 1e-6, 0.5):
    Z = int((gz - z0) * px); d.line([(0, Z), (W, Z)], fill=(60, 90, 80) if gz % 1 else (90, 160, 140))
    if gz % 1 == 0: d.text((2, Z + 2), f'z{gz:g}', fill=(160, 220, 200))
im.save(out)
print('drawn', ok.sum(), 'of', s['n'])
