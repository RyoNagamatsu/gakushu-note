# 英検2級 面接れんしゅう No.2 の3コマの絵（SVG）をつくる
import math, json
W, H = 300, 220
INK = '#2b2d42'
SK = '#ffd9b8'

def f(v): return ('%.1f' % v).rstrip('0').rstrip('.')

def line(x1, y1, x2, y2, c=INK, w=2.5):
    return f'<line x1="{f(x1)}" y1="{f(y1)}" x2="{f(x2)}" y2="{f(y2)}" stroke="{c}" stroke-width="{w}" stroke-linecap="round"/>'

def rect(x, y, w, h, fill, rx=0, sw=2, st=INK):
    return f'<rect x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(h)}" rx="{rx}" fill="{fill}" stroke="{st}" stroke-width="{sw}"/>'

def circ(x, y, r, fill, sw=2, st=INK):
    return f'<circle cx="{f(x)}" cy="{f(y)}" r="{f(r)}" fill="{fill}" stroke="{st}" stroke-width="{sw}"/>'

def path(d, fill='none', sw=2, st=INK, extra=''):
    return f'<path d="{d}" fill="{fill}" stroke="{st}" stroke-width="{sw}" stroke-linejoin="round" stroke-linecap="round" {extra}/>'

def text(x, y, s, size=11, fill=INK, weight=700, anchor='middle', fam='Arial,Helvetica,sans-serif'):
    s = s.replace('&', '&amp;').replace('<', '&lt;')
    return f'<text x="{f(x)}" y="{f(y)}" font-size="{size}" font-weight="{weight}" fill="{fill}" text-anchor="{anchor}" font-family="{fam}">{s}</text>'

KINDS = {
    'boy':     dict(h=1.0, shirt='#4dabf7', pants='#1d4e89', hair='#2b2d42', style='short'),
    'boy2':    dict(h=1.0, shirt='#ff922b', pants='#495057', hair='#6b4226', style='short'),
    'blond':   dict(h=1.05, shirt='#51cf66', pants='#1d4e89', hair='#f2c14e', style='short'),
    'girl':    dict(h=0.98, shirt='#f783ac', pants='#d6336c', hair='#2b2d42', style='pig', skirt=True),
    'girl2':   dict(h=0.98, shirt='#ffd43b', pants='#e8590c', hair='#7a4a2a', style='pony', skirt=True),
    'mom':     dict(h=1.3, shirt='#63c174', pants='#2f7d4a', hair='#3b2a20', style='bun', skirt=True),
    'dad':     dict(h=1.38, shirt='#74c0fc', pants='#3d4a5c', hair='#2b2d42', style='short', glasses=True),
    'teacher': dict(h=1.32, shirt='#b197fc', pants='#5f3dc4', hair='#3b2a20', style='long', skirt=True, glasses=True),
    'man':     dict(h=1.35, shirt='#ffa94d', pants='#495057', hair='#495057', style='short'),
    'woman':   dict(h=1.3, shirt='#ff8787', pants='#5c7cfa', hair='#6b4226', style='pony', skirt=True),
}

