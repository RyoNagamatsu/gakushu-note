"""Check one week file of ぴょんぴょんノート.
python3 kaede/tools/check_week.py kaede/weeks/2026-10-19.json
Checks: shape, unique ids per day, arithmetic in 'a ＋ b ＝' style fill items and in work.model, kanji stroke counts against ../kv."""
import json, re, sys, os
p = sys.argv[1]; w = json.load(open(p, encoding='utf8')); err = []
kvdir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'kv')
OPS = {'＋': lambda a, b: a + b, '－': lambda a, b: a - b, '×': lambda a, b: a * b, '÷': lambda a, b: a // b if b and a % b == 0 else None}
assert w['id'] == os.path.basename(p)[:-5], 'id must equal file name'
if len(w['days']) != 5: err.append('days must be 5')
def strokes(ch):
    f = os.path.join(kvdir, '%02x.json' % (ord(ch) >> 8))
    d = json.load(open(f, encoding='utf8')).get(ch) if os.path.exists(f) else None
    return len(d['p']) if d else None
def check(name, part):
    ids = set(); n = 0
    for s in part['sections']:
        for it in s['items']:
            if 'k' not in it: continue
            n += 1
            if it['id'] in ids: err.append('%s: duplicate id %s' % (name, it['id']))
            ids.add(it['id'])
            if it['k'] == 'fill':
                m = re.match(r'^\s*(\d+)\s*([＋－×÷])\s*(\d+)\s*＝\s*\{\}$', it['tpl'])
                if m:
                    v = OPS[m.group(2)](int(m.group(1)), int(m.group(3)))
                    if str(v) != it['b'][0]['a'][0]: err.append('%s %s: %s should be %s, file says %s' % (name, it['id'], it['tpl'], v, it['b'][0]['a'][0]))
                if it.get('work'):
                    m = re.match(r'^\s*(\d+)\s*([＋－×÷])\s*(\d+)\s*＝\s*(\d+)$', it['work']['model'])
                    if not m or OPS[m.group(2)](int(m.group(1)), int(m.group(3))) != int(m.group(4)) or m.group(4) != it['b'][0]['a'][0]: err.append('%s %s: check work.model %s' % (name, it['id'], it['work']['model']))
            if it['k'] == 'choice' and (it.get('lab') or 'ABCD').find(it['a']) not in range(len(it['opts'])): err.append('%s %s: bad answer key' % (name, it['id']))
            if it['k'] == 'kana' and strokes(it['ch']) is None: err.append('%s %s: no stroke data for %s' % (name, it['id'], it['ch']))
            if it['k'] == 'kanji':
                st = strokes(it['ch'])
                if st is None: err.append('%s %s: no stroke data for %s' % (name, it['id'], it['ch']))
                elif str(st) != str(it['st']): err.append('%s %s: %s has %d strokes, file says %s' % (name, it['id'], it['ch'], st, it['st']))
    return n
for i, d in enumerate(w['days']):
    n = check(d['wd'], d)
    if d.get('min') != 20: err.append('%s: min should be 20' % d['wd'])
    print(d['d'], d['wd'], n, 'items')
print(w['test']['d'], 'test', check('test', w['test']), 'items')
print('\n'.join(err) if err else 'OK'); sys.exit(1 if err else 0)
