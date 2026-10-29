# 英検2級 面接れんしゅう No.2 の3コマ（6セット×3）。mzart.py の人物と道具で描く。
# 使い方: python3 tools/mzscenes.py <出力json> [<確認用html>]
import json, math, sys, os
sys.path.insert(0, os.path.dirname(__file__))
from mzart import *

WALL = '#f5eddc'
FLOOR = '#dcbc8e'
SKY = '#cde7f6'
GRASS = '#a9d68b'
SAND = '#f0dca8'
SEA = '#7cc3e6'


# ---------- 背景 ----------
def room(wall=WALL, floor=FLOOR, fy=178):
    return (rect(0, 0, W, fy, wall, 0, 0) + rect(0, fy, W, H - fy, floor, 0, 0) +
            rect(0, fy - 6, W, 6, '#c9a877', 0, 0) + line(0, fy, W, fy, INK, 2) +
            ''.join(line(0, fy + 18 + i * 22, W, fy + 18 + i * 22, '#c9a576', 1.2) for i in range(4)))


def outdoor(sky=SKY, ground=GRASS, gy=170):
    return rect(0, 0, W, gy, sky, 0, 0) + rect(0, gy, W, H - gy, ground, 0, 0) + line(0, gy, W, gy, INK, 2)


def cloud(x, y, s=1):
    return path(f'M{f(x)} {f(y)} q{f(4*s)} {f(-14*s)} {f(18*s)} {f(-10*s)} q{f(8*s)} {f(-12*s)} {f(22*s)} {f(-2*s)} '
                f'q{f(14*s)} {f(-2*s)} {f(12*s)} {f(12*s)} z', '#fff', 1.8)


def sun(x, y, r=13):
    o = [circ(x, y, r, '#ffd54a', 2)]
    for i in range(8):
        a = math.radians(i * 45)
        o.append(line(x + math.cos(a) * (r + 4), y + math.sin(a) * (r + 4), x + math.cos(a) * (r + 10), y + math.sin(a) * (r + 10), '#f2a900', 2.4))
    return ''.join(o)


def window(x, y, w, h, night=False, curtain='#e8a0a0', sky=None):
    c = sky or ('#2d3a6b' if night else '#bfe3f7')
    o = [rect(x, y, w, h, c, 3, 3, INK), line(x + w / 2, y, x + w / 2, y + h, INK, 3), line(x, y + h / 2, x + w, y + h / 2, INK, 3)]
    if night:
        o.append(path(f'M{f(x+w*0.72)} {f(y+h*0.14)} a9 9 0 1 0 8 13 a7 7 0 1 1 -8 -13 z', '#ffe680', 1.6))
        o.append(circ(x + w * 0.2, y + h * 0.25, 1.6, '#fff', 0) + circ(x + w * 0.35, y + h * 0.7, 1.4, '#fff', 0) + circ(x + w * 0.8, y + h * 0.75, 1.4, '#fff', 0))
    if curtain:
        o.append(path(f'M{f(x-8)} {f(y-6)} L{f(x+12)} {f(y-6)} Q{f(x+4)} {f(y+h*0.5)} {f(x+14)} {f(y+h+6)} L{f(x-8)} {f(y+h+6)} Z', curtain, 2.2))
        o.append(path(f'M{f(x+w+8)} {f(y-6)} L{f(x+w-12)} {f(y-6)} Q{f(x+w-4)} {f(y+h*0.5)} {f(x+w-14)} {f(y+h+6)} L{f(x+w+8)} {f(y+h+6)} Z', curtain, 2.2))
        o.append(rect(x - 12, y - 10, w + 24, 5, '#9a7b5a', 2, 1.6))
    return ''.join(o)


def table(x0, x1, ytop, fy, color='#c08a55', th=7):
    return (line(x0 + 10, ytop + th, x0 + 10, fy, INK, 8) + line(x0 + 10, ytop + th, x0 + 10, fy, color, 5) +
            line(x1 - 10, ytop + th, x1 - 10, fy, INK, 8) + line(x1 - 10, ytop + th, x1 - 10, fy, color, 5) +
            rect(x0, ytop, x1 - x0, th, color, 2, 2.4))


def chair(x, fy, d=1, color='#b07a48', seat=None):
    sy = seat if seat is not None else fy - 36
    bx = x - d * 16
    return (line(bx, sy - 40, bx, fy, INK, 7) + line(bx, sy - 40, bx, fy, color, 4) +
            line(x + d * 14, sy, x + d * 14, fy, INK, 7) + line(x + d * 14, sy, x + d * 14, fy, color, 4) +
            rect(min(bx, x + d * 18) - 2, sy - 3, 36, 7, color, 2, 2.2) +
            rect(bx - 4, sy - 44, 8, 26, color, 2, 2))


def clock(x, y, r, hh, mm, rim='#ffffff'):
    o = [circ(x, y, r, rim, 2.6), circ(x, y, r - 4, '#fff', 1.2)]
    for i in range(12):
        a = math.radians(i * 30)
        o.append(line(x + math.sin(a) * (r - 6), y - math.cos(a) * (r - 6), x + math.sin(a) * (r - 9 if i % 3 else r - 11), y - math.cos(a) * (r - 9 if i % 3 else r - 11), INK, 1.6 if i % 3 else 2.4))
    ah = math.radians((hh % 12 + mm / 60) * 30)
    am = math.radians(mm * 6)
    o.append(line(x, y, x + math.sin(ah) * r * 0.45, y - math.cos(ah) * r * 0.45, INK, 3.2))
    o.append(line(x, y, x + math.sin(am) * r * 0.7, y - math.cos(am) * r * 0.7, INK, 2.2))
    o.append(circ(x, y, 2.2, INK, 0))
    return ''.join(o)


def plant_pot(x, fy, s=1):
    return (path(f'M{f(x-12*s)} {f(fy-26*s)} L{f(x+12*s)} {f(fy-26*s)} L{f(x+9*s)} {f(fy)} L{f(x-9*s)} {f(fy)} Z', '#d9774a', 2) +
            ''.join(ell(x + dx * s, fy - 26 * s - dy * s, 8 * s, 14 * s, '#5aa560', 1.8, INK, f'transform="rotate({r} {f(x+dx*s)} {f(fy-26*s-dy*s)})"')
                    for dx, dy, r in ((-10, 14, -30), (10, 14, 30), (0, 22, 0))))


