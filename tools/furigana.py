"""Add furigana markup (｜漢字《よみ》) to child-facing Japanese text.
Usage: from furigana import ann, ann_week
Text inside 【…】 (the word a question asks about), {} blanks and existing ｜…《…》 is left untouched.
FIX holds corrections for readings the dictionary gets wrong; add to it whenever a review finds one."""
import re, pykakasi
_k = pykakasi.kakasi()
KJ = r'[一-龥々]'
FIX = {
 '｜画《が》｜目《め》': '｜画目《かくめ》', '｜日本《にっぽん》': '｜日本《にほん》', '｜牛《うし》にゅう': '｜牛《ぎゅう》にゅう',
 '｜帯《おび》｜分数《ぶんすう》': '｜帯分数《たいぶんすう》', '｜仮《かり》｜分数《ぶんすう》': '｜仮分数《かぶんすう》',
 '｜小《ちー》さ': '｜小《ちい》さ', '｜組《く》に': '｜組《くみ》に', 'にごる｜音《おと》': 'にごる｜音《おん》',
 'け｜算《さん》': 'け｜算《ざん》', 'り｜算《さん》': 'り｜算《ざん》', 'し｜算《さん》': 'し｜算《ざん》', 'き｜算《さん》': 'き｜算《ざん》',
 'には｜入《い》りません': 'には｜入《はい》りません',
 'の｜内《ない》がわ': 'の｜内《うち》がわ', '｜対《つい》': '｜対《たい》', 'の｜間《ま》に': 'の｜間《あいだ》に',
 '｜位《くらい》になった': '｜位《い》になった', '｜歳《とし》': '｜歳《さい》', '｜止《や》める': '｜止《と》める',
 '｜入《いっ》': '｜入《はい》', '｜入《い》ろう': '｜入《はい》ろう', 'が｜入《い》る': 'が｜入《はい》る',
 '2｜回《まわ》つ': '2｜回《かい》つ', 'その｜日《にち》': 'その｜日《ひ》', '10｜本《ほん》の｜指': '｜10本《じっぽん》の｜指',
 '｜目《め》ひょう': '｜目《もく》ひょう',
}
def _tok(o, h):
    segs = re.findall(KJ + r'+|[^一-龥々]+', o)
    kana = lambda sg: ''.join(chr(ord(c) - 0x60) if 'ァ' <= c <= 'ヶ' else c for c in sg)
    rx = '^' + ''.join('(.+?)' if re.match(KJ, sg) else re.escape(kana(sg)) for sg in segs) + '$'
    m = re.match(rx, h)
    if not m: return '｜%s《%s》' % (o, h)
    out, gi = [], 0
    for sg in segs:
        if re.match(KJ, sg): gi += 1; out.append('｜%s《%s》' % (sg, m.group(gi)))
        else: out.append(sg)
    return ''.join(out)
def ann(text):
    if not text or not re.search(KJ, text): return text
    out = []
    for p in re.split(r'(【[^】]*】|\{\}|｜[^《]*《[^》]*》|\n)', text):
        if not p: continue
        if p[0] in '【｜' or p in ('{}', '\n'): out.append(p); continue
        # only Japanese runs go through the dictionary; digits, symbols and spaces pass through untouched
        for q in re.split(r'([ぁ-んァ-ヶー一-龥々]+)', p):
            if not re.search(KJ, q): out.append(q); continue
            for t in _k.convert(q):
                out.append(_tok(t['orig'], t['hira']) if re.search(KJ, t['orig']) else t['orig'])
    s = ''.join(out)
    for a, b in FIX.items(): s = s.replace(a, b)
    s = re.sub(r'(?<![0-9０-９])1｜人《にん》', '｜1人《ひとり》', s)
    s = re.sub(r'(?<![0-9０-９])2｜人《にん》', '｜2人《ふたり》', s)
    s = re.sub(r'(?<![0-9０-９])｜人《にん》', '｜人《ひと》', s)
    return s
def strip(text):
    return re.sub(r'｜([^《｜]+)《[^》]+》', r'\1', text)
def ann_week(w):
    """Annotate one week document in place. English sections/items and answer keys are skipped."""
    def sec(s):
        if s.get('en'): return
        if s.get('note'): s['note'] = ann(s['note'])
        h = s.get('h') or ''
        if h:
            lead = h[0] if re.match(r'^[一二三四五六七八九十]　', h) else ''   # section number of a test
            body = h[len(lead):]
            cut = body.find('（') if '漢字（' in body else -1            # do not give away the day's kanji
            s['h'] = lead + (ann(body) if cut < 0 else ann(body[:cut]) + body[cut:])
        if s.get('passage'): s['passage'] = [ann(p) for p in s['passage']]
        for it in s.get('items', []):
            if it.get('en'): continue
            for k in ('sub', 'q', 'tpl', 'why', 'tip', 'rubric_child'):
                if it.get(k): it[k] = ann(it[k])
            if it.get('work'): it['work']['label'] = ann(it['work']['label'])
    for d in w.get('days', []):
        for s in d.get('sections', []): sec(s)
    if w.get('test'):
        for s in w['test'].get('sections', []): sec(s)
    return w
