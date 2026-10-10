#!/usr/bin/env python3
"""Nettoie une voix brute : hésitations, mots de remplissage, faux départs et prises ratées.

1) Repérer ce qu'il faut enlever :
   python3 clean_voice.py suggest brut.scribe.json
   -> la transcription avec, entre [ ], les mots de remplissage, les phrases coupées (« -- », « ... »)
      et les passages répétés (une même suite de 4 mots ou plus dite deux fois : on garde la DERNIÈRE prise).
2) Écrire script_propre.txt : ce qui doit rester, mot pour mot comme dit (ne rien reformuler ;
   corriger seulement l'orthographe des noms : « Cloud Code » -> « Claude Code »).
3) Couper :
   python3 clean_voice.py cut brut.scribe.json voix_brute.mp3 script_propre.txt sortie/
   -> sortie/voix.mp3 (coupes avec fondus de 15 ms, pause gardée ≤ 0,25 s), sortie/mots.json (temps recalés
      sur l'audio coupé, mots du script), sortie/coupes.json (ce qui a été retiré, pour vérification).
Dépendances : ffmpeg, Python standard.
"""
import difflib, json, os, re, subprocess, sys, unicodedata

FILLERS = {"euh", "heu", "hum", "hmm", "bah", "ben", "bon", "hein", "voila", "genre", "enfin", "quoi", "tsais", "ouais"}
PAUSE_KEEP, PAD_IN, PAD_OUT, FADE = 0.25, 0.04, 0.08, 0.015


def norm(w):
    w = unicodedata.normalize("NFD", w.lower())
    return re.sub(r"[^a-z0-9]", "", "".join(c for c in w if unicodedata.category(c) != "Mn"))


def heard_words(raw):
    out = []
    for w in raw["words"]:
        if w.get("type") == "word" and w["text"].strip():
            out.append({"text": w["text"].strip(), "start": w["start"], "end": w["end"]})
    return out


def suggest(raw):
    hw = heard_words(raw)
    n = [norm(w["text"]) for w in hw]
    mark = [""] * len(hw)
    for i, w in enumerate(hw):
        if n[i] in FILLERS: mark[i] = "remplissage"
        if w["text"].endswith(("--", "…", "...")) or w["text"].endswith("-"): mark[i] = "coupé"
    K = 4  # suites répétées : la première occurrence est une prise ratée probable
    seen = {}
    for i in range(len(n) - K + 1):
        key = tuple(n[i:i + K])
        if key in seen and i - seen[key] < 80:
            for j in range(seen[key], seen[key] + K):
                mark[j] = mark[j] or "répété"
        seen[key] = i
    out, cur = [], None
    for w, m in zip(hw, mark):
        if m != cur:
            if cur: out.append("]")
            if m: out.append(f"[{m}:")
            cur = m
        out.append(w["text"])
    if cur: out.append("]")
    print(" ".join(out))


def align(hw, script_words):
    """Pour chaque mot du script : l'index du mot entendu correspondant (ou None)."""
    a, b = [norm(w["text"]) for w in hw], [norm(w) for w in script_words]
    m = [None] * len(b)
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes():
        if tag == "equal" or (tag == "replace" and i2 - i1 == j2 - j1):
            for k in range(j2 - j1): m[j1 + k] = [i1 + k, i1 + k]
        elif tag == "replace":  # fusions (« Nana Pay » -> « NanaPay ») puis répartition
            i = i1
            for j in range(j1, j2):
                if i >= i2: break
                acc, k = a[i], i
                while acc != b[j] and k + 1 < i2 and len(acc) < len(b[j]): k += 1; acc += a[k]
                if acc == b[j]: m[j] = [i, k]; i = k + 1
                elif j2 - j1 < i2 - i1: m[j] = [i, i]; i += 1
                else: m[j] = [i, min(i, i2 - 1)]; i += 1 if j - j1 < i2 - i1 - 1 else 0
    return m


def cut(raw_path, audio, script_path, out_dir):
    raw = json.load(open(raw_path)); hw = heard_words(raw)
    sw = re.findall(r"[\wÀ-ÿ'’-]+", open(script_path, encoding="utf-8").read())
    m = align(hw, sw)
    keep = sorted({i for r in m if r for i in range(r[0], r[1] + 1)})
    # segments continus d'audio : mots gardés consécutifs dans l'entendu
    segs, start = [], None
    for k, i in enumerate(keep):
        if start is None: start = i
        if k + 1 == len(keep) or keep[k + 1] != i + 1:
            segs.append([start, i]); start = None
    spans = [[max(0, hw[a]["start"] - PAD_IN), hw[b]["end"] + PAD_OUT] for a, b in segs]
    # entre deux segments, garder au plus PAUSE_KEEP de silence ; supprimer tout trou entendu
    os.makedirs(out_dir, exist_ok=True)
    parts, filt, t_new, offsets = [], [], 0.0, []
    for k, (s, e) in enumerate(spans):
        if k: t_new += min(PAUSE_KEEP, max(0.0, s - spans[k - 1][1])) * 0  # les pauses naturelles restent dans les segments
        offsets.append((s, e, t_new))
        d = e - s
        filt.append(f"[0:a]atrim={s:.3f}:{e:.3f},asetpts=PTS-STARTPTS,afade=t=in:d={FADE},afade=t=out:st={max(0, d - FADE):.3f}:d={FADE}[s{k}]")
        parts.append(f"[s{k}]"); t_new += d
    filt.append("".join(parts) + f"concat=n={len(spans)}:v=0:a=1[out]")
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", audio, "-filter_complex", ";".join(filt),
                    "-map", "[out]", "-ar", "48000", "-b:a", "192k", f"{out_dir}/voix.mp3"], check=True)

    def remap(t):
        for s, e, o in offsets:
            if s - 1e-6 <= t <= e + 1e-6: return round(o + (t - s), 2)
        return None
    words = []
    for j, w in enumerate(sw):
        if m[j]:
            a, b = m[j]
            words.append({"word": w, "start": remap(hw[a]["start"]), "end": remap(hw[b]["end"])})
        else:
            words.append({"word": w, "start": None, "end": None, "guess": True})
    for j, w in enumerate(words):  # mots non entendus : temps du voisin
        if w["start"] is None:
            prev = next((words[k]["end"] for k in range(j - 1, -1, -1) if words[k]["end"] is not None), 0.0)
            w["start"] = w["end"] = prev
    json.dump(words, open(f"{out_dir}/mots.json", "w"), ensure_ascii=False, indent=1)
    removed, prev = [], -1
    for a, b in segs:
        if a > prev + 1: removed.append(" ".join(x["text"] for x in hw[prev + 1:a]))
        prev = b
    if prev + 1 < len(hw): removed.append(" ".join(x["text"] for x in hw[prev + 1:]))
    json.dump({"retire": removed, "segments": [[round(s, 2), round(e, 2)] for s, e in spans],
               "duree": round(t_new, 2)}, open(f"{out_dir}/coupes.json", "w"), ensure_ascii=False, indent=1)
    print(f"{len(spans)} segments, {len(removed)} passages retirés, voix nettoyée : {t_new:.1f} s")
    for r in removed: print("  retiré :", r)


if __name__ == "__main__":
    if sys.argv[1] == "suggest": suggest(json.load(open(sys.argv[2])))
    elif sys.argv[1] == "cut": cut(*sys.argv[2:6])
    else: sys.exit(__doc__)
