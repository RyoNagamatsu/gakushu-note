"""Render a child's handwriting to PNG sheets for grading.
python3 tools/render_ink.py /path/gakushu-data/data/w2026-10-12-t.json outdir
Each image shows one answer box labelled with its item id (the part after '__')."""
import json, sys, os
from PIL import Image, ImageDraw
d = json.load(open(sys.argv[1], encoding='utf8')); out = sys.argv[2]; os.makedirs(out, exist_ok=True)
tiles = []
for key in sorted(d.get('ink', {})):
    st = [list(map(int, s.split(','))) for s in d['ink'][key].get('s', []) if s]
    if not st: continue
    mx = max(max(s[0::2]) for s in st); my = max(max(s[1::2]) for s in st)
    W = 1000 if my > 420 or mx > 0 else 1000; sc = 0.9 if my > 700 else 0.45
    w, h = int(1000 * sc), int((my + 40) * sc) + 24
    im = Image.new('RGB', (w, h), 'white'); g = ImageDraw.Draw(im)
    for s in st:
        pts = [(s[i] * sc, s[i + 1] * sc + 22) for i in range(0, len(s), 2)]
        if len(pts) == 1: g.ellipse([pts[0][0] - 2, pts[0][1] - 2, pts[0][0] + 2, pts[0][1] + 2], fill='black')
        else: g.line(pts, fill='black', width=3)
    g.text((4, 4), key.split('__')[1] + '  (%d strokes)' % len(st), fill=(200, 0, 0)); g.rectangle([0, 0, w - 1, h - 1], outline=(190, 190, 190))
    tiles.append(im)
# pack tiles into sheets about 1400px tall
sheet, y, n = [], 0, 0
def flush():
    global sheet, y, n
    if not sheet: return
    W = max(t.width for t in sheet); S = Image.new('RGB', (W, sum(t.height for t in sheet)), 'white'); yy = 0
    for t in sheet: S.paste(t, (0, yy)); yy += t.height
    n += 1; S.save(os.path.join(out, 'sheet%02d.png' % n)); sheet, y = [], 0
for t in tiles:
    if y + t.height > 1400: flush()
    sheet.append(t); y += t.height
flush(); print(n, 'sheets,', len(tiles), 'boxes ->', out)