def label_sign(x, y, w, h, s, bg='#fff', fg=INK, size=12):
    return rect(x, y, w, h, bg, 4, 2.2) + text(x + w / 2, y + h / 2 + size * 0.36, s, size, fg, 900)


# ---------- 道具 ----------
def tomato(x, y, r=6):
    return circ(x, y, r, '#e5463b', 1.8) + path(f'M{f(x-4)} {f(y-r+1)} L{f(x)} {f(y-r-3)} L{f(x+4)} {f(y-r+1)}', '#4f9a4a', 1.4)


def seed_packet(x, y, w=22, h=30, col='#ffffff', veg='tomato'):
    o = [rect(x, y, w, h, col, 2, 1.8), rect(x + 2, y + 2, w - 4, 6, '#4f9a4a', 1, 0)]
    cx, cy = x + w / 2, y + h * 0.6
    if veg == 'tomato':
        o.append(tomato(cx, cy, w * 0.24))
    elif veg == 'carrot':
        o.append(path(f'M{f(cx-4)} {f(cy-6)} L{f(cx+4)} {f(cy-6)} L{f(cx)} {f(cy+8)} Z', '#f08a24', 1.4) + path(f'M{f(cx)} {f(cy-6)} l-3 -5 M{f(cx)} {f(cy-6)} l3 -5', 'none', 1.6, '#3f8f3f'))
    elif veg == 'corn':
        o.append(ell(cx, cy, 4, 8, '#f5cf3a', 1.4) + path(f'M{f(cx-5)} {f(cy+6)} Q{f(cx-8)} {f(cy-2)} {f(cx-2)} {f(cy-8)}', 'none', 1.6, '#3f8f3f'))
    else:
        o.append(ell(cx, cy, 6, 5, '#7cc06e', 1.4))
    return ''.join(o)


def basket(x, y, w=40, fill=True):
    o = [path(f'M{f(x-w/2)} {f(y)} Q{f(x)} {f(y-30)} {f(x+w/2)} {f(y)}', 'none', 3.2, '#8a5a2b')]
    if fill:
        for i, dx in enumerate((-12, 0, 12, -6, 6)):
            o.append(tomato(x + dx, y - (6 if i > 2 else 1), 6))
    o.append(path(f'M{f(x-w/2)} {f(y)} L{f(x+w/2)} {f(y)} L{f(x+w/2-5)} {f(y+18)} L{f(x-w/2+5)} {f(y+18)} Z', '#c9914f', 2.2))
    o.append(line(x - w / 2 + 3, y + 7, x + w / 2 - 3, y + 7, '#8a5a2b', 1.4) + line(x - w / 2 + 4, y + 13, x + w / 2 - 4, y + 13, '#8a5a2b', 1.4))
    return ''.join(o)


def tomato_plant(x, gy, h=110, n=5):
    o = [line(x + 6, gy, x + 6, gy - h, '#a0764a', 3.4)]
    o.append(path(f'M{f(x)} {f(gy)} Q{f(x-6)} {f(gy-h*0.5)} {f(x+2)} {f(gy-h+6)}', 'none', 3, '#3f8f3f'))
    for i in range(6):
        yy = gy - 14 - i * (h - 20) / 5
        side = -1 if i % 2 else 1
        o.append(ell(x + side * 13, yy, 12, 6, '#5aa560', 1.6, INK, f'transform="rotate({side*-25} {f(x+side*13)} {f(yy)})"'))
    for i in range(n):
        yy = gy - 24 - i * (h - 34) / max(1, n - 1)
        o.append(tomato(x + (-9 if i % 2 else 10), yy, 6.5))
    return ''.join(o)


def fence(x0, x1, y, h=34, col='#f3e3c3'):
    o = [rect(x0, y - h * 0.7, x1 - x0, 5, col, 1, 1.6), rect(x0, y - h * 0.3, x1 - x0, 5, col, 1, 1.6)]
    xx = x0 + 4
    while xx < x1:
        o.append(path(f'M{f(xx)} {f(y)} L{f(xx)} {f(y-h+5)} L{f(xx+5)} {f(y-h)} L{f(xx+10)} {f(y-h+5)} L{f(xx+10)} {f(y)} Z', col, 1.6))
        xx += 16
    return ''.join(o)


def house(x, y, w, h):
    return (rect(x, y - h, w, h, '#f7e1c8', 0, 2.4) + poly([(x - 10, y - h), (x + w / 2, y - h - 46), (x + w + 10, y - h)], '#d2694a', 2.4) +
            rect(x + w * 0.55, y - 48, 26, 48, '#a8714a', 2, 2.2) + circ(x + w * 0.55 + 20, y - 24, 2, INK, 0) +
            window(x + 12, y - h + 14, 30, 26, curtain=None))


def soil_bed(x, y, w, h=20):
    o = [path(f'M{f(x)} {f(y+h)} Q{f(x+4)} {f(y)} {f(x+18)} {f(y)} L{f(x+w-18)} {f(y)} Q{f(x+w-4)} {f(y)} {f(x+w)} {f(y+h)} Z', '#8b5a3c', 2.4)]
    for i in range(3):
        o.append(path(f'M{f(x+16)} {f(y+6+i*5)} L{f(x+w-16)} {f(y+6+i*5)}', 'none', 1.4, '#6b4029', 'stroke-dasharray="6 5"'))
    return ''.join(o)


def shovel(x, y, ang=20):
    return g(line(0, 0, 0, -50, '#a0764a', 4.4) + rect(-7, -58, 14, 8, '#a0764a', 2, 1.8) + path('M-9 0 L9 0 L7 16 Q0 24 -7 16 Z', '#a9b4bd', 2), f'translate({x} {y}) rotate({ang})')


def watering_can(x, y):
    return (path(f'M{f(x)} {f(y)} L{f(x+30)} {f(y)} L{f(x+28)} {f(y-24)} L{f(x+2)} {f(y-24)} Z', '#5aa0d8', 2.2) +
            path(f'M{f(x+28)} {f(y-6)} L{f(x+46)} {f(y-24)}', 'none', 4, '#5aa0d8') + path(f'M{f(x+6)} {f(y-24)} Q{f(x+16)} {f(y-40)} {f(x+26)} {f(y-24)}', 'none', 3, INK))


