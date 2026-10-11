"""Example only: how weeks 1 and 2 (hiragana from the basics) were generated on 2026-10-11. It rewrote those two files in place, reusing their sums. Do not re-run it; copy the pattern for new weeks."""
import json,random,sys,copy,os
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from kana_days import *
R=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','weeks','')
def math_sec(old_day,h,note_en):
    sec=next(s for s in old_day['sections'] if 'さんすう' in s['h'])
    cs=[it for it in sec['items'] if it.get('k')=='fill' and it['id'][0]=='c' and it['id'][1:].isdigit() and it['b'][0].get('t')=='num' and '×' in it['tpl'] or (it.get('k')=='fill' and it['id'][0]=='c' and ('－' in it['tpl'] or '＋' in it['tpl']))][:10]
    for n,it in enumerate(cs):it['id']='c%d'%(n+1)
    return {"h":h,"note":note_en,"items":cs}
def day(old,chars,words,ww,math_note,rev=None,pool=None,rnd=None,extra=None):
    secs=[kana_sec('ひらがな（%d字） Hiragana'%len(chars),chars,N_TRACE)]
    if rev:secs.append({"h":"ふくしゅう Review","note":N_REV,"items":read_items('f',rev,rev+chars,rnd)})
    pick=chars[:]; rnd.shuffle(pick)
    secs.append({"h":"よめるかな Reading","note":N_READ,"items":read_items('y',pick[:5],pool or chars,rnd)})
    pick2=[c for c in chars if c not in pick[:5]] or chars[:]; rnd.shuffle(pick2)
    secs.append({"h":"かけるかな Writing","note":N_WRITE,"items":write_items('w',(pick2+pick)[:5])})
    secs.append({"h":"ことば Words","note":N_WORD,"items":word_items('t',words,rnd)+[word_write('t9',*ww)]})
    if extra:secs+=extra
    secs.append(math_sec(old,'さんすう Math',math_note))
    for n,s in enumerate(secs):s['h']='一二三四五六七'[n]+'　'+s['h']
    return secs
# ---------------- week 1: Tuesday to Friday and the Saturday test ----------------
w=json.load(open(R+'2026-10-12.json',encoding='utf8'));old=copy.deepcopy(w);rnd=random.Random(1012)
AK=list('あいうえおかきくけこ');ST=list('さしすせそたちつてと');NH=list('なにぬねのはひふへほ');MY=list('まみむめもやゆよ')
w['days'][1]['sections']=day(old['days'][1],AK,[('あか','red','blue','big'),('かお','face','hand','foot'),('えき','station','school','park'),('いえ','house','tree','car')],('blue','あお'),
 "ひけない ときは、十の くらいから 10を かります。5の だんは 5ずつ ふえます。\n(Subtract. Borrow 10 from the tens when you need to. Then the 5 times table: 5, 10, 15, 20 ...)",rnd=rnd)
w['days'][2]['sections']=day(old['days'][2],ST,[('いす','chair','desk','door'),('つき','moon','sun','star'),('くつ','shoes','hat','bag'),('うし','cow','horse','pig')],('octopus','たこ'),
 "くり下がりの ひきざんと、2の だん。2の だんは 2ずつ ふえます。\n(Subtract with borrowing. Then the 2 times table: 2, 4, 6, 8 ...)",rev=AK[:4]+AK[6:8],rnd=rnd)
w['days'][3]['sections']=day(old['days'][3],NH,[('ねこ','cat','bird','fish'),('はな','flower','tree','grass'),('ほし','star','moon','cloud'),('さかな','fish','meat','egg')],('dog','いぬ'),
 "2の だんの つづきと、ふくしゅう。\n(More of the 2 times table, and some review.)",rev=ST[:3]+ST[6:9],rnd=rnd)
w['days'][4]['sections']=day(old['days'][4],MY,[('やま','mountain','river','sea'),('ゆき','snow','rain','wind'),('みみ','ear','eye','nose'),('あめ','rain','snow','sun')],('peach','もも'),
 "なん十の けいさんは、10の まとまりで かんがえます。30＋40 は、10が 7こで 70。\n(Tens: 30 + 40 is 7 tens, so 70. Then review.)",rev=NH[:3]+NH[5:8],rnd=rnd)
