#!/usr/bin/env python3
"""Vérifie un storyboard abdoul.dev avant rendu. Usage : python3 check_storyboard.py storyboard.json
Code de sortie 1 s'il y a au moins une ERREUR (le rendu est bloqué). Les ALERTES n'empêchent pas le rendu."""
import json, re, sys

POSES = set("""point explain count present thumbs_up thumbs_down arms_crossed facepalm shrug think idea arms_up
stop whisper wave hands_heart money empty_pockets stopwatch laptop phone chart_up shocked angry laugh sad
star_eyes heart_eyes skeptical mind_blown""".split()) | {f"count_{i}" for i in range(1, 11)}
# composants avec lesquels le personnage peut partager l'écran
WITH_AVATAR = {"Sticker", "Caption", "PunchTitle", "BigNumber", "Tile", "EndCard"}
LIAISON = {"alors", "donc", "et", "mais", "bref", "puis", "ensuite", "voilà", "genre", "enfin"}
MAX_GAP, TYPE_CPS = 2.5, 25

err, warn = [], []
def E(m): err.append(m)
def W(m): warn.append(m)
def words(html): return len(re.sub(r"<[^>]+>", " ", html or "").split())

sb = json.load(open(sys.argv[1]))
D, scenes = sb["duration"], sb["scenes"]
prev_end = 0.0
times = []          # (début, fin) de chaque événement, pour le rythme
stickers = []       # (début, fin, pose, scène)
for s in scenes:
    sid = s["id"]
    if abs(s["start"] - prev_end) > 0.05: E(f"{sid}: commence à {s['start']} au lieu de {prev_end} (trou ou chevauchement)")
    prev_end = s["end"]
    ev = s.get("events", [])
    if not ev: E(f"{sid}: aucun événement")
    if [e["t"] for e in ev] != sorted(e["t"] for e in ev): E(f"{sid}: événements pas dans l'ordre")
    acc = sum(1 for e in ev if e.get("accent") and not str(e["el"]).startswith("badge"))
    if acc > 1: E(f"{sid}: {acc} éléments accent (1 maximum hors badges)")
    for e in ev:
        if not (s["start"] - 0.01 <= e["t"] <= s["end"]): E(f"{sid}: événement {e['el']} à {e['t']} hors de la scène")
        dur = len(re.sub(r"<[^>]+>", "", e.get("text", ""))) / TYPE_CPS if e.get("typing") else 0
        times.append((e["t"], e["t"] + dur))
        if e["el"] != "caption" and e.get("word", "").lower() in LIAISON: E(f"{sid}: {e['el']} déclenché par un mot de liaison « {e['word']} »")
        if e["el"] not in ("caption", "punch") and words(e.get("text")) > 6: E(f"{sid}: {e['el']} a plus de 6 mots lisibles")
        if "logo" in e and not e["logo"]: E(f"{sid}: LOGO REQUIS pour {e['el']} (vrai logo manquant)")
        if e["el"] == "sticker":
            p = e.get("pose")
            if p not in POSES: E(f"{sid}: pose inconnue « {p} »")
            if s["component"] not in WITH_AVATAR: E(f"{sid}: personnage avec {s['component']} (jamais avec un schéma ou une interface)")
            stickers.append((e["t"], min(e.get("until", s["end"]), s["end"]), p, sid))
if abs(prev_end - D) > 0.05: E(f"la dernière scène finit à {prev_end}, la vidéo dure {D}")

# rythme : rien de figé plus de MAX_GAP
marks = sorted(times) + [(D, D)]
cur = 0.0
for a, b in marks:
    if a - cur > MAX_GAP: E(f"rien ne bouge de {cur:.2f} à {a:.2f} s ({a-cur:.1f} s > {MAX_GAP})")
    cur = max(cur, b, a)

# personnage
stickers.sort()
total = 0.0
for i, (a, b, p, sid) in enumerate(stickers):
    d = b - a; total += d
    if not 1 <= d <= 4.05: E(f"{sid}: personnage {d:.1f} s (1 à 4 s)")
    if i:
        pa, pb, pp, _ = stickers[i - 1]
        if a - pb < 4: E(f"{sid}: personnage revenu {a-pb:.1f} s après le précédent (4 s minimum)")
        if p == pp: E(f"{sid}: même pose « {p} » deux fois de suite")
if not stickers: W("aucune apparition du personnage")
else:
    if stickers[0][0] > 3: W("pas de personnage dans l'accroche (0 à 3 s)")
    share = total / D
    if not 0.15 <= share <= 0.25: W(f"personnage {share:.0%} du temps (cible 15 à 25 %)")
    pts = [0.0] + [x[0] for x in stickers] + [D]
    for a, b in zip(pts, pts[1:]):
        if b - a > 14: W(f"{b-a:.0f} s sans personnage ({a:.1f} → {b:.1f} s ; cible : une apparition toutes les 8 à 12 s)")

for m in err: print("ERREUR ", m)
for m in warn: print("ALERTE ", m)
print(f"{len(scenes)} scènes, {len(stickers)} apparitions du personnage, {len(err)} erreur(s), {len(warn)} alerte(s)")
sys.exit(1 if err else 0)
