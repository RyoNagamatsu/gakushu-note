"""Example only: how week 2 was rebuilt on 2026-10-12 with pictures instead of romaji. Do not re-run it; copy the pattern."""
import json,sys,copy
import os;sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from kana_days import *
P=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','weeks','2026-10-19.json')
w=json.load(open(P,encoding='utf8'));old=copy.deepcopy(w)
def math(d):
    s=copy.deepcopy(next(s for s in old['days'][d]['sections'] if 'さんすう' in s['h'] or 'Math' in s['h']));s['h']='さんすう Math';return s
def num(secs):
    for i,s in enumerate(secs):s['h']='一二三四五六七'[i]+'　'+s['h']
    return secs
REV="まえに ならった 字の ことばです。えを 見て、あう ことばを えらびます。\n(Words from before. Look at the picture and choose the word.)"
def rev(rows):return {"h":"ふくしゅう Review","note":REV,"items":[pick_word('f%d'%(i+1),*r,order=i) for i,r in enumerate(rows)]}
def miss(rows):return {"h":"かけるかな Writing","note":N_MISS,"items":[missing('w%d'%(i+1),*r) for i,r in enumerate(rows)]}
def words(rows,ww):return {"h":"ことば Words","note":N_WORDS,"items":[pick_pic('t%d'%(i+1),*r,order=i+1) for i,r in enumerate(rows)]+[write_word('t9',*ww)]}
D=w['days']
D[0]['sections']=num([kana_sec('ひらがな（8字） Hiragana',[('ら','らくだ','🐫'),('り','りす','🐿️'),('る','さる','🐒'),('れ','れっしゃ','🚆'),('ろ','ろうそく','🕯️'),('わ','わに','🐊'),('を','ほんを よむ','📖'),('ん','ほん','📕')],N_TRACE),
 rev([('🍑','もも','まめ','むし'),('⛰️','やま','ゆき','よる'),('👓','めがね','まど','みみ'),('⛄','ゆき','やま','もも'),('🐛','むし','みみ','まめ'),('👂','みみ','むし','もも')]),
 miss([('🐫','','ら','くだ'),('🐿️','','り','す'),('🐒','さ','る',''),('🐊','','わ','に'),('📕','ほ','ん','')]),
 words([('くるま','🚗','🚲','🚢'),('かわ','🏞️','⛰️','🏠'),('とり','🐦','🐟','🐶'),('ほし','⭐','🌙','☀️')],('🍑','もも')),math(0)])
D[1]['sections']=num([kana_sec('ひらがな（10字） Hiragana',[('が','めがね','👓'),('ぎ','かぎ','🔑'),('ぐ','どんぐり','🌰'),('げ','ひげ','🧔'),('ご','ごはん','🍚'),('ざ','ざりがに','🦞'),('じ','にじ','🌈'),('ず','みず','💧'),('ぜ','かぜ','🌬️'),('ぞ','ぞう','🐘')],
  "てんてん「゛」が つくと、おとが かわります。か → が、さ → ざ。\n(Two little dots change the sound of a letter.)\n"+N_TRACE),
 rev([('🐫','らくだ','りす','わに'),('🐿️','りす','さる','わに'),('🐊','わに','らくだ','さる'),('🕯️','ろうそく','れっしゃ','ほん'),('🚆','れっしゃ','ろうそく','りす'),('📕','ほん','さる','わに')]),
 miss([('🔑','か','ぎ',''),('🍚','','ご','はん'),('🌈','に','じ',''),('💧','み','ず',''),('🐘','','ぞ','う')]),
 words([('みず','💧','🔥','🌬️'),('かぜ','🌬️','💧','☀️'),('ぞう','🐘','🦒','🦁'),('かぎ','🔑','🚪','🪟')],('👓','めがね')),math(1)])
D[2]['sections']=num([kana_sec('ひらがな（15字） Hiragana',[('だ','だんご','🍡'),('ぢ','はなぢ','👃'),('づ','こづつみ','📦'),('で','でんわ','☎️'),('ど','まど','🪟'),('ば','ばら','🌹'),('び','えび','🦐'),('ぶ','ぶた','🐷'),('べ','べんとう','🍱'),('ぼ','ぼうし','🧢'),('ぱ','かんぱい','🥂'),('ぴ','えんぴつ','✏️'),('ぷ','てんぷら','🍤'),('ぺ','ぺろぺろ','👅'),('ぽ','たんぽぽ','🌼')],
  "は に てんてんで ば、まる「゜」で ぱ。「ぢ」「づ」は あまり つかいません。\n(Two little dots or a little circle change the sound. ぢ and づ are rare.)\n"+N_TRACE),
 rev([('🔑','かぎ','かぜ','ぞう'),('🐘','ぞう','みず','にじ'),('🌈','にじ','ひげ','ごはん'),('💧','みず','かぜ','かぎ'),('🍚','ごはん','ひげ','めがね'),('🧔','ひげ','にじ','ぞう')]),
 miss([('🐷','','ぶ','た'),('🦐','え','び',''),('☎️','','で','んわ'),('🧢','','ぼ','うし'),('✏️','えん','ぴ','つ')]),
 words([('ぶた','🐷','🐮','🐴'),('えび','🦐','🦀','🐟'),('でんわ','☎️','⏰','📺'),('ぼうし','🧢','👟','👜')],('🍡','だんご')),math(2)])