for d in w['days'][1:]:d['min']=20
ALL1=AK+ST+NH+MY;t=rnd.sample(ALL1,10);t2=rnd.sample([c for c in ALL1 if c not in t],10)
calc=[it for s in old['test']['sections'] for it in s['items'] if it.get('k')=='fill' and it['id'][0]=='c']+[it for s in old['test']['sections'] for it in s['items'] if it.get('scratch')]
w['test']={"d":"2026-10-17","min":20,"sections":[
 {"h":"一　よめるかな Reading（1もん1点）","note":N_READ,"items":read_items('y',t,ALL1,rnd)},
 {"h":"二　かけるかな Writing（1もん1点）","note":N_WRITE,"items":write_items('w',t2)},
 {"h":"三　ことば Words（1もん1点）","note":"ことばを よんで、いみを えらびます。\n(Read the word and choose what it means.)","items":word_items('t',[('いぬ','dog','cat','cow'),('かさ','umbrella','shoes','hat'),('そと','outside','inside','under'),('ふね','ship','car','train'),('よる','night','morning','noon')],rnd)},
 {"h":"四　けいさん Math（1もん1点）","note":"けいさんを しましょう。\n(Work out the answers.)","items":calc}]}
json.dump(w,open(R+'2026-10-12.json','w',encoding='utf8'),ensure_ascii=False,separators=(',',':'))
# ---------------- week 2 ----------------
w=json.load(open(R+'2026-10-19.json',encoding='utf8'));old=copy.deepcopy(w);rnd=random.Random(1019)
RW=list('らりるれろわをん');GZ=list('がぎぐげござじずぜぞ');DBP=list('だぢづでどばびぶべぼぱぴぷぺぽ')
w['days'][0]['sections']=day(old['days'][0],RW,[('くるま','car','bus','train'),('ほん','book','pen','paper'),('そら','sky','sea','ground'),('さる','monkey','bear','deer')],('river','かわ'),
 "3の だんは、3ずつ ふえます。3、6、9、12、15。\n(The 3 times table: 3, 6, 9, 12, 15 ...)",rev=MY[:3]+MY[5:8],pool=RW+MY,rnd=rnd)
w['days'][1]['sections']=day(old['days'][1],GZ,[('みず','water','fire','wind'),('かぜ','wind','rain','cloud'),('ぞう','elephant','giraffe','lion'),('かぎ','key','door','window')],('glasses','めがね'),
 "3の だんの つづき：18、21、24、27。\n(More of the 3 times table: 18, 21, 24, 27.)",rev=RW[:6],rnd=rnd)
w['days'][1]['sections'][0]['note']="てんてん「゛」が つくと、おとが かわります。か (ka) → が (ga)、さ (sa) → ざ (za)。\n(Two little dots change the sound: ka → ga, sa → za.)\n"+N_TRACE
w['days'][2]['sections']=day(old['days'][2],DBP,[('ぶた','pig','cow','horse'),('えび','shrimp','crab','fish'),('でんわ','phone','clock','TV'),('ぼうし','hat','shoes','coat')],('pencil','えんぴつ'),
 "4の だんは、4ずつ ふえます。4、8、12、16、20。\n(The 4 times table: 4, 8, 12, 16, 20 ...)",rev=GZ[:3]+GZ[5:8],rnd=rnd)
w['days'][2]['sections'][0]['note']="は (ha) に てんてんで ば (ba)、まる「゜」で ぱ (pa)。「ぢ」は ji、「づ」は zu と よみます。\n(ha → ba with dots, → pa with a little circle. ぢ sounds like ji and づ like zu.)\n"+N_TRACE
# Thursday: small っ and long vowels
th=old['days'][3]
w['days'][3]['sections']=[
 kana_sec('ひらがな：小さい「っ」 Small tsu',['っ'],"小さい「っ」は、つぎの おとの まえで、いきを 1つ とめます。ねこ (neko) は cat、ねっこ (nekko) は root。\n(A small っ makes a tiny stop before the next sound: neko = cat, nekko = root.)\n"+N_TRACE),
 {"h":"ふくしゅう Review","note":N_REV,"items":read_items('f',DBP[0:2]+DBP[5:7]+DBP[10:12],DBP,rnd)},
 {"h":"小さい「っ」の ことば Words with small tsu","note":"ことばを よんで、いみを えらびます。\n(Read the word and choose what it means.)","items":word_items('t',[('きって','stamp','ticket','cut'),('がっこう','school','hospital','station'),('ねっこ','root','cat','leaf'),('きっぷ','ticket','stamp','cup')],rnd)+
   [{"k":"fill","id":"t8","tpl":"gakkou (school) → {}","b":[{"a":["がっこう"],"w":6}],"pts":1},{"k":"fill","id":"t9","tpl":"kitte (stamp) → {}","b":[{"a":["きって"],"w":5}],"pts":1}]},
 {"h":"のばす おと Long sounds","note":"のばす おとは、あ・い・う・え・お を かいて のばします。おかあさん (okaasan)、おにいさん (oniisan)、くうき (kuuki)、おねえさん (oneesan)、おとうさん (otousan)。\n(Long sounds are written with an extra あ い う え お.)","items":word_items('n',[('おかあさん','mother','father','sister'),('おとうさん','father','mother','brother'),('せんせい','teacher','student','doctor'),('とけい','clock','desk','chair')],rnd)+
   [{"k":"fill","id":"n8","tpl":"okaasan (mother) → {}","b":[{"a":["おかあさん"],"w":7}],"pts":1},{"k":"fill","id":"n9","tpl":"otousan (father) → {}","b":[{"a":["おとうさん"],"w":7}],"pts":1}]},
 math_sec(th,'さんすう Math',"4の だんの つづき：24、28、32、36。\n(More of the 4 times table: 24, 28, 32, 36.)")]
