"""Minimal lossless SPZ (Niantic gaussian splat) reader / filter writer.
Layout after gzip: 16-byte header, then planar blocks: positions (N*9), alphas (N), colors (N*3),
scales (N*3), rotations (N*3 for v2, N*4 for v3), SH (N*shDim*3)."""
import gzip, struct
import numpy as np

SH_DIM = {0: 0, 1: 3, 2: 8, 3: 15}


def read(path):
    raw = gzip.decompress(open(path, 'rb').read())
    magic, version, n, sh, frac, flags, _ = struct.unpack_from('<IIIBBBB', raw, 0)
    assert magic == 0x5053474E, hex(magic)
    rot = 3 if version < 3 else 4
    sizes = [('pos', 9), ('alpha', 1), ('color', 3), ('scale', 3), ('rot', rot), ('sh', SH_DIM[sh] * 3)]
    blocks, off = {}, 16
    for name, per in sizes:
        blocks[name] = np.frombuffer(raw, dtype=np.uint8, count=n * per, offset=off).reshape(n, per) if per else np.zeros((n, 0), np.uint8)
        off += n * per
    assert off == len(raw), (off, len(raw))
    return dict(version=version, n=n, sh=sh, frac=frac, flags=flags, blocks=blocks)


def positions(s):
    p = s['blocks']['pos'].astype(np.int32).reshape(-1, 3, 3)
    v = p[:, :, 0] | (p[:, :, 1] << 8) | (p[:, :, 2] << 16)
    v = np.where(v & 0x800000, v - 0x1000000, v)
    return v.astype(np.float64) / (1 << s['frac'])


def alphas(s):  # 0..1
    return s['blocks']['alpha'][:, 0].astype(np.float64) / 255.0


def scales(s):  # linear scale per axis
    return np.exp(s['blocks']['scale'].astype(np.float64) / 16.0 - 10.0)


def write(s, keep, path):
    keep = np.asarray(keep)
    n = int(keep.sum()) if keep.dtype == bool else len(keep)
    head = struct.pack('<IIIBBBB', 0x5053474E, s['version'], n, s['sh'], s['frac'], s['flags'], 0)
    body = b''.join(s['blocks'][k][keep].tobytes() for k in ('pos', 'alpha', 'color', 'scale', 'rot', 'sh'))
    open(path, 'wb').write(gzip.compress(head + body, compresslevel=9))
    return n