def blackboard(x, y, w, h, lines_, sizes=None, extra=''):
    o = [rect(x - 6, y - 6, w + 12, h + 12, '#b98b5a', 3, 2.4), rect(x, y, w, h, '#2f6b4f', 2, 2)]
    sizes = sizes or [14] * len(lines_)
    yy = y + 12
    for s_, sz in zip(lines_, sizes):
        yy += sz + 4
        o.append(text(x + w / 2, yy, s_, sz, '#ffffff', 700, extra='font-family="Comic Sans MS,Chalkboard,Arial"'))
    o.append(rect(x + w * 0.65, y + h + 2, 24, 4, '#ffffff', 1, 1))
    return ''.join(o) + extra


def school_desk(x, fy, w=56, top=None, col='#d9a86c'):
    ty = top if top is not None else fy - 52
    return (line(x - w / 2 + 6, ty, x - w / 2 + 6, fy, '#7c8a96', 4) + line(x + w / 2 - 6, ty, x + w / 2 - 6, fy, '#7c8a96', 4) +
            rect(x - w / 2, ty - 4, w, 8, col, 2, 2.2))


def penguin(x, y, s=1):
    return g(ell(0, 0, 12, 18, '#2b2d42', 1.6) + ell(0, 4, 8, 13, '#fff', 0) + circ(0, -14, 9, '#2b2d42', 1.6) +
             circ(-3, -15, 1.8, '#fff', 0) + circ(3, -15, 1.8, '#fff', 0) + circ(-3, -15, 0.9, INK, 0) + circ(3, -15, 0.9, INK, 0) +
             path('M-3 -11 L3 -11 L0 -7 Z', '#f5a524', 1) + ell(-6, 18, 5, 2.6, '#f5a524', 1) + ell(6, 18, 5, 2.6, '#f5a524', 1) +
             path('M-12 -2 Q-18 8 -12 14', 'none', 3, '#2b2d42') + path('M12 -2 Q18 8 12 14', 'none', 3, '#2b2d42'),
             f'translate({f(x)} {f(y)}) scale({s})')


def tablet(x, y, w=46, h=34, screen=''):
    return rect(x, y, w, h, '#3b3f46', 4, 2.2) + rect(x + 4, y + 4, w - 8, h - 8, '#e6f4ff', 2, 0) + screen


def bill(x, y, w, h, amount, col='#d63b3b', rot=0, arrow=False):
    o = [rect(x, y, w, h, '#ffffff', 3, 2.2), rect(x, y, w, 14, '#f4d35e', 3, 2.2),
         text(x + w / 2, y + 10, 'ELECTRICITY BILL', 6.6, INK, 900)]
    o.append(line(x + 8, y + 22, x + w - 8, y + 22, '#c9c9c9', 2) + line(x + 8, y + 29, x + w - 20, y + 29, '#c9c9c9', 2))
    o.append(text(x + w / 2, y + h - 10, amount, 15, col, 900))
    if arrow:
        o.append(path(f'M{f(x+w+12)} {f(y+10)} L{f(x+w+12)} {f(y+h-4)} M{f(x+w+4)} {f(y+h-14)} L{f(x+w+12)} {f(y+h-4)} L{f(x+w+20)} {f(y+h-14)}', 'none', 4, '#2f9e44'))
    s = ''.join(o)
    return g(s, f'rotate({rot} {f(x+w/2)} {f(y+h/2)})') if rot else s


def ceiling_lamp(x, on=True, top=0, len_=26):
    o = [line(x, top, x, top + len_, INK, 2)]
    o.append(path(f'M{f(x-20)} {f(top+len_+18)} Q{f(x)} {f(top+len_-6)} {f(x+20)} {f(top+len_+18)} Z', '#f4e2b8', 2.2))
    o.append(circ(x, top + len_ + 19, 5, '#fff7c2' if on else '#bdbdbd', 1.6))
    if on:
        o.append(path(f'M{f(x-18)} {f(top+len_+20)} L{f(x-70)} {f(top+len_+120)} L{f(x+70)} {f(top+len_+120)} L{f(x+18)} {f(top+len_+20)} Z', '#fff3a8', 0, INK, 'opacity="0.45"'))
    return ''.join(o)


def tv(x, fy):
    return (rect(x - 30, fy - 34, 60, 34, '#9a6b45', 2, 2.2) + rect(x - 34, fy - 76, 68, 42, '#2b2d42', 3, 2.4) +
            rect(x - 29, fy - 71, 58, 32, '#454b57', 1, 0))


def sofa(x, fy, w=110, col='#e98a6b'):
    return (rect(x, fy - 52, w, 34, col, 10, 2.4) + rect(x - 8, fy - 36, 20, 34, col, 6, 2.4) + rect(x + w - 12, fy - 36, 20, 34, col, 6, 2.4) +
            rect(x + 8, fy - 26, w - 16, 18, col, 5, 2.2) + line(x + w / 2, fy - 26, x + w / 2, fy - 8, INK, 1.6) +
            line(x + 4, fy - 2, x + 4, fy + 4, INK, 3) + line(x + w - 4, fy - 2, x + w - 4, fy + 4, INK, 3))


def switch_plate(x, y, on):
    return rect(x - 7, y - 11, 14, 22, '#ffffff', 2, 2) + rect(x - 3.5, y - 7 + (0 if on else 5), 7, 9, '#cfcfcf', 1.5, 1.6)


def bottle(x, y, rot=0, col='#9ed6ef'):
    return g(rect(-5, -12, 10, 20, col, 3, 1.8) + rect(-2.5, -17, 5, 6, '#3f87c9', 1, 1.6), f'translate({f(x)} {f(y)}) rotate({rot})')


def can(x, y, rot=0, col='#e05a4f'):
    return g(rect(-5, -8, 10, 15, col, 2, 1.8) + line(-5, -3, 5, -3, '#fff', 1.6), f'translate({f(x)} {f(y)}) rotate({rot})')


def plastic_bag(x, y):
    return path(f'M{f(x-10)} {f(y)} Q{f(x-14)} {f(y-14)} {f(x-6)} {f(y-18)} L{f(x-8)} {f(y-24)} M{f(x-6)} {f(y-18)} L{f(x+6)} {f(y-18)} L{f(x+8)} {f(y-24)} M{f(x+6)} {f(y-18)} Q{f(x+14)} {f(y-14)} {f(x+10)} {f(y)} Z', '#ffffff', 1.8)