def person(x, y, kind, arms=(20, -20), mouth='smile', face=0, s=1.0, legs='stand', held=None, eyes='open', back=False):
    """x: 中心, y: 足もと。arms: 左右の腕の角度（真下=0, 前=90, 上=180。左腕は左へ、右腕は右へ開く）。
    face: -1 左を向く, 1 右を向く, 0 正面。held: {'L':svg関数, 'R':svg関数}（手の位置を受け取る）"""
    k = KINDS[kind]
    sc = s * k['h']
    out = []
    leg = 30 * sc; body = 34 * sc; hr = 15 * s
    hip = y - leg; sh = hip - body; hy = sh - hr + 1
    # 足
    if legs == 'stand':
        out.append(line(x - 6 * sc, hip, x - 7 * sc, y, k['pants'], 6 * sc))
        out.append(line(x + 6 * sc, hip, x + 7 * sc, y, k['pants'], 6 * sc))
    elif legs == 'run':
        out.append(line(x - 4 * sc, hip, x - 18 * sc, y - 4 * sc, k['pants'], 6 * sc))
        out.append(line(x + 4 * sc, hip, x + 14 * sc, y, k['pants'], 6 * sc))
    elif legs == 'sit':  # 横向きにすわる（face の方へひざ）
        d = face or 1
        out.append(line(x, hip, x + d * 18 * sc, hip, k['pants'], 7 * sc))
        out.append(line(x + d * 18 * sc, hip, x + d * 18 * sc, y, k['pants'], 6 * sc))
    elif legs == 'kneel':
        d = face or 1
        out.append(line(x, hip, x + d * 14 * sc, hip + 10 * sc, k['pants'], 7 * sc))
        out.append(line(x + d * 14 * sc, hip + 10 * sc, x - d * 4 * sc, y, k['pants'], 6 * sc))
    elif legs == 'none':
        pass
    # 体
    if k.get('skirt'):
        out.append(path(f'M{f(x-9*sc)} {f(sh+4)} L{f(x+9*sc)} {f(sh+4)} L{f(x+16*sc)} {f(hip+4*sc)} L{f(x-16*sc)} {f(hip+4*sc)} Z', k['pants'], 2))
        out.append(path(f'M{f(x-11*sc)} {f(sh)} Q{f(x)} {f(sh-4*sc)} {f(x+11*sc)} {f(sh)} L{f(x+11*sc)} {f(sh+body*0.55)} L{f(x-11*sc)} {f(sh+body*0.55)} Z', k['shirt'], 2))
    else:
        out.append(path(f'M{f(x-12*sc)} {f(sh)} Q{f(x)} {f(sh-4*sc)} {f(x+12*sc)} {f(sh)} L{f(x+11*sc)} {f(hip)} L{f(x-11*sc)} {f(hip)} Z', k['shirt'], 2))
    # 腕
    hands = {}
    al = 26 * sc
    for side, ang in (('L', arms[0]), ('R', arms[1])):
        sx = x - 10 * sc if side == 'L' else x + 10 * sc
        a = math.radians(ang)
        dx = math.sin(a) * al * (-1 if side == 'L' else 1)
        dy = math.cos(a) * al
        ex, ey = sx + dx, sh + 4 * sc + dy
        out.append(line(sx, sh + 4 * sc, ex, ey, k['shirt'], 6 * sc))
        out.append(circ(ex, ey, 3.6 * sc, SK, 1.5))
        hands[side] = (ex, ey)
    # 頭
    hc = k['hair']
    st = k['style']
    if st == 'long':
        out.append(path(f'M{f(x-hr-2)} {f(hy)} Q{f(x-hr-4)} {f(hy+hr+12)} {f(x-hr+2)} {f(hy+hr+14)} L{f(x+hr-2)} {f(hy+hr+14)} Q{f(x+hr+4)} {f(hy+hr+12)} {f(x+hr+2)} {f(hy)} Z', hc, 2))
    if st == 'pony':
        bx = x + (-1 if face > 0 else 1) * (hr + 2)
        out.append(path(f'M{f(bx)} {f(hy-4)} Q{f(bx+(-8 if face>0 else 8))} {f(hy+8)} {f(bx+(-3 if face>0 else 3))} {f(hy+20)}', hc, 5, hc))
    if st == 'pig':
        for d in (-1, 1):
            out.append(circ(x + d * (hr + 3), hy + 4, 5 * s, hc, 1.5))
    if st == 'bun':
        out.append(circ(x + (-hr + 2 if face >= 0 else hr - 2), hy - hr + 2, 7 * s, hc, 1.5))
    out.append(circ(x, hy, hr, SK, 2))
    if back:
        out.append(path(f'M{f(x-hr)} {f(hy+2)} A{f(hr)} {f(hr)} 0 1 1 {f(x+hr)} {f(hy+2)} Q{f(x)} {f(hy+8)} {f(x-hr)} {f(hy+2)} Z', hc, 2))
        return '\n'.join(out), hands, (x, hy - hr)
    # 前がみ
    if st == 'short':
        out.append(path(f'M{f(x-hr)} {f(hy+1)} A{f(hr)} {f(hr)} 0 0 1 {f(x+hr)} {f(hy+1)} L{f(x+hr*0.6)} {f(hy-5*s)} L{f(x+hr*0.25)} {f(hy-2*s)} L{f(x-hr*0.15)} {f(hy-6*s)} L{f(x-hr*0.55)} {f(hy-2*s)} Z', hc, 2))
    else:
        out.append(path(f'M{f(x-hr)} {f(hy+3)} A{f(hr)} {f(hr)} 0 0 1 {f(x+hr)} {f(hy+3)} Q{f(x+hr*0.3)} {f(hy-8*s)} {f(x-hr*0.2)} {f(hy-3*s)} Q{f(x-hr*0.6)} {f(hy-1)} {f(x-hr)} {f(hy+3)} Z', hc, 2))
    fx = x + face * 4 * s
    ey = hy + 3 * s
    if eyes == 'open':
        out.append(circ(fx - 5 * s, ey, 1.8 * s, INK, 0)); out.append(circ(fx + 5 * s, ey, 1.8 * s, INK, 0))
    elif eyes == 'happy':
        out.append(path(f'M{f(fx-7*s)} {f(ey+1)} Q{f(fx-5*s)} {f(ey-3)} {f(fx-3*s)} {f(ey+1)}', 'none', 1.8))
        out.append(path(f'M{f(fx+3*s)} {f(ey+1)} Q{f(fx+5*s)} {f(ey-3)} {f(fx+7*s)} {f(ey+1)}', 'none', 1.8))
    elif eyes == 'tired':
        out.append(line(fx - 7 * s, ey, fx - 3 * s, ey, INK, 1.8)); out.append(line(fx + 3 * s, ey, fx + 7 * s, ey, INK, 1.8))
    elif eyes == 'wide':
        out.append(circ(fx - 5 * s, ey, 2.6 * s, '#fff', 1.4)); out.append(circ(fx + 5 * s, ey, 2.6 * s, '#fff', 1.4))
        out.append(circ(fx - 5 * s, ey, 1.2 * s, INK, 0)); out.append(circ(fx + 5 * s, ey, 1.2 * s, INK, 0))
    if k.get('glasses'):
        out.append(circ(fx - 5 * s, ey, 4 * s, 'none', 1.3)); out.append(circ(fx + 5 * s, ey, 4 * s, 'none', 1.3)); out.append(line(fx - 1 * s, ey, fx + 1 * s, ey, INK, 1.3))
    my = hy + 9 * s
    if mouth == 'smile':
        out.append(path(f'M{f(fx-4*s)} {f(my)} Q{f(fx)} {f(my+4*s)} {f(fx+4*s)} {f(my)}', 'none', 1.8))
    elif mouth == 'open':
        out.append(path(f'M{f(fx-4*s)} {f(my-1)} Q{f(fx)} {f(my+7*s)} {f(fx+4*s)} {f(my-1)} Z', '#e8453c', 1.5))
    elif mouth == 'o':
        out.append(f'<ellipse cx="{f(fx)}" cy="{f(my+1)}" rx="{f(2.6*s)}" ry="{f(3.4*s)}" fill="#e8453c" stroke="{INK}" stroke-width="1.5"/>')
    elif mouth == 'sad':
        out.append(path(f'M{f(fx-4*s)} {f(my+3*s)} Q{f(fx)} {f(my-1*s)} {f(fx+4*s)} {f(my+3*s)}', 'none', 1.8))
    elif mouth == 'flat':
        out.append(line(fx - 3 * s, my + 1, fx + 3 * s, my + 1, INK, 1.8))
    # ほお
    if mouth in ('smile', 'open') and eyes in ('open', 'happy'):
        out.append(f'<ellipse cx="{f(fx-9*s)}" cy="{f(my-2)}" rx="{f(2.6*s)}" ry="1.6" fill="#ffa8a8"/>')
        out.append(f'<ellipse cx="{f(fx+9*s)}" cy="{f(my-2)}" rx="{f(2.6*s)}" ry="1.6" fill="#ffa8a8"/>')
    return '\n'.join(out), hands, (x, hy - hr)

