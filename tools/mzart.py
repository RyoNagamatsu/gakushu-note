# 英検2級 面接れんしゅう No.2 の3コマの絵（SVG）を描く道具（2026-10-29 描き直し）
# 人物は「右向き」で描いてから、左向きは左右反転する。ひじ・ひざの角度で動きを出す。
import math

W, H = 360, 260
INK = '#3a3532'
SKIN = '#fbd7b5'
SKIN_SH = '#efbf98'
FONT = "Arial,Helvetica,sans-serif"


def f(v):
    return ('%.1f' % v).rstrip('0').rstrip('.')


def esc(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


# ---------- 基本の図形 ----------
def line(x1, y1, x2, y2, c=INK, w=2, cap='round', dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ''
    return f'<line x1="{f(x1)}" y1="{f(y1)}" x2="{f(x2)}" y2="{f(y2)}" stroke="{c}" stroke-width="{f(w)}" stroke-linecap="{cap}"{d}/>'


def rect(x, y, w, h, fill, rx=0, sw=2, st=INK, extra=''):
    return f'<rect x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(h)}" rx="{f(rx)}" fill="{fill}" stroke="{st}" stroke-width="{f(sw)}" {extra}/>'


def circ(x, y, r, fill, sw=2, st=INK, extra=''):
    return f'<circle cx="{f(x)}" cy="{f(y)}" r="{f(r)}" fill="{fill}" stroke="{st}" stroke-width="{f(sw)}" {extra}/>'


def ell(x, y, rx, ry, fill, sw=2, st=INK, extra=''):
    return f'<ellipse cx="{f(x)}" cy="{f(y)}" rx="{f(rx)}" ry="{f(ry)}" fill="{fill}" stroke="{st}" stroke-width="{f(sw)}" {extra}/>'


def path(d, fill='none', sw=2, st=INK, extra=''):
    return f'<path d="{d}" fill="{fill}" stroke="{st}" stroke-width="{f(sw)}" stroke-linejoin="round" stroke-linecap="round" {extra}/>'


def poly(pts, fill, sw=2, st=INK):
    return f'<polygon points="{" ".join(f(a)+","+f(b) for a, b in pts)}" fill="{fill}" stroke="{st}" stroke-width="{f(sw)}" stroke-linejoin="round"/>'


def text(x, y, s, size=11, fill=INK, weight=700, anchor='middle', fam=FONT, extra=''):
    return f'<text x="{f(x)}" y="{f(y)}" font-size="{f(size)}" font-weight="{weight}" fill="{fill}" text-anchor="{anchor}" font-family="{fam}" {extra}>{esc(s)}</text>'


def g(inner, tr):
    return f'<g transform="{tr}">{inner}</g>'


def limb(pts, color, w):
    """輪郭つきの太い線（腕・足）。"""
    d = 'M' + ' L'.join(f'{f(x)} {f(y)}' for x, y in pts)
    return (f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="{f(w+3.2)}" stroke-linecap="round" stroke-linejoin="round"/>'
            f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{f(w)}" stroke-linecap="round" stroke-linejoin="round"/>')


def vec(a, d):
    r = math.radians(a)
    return math.sin(r) * d, math.cos(r) * d


# ---------- 人物 ----------
KINDS = {
    # h: 身長(px), hair: 髪型, top/bottom: 服の色
    'boy':    dict(h=104, kid=True, hair='short', hc='#3b2b22', top='#4f8fd8', bottom='#2f4a72', shoe='#d9473f'),
    'boy2':   dict(h=100, kid=True, hair='spiky', hc='#2b2420', top='#f0913a', bottom='#55606e', shoe='#3b3b3b'),
    'tom':    dict(h=108, kid=True, hair='short', hc='#e7b84d', top='#5cb85c', bottom='#3a5f8f', shoe='#ffffff'),
    'girl':   dict(h=102, kid=True, hair='pony', hc='#3b2b22', top='#ef7fa6', bottom='#7b5cc4', shoe='#7b5cc4', skirt=True),
    'girl2':  dict(h=100, kid=True, hair='bob', hc='#6b4129', top='#f5c842', bottom='#4f8fd8', shoe='#e8603c', skirt=True),
    'mom':    dict(h=140, hair='bun', hc='#4a3022', top='#6fbf8f', bottom='#3f6f8f', shoe='#7a4a2a', skirt=True),
    'dad':    dict(h=150, hair='adult', hc='#2e2622', top='#8ab6e0', bottom='#4a5260', shoe='#4a3426', glasses=True),
    'teacher': dict(h=142, hair='long', hc='#3b2b22', top='#a98ad8', bottom='#4a4f6a', shoe='#3b3b3b', skirt=True, glasses=True),
    'clerk':  dict(h=146, hair='adult', hc='#5a3a28', top='#f2f2f2', bottom='#4a5260', shoe='#3b3b3b', apron='#2f8f5f'),
    'man':    dict(h=148, hair='adult', hc='#4a4a4a', top='#e7955a', bottom='#545c66', shoe='#3b3b3b'),
    'woman':  dict(h=138, hair='long', hc='#8a5a3a', top='#e86a6a', bottom='#5c6fb8', shoe='#3b3b3b'),
    'kid3':   dict(h=98, kid=True, hair='short', hc='#5a3a28', top='#e86a6a', bottom='#33558a', shoe='#ffffff'),
    'kid4':   dict(h=100, kid=True, hair='bob', hc='#2b2420', top='#62c2c7', bottom='#e07a5f', shoe='#3b3b3b', skirt=True),
}


def head(kind, eyes='open', mouth='smile', back=False, brows='normal', sweat=False):
    """右向き 3/4 の顔。原点が頭の中心、半径 50 の座標で描く。"""
    k = KINDS[kind]
    hc = k['hc']
    o = []
    st = 3.2
    style = k['hair']
    # 後ろの髪
    if style in ('long',):
        o.append(path('M-38 -30 Q-58 20 -48 70 Q-10 80 14 64 Q20 30 10 0 Z', hc, st))
    if style == 'bob':
        o.append(path('M-44 -24 Q-60 30 -40 52 Q-10 60 10 50 Q14 20 4 0 Z', hc, st))
    if style == 'pony':
        o.append(path('M-40 -34 Q-82 -20 -74 30 Q-70 54 -56 62 Q-64 30 -48 0 Z', hc, st))
        o.append(circ(-44, -30, 8, '#e8475f', 2.6))
    if style == 'bun':
        o.append(circ(-40, -42, 18, hc, st))
    if back:
        o.append(ell(0, 0, 47, 50, hc, st))
        o.append(ell(-44, 8, 8, 12, SKIN, st))
        o.append(ell(44, 8, 8, 12, SKIN, st))
        if style == 'pony':
            o.append(path('M-6 -40 Q-14 10 0 56 Q14 10 6 -40 Z', hc, st))
        return ''.join(o)
    # 顔
    o.append(ell(0, 0, 46, 50, SKIN, st))
    o.append(ell(-24, 8, 9, 12, SKIN, st))
    o.append(path('M-26 2 Q-20 8 -25 14', 'none', 2.2))
    # 前の髪
    if style == 'short':
        o.append(path('M-16 -2 L-30 20 Q-48 16 -50 -4 Q-50 -42 -10 -56 Q30 -62 48 -26 L48 -12 '
                      'L40 -20 L32 -10 L24 -24 L12 -12 L4 -26 L-6 -10 Z', hc, st))
    elif style == 'spiky':
        o.append(path('M-16 -2 L-30 20 Q-50 14 -50 -6 L-60 -24 L-44 -34 L-46 -54 L-26 -52 L-14 -68 L0 -56 '
                      'L18 -66 L26 -50 L46 -52 L44 -32 L56 -22 L46 -12 L38 -22 L28 -10 L20 -24 L8 -12 L0 -24 L-8 -8 Z', hc, st))
    elif style == 'adult':
        o.append(path('M-14 -4 L-28 16 Q-48 12 -50 -8 Q-50 -46 -6 -56 Q34 -60 48 -24 L46 -16 '
                      'Q30 -30 6 -26 Q-6 -24 -10 -14 Z', hc, st))
    elif style in ('long', 'bob'):
        o.append(path('M-14 -2 L-30 26 Q-50 20 -50 -6 Q-48 -48 -4 -56 Q38 -58 50 -18 '
                      'Q36 -20 26 -32 Q18 -18 2 -20 Q-6 -18 -10 -10 Z', hc, st))
    elif style == 'pony':
        o.append(path('M-14 -2 L-28 22 Q-48 16 -50 -6 Q-48 -48 -4 -56 Q38 -58 50 -18 '
                      'Q34 -22 26 -32 Q18 -18 2 -20 Q-6 -18 -10 -10 Z', hc, st))
    elif style == 'bun':
        o.append(path('M-14 -4 L-28 18 Q-48 14 -50 -6 Q-48 -48 -4 -56 Q38 -58 50 -18 '
                      'Q30 -30 4 -24 Q-6 -20 -10 -12 Z', hc, st))
    # 目
    ey = 6
    if eyes == 'open':
        o.append(ell(8, ey, 5.6, 8, INK, 0) + ell(32, ey, 4.6, 7.6, INK, 0))
        o.append(circ(10, ey - 3, 2, '#fff', 0) + circ(33.5, ey - 3, 1.7, '#fff', 0))
    elif eyes == 'wide':
        o.append(ell(8, ey, 7, 9, '#fff', 2.4) + ell(32, ey, 6, 8.6, '#fff', 2.4))
        o.append(circ(9, ey, 3.4, INK, 0) + circ(33, ey, 3, INK, 0))
    elif eyes == 'happy':
        o.append(path(f'M2 {ey+2} Q8 {ey-7} 14 {ey+2}', 'none', 3.4) + path(f'M27 {ey+2} Q32 {ey-6} 37 {ey+2}', 'none', 3.4))
    elif eyes == 'closed':
        o.append(path(f'M2 {ey} Q8 {ey+6} 14 {ey}', 'none', 3.4) + path(f'M27 {ey} Q32 {ey+5} 37 {ey}', 'none', 3.4))
    elif eyes == 'tired':
        o.append(path(f'M1 {ey} L15 {ey+1}', 'none', 3.4) + path(f'M26 {ey+1} L38 {ey}', 'none', 3.4))
        o.append(path(f'M3 {ey+6} Q8 {ey+9} 13 {ey+6}', 'none', 1.8) + path(f'M28 {ey+6} Q32 {ey+9} 36 {ey+6}', 'none', 1.8))
    elif eyes == 'down':  # 下を見る
        o.append(path(f'M2 {ey+2} Q8 {ey+8} 14 {ey+2}', 'none', 3.4) + path(f'M27 {ey+2} Q32 {ey+7} 37 {ey+2}', 'none', 3.4))
    # まゆ
    if brows == 'normal':
        o.append(path('M1 -12 Q8 -16 15 -13', 'none', 2.6) + path('M27 -13 Q33 -16 38 -12', 'none', 2.6))
    elif brows == 'worried':
        o.append(path('M1 -10 L15 -15', 'none', 2.6) + path('M27 -15 L38 -10', 'none', 2.6))
    elif brows == 'up':
        o.append(path('M1 -16 Q8 -22 15 -18', 'none', 2.6) + path('M27 -18 Q33 -22 38 -16', 'none', 2.6))
    # 鼻
    o.append(path('M41 14 Q47 22 40 25', 'none', 2.4))
    # ほお
    o.append(ell(6, 24, 7, 4.5, '#f6a7a0', 0, INK, 'opacity="0.6"') + ell(38, 24, 5, 4, '#f6a7a0', 0, INK, 'opacity="0.6"'))
    # 口
    if mouth == 'smile':
        o.append(path('M16 32 Q25 40 34 31', 'none', 2.8))
    elif mouth == 'grin':
        o.append(path('M14 30 Q25 32 36 29 Q32 44 24 44 Q16 43 14 30 Z', '#b8433f', 2.6))
        o.append(path('M18 39 Q24 36 30 40', '#f08c8c', 0))
    elif mouth == 'open':
        o.append(ell(25, 34, 6.5, 7.5, '#b8433f', 2.6) + ell(25, 38, 4, 2.6, '#f08c8c', 0))
    elif mouth == 'o':
        o.append(ell(26, 34, 4, 5, '#b8433f', 2.4))
    elif mouth == 'frown':
        o.append(path('M17 38 Q25 31 33 37', 'none', 2.8))
    elif mouth == 'flat':
        o.append(path('M18 35 L32 34', 'none', 2.8))
    elif mouth == 'wavy':
        o.append(path('M15 36 Q19 32 23 36 Q27 40 31 35 Q33 33 35 35', 'none', 2.6))
    if k.get('glasses'):
        o.append(circ(9, ey, 11, 'none', 2.4) + circ(33, ey, 9.5, 'none', 2.4) + line(20, ey, 23.5, ey, INK, 2.4) + line(-2, ey - 2, -18, ey - 4, INK, 2.4))
    if sweat:
        o.append(path('M50 -18 Q58 -6 52 0 Q44 -4 50 -18 Z', '#9fd3f2', 2))
    return ''.join(o)


def person(x, y, kind, d=1, s=1.0, arms=((10, 20), (-10, 10)), legs=((4, 2), (-4, -2)),
           lean=0, face='open', mouth='smile', brows='normal', back=False, held=None, sweat=False,
           tilt=0, sit=False):
    """x: 体の中心, y: 足もと。d: 1=右向き, -1=左向き。
    arms: ((近い腕の上腕, 前腕), (遠い腕の上腕, 前腕))。角度は真下0、前へ+（度）。
    legs: ((近い足のもも, すね), (遠い足のもも, すね))。
    held: {'near': fn(hx,hy), 'far': fn(hx,hy)} 手の位置で道具を描く（右向きの座標で）。
    返り値: (svg, 手の位置 {'near':(x,y),'far':(x,y)}（実際の座標）)"""
    k = KINDS[kind]
    Ht = k['h'] * s * (1.12 if k.get('kid') else 1.05)
    kid = k.get('kid', False)
    hr = Ht * (0.135 if kid else 0.098)        # 頭の半径
    leg_len = Ht * (0.40 if kid else 0.46)
    torso = Ht * (0.27 if kid else 0.29)
    ua, fa = Ht * (0.17 if kid else 0.18), Ht * (0.16 if kid else 0.17)
    th = leg_len * 0.52
    sh_ = leg_len * 0.48
    aw = Ht * (0.07 if kid else 0.058)
    lw = Ht * (0.085 if kid else 0.07)
    tw = Ht * (0.22 if kid else 0.19)
    hip_y = y - leg_len
    if sit:
        hip_y = y - sh_  # すね＝いすの高さ
    hx = 0.0
    # 胴のかたむき
    lx, ly = vec(lean, torso)
    shx, shy = hx + lx, hip_y - ly
    sc = 50 / hr
    out_far, out_body, out_near = [], [], []
    hands = {}

    def legpts(a1, a2, ox):
        p0 = (hx + ox, hip_y)
        dx, dy = vec(a1, th)
        p1 = (p0[0] + dx, p0[1] + dy)
        dx, dy = vec(a2, sh_)
        p2 = (p1[0] + dx, p1[1] + dy)
        return [p0, p1, p2]

    def shoe(p, a2):
        return ell(p[0] + Ht * 0.03, p[1] + Ht * 0.005, Ht * 0.05, Ht * 0.026, k['shoe'], 2.4)

    def armpts(a1, a2, ox):
        p0 = (shx + ox, shy + aw * 0.5)
        dx, dy = vec(a1, ua)
        p1 = (p0[0] + dx, p0[1] + dy)
        dx, dy = vec(a2, fa)
        p2 = (p1[0] + dx, p1[1] + dy)
        return [p0, p1, p2]

    legcol = k['bottom']
    skirt = k.get('skirt')
    # 遠い足
    for i, (a1, a2) in enumerate(legs):
        pts = legpts(a1, a2, Ht * (0.035 if i else -0.03))
        tgt = out_far if i else out_near
        if skirt:
            tgt.append(limb(pts, SKIN, lw * 0.82))
        else:
            tgt.append(limb(pts, legcol, lw))
        tgt.append(shoe(pts[2], a2))
    far_leg = out_far[:]
    near_leg = out_near[:]
    out_far, out_near = [], []
    # 腕
    for i, (a1, a2) in enumerate(arms):
        pts = armpts(a1, a2, tw * (0.18 if i else -0.12))
        tgt = out_far if i else out_near
        tgt.append(limb(pts[:2] + [pts[2]], k['top'], aw))
        hx2, hy2 = pts[2]
        tgt.append(limb([pts[1], (pts[1][0] + (pts[2][0]-pts[1][0])*0.999, pts[1][1] + (pts[2][1]-pts[1][1])*0.999)], k['top'], aw) if False else '')
        tgt.append(circ(hx2, hy2, aw * 0.62, SKIN, 2.2))
        key = 'far' if i else 'near'
        hands[key] = (hx2, hy2)
        if held and key in held:
            tgt.append(held[key](hx2, hy2))
    # 胴
    body = []
    if skirt:
        sk_top = hip_y - torso * 0.12
        body.append(poly([(hx - tw * 0.42, sk_top), (hx + tw * 0.42 + lx * 0.2, sk_top),
                          (hx + tw * 0.68, hip_y + leg_len * 0.38), (hx - tw * 0.68, hip_y + leg_len * 0.38)], legcol, 2.6))
    else:
        body.append(path(f'M{f(hx - tw*0.46)} {f(hip_y - 4)} L{f(hx + tw*0.46)} {f(hip_y - 4)} L{f(hx + tw*0.44)} {f(hip_y + lw*0.6)} '
                         f'L{f(hx - tw*0.44)} {f(hip_y + lw*0.6)} Z', legcol, 2.6))
    # シャツ（肩は丸く）
    bx0, bx1 = hx - tw * 0.5, hx + tw * 0.5
    top_end = hip_y if not skirt else hip_y - torso * 0.08
    body.append(path(f'M{f(bx0 + lx*0.0 + 0)} {f(top_end)} L{f(shx - tw*0.46)} {f(shy + aw*0.9)} '
                     f'Q{f(shx - tw*0.5)} {f(shy - aw*0.15)} {f(shx - tw*0.1)} {f(shy - aw*0.1)} '
                     f'L{f(shx + tw*0.1)} {f(shy - aw*0.1)} Q{f(shx + tw*0.5)} {f(shy - aw*0.15)} {f(shx + tw*0.46)} {f(shy + aw*0.9)} '
                     f'L{f(bx1)} {f(top_end)} Z', k['top'], 2.6))
    if k.get('apron'):
        ac = k['apron'] if isinstance(k['apron'], str) else '#f7f2e8'
        body.append(path(f'M{f(shx + tw*0.05)} {f(shy + torso*0.25)} L{f(hx + tw*0.5)} {f(shy + torso*0.25)} L{f(hx + tw*0.62)} {f(hip_y + leg_len*0.3)} '
                         f'L{f(hx + tw*0.02)} {f(hip_y + leg_len*0.3)} Z', ac, 2.2))
    # 首
    neck = limb([(shx + tw*0.08, shy), (shx + tw*0.1, shy - hr * 0.35)], SKIN, hr * 0.5)
    # 頭
    hcx, hcy = shx + tw * 0.12, shy - hr * 0.95
    hd = g(head(kind, face, mouth, back, brows, sweat), f'translate({f(hcx)} {f(hcy)}) rotate({tilt}) scale({f(1/sc)})')
    parts = ''.join(out_far) + ''.join(far_leg) + ''.join(near_leg) + neck + ''.join(body) + ''.join(out_near) + hd
    if back:  # 後ろ向き：顔なし、腕は体のうしろに隠れない
        parts = ''.join(far_leg) + ''.join(near_leg) + neck + ''.join(body) + hd + ''.join(out_far) + ''.join(out_near)
    tr = f'translate({f(x)} 0) scale({d} 1)'
    real = {kk: (x + d * vx, vy) for kk, (vx, vy) in hands.items()}
    real['head'] = (x + d * hcx, hcy - hr)
    real['mouth'] = (x + d * (hcx + hr * 0.5), hcy + hr * 0.6)
    return g(parts, tr), real


# ---------- ふきだし ----------
def bubble(x, y, w, lines, tail, size=12.5, think=False):
    """x,y: 左上。tail: しっぽの先 (tx, ty)。"""
    lh = size * 1.25
    h = len(lines) * lh + 12
    cx, cy = x + w / 2, y + h / 2
    tx, ty = tail
    o = []
    if think:
        o.append(rect(x, y, w, h, '#fff', h / 2, 2.4))
        # 小さな丸
        for i, r in enumerate((5, 3.5, 2.4)):
            t = (i + 1) / 4
            o.append(circ(cx + (tx - cx) * (0.55 + t * 0.4), cy + (ty - cy) * (0.55 + t * 0.4), r, '#fff', 2))
    else:
        # しっぽ：泡のふちから先まで
        bx = min(max(tx, x + 18), x + w - 18)
        by = y + h if ty > y + h else y
        o.append(path(f'M{f(bx - 9)} {f(by)} L{f(tx)} {f(ty)} L{f(bx + 9)} {f(by)}', '#fff', 2.4))
        o.append(rect(x, y, w, h, '#fff', 12, 2.4))
        o.append(line(bx - 7.5, by, bx + 7.5, by, '#fff', 3.4, 'butt'))
    for i, s in enumerate(lines):
        o.append(text(cx, y + 6 + lh * (i + 0.78), s, size, INK, 700))
    return ''.join(o)


def svg(body, bg='#ffffff'):
    return (f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" font-family="{FONT}">'
            f'<rect width="{W}" height="{H}" fill="{bg}"/>{body}</svg>')
