"""Clean room_Chair.spz: keep the room box, drop floaters / isolated specks, erase the scanned desk chair."""
import sys, json
import numpy as np
import spz

src, out = sys.argv[1], sys.argv[2]
cfg = dict(
    wall_deg=124.0,                   # direction of the desk wall in the xz plane
    u=(-2.6, 2.35), v=(-4.0, 1.42),   # room box along / across the wall (m)
    y=(-1.0, 1.7),                    # floor -0.9, keep up to ~2.6 m above floor
    min_alpha=0.08, max_scale=0.30,   # near-invisible / oversized blobs
    voxel=0.06, min_count=3,          # isolated specks
    chair=(0.078, 0.029, 0.56, -0.83, 0.4),   # scanned chair: x, z, radius, y0, y1 (floor kept)
)
s = spz.read(src)
p, a, sc = spz.positions(s), spz.alphas(s), spz.scales(s).max(1)
t = np.radians(cfg['wall_deg'])
u = p[:, 0] * np.cos(t) + p[:, 2] * np.sin(t)
v = p[:, 0] * np.sin(t) - p[:, 2] * np.cos(t)
steps = {}
keep = np.ones(s['n'], bool)
def apply(name, m):
    global keep
    before = keep.sum(); keep &= m; steps[name] = int(before - keep.sum())
apply('outside_room', (u > cfg['u'][0]) & (u < cfg['u'][1]) & (v > cfg['v'][0]) & (v < cfg['v'][1])
      & (p[:, 1] > cfg['y'][0]) & (p[:, 1] < cfg['y'][1]))
apply('beyond_end_wall', ~((u < -2.2) & (v > -1.4)))   # streaks past the end wall (no floor there)
apply('faint', a >= cfg['min_alpha'])
apply('oversized', sc <= cfg['max_scale'])
# isolated specks: voxel occupancy among the splats still kept
vox = np.floor(p / cfg['voxel']).astype(np.int64)
key = (vox[:, 0] * 73856093) ^ (vox[:, 1] * 19349663) ^ (vox[:, 2] * 83492791)
k = key[keep]; uniq, inv, cnt = np.unique(k, return_inverse=True, return_counts=True)
dense = np.zeros(s['n'], bool); dense[np.where(keep)[0]] = cnt[inv] >= cfg['min_count']
apply('isolated', dense)
# dark smudges: low dark floaters over open floor (cells with nothing taller above them)
col = s['blocks']['color'].astype(np.float64)
lum = np.clip(0.5 + 0.28209 * ((col / 255.0 - 0.5) / 0.15), 0, 1).mean(1)
cell = np.floor(p[:, [0, 2]] / 0.1).astype(np.int64)
ckey = cell[:, 0] * 100003 + cell[:, 1]
tall_cells = set(np.unique(ckey[keep & (p[:, 1] > -0.45)]).tolist())
grown = set()
for c in tall_cells:                                   # dilate by one cell so object edges stay
    cxx, czz = divmod(c, 100003) if c >= 0 else (c // 100003, c % 100003)
    for dx in (-1, 0, 1):
        for dz in (-1, 0, 1):
            grown.add((cxx + dx) * 100003 + (czz + dz))
open_floor = ~np.isin(ckey, np.fromiter(grown, np.int64))
apply('floor_smudge', ~((p[:, 1] > -0.85) & (p[:, 1] < -0.45) & (lum < 0.3) & open_floor))
cx, cz, r, y0, y1 = cfg['chair']
apply('scanned_chair', ~(((p[:, 0] - cx) ** 2 + (p[:, 2] - cz) ** 2 < r * r) & (p[:, 1] > y0) & (p[:, 1] < y1)))
n = spz.write(s, keep, out)
np.save(out + '.keep.npy', keep)
print(json.dumps(dict(total=s['n'], kept=n, removed=steps), ensure_ascii=False))