def trash_bag(x, y, s=1, col='#59a8e6'):
    return g(path('M-14 0 Q-20 -18 -8 -28 L-4 -34 L4 -34 L8 -28 Q20 -18 14 0 Z', col, 2.2) + path('M-5 -34 L-8 -42 M5 -34 L8 -42', 'none', 2.4, col) + path('M-6 -20 Q0 -14 6 -22', 'none', 1.4),
             f'translate({f(x)} {f(y)}) scale({s})')


def beach(gy=150, sea_y=96):
    o = [rect(0, 0, W, sea_y, SKY, 0, 0), rect(0, sea_y, W, gy - sea_y + 6, SEA, 0, 0)]
    for i in range(3):
        yy = sea_y + 12 + i * 14
        o.append(path('M0 %s ' % f(yy) + ' '.join(f'q10 -6 20 0 t20 0' for _ in range(9)), 'none', 2, '#ffffff'))
    o.append(path(f'M0 {f(gy)} ' + ' '.join('q15 -8 30 0' for _ in range(12)) + f' L{W} {H} L0 {H} Z', SAND, 2))
    return ''.join(o)


def volleyball(x, y, r=10):
    return circ(x, y, r, '#ffffff', 2) + path(f'M{f(x-r)} {f(y)} Q{f(x)} {f(y-6)} {f(x+r)} {f(y-2)} M{f(x-3)} {f(y-r)} Q{f(x+5)} {f(y)} {f(x)} {f(y+r)}', 'none', 1.6, '#f2a900')


def soccer_ball(x, y, r=8):
    return circ(x, y, r, '#fff', 2) + poly([(x, y - 3.5), (x + 3.3, y - 1), (x + 2, y + 3), (x - 2, y + 3), (x - 3.3, y - 1)], INK, 0)


def plate_toast(x, y):
    return ell(x, y, 18, 5, '#ffffff', 2) + rect(x - 11, y - 18, 22, 16, '#e9b46a', 5, 2) + rect(x - 7, y - 14, 14, 9, '#f7dca5', 3, 0)


def rice_bowl(x, y):
    return path(f'M{f(x-12)} {f(y-10)} L{f(x+12)} {f(y-10)} Q{f(x+10)} {f(y+2)} {f(x)} {f(y+2)} Q{f(x-10)} {f(y+2)} {f(x-12)} {f(y-10)} Z', '#ffffff', 2) + path(f'M{f(x-11)} {f(y-10)} Q{f(x)} {f(y-22)} {f(x+11)} {f(y-10)}', '#ffffff', 2)


def miso(x, y):
    return path(f'M{f(x-11)} {f(y-10)} L{f(x+11)} {f(y-10)} Q{f(x+9)} {f(y+2)} {f(x)} {f(y+2)} Q{f(x-9)} {f(y+2)} {f(x-11)} {f(y-10)} Z', '#b5432f', 2) + ell(x, y - 10, 11, 3, '#c98a4b', 1.4)


def egg_plate(x, y):
    return ell(x, y, 18, 5, '#ffffff', 2) + path(f'M{f(x-12)} {f(y-3)} Q{f(x-10)} {f(y-12)} {f(x)} {f(y-10)} Q{f(x+12)} {f(y-12)} {f(x+11)} {f(y-3)} Z', '#ffffff', 1.6) + circ(x, y - 7, 4.5, '#f5b82e', 1.4)


def backpack(x, y, d=1):
    return g(rect(-14, -20, 22, 30, '#e05a4f', 6, 2.2) + rect(-12, -2, 18, 10, '#c9443a', 3, 1.6), f'translate({f(x)} {f(y)}) scale({d} 1)')


def camera(x, y, s=1):
    return g(rect(-11, -7, 22, 15, '#4a4f58', 3, 1.8) + rect(-5, -11, 9, 5, '#4a4f58', 1, 1.6) + circ(1, 0.5, 5, '#9fc3e6', 1.6) + circ(1, 0.5, 2, INK, 0), f'translate({f(x)} {f(y)}) scale({s})')


def envelope(x, y, w=40, h=26):
    o = [rect(x, y, w, h, '#ffffff', 2, 2), path(f'M{f(x)} {f(y)} L{f(x+w/2)} {f(y+h*0.55)} L{f(x+w)} {f(y)}', 'none', 1.8)]
    i = 0
    xx = x
    while xx < x + w - 4:
        o.append(rect(xx + 1, y + h - 4, 5, 3, '#e05a4f' if i % 2 else '#3f6fc9', 0, 0))
        xx += 7; i += 1
    o.append(rect(x + w - 12, y + 3, 9, 10, '#f7c948', 1, 1.2))
    return ''.join(o)


def pagoda_temple(x, gy):
    """お寺の本堂（横長）。"""
    o = []
    o.append(rect(x - 70, gy - 16, 140, 16, '#d9d1c3', 1, 2.2))  # 基だん
    o.append(rect(x - 56, gy - 62, 112, 46, '#c9483b', 1, 2.4))
    for i in range(5):
        o.append(line(x - 56 + 22 + i * 22, gy - 62, x - 56 + 22 + i * 22, gy - 16, INK, 1.8))
    o.append(rect(x - 16, gy - 50, 32, 34, '#8a4a2c', 1, 2))
    o.append(path(f'M{f(x-96)} {f(gy-58)} Q{f(x-60)} {f(gy-70)} {f(x-44)} {f(gy-96)} L{f(x+44)} {f(gy-96)} Q{f(x+60)} {f(gy-70)} {f(x+96)} {f(gy-58)} Z', '#5b6470', 2.4))
    o.append(path(f'M{f(x-40)} {f(gy-96)} L{f(x-30)} {f(gy-112)} L{f(x+30)} {f(gy-112)} L{f(x+40)} {f(gy-96)} Z', '#5b6470', 2.2))
    o.append(line(x - 34, gy - 112, x + 34, gy - 112, INK, 3))
    return ''.join(o)


def tree(x, gy, s=1, col='#6fb66a'):
    return line(x, gy, x, gy - 40 * s, '#8a5a2b', 7 * s) + circ(x - 12 * s, gy - 48 * s, 18 * s, col, 2) + circ(x + 12 * s, gy - 50 * s, 18 * s, col, 2) + circ(x, gy - 66 * s, 20 * s, col, 2)


def lines_mark(x, y, d=1, col='#f08c00'):
    """うれしい・おどろきの線"""
    return path(f'M{f(x)} {f(y)} l{f(-6*d)} -8 M{f(x+10*d)} {f(y-4)} l0 -10 M{f(x+20*d)} {f(y)} l{f(6*d)} -8', 'none', 2.2, col)