def P(*a, lean=0, **kw):
    g, hands, top = person(*a, **kw)
    if lean:
        x, y = a[0], a[1]
        r = math.radians(lean)
        def rot(p):
            dx, dy = p[0] - x, p[1] - y
            return (x + dx * math.cos(r) - dy * math.sin(r), y + dx * math.sin(r) + dy * math.cos(r))
        g = f'<g transform="rotate({lean} {x} {y})">{g}</g>'
        hands = {k: rot(v) for k, v in hands.items()}
        top = rot(top)
    return g, hands, top

def chair(x, y, d=1):
    """x: すわる位置の中心, y: 床。d: 向き（1=右向き）"""
    return rect(x - 14, y - 44, 28, 6, '#8b5a2b', 2, 1.6) + line(x - 10, y - 38, x - 10, y, '#8b5a2b', 3) + line(x + 10, y - 38, x + 10, y, '#8b5a2b', 3) + line(x - d * 14, y - 44, x - d * 14, y - 80, '#8b5a2b', 4)

def bubble(x, y, w, lines, tx, ty, size=11, kind='say'):
    """(x,y) 左上, w 幅。tx,ty はしっぽの先（話す人の口もと）"""
    lh = size * 1.25
    h = len(lines) * lh + 10
    out = []
    cx = x + w / 2
    bx = max(x + 14, min(x + w - 14, tx))
    if kind == 'say':
        out.append(path(f'M{f(bx-7)} {f(y+h-1)} L{f(tx)} {f(ty)} L{f(bx+7)} {f(y+h-1)} Z', '#fff', 2))
        out.append(rect(x, y, w, h, '#fff', 10, 2))
        out.append(rect(bx - 6, y + h - 3, 12, 4, '#fff', 0, 0, '#fff'))
    else:  # think
        out.append(f'<ellipse cx="{f(cx)}" cy="{f(y+h/2)}" rx="{f(w/2)}" ry="{f(h/2+4)}" fill="#fff" stroke="{INK}" stroke-width="2"/>')
        out.append(circ(tx + (bx - tx) * 0.55, ty + (y + h - ty) * 0.55, 4, '#fff', 1.8))
        out.append(circ(tx + (bx - tx) * 0.2, ty + (y + h - ty) * 0.2, 2.5, '#fff', 1.6))
    for i, s in enumerate(lines):
        out.append(text(cx, y + 5 + size + i * lh - 2, s, size))
    return '\n'.join(out)

def svg(body, bg):
    return f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" font-family="Arial,Helvetica,sans-serif"><rect width="{W}" height="{H}" fill="{bg}"/>{body}</svg>'

# ---- 背景・小物 ----
def sky_ground(sky='#d0ebff', ground='#b2f2bb', gy=165):
    return rect(0, 0, W, gy, sky, 0, 0, sky) + rect(0, gy, W, H - gy, ground, 0, 0, ground) + line(0, gy, W, gy, '#5c940d', 2)

def room(wall='#fff3bf', floor='#e9c46a', fy=170):
    return rect(0, 0, W, fy, wall, 0, 0, wall) + rect(0, fy, W, H - fy, floor, 0, 0, floor) + line(0, fy, W, fy, '#a0773b', 2)

def house(x, y, w=80, h=60, c='#ffe8cc', roof='#e8590c'):
    return rect(x, y, w, h, c) + path(f'M{f(x-8)} {f(y)} L{f(x+w/2)} {f(y-32)} L{f(x+w+8)} {f(y)} Z', roof) + rect(x + w * 0.62, y + h - 34, 18, 34, '#a0522d') + rect(x + 10, y + 12, 20, 18, '#a5d8ff')

def fence(y, x0=0, x1=W):
    o = [line(x0, y - 18, x1, y - 18, '#8d6e63', 3), line(x0, y - 8, x1, y - 8, '#8d6e63', 3)]
    for x in range(x0 + 6, x1, 22):
        o.append(path(f'M{x} {y} L{x} {y-26} L{x+5} {y-31} L{x+10} {y-26} L{x+10} {y} Z', '#d7b899', 1.5, '#8d6e63'))
    return ''.join(o)

