#!/usr/bin/env python3
"""Temps de chaque mot d'une voix avec ElevenLabs Scribe (speech-to-text).

Usage :
  ELEVENLABS_API_KEY=... python3 scribe_words.py voix.mp3 mots.json [script.txt]

- Envoie l'audio à POST https://api.elevenlabs.io/v1/speech-to-text (model scribe_v2, français, horodatage au mot).
- Garde la réponse brute dans <mots>.scribe.json (pour ne pas repayer une transcription).
- Si script.txt est fourni : recale la transcription sur le texte exact du script (orthographe, chiffres),
  les mots du script non reconnus reçoivent un temps interpolé et sont marqués "guess": true.
Sortie : [{"word", "start", "end"}...] en secondes, même format que align_words.py.
Dépendance : requests.
"""
import difflib, json, os, re, sys, unicodedata
import requests

API = "https://api.elevenlabs.io/v1/speech-to-text"
MODEL = os.environ.get("SCRIBE_MODEL", "scribe_v2")


def transcribe(audio, keyterms=None):
    key = os.environ.get("ELEVENLABS_API_KEY")
    if not key:
        sys.exit("ELEVENLABS_API_KEY manquante")
    data = [("model_id", MODEL), ("language_code", "fr"), ("timestamps_granularity", "word"),
            ("tag_audio_events", "false"), ("diarize", "false")]
    # aide Scribe à reconnaître les noms propres et marques du script (un champ par terme)
    data += [("keyterms", k) for k in (keyterms or [])[:100]]
    try:
        with open(audio, "rb") as f:
            r = requests.post(API, headers={"xi-api-key": key}, data=data,
                              files={"file": (os.path.basename(audio), f)}, timeout=600)
    except requests.exceptions.ProxyError:
        sys.exit("api.elevenlabs.io est bloqué par le réseau de cet environnement : autoriser ce domaine, "
                 "ou lancer ce script sur une machine qui y a accès")
    if r.status_code != 200:
        sys.exit(f"Scribe {r.status_code} : {r.text[:500]}")
    return r.json()


def norm(w):
    w = unicodedata.normalize("NFD", w.lower())
    return re.sub(r"[^a-z0-9]", "", "".join(c for c in w if unicodedata.category(c) != "Mn"))


def words_from(resp):
    return [{"word": w["text"].strip(), "start": round(w["start"], 2), "end": round(w["end"], 2)}
            for w in resp.get("words", []) if w.get("type") == "word" and w["text"].strip()]


def align_to_script(heard, script_words):
    a, b = [norm(w["word"]) for w in heard], [norm(w) for w in script_words]
    out = [None] * len(script_words)
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes():
        if tag == "equal" or (tag == "replace" and i2 - i1 == j2 - j1):
            for k in range(j2 - j1):
                h = heard[i1 + k]
                out[j1 + k] = {"word": script_words[j1 + k], "start": h["start"], "end": h["end"]}
        elif tag == "replace":  # n mots entendus pour m mots écrits (« 7 » / « sept », etc.) : on répartit
            s, e = heard[i1]["start"], heard[i2 - 1]["end"]
            n = j2 - j1
            for k in range(n):
                out[j1 + k] = {"word": script_words[j1 + k], "start": round(s + (e - s) * k / n, 2),
                               "end": round(s + (e - s) * (k + 1) / n, 2), "guess": True}
    # mots du script absents de l'audio : temps interpolé entre voisins connus
    for j, v in enumerate(out):
        if v is None:
            prev = next((out[k]["end"] for k in range(j - 1, -1, -1) if out[k]), 0.0)
            nxt = next((out[k]["start"] for k in range(j + 1, len(out)) if out[k]), prev)
            out[j] = {"word": script_words[j], "start": prev, "end": max(prev, nxt), "guess": True}
    return out


if __name__ == "__main__":
    audio, dst = sys.argv[1], sys.argv[2]
    script = open(sys.argv[3], encoding="utf-8").read() if len(sys.argv) > 3 else None
    script_words = re.findall(r"[\wÀ-ÿ'’-]+", script) if script else None
    raw = dst.rsplit(".", 1)[0] + ".scribe.json"
    if os.path.exists(raw):
        resp = json.load(open(raw))
        print(f"réponse Scribe réutilisée : {raw}")
    else:
        terms = sorted({w for w in (script_words or []) if w[:1].isupper() and len(w) > 2})
        resp = transcribe(audio, terms)
        json.dump(resp, open(raw, "w"), ensure_ascii=False, indent=1)
    heard = words_from(resp)
    res = align_to_script(heard, script_words) if script_words else heard
    json.dump(res, open(dst, "w"), ensure_ascii=False, indent=1)
    g = sum(1 for w in res if w.get("guess"))
    print(f"{len(res)} mots, {g} à vérifier (guess)" if script_words else f"{len(res)} mots")