def clap_mark(x, y):
    return path(f'M{f(x-8)} {f(y-6)} l-5 -5 M{f(x)} {f(y-9)} l0 -7 M{f(x+8)} {f(y-6)} l5 -5', 'none', 2, '#f08c00')


def held_packet(col='#ffffff', veg='tomato'):
    return lambda hx, hy: seed_packet(hx - 4, hy - 26, 18, 24, col, veg)


# ================= s1 Community Gardens =================
def s1p1():
    gy = 160
    o = [outdoor(gy=gy), cloud(250, 40), sun(318, 34), house(-20, gy, 92, 66), fence(72, 360, gy)]
    o.append(soil_bed(180, 196, 166, 24))
    o.append(shovel(342, 218, 18))
    o.append(watering_can(186, 250))
    m, mh = person(64, 236, 'mom', d=1, arms=((20, 50), (10, 20)), mouth='smile')
    b, bh = person(150, 238, 'boy', d=-1, arms=((15, 35), (-75, -85)), mouth='open', brows='up')
    o += [m, b]
    o.append(bubble(164, 62, 176, ["Let's plant", 'some vegetables!'], bh['mouth'], 13))
    return svg(''.join(o))


def s1p2():
    fy = 182
    o = [room('#f3efe2', '#d8d2c4', fy)]
    o.append(label_sign(28, 12, 120, 22, 'GARDEN SHOP', '#3f8f5a', '#ffffff', 11))
    # たな
    o.append(rect(16, 40, 144, 136, '#c8945f', 3, 2.4))
    cols = ['#ffffff', '#fff3c4', '#e7f6e0', '#fde4e4']
    vegs = ['tomato', 'carrot', 'corn', 'leaf']
    for r in range(3):
        o.append(rect(20, 44 + r * 44, 136, 40, '#f1dfc0', 1, 1.4))
        for c in range(5):
            o.append(seed_packet(25 + c * 26, 49 + r * 44, 22, 30, cols[(r + c) % 4], vegs[(r * 2 + c) % 4]))
    # 店の人とカウンター
    cl, _ = person(304, 232, 'clerk', d=-1, arms=((40, 70), (20, 30)), mouth='smile')
    o.append(cl)
    o.append(rect(222, 160, 136, 72, '#8fbf9f', 3, 2.4) + rect(216, 152, 148, 10, '#e9d7b5', 2, 2.2))
    o.append(rect(318, 128, 34, 24, '#5b6470', 3, 2) + rect(322, 132, 20, 8, '#bfe3c9', 1, 0))
    o.append(seed_packet(256, 128, 18, 24, '#ffffff', 'tomato') + seed_packet(277, 130, 18, 24, '#fff3c4', 'carrot'))
    m, _ = person(186, 238, 'mom', d=1, arms=((60, 95), (15, 30)), mouth='smile',
                  held={'near': lambda hx, hy: seed_packet(hx - 2, hy - 28, 18, 24, '#e7f6e0', 'corn')})
    o.append(m)
    o.append(basket(166, 214, 30, False))
    return svg(''.join(o))


def s1p3():
    gy = 150
    o = [outdoor(gy=gy), sun(36, 30), cloud(220, 34), fence(0, 360, gy)]
    o.append(soil_bed(150, 214, 200, 22))
    for x in (172, 226, 280, 334):
        o.append(tomato_plant(x, 222, 118, 5))
    b, bh = person(130, 240, 'boy', d=1, arms=((95, 135), (20, 40)), face='happy', mouth='grin',
                   held={'near': lambda hx, hy: tomato(hx + 4, hy - 4, 6.5)})
    o.append(b)
    o.append(basket(96, 226, 38))
    m, _ = person(46, 236, 'mom', d=1, arms=((40, 100), (35, 95)), face='happy', mouth='smile')
    o.append(m)
    o.append(lines_mark(112, 92, 1))
    return svg(''.join(o))


# ================= s2 Tablets at School =================
def s2p1():
    fy = 168
    o = [room('#e7f1e6', '#d7b98b', fy)]
    o.append(blackboard(150, 26, 196, 96, ['Presentation', '"ANIMALS"'], [17, 19]))
    o.append(penguin(318, 108, 0.6) + text(176, 112, 'Next Friday', 10, '#ffffff', 700))
    t, th = person(110, 222, 'teacher', d=1, arms=((150, 150), (20, 30)), mouth='open')
    o.append(t)
    o.append(bubble(6, 8, 138, ['Please make a', 'presentation', 'about animals.'], th['mouth'], 12))
    for x, kd in ((60, 'boy2'), (182, 'girl'), (300, 'kid3')):
        o.append(school_desk(x, 262, 76, 224))
        s, _ = person(x, 262, kd, d=1, back=True, sit=True, arms=((50, 70), (50, 70)), legs=((90, 0), (90, 0)), s=1.05)
        o.append(s)
    return svg(''.join(o))


def s2p2():
    fy = 186
    o = [room('#e6e1f2', '#c9a77c', fy)]
    o.append(window(26, 22, 86, 70, night=True, curtain='#9fb7e8'))
    o.append(table(150, 352, 150, fy + 40, '#b98557'))
    # 電気スタンド
    o.append(path('M328 150 L328 96 L300 78', 'none', 4, '#5b6470') + path('M286 70 L316 66 L310 92 Z', '#f6c945', 2) +
             path('M304 90 L250 150 L330 150 Z', '#fff3a8', 0, INK, 'opacity="0.5"'))
    o.append(chair(118, fy + 40, 1))
    scr = penguin(232, 122, 0.62) + text(218, 108, 'PENGUINS', 6.5, '#2b6cb0', 900, 'start')
    o.append(path('M198 150 L206 148 L210 100 L202 102 Z', '#5b6470', 1.6))
    o.append(tablet(206, 98, 58, 44, scr))
    o.append(rect(270, 144, 42, 6, '#ffffff', 1, 1.6) + line(274, 147, 306, 147, '#c9c9c9', 1))
    gch, _ = person(124, fy + 40, 'girl', d=1, sit=True, legs=((90, 0), (90, 0)), arms=((60, 95), (40, 80)),
                    mouth='smile', held={'near': lambda hx, hy: line(hx, hy, hx + 8, hy - 12, '#f6c945', 3)})
    o.append(gch)
    o.append(clock(320, 30, 16, 8, 0))
    return svg(''.join(o))