def soil(x, y, w, h=14):
    o = [rect(x, y, w, h, '#a0522d', 4, 2)]
    for i in range(int(w // 18)):
        o.append(path(f'M{x+8+i*18} {y+3} q4 4 8 0', 'none', 1.5, '#6d3b1d'))
    return ''.join(o)

def sprout(x, y):
    return line(x, y, x, y - 10, '#2f9e44', 2.5) + path(f'M{x} {y-8} q-8 -6 -10 0 q6 4 10 0', '#69db7c', 1.4, '#2f9e44') + path(f'M{x} {y-10} q8 -6 10 0 q-6 4 -10 0', '#69db7c', 1.4, '#2f9e44')

def tomato_plant(x, y, h=70, n=4):
    o = [line(x, y, x, y - h, '#2f9e44', 3), line(x + 10, y, x + 10, y - h - 4, '#8d6e63', 2)]
    for i in range(5):
        yy = y - 12 - i * h / 5.5
        d = -1 if i % 2 else 1
        o.append(path(f'M{x} {f(yy)} q{d*14} -8 {d*20} 2 q{-d*10} 6 {-d*20} -2', '#51cf66', 1.4, '#2f9e44'))
    for i in range(n):
        yy = y - 20 - i * h / (n + 1)
        xx = x + (-9 if i % 2 else 9)
        o.append(circ(xx, yy, 6.5, '#fa5252', 1.6) + path(f'M{f(xx-3)} {f(yy-6)} l3 2 l3 -2', 'none', 1.5, '#2f9e44'))
    return ''.join(o)

def basket(x, y, w=34, fill_tomato=True):
    o = []
    if fill_tomato:
        for i, dx in enumerate((-9, 0, 9, -4, 5)):
            o.append(circ(x + dx, y - 4 - (6 if i > 2 else 0), 6, '#fa5252', 1.4))
    o.append(path(f'M{x-w/2} {y-4} L{x+w/2} {y-4} L{x+w/2-5} {y+14} L{x-w/2+5} {y+14} Z', '#e9b872', 2))
    o.append(line(x - w / 2 + 3, y + 3, x + w / 2 - 3, y + 3, '#a0773b', 1.5))
    o.append(path(f'M{x-w/2+2} {y-4} Q{x} {y-30} {x+w/2-2} {y-4}', 'none', 2.5, '#a0773b'))
    return ''.join(o)

def seed_pack(x, y, w=22, h=28, c='#ffd43b'):
    return rect(x, y, w, h, c, 3, 1.6) + circ(x + w / 2, y + 10, 5, '#fa5252', 1.2) + text(x + w / 2, y + h - 4, 'SEEDS', 6)

def window_night(x, y, w=60, h=50):
    return rect(x, y, w, h, '#364fc7') + line(x + w / 2, y, x + w / 2, y + h, INK, 2) + path(f'M{x+w*0.72} {y+10} a9 9 0 1 0 6 14 a7 7 0 1 1 -6 -14 Z', '#ffe066', 1.2) + circ(x + 12, y + 12, 1.3, '#fff', 0) + circ(x + 20, y + 30, 1.1, '#fff', 0)

def sun(x, y, r=13):
    o = [circ(x, y, r, '#ffd43b', 2, '#f08c00')]
    for i in range(8):
        a = i * math.pi / 4
        o.append(line(x + math.cos(a) * (r + 4), y + math.sin(a) * (r + 4), x + math.cos(a) * (r + 10), y + math.sin(a) * (r + 10), '#f08c00', 2))
    return ''.join(o)

def penguin(x, y, s=1.0):
    return (f'<ellipse cx="{f(x)}" cy="{f(y)}" rx="{f(11*s)}" ry="{f(15*s)}" fill="{INK}"/>' +
            f'<ellipse cx="{f(x)}" cy="{f(y+3*s)}" rx="{f(7*s)}" ry="{f(11*s)}" fill="#fff"/>' +
            circ(x - 3 * s, y - 8 * s, 1.4 * s, INK, 0) + circ(x + 3 * s, y - 8 * s, 1.4 * s, INK, 0) +
            path(f'M{f(x-2.5*s)} {f(y-5*s)} L{f(x)} {f(y-2*s)} L{f(x+2.5*s)} {f(y-5*s)} Z', '#ff922b', 1) +
            path(f'M{f(x-5*s)} {f(y+15*s)} l-3 2 l7 0 Z M{f(x+5*s)} {f(y+15*s)} l3 2 l-7 0 Z', '#ff922b', 1))

def clap(x, y):
    return path(f'M{x-6} {y-6} l-4 -4 M{x} {y-9} l0 -5 M{x+6} {y-6} l4 -4', 'none', 1.8, '#f08c00')

def bill(x, y, amount, w=58, h=70, c='#fff', title='ELECTRICITY'):
    o = [rect(x, y, w, h, c, 3, 2), text(x + w / 2, y + 12, title, 6.5), text(x + w / 2, y + 21, 'BILL', 6.5), line(x + 6, y + 27, x + w - 6, y + 27, '#adb5bd', 1.4), line(x + 6, y + 34, x + w - 12, y + 34, '#adb5bd', 1.4)]
    o.append(text(x + w / 2, y + 54, amount, 12, '#e03131', 900))
    return ''.join(o)

def lamp(x, y, on=True):
    o = []
    if on:
        o.append(f'<path d="M{x-12} {y+6} L{x-34} {y+70} L{x+34} {y+70} L{x+12} {y+6} Z" fill="#fff3bf" opacity=".8"/>')
    o.append(line(x, 0, x, y - 6, INK, 2))
    o.append(path(f'M{x-14} {y+6} L{x-8} {y-8} L{x+8} {y-8} L{x+14} {y+6} Z', '#fcc419' if on else '#ced4da', 2))
    if on:
        for a in (-60, -30, 0, 30, 60):
            r = math.radians(a + 90)
    return ''.join(o)

def switch(x, y, on):
    return rect(x, y, 16, 24, '#fff', 3, 1.8) + rect(x + 4, y + (3 if on else 12), 8, 9, '#868e96', 2, 1.2)

def trash_items(spots):
    o = []
    for kind, x, y in spots:
        if kind == 'bottle':
            o.append(f'<g transform="rotate(70 {x} {y})">' + rect(x - 4, y - 14, 8, 16, '#a5d8ff', 2, 1.5) + rect(x - 2, y - 18, 4, 5, '#4dabf7', 1, 1.2) + '</g>')
        elif kind == 'can':
            o.append(rect(x - 5, y - 10, 10, 11, '#ff8787', 2, 1.5) + line(x - 5, y - 6, x + 5, y - 6, '#fff', 1.4))
        elif kind == 'bag':
            o.append(path(f'M{x-9} {y} Q{x-11} {y-12} {x-4} {y-14} L{x-6} {y-19} M{x+4} {y-14} L{x+6} {y-19} M{x-4} {y-14} Q{x+12} {y-14} {x+9} {y} Z', '#f1f3f5', 1.5))
    return ''.join(o)

def trash_bag(x, y, c='#495057'):
    return path(f'M{x-10} {y} Q{x-14} {y-18} {x-4} {y-22} L{x-6} {y-28} L{x+6} {y-28} L{x+4} {y-22} Q{x+14} {y-18} {x+10} {y} Z', c, 1.8)

def beach(sea_y=95, sand_y=120):
    return (rect(0, 0, W, sea_y, '#d0ebff', 0, 0, '#d0ebff') + rect(0, sea_y, W, sand_y - sea_y, '#4dabf7', 0, 0, '#4dabf7') +
            path(f'M0 {sea_y+10} q15 -6 30 0 t30 0 t30 0 t30 0 t30 0 t30 0 t30 0 t30 0 t30 0 t30 0', 'none', 2, '#e7f5ff') +
            path(f'M0 {sand_y} q20 -6 40 0 t40 0 t40 0 t40 0 t40 0 t40 0 t40 0 t40 0 L{W} {H} L0 {H} Z', '#ffe8a3', 2, '#e9c46a'))

def toast(x, y):
    return rect(x - 9, y - 8, 18, 15, '#e9b872', 5, 1.5) + rect(x - 6, y - 5, 12, 9, '#fff3bf', 3, 0)

def plate(x, y):
    return f'<ellipse cx="{x}" cy="{y}" rx="16" ry="5" fill="#fff" stroke="{INK}" stroke-width="1.8"/>'

def clock(x, y, r, h, m, c='#fff'):
    o = [circ(x, y, r, c, 2)]
    for i in range(12):
        a = math.radians(i * 30)
        o.append(line(x + math.sin(a) * r * 0.82, y - math.cos(a) * r * 0.82, x + math.sin(a) * r * 0.92, y - math.cos(a) * r * 0.92, INK, 1.2))
    ah = math.radians((h % 12) * 30 + m * 0.5); am = math.radians(m * 6)
    o.append(line(x, y, x + math.sin(ah) * r * 0.5, y - math.cos(ah) * r * 0.5, INK, 2.2))
    o.append(line(x, y, x + math.sin(am) * r * 0.75, y - math.cos(am) * r * 0.75, INK, 1.6))
    return ''.join(o)

def alarm(x, y, h, m):
    return (circ(x - 9, y - 15, 5, '#fa5252', 1.6) + circ(x + 9, y - 15, 5, '#fa5252', 1.6) + clock(x, y, 14, h, m, '#fff') +
            line(x - 9, y + 12, x - 13, y + 17, INK, 2) + line(x + 9, y + 12, x + 13, y + 17, INK, 2) +
            path(f'M{x-24} {y-14} l-6 -4 M{x-24} {y-6} l-8 0 M{x+24} {y-14} l6 -4 M{x+24} {y-6} l8 0', 'none', 1.8, '#f08c00'))

def table(x, y, w=110, h=10):
    return rect(x, y, w, h, '#c08552', 2, 2) + line(x + 8, y + h, x + 8, y + 42, '#8b5a2b', 4) + line(x + w - 8, y + h, x + w - 8, y + 42, '#8b5a2b', 4)

def desk(x, y, w=90):
    return table(x, y, w)

def egg_plate(x, y):
    return plate(x, y) + f'<ellipse cx="{x}" cy="{y-2}" rx="10" ry="4" fill="#fff" stroke="{INK}" stroke-width="1.2"/>' + circ(x, y - 3, 3.4, '#fcc419', 1.2)

def soccer_ball(x, y, r=8):
    return circ(x, y, r, '#fff', 1.8) + path(f'M{x} {y-3.5} l3.3 2.4 -1.3 3.9 -4 0 -1.3 -3.9 Z', INK, 0.8)

def volley(x, y, r=9):
    return circ(x, y, r, '#fff', 1.8) + path(f'M{x-r} {y} Q{x} {y-5} {x+r} {y-2} M{x-3} {y-r+1} Q{x+2} {y} {x-2} {y+r} M{x+2} {y-r} Q{x+8} {y+2} {x+4} {y+r-1}', 'none', 1.2, '#4dabf7')

def net(x0, x1, y_top, y_bot):
    o = [line(x0, y_top, x0, y_bot, INK, 3), line(x1, y_top, x1, y_bot, INK, 3), rect(x0, y_top, x1 - x0, 18, 'none', 0, 1.5)]
    for xx in range(int(x0) + 8, int(x1), 8):
        o.append(line(xx, y_top, xx, y_top + 18, '#868e96', 0.8))
    o.append(line(x0, y_top + 9, x1, y_top + 9, '#868e96', 0.8))
    return ''.join(o)

def torii(x, y, w=110, h=100):
    c = '#e8453c'
    return (rect(x + 14, y - h + 14, 9, h - 14, c, 1, 2) + rect(x + w - 23, y - h + 14, 9, h - 14, c, 1, 2) +
            path(f'M{x-6} {y-h+2} Q{x+w/2} {y-h+10} {x+w+6} {y-h+2} L{x+w+2} {y-h+14} L{x-2} {y-h+14} Z', c, 2) +
            rect(x + 6, y - h + 26, w - 12, 7, c, 1, 2) + rect(x + w / 2 - 6, y - h + 14, 12, 12, '#fff3bf', 1, 1.5))

def camera(x, y):
    return rect(x - 11, y - 7, 22, 15, '#495057', 3, 1.6) + circ(x, y + 0.5, 4.5, '#a5d8ff', 1.4) + rect(x - 8, y - 10, 7, 3, '#495057', 1, 1.2)

def flash(x, y):
    return path(f'M{x} {y-12} l3 8 8 -3 -5 7 8 4 -9 1 1 8 -6 -6 -6 6 1 -8 -9 -1 8 -4 -5 -7 8 3 Z', '#fff3bf', 1.4, '#f08c00')

def letter(x, y, w, h, lines_, sign=None):
    o = [rect(x, y, w, h, '#fffdf5', 4, 2)]
    for i, s in enumerate(lines_):
        o.append(text(x + 10, y + 18 + i * 15, s, 10.5, '#1d3557', 700, 'start', 'Comic Sans MS,Chalkboard SE,Arial,sans-serif'))
    if sign:
        o.append(text(x + w - 10, y + h - 9, sign, 10, '#1d3557', 700, 'end', 'Comic Sans MS,Chalkboard SE,Arial,sans-serif'))
    return ''.join(o)

def envelope(x, y):
    return (rect(x, y, 40, 26, '#fff', 2, 1.8) + path(f'M{x} {y} L{x+20} {y+14} L{x+40} {y}', 'none', 1.6) +
            rect(x + 28, y + 3, 9, 10, '#ffd43b', 1, 1) + text(x + 32.5, y + 11, 'AU', 4.5))

def map_paper(x, y, w=80, h=50):
    return (rect(x, y, w, h, '#e6fcf5', 2, 2) + path(f'M{x+8} {y+40} Q{x+30} {y+10} {x+50} {y+30} T{x+w-6} {y+12}', 'none', 2, '#e8453c', 'stroke-dasharray="4 3"') +
            circ(x + 8, y + 40, 3, '#e8453c', 1) + path(f'M{x+w-12} {y+6} l6 12 l6 -12 a6 6 0 1 0 -12 0 Z', '#e8453c', 1.2) +
            path(f'M{x+20} {y+8} l6 0 M{x+56} {y+42} l10 0', 'none', 1.5, '#74c0fc'))

def tablet(x, y, w=40, h=30, content=''):
    return rect(x, y, w, h, '#343a40', 4, 1.6) + rect(x + 3, y + 3, w - 6, h - 6, '#e7f5ff', 2, 0) + content

def blackboard(x, y, w, h, words):
    o = [rect(x, y, w, h, '#2b8a3e', 3, 3, '#8b5a2b')]
    for i, s in enumerate(words):
        o.append(text(x + w / 2, y + 22 + i * 18, s, 14, '#fff', 700, 'middle', 'Comic Sans MS,Chalkboard SE,Arial,sans-serif'))
    return ''.join(o)

def shelf(x, y, w, h):
    o = [rect(x, y, w, h, '#deb887', 2, 2)]
    for i in range(1, 3):
        o.append(line(x, y + h * i / 3, x + w, y + h * i / 3, '#8b5a2b', 2))
    return ''.join(o)

def sweat(x, y):
    return path(f'M{x} {y} q-4 6 0 8 q4 -2 0 -8 Z', '#74c0fc', 1.2, '#1c7ed6')

def growl(x, y):
    return text(x, y, 'growl', 9, '#e8453c', 900)

def cap_sign(x, y, w, s, c='#fff3bf'):
    return rect(x, y, w, 16, c, 3, 1.6) + text(x + w / 2, y + 12, s, 9)

# ===================== コマ =====================
pics = {}

# s1 Community Gardens
def s1p1():
    o = [sky_ground(), sun(122, 26), house(18, 72), fence(165, 110, 300), soil(150, 172, 120)]
    a, h, t = P(118, 196, 'mom', arms=(15, 25), face=1)
    b, hb, tb = P(208, 198, 'boy', arms=(10, 55), mouth='open', face=1)
    o += [a, b, bubble(150, 6, 142, ["Let's plant some", 'vegetables!'], tb[0] + 2, tb[1] + 2)]
    return svg(''.join(o), '#d0ebff')

def s1p2():
    o = [room('#fff9db', '#dee2e6'), cap_sign(108, 8, 84, 'GARDEN SHOP', '#d3f9d8'), shelf(14, 34, 110, 100)]
    for r in range(3):
        for c in range(4):
            col = ['#ffd43b', '#ff8787', '#69db7c', '#ffa94d'][(r + c) % 4]
            o.append(seed_pack(20 + c * 26, 40 + r * 33, 20, 26, col))
    o.append(rect(186, 120, 100, 50, '#ced4da', 3, 2))  # レジ台
    clerk, _, _ = P(258, 120, 'man', arms=(70, 10), face=-1, legs='none', s=0.9)
    o.append(clerk)
    o.append(rect(186, 120, 100, 50, '#ced4da', 3, 2))
    m, hm, _ = P(160, 200, 'mom', arms=(15, 95), face=1)
    o.append(m)
    hx, hy = hm['R']
    o.append(seed_pack(hx - 4, hy - 26, 22, 28, '#ff8787'))
    o.append(text(236, 142, '$3', 13, '#2b8a3e', 900))
    return svg(''.join(o), '#fff9db')

def s1p3():
    o = [sky_ground(), sun(30, 26), fence(165, 0, 300)]
    for x in (40, 230, 275):
        o.append(tomato_plant(x, 172, 80))
    b, hb, tb = P(150, 202, 'boy', arms=(150, 30), eyes='happy', mouth='open', face=1)
    o.append(b)
    hx, hy = hb['L']
    o.append(circ(hx, hy - 4, 6.5, '#fa5252', 1.6))
    o.append(tomato_plant(106, 178, 90, 5))
    hx, hy = hb['R']
    o.append(basket(hx + 6, hy - 2))
    return svg(''.join(o), '#d0ebff')

# s2 Tablets at School
def s2p1():
    o = [room('#e7f5ff', '#d8b98a', 150), blackboard(150, 40, 140, 60, ['Presentation:', 'ANIMALS'])]
    t, ht, tt = P(62, 170, 'teacher', arms=(10, 115), mouth='open', face=1)
    o.append(t)
    for i, (x, k) in enumerate(((150, 'boy2'), (240, 'girl'))):
        s, _, _ = P(x, 214, k, arms=(20, -10), back=True, legs='none')
        o.append(s)
        o.append(desk(x - 40, 188, 80))
    o.append(bubble(6, 6, 176, ['Please make a presentation', 'about animals.'], tt[0] + 6, tt[1] + 18))
    return svg(''.join(o), '#e7f5ff')

def s2p2():
    o = [room('#dbe4ff', '#c5a880'), window_night(26, 24, 70, 56), lamp(232, 40)]
    o.append(desk(130, 150, 140))
    o.append(chair(112, 210))
    g, hg, _ = P(112, 172, 'girl', arms=(20, 85), face=1, legs='none')
    o.append(line(112, 168, 132, 168, '#d6336c', 7) + line(132, 168, 132, 206, '#d6336c', 6))
    o.append(g)
    o.append(tablet(176, 112, 56, 40, penguin(204, 132, 0.85)))
    o.append(path('M176 152 l-8 0', 'none', 2))
    o.append(rect(150, 140, 22, 10, '#ffe066', 1, 1.4))
    return svg(''.join(o), '#dbe4ff')

def s2p3():
    o = [room('#e7f5ff', '#d8b98a', 150)]
    o.append(rect(30, 18, 104, 112, '#fff', 4, 2) + text(82, 36, 'PENGUINS', 12, '#1c7ed6', 900) + penguin(64, 76, 1.5) + penguin(104, 84, 1.0) + rect(40, 108, 84, 3, '#adb5bd', 0, 0, '#adb5bd') + rect(40, 116, 60, 3, '#adb5bd', 0, 0, '#adb5bd'))
    g, hg, tg = P(162, 168, 'girl', arms=(110, 20), mouth='open', face=-1)
    o.append(g)
    for x, k in ((220, 'boy2'), (270, 'girl2')):
        s, hs, ts = P(x, 214, k, arms=(155, 155), mouth='open', eyes='happy', face=-1, legs='none', s=0.95)
        o.append(desk(x - 30, 192, 60))
        o.append(s)
        o.append(clap(x, ts[1] - 4))
    return svg(''.join(o), '#e7f5ff')

# s3 Saving Energy
def s3p1():
    o = [room('#fff3bf', '#e9c46a')]
    o.append(rect(14, 20, 50, 40, '#d0ebff') + line(39, 20, 39, 60, INK, 2))
    d, hd, td = P(92, 200, 'dad', arms=(10, 85), mouth='o', eyes='wide', face=1)
    b, hb, tb = P(212, 194, 'boy', arms=(80, 10), mouth='o', eyes='wide', face=-1)
    o += [d, b]
    o.append(bill(126, 86, '¥30,000', 60, 72))
    o.append(path('M158 82 l-6 -12 M166 82 l0 -14 M174 82 l6 -12', 'none', 2, '#e8453c'))
    o.append(bubble(90, 6, 130, ['The bill is', 'very high!'], td[0] + 10, td[1] + 6))
    return svg(''.join(o), '#fff3bf')

def s3p2():
    o = [room('#495057', '#343a40', 170)]
    # 左: だれもいない部屋（電気がついている）
    o.append(rect(10, 14, 168, 156, '#fff3bf', 0, 0, '#fff3bf') + rect(10, 170, 168, 40, '#e9c46a', 0, 0, '#e9c46a'))
    o.append(lamp(80, 40))
    o.append(rect(28, 120, 70, 26, '#ff8787', 8, 2) + rect(34, 104, 58, 20, '#ff8787', 8, 2))  # ソファ
    o.append(rect(124, 108, 40, 30, '#343a40', 3, 2) + rect(140, 138, 8, 14, '#343a40', 0, 1.5))  # テレビ
    o.append(rect(178, 10, 8, 200, '#adb5bd', 0, 1.5))  # かべ
    o.append(window_night(230, 20, 52, 44))
    o.append(switch(194, 116, False))
    b, hb, tb = P(232, 206, 'boy', arms=(100, 10), face=-1)
    o.append(b)
    o.append(path('M190 112 l-6 -6 M200 108 l0 -9 M210 112 l5 -6', 'none', 1.8, '#f08c00'))
    return svg(''.join(o), '#495057')

def s3p3():
    o = [room('#fff3bf', '#e9c46a'), sun(262, 28)]
    d, hd, td = P(100, 200, 'dad', arms=(80, 150), eyes='happy', mouth='open', face=1)
    o.append(d)
    hx, hy = hd['R']
    o.append(bill(hx - 8, hy - 66, '¥15,000', 60, 72))
    o.append(path('M204 120 l0 34 M196 146 l8 10 l8 -10', 'none', 3.5, '#2b8a3e'))
    o.append(text(204, 176, 'DOWN!', 12, '#2b8a3e', 900))
    b, _, _ = P(262, 204, 'boy', arms=(150, 150), eyes='happy', mouth='open', face=-1, s=0.9)
    o.append(b)
    return svg(''.join(o), '#fff3bf')

# s4 Cleaning Beaches
def s4p1():
    o = [beach()]
    o.append(trash_items([('bottle', 40, 190), ('can', 70, 200), ('bag', 110, 186), ('bottle', 250, 196), ('can', 272, 176), ('bag', 160, 206), ('can', 20, 168), ('bottle', 214, 210)]))
    g, hg, tg = P(196, 186, 'girl', arms=(60, 20), mouth='open', face=-1)
    b, hb, tb = P(252, 188, 'boy2', arms=(15, 10), mouth='sad', face=-1)
    o += [g, b]
    o.append(bubble(14, 8, 160, ["Let's clean the beach", 'next Sunday!'], tg[0] - 2, tg[1] + 4))
    return svg(''.join(o), '#d0ebff')

def s4p2():
    o = [beach(80, 100)]
    o.append(cap_sign(14, 12, 110, 'BEACH CLEAN-UP', '#d3f9d8'))
    o.append(trash_items([('bottle', 70, 210), ('can', 250, 208)]))
    for x, y, k, d in ((56, 184, 'man', 1), (156, 202, 'girl', 1), (252, 188, 'woman', -1)):
        arms = (15, 55) if d > 0 else (55, 15)
        p, hp, tp = P(x, y, k, arms=arms, face=d, s=0.9)
        hold = hp['R' if d > 0 else 'L']
        o.append(p)
        bx = hold[0] + 10 * d
        o.append(trash_bag(bx, y - 2, '#4dabf7' if k == 'girl' else '#495057'))
        o.append(trash_items([('can' if k != 'girl' else 'bottle', hold[0] + 2 * d, hold[1] + 2)]))
        o.append(path(f'M{bx} {hold[1]+12} l0 8 M{bx-3} {hold[1]+17} l3 3 l3 -3', 'none', 1.6, '#f08c00'))
        o.append(trash_items([('can', x - 22 * d, y + 8)]))
    return svg(''.join(o), '#d0ebff')

def s4p3():
    o = [beach(80, 100), sun(270, 24), net(118, 182, 92, 200)]
    a, ha, ta = P(74, 196, 'girl', arms=(170, 165), eyes='happy', mouth='open', face=1)
    b, hb, tb = P(236, 200, 'boy2', arms=(140, 150), eyes='happy', mouth='open', face=-1)
    c, hc, tc = P(32, 206, 'girl2', arms=(30, 30), eyes='happy', mouth='open', face=1, s=0.9)
    o += [a, b, c]
    o.append(volley(82, 58))
    o.append(path('M96 66 q14 -14 30 -18', 'none', 1.5, '#868e96', 'stroke-dasharray="3 3"'))
    return svg(''.join(o), '#d0ebff')

# s5 Breakfast
def s5p1():
    o = [sky_ground('#d0ebff', '#b2f2bb', 170)]
    o.append(rect(0, 30, 120, 140, '#ffe8cc') + rect(60, 70, 50, 100, '#fff') + rect(66, 76, 38, 94, '#a0522d') )
    o.append(clock(30, 70, 18, 8, 25))
    m, hm, tm = P(84, 196, 'mom', arms=(10, 95), mouth='open', face=1)
    o.append(m)
    hx, hy = hm['R']
    o.append(plate(hx + 8, hy - 1) + toast(hx + 8, hy - 7))
    b, hb, tb = P(222, 206, 'boy', arms=(150, 40), mouth='open', eyes='wide', face=1, legs='run')
    o.append(b)
    o.append(rect(201, 140, 16, 24, '#e8453c', 4, 1.8))  # ランドセル
    o.append(path('M182 150 l-18 0 M184 166 l-20 0 M186 182 l-16 0', 'none', 2, '#868e96'))
    o.append(bubble(104, 8, 120, ['Eat your', 'breakfast!'], tm[0] + 10, tm[1] + 8))
    return svg(''.join(o), '#d0ebff')

def s5p2():
    o = [sky_ground('#d0ebff', '#8ce99a', 120)]
    o.append(rect(240, 70, 56, 50, 'none', 0, 3, '#fff') + path('M240 70 l56 0 l-4 30', 'none', 1, '#dee2e6'))
    f1, _, _ = P(268, 150, 'boy2', arms=(40, 60), face=-1, legs='run', s=0.7)
    o.append(f1)
    o.append(rect(96, 168, 90, 8, '#8b5a2b', 2, 1.6) + line(104, 176, 104, 204, '#8b5a2b', 3) + line(178, 176, 178, 204, '#8b5a2b', 3))
    b, hb, tb = P(132, 206, 'boy', arms=(40, 35), eyes='tired', mouth='sad', face=1, legs='none')
    o.append(line(132, 168, 150, 168, '#1d4e89', 7) + line(150, 168, 150, 204, '#1d4e89', 6))
    o.append(b)
    o.append(soccer_ball(214, 198, 10))
    o.append(sweat(116, tb[1] + 6) + sweat(152, tb[1] + 12))
    o.append(text(176, 150, 'growl...', 11, '#e8453c', 900))
    o.append(bubble(28, 10, 110, ["I'm so hungry..."], tb[0] - 6, tb[1] - 2, 11, 'think'))
    return svg(''.join(o), '#d0ebff')

def s5p3():
    o = [room('#fff3bf', '#e9c46a'), rect(18, 18, 60, 48, '#ffec99') + line(48, 18, 48, 66, INK, 2) + sun(62, 40, 8)]
    o.append(alarm(160, 50, 6, 0))
    o.append(text(160, 84, '6:00', 12, INK, 900))
    o.append(chair(104, 210))
    b, hb, tb = P(104, 172, 'boy', arms=(20, 80), eyes='happy', mouth='smile', face=1, legs='none')
    o.append(line(104, 168, 124, 168, '#1d4e89', 7) + line(124, 168, 124, 206, '#1d4e89', 6))
    o.append(b)
    m, _, _ = P(258, 196, 'mom', arms=(30, 20), eyes='happy', face=-1)
    o.append(m)
    o.append(table(130, 150, 140))
    o.append(egg_plate(160, 148) + toast(196, 143) + rect(222, 128, 12, 20, '#fff', 2, 1.6))
    return svg(''.join(o), '#fff3bf')

# s6 Australia friend
def s6p1():
    o = [room('#e7f5ff', '#d8b98a', 175)]
    o.append(letter(90, 36, 196, 112, ['Dear Sho,', 'I will visit', 'Japan in August!'], 'Tom'))
    b, hb, tb = P(58, 206, 'boy', arms=(20, 95), eyes='wide', mouth='open', face=1)
    o.append(b)
    o.append(envelope(150, 172))
    o.append(path('M44 96 l-6 -8 M56 90 l0 -10 M68 96 l6 -8', 'none', 1.8, '#f08c00'))
    return svg(''.join(o), '#e7f5ff')

def s6p2():
    o = [room('#e7f5ff', '#d8b98a', 160), window_day := rect(220, 20, 60, 46, '#d0ebff') + line(250, 20, 250, 66, INK, 2)]
    o.append(desk(96, 140, 190))
    o.append(chair(70, 210))
    b, hb, tb = P(70, 172, 'boy', arms=(20, 75), face=1, legs='none')
    o.append(line(70, 168, 90, 168, '#1d4e89', 7) + line(90, 168, 90, 206, '#1d4e89', 6))
    o.append(b)
    o.append(map_paper(108, 88, 88, 50))
    o.append(rect(204, 84, 72, 54, '#fff', 2, 1.8) + text(240, 98, 'PLAN', 10, '#e8453c', 900) +
             text(212, 113, '1. temple', 8.5, INK, 700, 'start') + text(212, 126, '2. sushi', 8.5, INK, 700, 'start'))
    o.append(line(hb['R'][0], hb['R'][1], hb['R'][0] + 10, hb['R'][1] - 14, '#fcc419', 3))
    return svg(''.join(o), '#e7f5ff')

def s6p3():
    o = [sky_ground('#d0ebff', '#e9ecef', 170), torii(170, 170, 120, 130)]
    o.append(path('M120 170 q30 -40 60 -10 q20 -30 50 0', '#8ce99a', 2, '#2f9e44'))
    t, ht, tt = P(36, 206, 'blond', arms=(20, 125), eyes='happy', mouth='open', face=1)
    s, hs, ts = P(128, 204, 'boy', arms=(20, 125), eyes='happy', mouth='smile', face=1)
    for g, h in ((t, ht['R']), (s, hs['R'])):
        o.append(g)
        o.append(camera(h[0] + 4, h[1] - 2))
        o.append(text(h[0] + 8, h[1] - 16, 'click!', 9, '#f08c00', 900))
    return svg(''.join(o), '#d0ebff')

ALL = {
 's1': [s1p1, s1p2, s1p3], 's2': [s2p1, s2p2, s2p3], 's3': [s3p1, s3p2, s3p3],
 's4': [s4p1, s4p2, s4p3], 's5': [s5p1, s5p2, s5p3], 's6': [s6p1, s6p2, s6p3],
}

if __name__ == '__main__':
    import sys
    out = {k: [fn() for fn in v] for k, v in ALL.items()}
    json.dump(out, open(sys.argv[1], 'w'))
    html = ['<html><body style="margin:0;background:#fff;font-family:sans-serif">']
    for k, v in out.items():
        html.append(f'<h3 style="margin:6px">{k}</h3><div style="display:grid;grid-template-columns:repeat(3,320px);gap:10px;margin:6px">')
        for s in v:
            html.append(f'<div style="border:2px solid #1d3557;border-radius:8px;overflow:hidden;width:320px">{s}</div>')
        html.append('</div>')
    open(sys.argv[2], 'w').write(''.join(html))
