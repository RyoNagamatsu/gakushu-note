"""Helpers for the kana phase of ぴょんぴょんノート: build the standard sections of one day from a list of kana.
Used as a library:  from kana_days import *   (run from kaede/tools)."""
import random
KANA = {  # char: (romaji, example word, English)
 'あ':('a','あり','ant'),'い':('i','いぬ','dog'),'う':('u','うみ','sea'),'え':('e','えき','station'),'お':('o','おかし','snack'),
 'か':('ka','かさ','umbrella'),'き':('ki','きつね','fox'),'く':('ku','くつ','shoes'),'け':('ke','けしごむ','eraser'),'こ':('ko','こども','child'),
 'さ':('sa','さかな','fish'),'し':('shi','しか','deer'),'す':('su','すいか','watermelon'),'せ':('se','せみ','cicada'),'そ':('so','そら','sky'),
 'た':('ta','たまご','egg'),'ち':('chi','ちず','map'),'つ':('tsu','つき','moon'),'て':('te','てがみ','letter'),'と':('to','とり','bird'),
 'な':('na','なつ','summer'),'に':('ni','にく','meat'),'ぬ':('nu','ぬの','cloth'),'ね':('ne','ねこ','cat'),'の':('no','のり','glue'),
 'は':('ha','はな','flower'),'ひ':('hi','ひと','person'),'ふ':('fu','ふね','ship'),'へ':('he','へや','room'),'ほ':('ho','ほし','star'),
 'ま':('ma','まど','window'),'み':('mi','みみ','ear'),'む':('mu','むし','bug'),'め':('me','めがね','glasses'),'も':('mo','もも','peach'),
 'や':('ya','やま','mountain'),'ゆ':('yu','ゆき','snow'),'よ':('yo','よる','night'),
 'ら':('ra','らくだ','camel'),'り':('ri','りす','squirrel'),'る':('ru','さる','monkey'),'れ':('re','れいぞうこ','fridge'),'ろ':('ro','ろうそく','candle'),
 'わ':('wa','わに','crocodile'),'を':('o (wo)','ほんを よむ','read a book'),'ん':('n','ほん','book'),
 'が':('ga','めがね','glasses'),'ぎ':('gi','かぎ','key'),'ぐ':('gu','えのぐ','paint'),'げ':('ge','ひげ','beard'),'ご':('go','ごはん','rice, meal'),
 'ざ':('za','ひざ','knee'),'じ':('ji','じかん','time'),'ず':('zu','みず','water'),'ぜ':('ze','かぜ','wind'),'ぞ':('zo','ぞう','elephant'),
 'だ':('da','だいこん','radish'),'ぢ':('ji','はなぢ','nosebleed'),'づ':('zu','つづき','the next part'),'で':('de','でんわ','phone'),'ど':('do','どうぶつ','animal'),
 'ば':('ba','ばら','rose'),'び':('bi','えび','shrimp'),'ぶ':('bu','ぶた','pig'),'べ':('be','かべ','wall'),'ぼ':('bo','ぼうし','hat'),
 'ぱ':('pa','かんぱい','cheers'),'ぴ':('pi','えんぴつ','pencil'),'ぷ':('pu','てんぷら','tempura'),'ぺ':('pe','ぺらぺら','fluent'),'ぽ':('po','たんぽぽ','dandelion'),
 'っ':('small tsu','きって','stamp'),'ゃ':('small ya','おちゃ','tea'),'ゅ':('small yu','きゅうり','cucumber'),'ょ':('small yo','きょう','today'),
}
def ro(c): return KANA[c][0].split(' ')[0]
def kana_sec(h, chars, note):
    return {"h": h, "note": note, "grid": True, "items": [{"k": "kana", "id": "k%d" % (i + 1), "ch": c, "ro": KANA[c][0], "ex": [KANA[c][1], KANA[c][2]]} for i, c in enumerate(chars)]}
def choice(i, q, opts, a): return {"k": "choice", "id": i, "q": q, "opts": opts, "a": "ABCD"[opts.index(a)], "pts": 1}
def read_items(prefix, chars, pool, rnd):
    """kana -> pick the romaji. Wrong options come from other kana in the pool with a different sound."""
    out = []
    for i, c in enumerate(chars):
        others = [ro(x) for x in pool if ro(x) != ro(c)]; rnd.shuffle(others)
        opts = [ro(c)] + list(dict.fromkeys(others))[:2]; rnd.shuffle(opts)
        out.append(choice("%s%d" % (prefix, i + 1), "【%s】" % c, opts, ro(c)))
    return out
def write_items(prefix, chars):
    return [{"k": "fill", "id": "%s%d" % (prefix, i + 1), "tpl": "%s → {}" % ro(c), "b": [{"a": [c], "w": 4}], "pts": 1} for i, c in enumerate(chars)]
def word_items(prefix, words, rnd):
    """words: [(かな, English, wrong1, wrong2)] -> read the word, pick the meaning."""
    out = []
    for i, (w, en, x1, x2) in enumerate(words):
        opts = [en, x1, x2]; rnd.shuffle(opts); out.append(choice("%s%d" % (prefix, i + 1), "【%s】" % w, opts, en))
    return out
def word_write(i, en, kana): return {"k": "fill", "id": i, "tpl": "%s → {}" % en, "b": [{"a": [kana], "w": max(3, len(kana) + 1)}], "pts": 1}
N_TRACE = "かきじゅんを 見て、なぞって、となりに かきます。\n(Watch the stroke order. Trace it, then write it in the next box.)"
N_READ = "ひらがなを 見て、おなじ おとを えらびます。\n(Look at the hiragana and choose its sound.)"
N_WRITE = "おとを 見て、ひらがなで かきます。\n(Read the sound and write it in hiragana.)"
N_WORD = "ことばを よんで、いみを えらびます。さいごの 1つは、ひらがなで かきます。\n(Read the word and choose what it means. Write the last one in hiragana.)"
N_REV = "まえに ならった 字です。おなじ おとを えらびます。\n(Letters from before. Choose the sound.)"
