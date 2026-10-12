"""Helpers for the kana phase of ぴょんぴょんノート (used as a library from kaede/tools).
No romaji anywhere: she learns English first, and alphabet -> kana confuses her (parent, 2026-10-12).
Sounds are taught with words and pictures (emoji) instead."""
def kana(i, ch, word, pic):
    """one letter: stroke-order model, an example word with a picture, then trace and write"""
    return {"k": "kana", "id": i, "ch": ch, "ro": "", "ex": [word, pic]}
def kana_sec(h, letters, note):
    """letters: [(ch, word, pic)]"""
    return {"h": h, "note": note, "grid": True, "items": [kana("k%d" % (n + 1), *x) for n, x in enumerate(letters)]}
def choice(i, q, opts, a):
    return {"k": "choice", "id": i, "q": q, "opts": opts, "a": "ABCD"[opts.index(a)], "pts": 1}
def pick_word(i, pic, right, wrong1, wrong2, order=0):
    """picture -> choose the word (reading)"""
    o = [right, wrong1, wrong2]; o = o[order % 3:] + o[:order % 3]
    return choice(i, pic, o, right)
def pick_pic(i, word, right, wrong1, wrong2, order=0):
    """word -> choose the picture (reading for meaning)"""
    o = [right, wrong1, wrong2]; o = o[order % 3:] + o[:order % 3]
    return choice(i, "【%s】" % word, o, right)
def missing(i, pic, before, ans, after):
    """picture + the word with one letter left out: write the missing letter(s)"""
    return {"k": "fill", "id": i, "tpl": "%s　%s{}%s" % (pic, before, after), "b": [{"a": [ans], "w": max(4, 2 * len(ans) + 2)}], "pts": 1}
def write_word(i, pic, word):
    """picture -> write the whole word"""
    return {"k": "fill", "id": i, "tpl": "%s → {}" % pic, "b": [{"a": [word], "w": max(4, len(word) + 2)}], "pts": 1}
N_TRACE = "かきじゅんを 見て、なぞって、となりに かきます。\n(Watch the stroke order. Trace it, then write it in the next box.)"
N_PICK = "えを 見て、あう ことばを えらびます。\n(Look at the picture and choose the word.)"
N_MISS = "えを 見て、ぬけて いる 字を かきます。\n(Look at the picture. Write the missing letter.)"
N_WORDS = "ことばを よんで、あう えを えらびます。さいごは、えを 見て ことばを ぜんぶ かきます。\n(Read the word and choose the picture. For the last one, write the whole word.)"
