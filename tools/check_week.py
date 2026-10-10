"""Check a week file before publishing.  python3 tools/check_week.py weeks/2026-10-12.json"""
import json, sys, re, datetime
w = json.load(open(sys.argv[1], encoding='utf8')); err = []
def items(secs): return [it for s in secs for it in s.get('items', []) if it.get('k')]
mon = datetime.date.fromisoformat(w['id'])
if mon.weekday() != 0: err.append('id is not a Monday')
if len(w.get('days', [])) != 5: err.append('need 5 days')
for i, d in enumerate(w.get('days', [])):
    if d['d'] != (mon + datetime.timedelta(days=i)).isoformat() or d['wd'] != '月火水木金'[i]: err.append('day %d date/wd wrong' % i)
    ids = [it['id'] for it in items(d['sections'])]
    if len(ids) != len(set(ids)): err.append('duplicate ids on ' + d['d'])
    if any(it.get('pts') for it in items(d['sections'])): err.append('homework items must have pts 0 on ' + d['d'])
t = w.get('test')
if not t: err.append('no test')
else:
    if t['d'] != (mon + datetime.timedelta(days=5)).isoformat(): err.append('test date must be Saturday')
    ids = [it['id'] for it in items(t['sections'])]
    if len(ids) != len(set(ids)): err.append('duplicate ids in test')
    tot = 0
    for it in items(t['sections']):
        if it['k'] == 'fill': tot += it['pts'] * (len(it['b']) if it.get('each') else 1) + (it.get('work') or {}).get('pts', 0)
        else: tot += it.get('pts', 0)
    if tot != 50: err.append('test total is %d, must be 50' % tot)
for it in items([s for d in w.get('days', []) for s in d['sections']] + (t or {}).get('sections', [])):
    if it['k'] == 'fill' and it['tpl'].count('{}') != len(it['b']): err.append('blank count mismatch: ' + it['id'])
    if it['k'] == 'choice' and it['a'] not in (it.get('lab') or 'ABCD')[:len(it['opts'])]: err.append('choice answer out of range: ' + it['id'])
    if it['k'] == 'kanji' and not all(k in it for k in ('ch', 'st', 'ex', 'rq', 'wq')): err.append('kanji fields missing: ' + it['id'])
    # simple arithmetic check for plain expressions
    if it['k'] == 'fill' and len(it['b']) == 1 and re.fullmatch(r'[0-9０-９\s＋－×÷（）+\-.]+＝\s*\{\}', it['tpl']):
        e = it['tpl'].split('＝')[0].replace('＋', '+').replace('－', '-').replace('×', '*').replace('÷', '/').replace('（', '(').replace('）', ')')
        try:
            if abs(eval(e) - float(it['b'][0]['a'][0])) > 1e-9: err.append('wrong answer: %s' % it['tpl'])
        except Exception: pass
print('OK' if not err else '\n'.join(err)); sys.exit(1 if err else 0)
