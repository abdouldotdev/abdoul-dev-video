#!/usr/bin/env python3
"""Effets sonores ElevenLabs, pilotés par sfx.config.json (rien n'est codé en dur).
Usage :
  ELEVENLABS_API_KEY=... python3 sfx_eleven.py sfx.config.json            # génère les sons manquants (cache)
  python3 sfx_eleven.py sfx.config.json --plan storyboard.json            # liste des sons à placer (JSON)
Config :
  enabled      true / false : coupe tous les sons (aucun fichier généré, plan vide)
  sounds       nom -> {prompt, duration (0,5 à 30 s), influence (0 à 1)}
  triggers     composant de scène ou élément ("sticker") -> nom du son ; retirer une ligne = plus de son pour ce cas
  volume, dir, model_id, output_format
Un son déjà généré est réutilisé tant que son prompt, sa durée et son influence ne changent pas.
Interdit : un son de transition (whoosh, swipe, swoosh) au changement de scène ; le script refuse ces sons."""
import hashlib, json, os, sys
import requests

API = "https://api.elevenlabs.io/v1/sound-generation"

TRANSITION = ("whoosh", "swoosh", "swipe", "swish", "transition")

def load(path):
    c = json.load(open(path)); c.setdefault("dir", "sfx"); c.setdefault("volume", 0.5)
    bad = [n for n, s in c.get("sounds", {}).items() if any(w in (n + " " + s["prompt"]).lower() for w in TRANSITION)]
    if bad: sys.exit(f"sons de transition interdits (pas de swipe aux changements de scène) : {', '.join(bad)}")
    return c

def key_of(s): return hashlib.sha1(json.dumps(s, sort_keys=True).encode()).hexdigest()[:10]

def generate(cfg):
    if not cfg.get("enabled"): print("sons désactivés (enabled: false)"); return {}
    api = os.environ.get("ELEVENLABS_API_KEY") or sys.exit("ELEVENLABS_API_KEY manquante")
    os.makedirs(cfg["dir"], exist_ok=True)
    idx_path = os.path.join(cfg["dir"], "index.json")
    idx = json.load(open(idx_path)) if os.path.exists(idx_path) else {}
    used = set(cfg.get("triggers", {}).values())
    for name, s in cfg["sounds"].items():
        if name not in used: continue
        k, f = key_of(s), os.path.join(cfg["dir"], f"{name}.mp3")
        if idx.get(name) == k and os.path.exists(f): continue
        r = requests.post(API, params={"output_format": cfg.get("output_format", "mp3_44100_128")},
                          headers={"xi-api-key": api, "Content-Type": "application/json"},
                          json={"text": s["prompt"], "duration_seconds": s.get("duration"),
                                "prompt_influence": s.get("influence", 0.3),
                                "model_id": cfg.get("model_id", "eleven_text_to_sound_v2")}, timeout=120)
        if r.status_code != 200: sys.exit(f"{name} : {r.status_code} {r.text[:300]}")
        open(f, "wb").write(r.content); idx[name] = k; print(f"généré : {f}")
    json.dump(idx, open(idx_path, "w"), indent=1)
    return idx

def plan(cfg, sb):
    """Une entrée par son à jouer : {t, sound, file, volume}."""
    if not cfg.get("enabled"): return []
    trig, out = cfg.get("triggers", {}), []
    for s in sb["scenes"]:
        if s["component"] in trig and s["component"] != "Sticker":
            out.append({"t": s["start"], "sound": trig[s["component"]]})
        for e in s["events"]:
            if e["el"] in trig: out.append({"t": e["t"], "sound": trig[e["el"]]})
    out.sort(key=lambda p: p["t"]); res = []
    for p in out:  # deux sons au même instant : on n'en garde qu'un
        if res and p["t"] - res[-1]["t"] < 0.15: continue
        p["file"] = f'{os.path.basename(cfg["dir"].rstrip("/"))}/{p["sound"]}.mp3'; p["volume"] = cfg["volume"]; res.append(p)
    return res

if __name__ == "__main__":
    cfg = load(sys.argv[1])
    if "--plan" in sys.argv:
        print(json.dumps(plan(cfg, json.load(open(sys.argv[sys.argv.index("--plan") + 1]))), indent=1))
    else:
        generate(cfg)