D[3]['sections']=num([kana_sec('ひらがな：小さい「っ」 Small っ',[('っ','きっぷ','🎫')],"小さい「っ」は、つぎの おとの まえで、いきを 1つ とめます。ねこ と ねっこ は べつの ことばです。\n(A small っ makes a tiny stop: ねこ is a cat, ねっこ is a root.)\n"+N_TRACE),
 rev([('🐷','ぶた','えび','ばら'),('🦐','えび','ぶた','だんご'),('🌹','ばら','ぼうし','たんぽぽ'),('🍱','べんとう','でんわ','えんぴつ'),('🌼','たんぽぽ','てんぷら','ばら'),('🍤','てんぷら','べんとう','だんご')]),
 {"h":"小さい「っ」の ことば Words with っ","note":"ことばを よんで、あう えを えらびます。さいごの 2つは、えを 見て ことばを かきます。\n(Read the word and choose the picture. Then write the words.)","items":[pick_pic('t%d'%(i+1),*r,order=i) for i,r in enumerate([('きっぷ','🎫','✉️','📦'),('がっこう','🏫','🏥','🏠'),('らっぱ','🎺','🥁','🎸'),('はっぱ','🍃','🌸','🌰')])]+[write_word('t8','🏫','がっこう'),write_word('t9','🎺','らっぱ')]},
 {"h":"のばす おと Long sounds","note":"のばす おとは、あ・い・う・え・お を かいて のばします。おかあさん、おにいさん、くうき、おねえさん、おとうさん。\n(A long sound is written with an extra あ, い, う, え or お.)","items":[pick_pic('n%d'%(i+1),*r,order=i+2) for i,r in enumerate([('おかあさん','👩','👨','👧'),('おとうさん','👨','👩','👦'),('せんせい','🧑‍🏫','👮','🧑‍🍳'),('とけい','⏰','📺','📱')])]+[write_word('n8','👨','おとうさん'),write_word('n9','👩','おかあさん')]},math(3)])
D[4]['sections']=num([kana_sec('ひらがな：小さい「ゃ・ゅ・ょ」 Small ゃ ゅ ょ',[('ゃ','おちゃ','🍵'),('ゅ','きゅうり','🥒'),('ょ','きょうりゅう','🦕')],"小さい「ゃ・ゅ・ょ」は、まえの 字と くっついて 1つの おとに なります。き＋ゃ＝きゃ、し＋ゅ＝しゅ、ち＋ょ＝ちょ。\n(A small ゃ, ゅ or ょ joins the letter before it to make one sound.)\n"+N_TRACE),
 {"h":"かけるかな Writing","note":"えを 見て、ぬけて いる 2つの 字を かきます。\n(Look at the picture. Write the two missing letters.)","items":[missing('w%d'%(i+1),*r) for i,r in enumerate([('🍵','お','ちゃ',''),('🥒','','きゅ','うり'),('🦕','','きょ','うりゅう'),('🚲','じてん','しゃ',''),('🐠','きん','ぎょ','')])]},
 words([('おちゃ','🍵','🥛','🧃'),('きんぎょ','🐠','🐦','🐰'),('じてんしゃ','🚲','🚗','🚆'),('ぎゅうにゅう','🥛','🍵','🧃'),('びょういん','🏥','🏫','🏠')],('🍵','おちゃ')),math(4)])
for d in D:d['min']=20
calc=[s for s in old['test']['sections'] if 'けいさん' in s['h'] or 'Math' in s['h']][0]
w['test']['sections']=num([
 {"h":"どれかな Reading（1もん1点）","note":N_PICK,"items":[pick_word('y%d'%(i+1),*r,order=i) for i,r in enumerate([('🐫','らくだ','りす','わに'),('🔑','かぎ','かぜ','ぞう'),('🐘','ぞう','ぶた','えび'),('🌈','にじ','ひげ','みず'),('🐷','ぶた','えび','ばら'),('✏️','えんぴつ','てんぷら','べんとう'),('🎫','きっぷ','がっこう','らっぱ'),('🏫','がっこう','きっぷ','はっぱ'),('🍵','おちゃ','きんぎょ','おかし'),('🚲','じてんしゃ','でんわ','ぼうし')])]},
 {"h":"かけるかな Writing（1もん1点）","note":N_MISS,"items":[missing('w%d'%(i+1),*r) for i,r in enumerate([('🐊','','わ','に'),('📕','ほ','ん',''),('💧','み','ず',''),('🍚','','ご','はん'),('🦐','え','び',''),('🧢','','ぼ','うし'),('🍤','てん','ぷ','ら'),('🎺','ら','っ','ぱ'),('🥒','','きゅ','うり'),('🐠','きん','ぎょ','')])]},
 {"h":"ことば Words（1もん1点）","note":"えを 見て、ことばを ぜんぶ かきます。\n(Look at the picture and write the whole word.)","items":[write_word('t%d'%(i+1),*r) for i,r in enumerate([('🐘','ぞう'),('🐷','ぶた'),('👨','おとうさん'),('🍵','おちゃ')])]},
 dict(calc,h=calc['h'].split('　',1)[1])])
json.dump(w,open(P,'w',encoding='utf8'),ensure_ascii=False,separators=(',',':'))