# Friday: small ゃ ゅ ょ
fr=old['days'][4]
def yo(i,k,a,x1,x2):
    o=[a,x1,x2];rnd.shuffle(o);return choice(i,'【%s】'%k,o,a)
w['days'][4]['sections']=[
 kana_sec('ひらがな：小さい「ゃ・ゅ・ょ」 Small ya, yu, yo',['ゃ','ゅ','ょ'],"小さい「ゃ・ゅ・ょ」は、まえの 字と くっついて 1つの おとに なります。き＋ゃ＝きゃ (kya)、し＋ゅ＝しゅ (shu)、ち＋ょ＝ちょ (cho)。\n(A small ゃ ゅ ょ joins the letter before it to make one sound: kya, shu, cho.)\n"+N_TRACE),
 {"h":"よめるかな Reading","note":"2つの 字で 1つの おとです。おなじ おとを えらびます。\n(Two letters, one sound. Choose the sound.)","items":[yo('y1','きゃ','kya','kiya','ka'),yo('y2','しゅ','shu','shiyu','su'),yo('y3','ちょ','cho','chiyo','to'),yo('y4','にゃ','nya','niya','na'),yo('y5','りょ','ryo','riyo','ro'),yo('y6','じゃ','ja','jiya','za')]},
 {"h":"かけるかな Writing","note":"おとを 見て、ひらがな 2字で かきます。\n(Write the sound with two hiragana.)","items":[{"k":"fill","id":"w%d"%(i+1),"tpl":"%s → {}"%r,"b":[{"a":[k],"w":5}],"pts":1} for i,(r,k) in enumerate([('sha','しゃ'),('kyu','きゅ'),('cho','ちょ'),('gyu','ぎゅ'),('hyo','ひょ')])]},
 {"h":"ことば Words","note":N_WORD,"items":word_items('t',[('おちゃ','tea','water','milk'),('きんぎょ','goldfish','bird','rabbit'),('じてんしゃ','bicycle','car','train'),('ぎゅうにゅう','milk','juice','tea'),('びょういん','hospital','school','station')],rnd)+[word_write('t9','tea','おちゃ')]},
 math_sec(fr,'さんすう Math',"3の だんと 4の だんの まとめ。こえに 出して いいながら かきましょう。\n(Review of the 3 and 4 times tables. Say them out loud as you write.)")]
for d in w['days']:
    for n,s in enumerate(d['sections']):
        s['h']=('一二三四五六七'[n]+'　'+s['h'].split('　',1)[-1]) if s['h'][0] in '一二三四五六七' and '　' in s['h'][:3] else '一二三四五六七'[n]+'　'+s['h']
ALL2=list('あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよ')+RW+GZ+DBP
t=rnd.sample(RW[:6]+GZ+DBP,10);t2=rnd.sample([c for c in ALL2 if c not in t and c not in 'ぢづを'],10)
calc=[it for s in old['test']['sections'] for it in s['items'] if it.get('k')=='fill' and it['id'][0]=='c']+[it for s in old['test']['sections'] for it in s['items'] if it.get('scratch')]
w['test']={"d":"2026-10-24","min":20,"sections":[
 {"h":"一　よめるかな Reading（1もん1点）","note":N_READ,"items":read_items('y',t,RW+GZ+DBP,rnd)},
 {"h":"二　かけるかな Writing（1もん1点）","note":N_WRITE,"items":write_items('w',t2)},
 {"h":"三　ことば Words（1もん1点）","note":"ことばを よんで、いみを えらびます。\n(Read the word and choose what it means.)","items":word_items('t',[('がっこう','school','hospital','park'),('おちゃ','tea','milk','water'),('みず','water','tea','fire'),('ぼうし','hat','shoes','bag'),('おかあさん','mother','father','teacher'),('じてんしゃ','bicycle','bus','ship')],rnd)},
 {"h":"四　けいさん Math（1もん1点）","note":"けいさんを しましょう。\n(Work out the answers.)","items":calc}]}
json.dump(w,open(R+'2026-10-19.json','w',encoding='utf8'),ensure_ascii=False,separators=(',',':'))