def s2p3():
    fy = 168
    o = [room('#e7f1e6', '#d7b98b', fy)]
    o.append(blackboard(26, 22, 150, 70, ['Animal', 'Presentations'], [13, 13]))
    # ポスター
    o.append(rect(196, 18, 128, 132, '#ffffff', 4, 2.4) + text(260, 40, 'PENGUINS', 15, '#2b6cb0', 900))
    o.append(penguin(236, 92, 1.3) + penguin(286, 100, 0.95))
    o.append(path('M204 132 q20 -8 40 0 t40 0 t36 0', 'none', 2, '#7cc3e6'))
    o.append(line(260, 150, 240, fy + 30, '#8a5a2b', 4) + line(260, 150, 280, fy + 30, '#8a5a2b', 4))
    gch, gh = person(166, 214, 'girl', d=1, arms=((120, 120), (20, 40)), mouth='open', face='open')
    o.append(gch)
    for x, kd in ((50, 'boy2'), (178, 'kid4'), (304, 'kid3')):
        o.append(school_desk(x, 262, 76, 230))
        s, sh = person(x, 262, kd, d=1, back=True, sit=True, arms=((70, 110), (70, 110)), legs=((90, 0), (90, 0)), s=1.05)
        o.append(s)
        o.append(clap_mark(x + 14, sh['head'][1] + 4))
    return svg(''.join(o))


# ================= s3 Saving Energy =================
def s3p1():
    fy = 176
    o = [room('#f4ead6', '#cfa979', fy)]
    o.append(window(220, 22, 90, 66, sky='#f6b98a', curtain='#9cc59a'))
    o.append(sofa(232, fy + 22, 110))
    d_, dh = person(104, 236, 'dad', d=1, arms=((55, 105), (45, 100)), brows='worried', mouth='o')
    o.append(d_)
    b, bh = person(214, 238, 'boy', d=-1, arms=((15, 30), (10, 20)), face='wide', mouth='o', brows='up')
    o.append(b)
    o.append(bill(130, 96, 66, 52, '¥30,000', rot=-4))
    o.append(path('M176 82 l-4 -10 M188 80 l2 -11 M198 86 l7 -8', 'none', 2.4, '#d63b3b'))
    o.append(bubble(8, 8, 150, ['The bill is', 'very high!'], dh['mouth'], 13))
    return svg(''.join(o))


def s3p2():
    fy = 176
    o = [room('#f4ead6', '#cfa979', fy)]
    o.append(sofa(40, fy + 24, 120) + tv(220, fy + 24))
    o.append(ceiling_lamp(120, on=False, len_=18))
    o.append(rect(0, 0, 268, H, '#1d2340', 0, 0, INK, 'opacity="0.42"'))
    # ろうかと戸口
    o.append(rect(268, 0, 92, H, '#f7efda', 0, 0) + line(268, 0, 268, H, INK, 3) + rect(262, 30, 8, 200, '#b98557', 1, 2))
    o.append(switch_plate(300, 122, False))
    b, bh = person(334, 238, 'boy', d=-1, arms=((120, 150), (10, 20)), mouth='smile', face='open')
    o.append(b)
    o.append(text(300, 98, 'click', 11, '#f08c00', 900))
    o.append(text(110, 120, 'OFF', 13, '#fff7c2', 900))
    return svg(''.join(o))


def s3p3():
    fy = 176
    o = [room('#f4ead6', '#cfa979', fy)]
    o.append(window(232, 22, 90, 66, curtain='#9cc59a'))
    d_, dh = person(104, 236, 'dad', d=1, arms=((60, 110), (50, 105)), face='happy', mouth='grin')
    o.append(d_)
    b, bh = person(232, 238, 'boy', d=-1, arms=((150, 165), (140, 160)), face='happy', mouth='grin')
    o.append(b)
    o.append(bill(130, 92, 66, 52, '¥15,000', col='#2f9e44', arrow=True))
    o.append(lines_mark(70, 70, -1) + lines_mark(248, 70, 1))
    return svg(''.join(o))


# ================= s4 Cleaning Beaches =================
def s4p1():
    o = [beach(150, 92), cloud(260, 36), sun(36, 34)]
    for args in ((40, 222, 70), (196, 232, -20), (300, 210, 80), (250, 250, 10)):
        o.append(bottle(*args))
    for args in ((150, 246, 30), (330, 240, -60), (92, 196, 0)):
        o.append(can(*args))
    o.append(bottle(278, 240, -70) + can(22, 250, 40))
    m, mh = person(110, 238, 'girl', d=1, arms=((60, 40), (10, 20)), mouth='open', brows='up')
    fr, fh = person(222, 238, 'boy2', d=-1, arms=((15, 25), (10, 20)), mouth='frown', brows='worried')
    o += [m, fr]
    o.append(bubble(130, 70, 176, ["Let's clean the beach", 'next Sunday!'], mh['mouth'], 12.5))
    return svg(''.join(o))


def s4p2():
    o = [beach(150, 92), cloud(300, 30)]
    o.append(line(150, 150, 150, 40, '#8a5a2b', 4) + line(250, 150, 250, 40, '#8a5a2b', 4) + rect(136, 14, 128, 30, '#ffffff', 3, 2.4) +
             text(200, 35, 'BEACH CLEAN-UP', 13, '#2b6cb0', 900))
    a, ah = person(56, 234, 'man', d=1, arms=((20, 30), (60, 100)), mouth='smile',
                   held={'near': lambda hx, hy: trash_bag(hx, hy + 30, 0.9, '#59a8e6')})
    o.append(a)
    gch, gh = person(150, 238, 'girl', d=1, lean=40, arms=((70, 40), (40, 30)), mouth='smile', legs=((10, 0), (-6, -2)),
                     held={'near': lambda hx, hy: bottle(hx + 4, hy + 2, 90)})
    o.append(gch)
    o.append(trash_bag(116, 244, 0.8, '#ffffff'))
    w_, wh = person(262, 236, 'woman', d=-1, arms=((40, 70), (20, 30)), mouth='smile',
                    held={'near': lambda hx, hy: trash_bag(hx, hy + 30, 0.9, '#7fcf7f')})
    o.append(w_)
    k, kh = person(320, 238, 'boy2', d=-1, lean=30, arms=((60, 30), (20, 10)), mouth='smile', s=0.95,
                   held={'near': lambda hx, hy: can(hx, hy + 4, 70)})
    o.append(k)
    o.append(bottle(206, 238, 75) + can(186, 252, -20))
    return svg(''.join(o))


def s4p3():
    o = [beach(150, 92), sun(318, 30), cloud(60, 36)]
    m, mh = person(206, 210, 'girl', d=-1, s=0.8, arms=((150, 165), (145, 160)), face='happy', mouth='grin', legs=((20, 10), (-10, -20)))
    o.append(m)
    # ネット（横から見る）
    o.append(line(60, 220, 60, 146, INK, 4) + line(300, 220, 300, 146, INK, 4))
    o.append(rect(60, 150, 240, 30, '#ffffff', 0, 0, INK, 'fill-opacity="0.25"'))
    for xx in range(66, 300, 8):
        o.append(line(xx, 150, xx, 180, '#6a6a6a', 0.9))
    for yy in range(156, 180, 7):
        o.append(line(60, yy, 300, yy, '#6a6a6a', 0.9))
    o.append(rect(60, 147, 240, 5, '#ffffff', 1, 1.8) + line(60, 180, 300, 180, INK, 1.6))
    fr, fh = person(130, 246, 'boy2', d=1, arms=((145, 160), (135, 155)), face='happy', mouth='open', legs=((15, 5), (-10, -15)))
    o.append(fr)
    o.append(volleyball(172, 46, 11) + path('M186 42 q20 -12 40 -2', 'none', 2, '#7a7a7a', 'stroke-dasharray="4 4"'))
    for i, x in enumerate((316, 338, 327)):
        o.append(trash_bag(x, 254 - (16 if i == 2 else 0), 0.75, '#59a8e6'))
    return svg(''.join(o))


# ================= s5 Breakfast =================
def s5p1():
    fy = 176
    o = [room('#fbefd9', '#d4ad7c', fy)]
    o.append(clock(150, 40, 20, 8, 0))
    o.append(rect(264, 18, 96, fy - 18 + 4, '#a8714a', 0, 2.4) + rect(272, 26, 88, fy - 26, '#cfe8f7', 0, 2) + tree(318, fy, 0.8))
    o.append(table(10, 120, 156, fy + 34, '#c08a55'))
    o.append(miso(30, 154) + rice_bowl(58, 154))
    m, mh = person(76, 236, 'mom', d=1, arms=((80, 90), (30, 60)), mouth='open', brows='up',
                   held={'near': lambda hx, hy: plate_toast(hx + 14, hy + 2)})
    o.append(m)
    b, bh = person(232, 240, 'boy', d=1, lean=14, legs=((45, 5), (-35, -60)), arms=((-45, 0), (60, 80)), mouth='open', sweat=True,
                   held={'far': lambda hx, hy: ''})
    o.append(backpack(216, 152, 1) if False else '')
    o.insert(-0 if False else len(o), rect(204, 162, 18, 32, '#e05a4f', 6, 2.2))
    o.append(b)
    o.append(path('M182 200 l-24 0 M186 214 l-30 0 M182 228 l-22 0', 'none', 2.4, '#9a9a9a'))
    o.append(bubble(8, 8, 120, ['Eat your', 'breakfast!'], mh['mouth'], 13))
    return svg(''.join(o))


def s5p2():
    gy = 120
    o = [outdoor('#cde7f6', '#8fcb6f', gy), cloud(40, 36)]
    o.append(rect(196, 64, 120, 58, 'none', 0, 3.4, '#ffffff') + ''.join(line(196 + i * 12, 64, 196 + i * 12, 122, '#ffffff', 1) for i in range(11)))
    o.append(line(0, 160, 360, 160, '#ffffff', 3))
    for x, kd in ((230, 'kid3'), (300, 'boy2')):
        p_, _ = person(x, 150, kd, d=-1 if x > 260 else 1, s=0.55, legs=((40, 10), (-30, -50)), arms=((-40, 0), (50, 80)), lean=10)
        o.append(p_)
    o.append(soccer_ball(268, 146, 5))
    # ベンチ
    o.append(rect(30, 196, 150, 9, '#b98557', 2, 2.2) + line(42, 205, 42, 240, INK, 4) + line(168, 205, 168, 240, INK, 4))
    b, bh = person(104, 240, 'boy', d=1, sit=True, legs=((80, 5), (85, 8)), arms=((10, 70), (15, 25)), face='tired', mouth='wavy',
                   brows='worried', sweat=True, tilt=8)
    # すわる高さをベンチに合わせる
    o.append(g(b, 'translate(0 -8)'))
    o.append(soccer_ball(150, 232, 10))
    o.append(text(150, 178, 'growl...', 12, '#d9480f', 900, 'start'))
    o.append(bubble(14, 8, 110, ['   ', '   '], (bh['head'][0] + 10, bh['head'][1] - 8), 12, think=True))
    o.append(rice_bowl(50, 34) + plate_toast(84, 36))
    return svg(''.join(o))


def s5p3():
    fy = 176
    o = [room('#fbefd9', '#d4ad7c', fy)]
    o.append(window(22, 22, 84, 62, curtain='#f2c46a', sky='#ffe9a8') + sun(80, 44, 9))
    o.append(rect(136, 70, 64, 6, '#a8714a', 1, 2))
    o.append(clock(168, 46, 20, 6, 30, '#ff9a8a') + circ(152, 26, 5, '#ff9a8a', 2) + circ(184, 26, 5, '#ff9a8a', 2))
    o.append(text(168, 90, '6:30', 12, INK, 900))
    o.append(chair(84, fy + 50, 1))
    o.append(table(110, 300, 168, fy + 50, '#c08a55'))
    b, bh = person(92, fy + 50, 'boy', d=1, sit=True, legs=((90, 0), (90, 0)), arms=((70, 120), (60, 100)), face='happy', mouth='grin',
                   held={'near': lambda hx, hy: line(hx, hy, hx + 16, hy + 8, '#a0764a', 2.2) + line(hx, hy - 3, hx + 16, hy + 4, '#a0764a', 2.2)})
    o.append(b)
    o.append(rice_bowl(146, 166) + miso(176, 166) + egg_plate(214, 166))
    m, _ = person(300, 240, 'mom', d=-1, arms=((40, 100), (30, 90)), face='happy', mouth='smile')
    o.append(m)
    return svg(''.join(o))


# ================= s6 Learning Languages / Friend from Australia =================
def s6p1():
    fy = 182
    o = [room('#e4effa', '#cfae80', fy)]
    o.append(window(18, 22, 70, 58, curtain='#f2c46a'))
    b, bh = person(84, 240, 'boy', d=1, arms=((70, 115), (60, 110)), face='wide', mouth='open', brows='up')
    o.append(b)
    hx, hy = bh['near']
    o.append(rect(hx - 6, hy - 22, 26, 32, '#ffffff', 2, 2))
    o.append(line(hx - 2, hy - 14, hx + 16, hy - 14, '#c9c9c9', 1.6) + line(hx - 2, hy - 8, hx + 16, hy - 8, '#c9c9c9', 1.6) + line(hx - 2, hy - 2, hx + 12, hy - 2, '#c9c9c9', 1.6))
    # 手紙の中身を大きく
    o.append(path(f'M{f(hx+20)} {f(hy-20)} L150 112 L150 52 Z', '#ffffff', 0, INK, 'opacity="0.9"'))
    o.append(line(hx + 20, hy - 20, 150, 52, '#9a9a9a', 1.4, dash='4 3') + line(hx + 20, hy + 8, 150, 140, '#9a9a9a', 1.4, dash='4 3'))
    o.append(rect(150, 20, 196, 124, '#fffdf4', 4, 2.4))
    o.append(text(164, 46, 'Dear Sho,', 13, INK, 700, 'start', "Georgia,'Times New Roman',serif"))
    o.append(text(176, 74, 'I will visit Japan', 14, INK, 900, 'start', "Georgia,'Times New Roman',serif"))
    o.append(text(176, 96, 'in August!', 14, INK, 900, 'start', "Georgia,'Times New Roman',serif"))
    o.append(text(330, 128, 'Tom', 13, INK, 700, 'end', "Georgia,'Times New Roman',serif"))
    o.append(table(180, 350, 196, fy + 52, '#b98557'))
    o.append(envelope(240, 168, 50, 28) + text(270, 162, 'from Australia', 9, '#2b6cb0', 900))
    o.append(lines_mark(60, 106, -1))
    return svg(''.join(o))


def s6p2():
    fy = 186
    o = [room('#e4effa', '#cfae80', fy)]
    o.append(window(250, 20, 80, 60, curtain='#f2c46a'))
    o.append(table(130, 350, 150, fy + 44, '#b98557'))
    o.append(chair(104, fy + 44, 1))
    # 地図とノート
    o.append(rect(170, 128, 70, 22, '#e9f6e6', 2, 2) + path('M182 146 q8 -14 16 -6 t18 -8 t14 4', 'none', 2, '#d63b3b', 'stroke-dasharray="3 3"') + circ(230, 136, 3, '#d63b3b', 1))
    o.append(rect(250, 96, 84, 56, '#ffffff', 3, 2.4) + text(292, 112, 'PLAN', 12, '#d63b3b', 900))
    o.append(text(258, 128, '1. temple', 10, INK, 700, 'start') + text(258, 143, '2. sushi', 10, INK, 700, 'start'))
    o.append(rect(150, 112, 18, 38, '#5b8bd8', 2, 2) + text(159, 136, 'JAPAN', 5.5, '#ffffff', 900, extra='transform="rotate(-90 159 133)"'))
    b, bh = person(110, fy + 44, 'boy', d=1, sit=True, legs=((90, 0), (90, 0)), arms=((70, 110), (50, 95)), mouth='smile', face='down',
                   held={'near': lambda hx, hy: line(hx, hy, hx + 6, hy - 14, '#f6c945', 3.2)})
    o.append(b)
    o.append(bubble(8, 8, 150, ['   ', '   '], (bh['head'][0] + 6, bh['head'][1] - 4), 12, think=True))
    o.append(g(pagoda_temple(0, 0), 'translate(46 50) scale(0.26)') + rect(98, 16, 46, 26, '#ffffff', 3, 1.8))
    o.append(ell(121, 34, 14, 5, '#ffffff', 1.6) + rect(110, 22, 22, 10, '#f28c6b', 4, 1.4))
    return svg(''.join(o))


def s6p3():
    gy = 180
    o = [outdoor('#cde7f6', '#e3ddd0', gy), cloud(40, 30), cloud(300, 44, 0.8)]
    o.append(tree(330, gy + 6, 1.1) + tree(26, gy + 4, 0.9, '#7dbf72'))
    o.append(pagoda_temple(196, gy))
    o.append(path(f'M0 {gy+30} L360 {gy+30}', 'none', 0))
    t, th = person(76, 240, 'tom', d=1, arms=((100, 140), (90, 135)), face='happy', mouth='grin',
                   held={'near': lambda hx, hy: camera(hx + 4, hy - 4)})
    s, sh = person(156, 242, 'boy', d=1, arms=((95, 145), (85, 140)), face='happy', mouth='grin', s=0.98,
                   held={'near': lambda hx, hy: camera(hx + 4, hy - 4, 0.9)})
    o += [t, s]
    o.append(text(120, 110, 'click!', 11, '#f08c00', 900) + text(196, 112, 'click!', 11, '#f08c00', 900))
    return svg(''.join(o))


ALL = {
    's1': [s1p1, s1p2, s1p3], 's2': [s2p1, s2p2, s2p3], 's3': [s3p1, s3p2, s3p3],
    's4': [s4p1, s4p2, s4p3], 's5': [s5p1, s5p2, s5p3], 's6': [s6p1, s6p2, s6p3],
}

if __name__ == '__main__':
    out = {k: [fn() for fn in v] for k, v in ALL.items()}
    json.dump(out, open(sys.argv[1], 'w'))
    if len(sys.argv) > 2:
        caps = {'s1': ['', 'The next day', 'A few months later'], 's2': ['', 'That evening', 'A week later'],
                's3': ['', 'That night', 'A month later'], 's4': ['', 'On Sunday', 'After that'],
                's5': ['', 'At soccer practice', 'The next morning'], 's6': ['', 'The next day', 'In August']}
        html = ['<html><body style="margin:0;background:#fff;font-family:Arial">']
        for k, v in out.items():
            html.append(f'<h3 style="margin:6px">{k}</h3><div style="display:grid;grid-template-columns:repeat(3,330px);gap:14px;margin:6px">')
            for i, s_ in enumerate(v):
                html.append(f'<div><div style="font-weight:700;font-size:13px;height:18px">{caps[k][i]}</div><div style="border:2px solid #333;width:330px">{s_}</div></div>')
            html.append('</div>')
        open(sys.argv[2], 'w').write(''.join(html))
