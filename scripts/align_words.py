#!/usr/bin/env python3
"""Temps de chaque mot d'une voix enregistrée, à partir du script exact (alignement forcé, sans modèle ni API).
Usage : python3 align_words.py voix.mp3 script.txt mots.json
Principe : espeak-ng (français) lit le script mot par mot -> on connaît les frontières dans cette voix de synthèse ;
DTW sur les MFCC entre synthèse et vraie voix -> on reporte chaque frontière sur la vraie voix.
Dépendances : espeak-ng (apt), librosa, numpy, ffmpeg."""
import json, re, subprocess, sys, tempfile, os
import numpy as np, librosa

SR, HOP = 16000, 160                      # 10 ms par trame
audio, script, out = sys.argv[1], sys.argv[2], sys.argv[3]
words = re.findall(r"[\wÀ-ÿ'’-]+", open(script, encoding="utf-8").read())

def synth(word):
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f: p = f.name
    subprocess.run(["espeak-ng", "-v", "fr", "-s", "175", "-w", p, word], check=True, capture_output=True)
    y, _ = librosa.load(p, sr=SR); os.unlink(p)
    y, _ = librosa.effects.trim(y, top_db=30)
    return y

gap = np.zeros(int(0.04 * SR))
parts, bounds, t = [], [], 0
for w in words:
    y = synth(w); parts += [y, gap]
    bounds.append((t, t + len(y))); t += len(y) + len(gap)
syn = np.concatenate(parts)
real, _ = librosa.load(audio, sr=SR)

def feats(y):
    m = librosa.feature.mfcc(y=y, sr=SR, n_mfcc=20, hop_length=HOP, n_fft=512)[1:]
    return (m - m.mean(1, keepdims=True)) / (m.std(1, keepdims=True) + 1e-6)
A, B = feats(syn), feats(real)
_, wp = librosa.sequence.dtw(X=A, Y=B, metric="cosine", subseq=False)
wp = wp[::-1]
syn2real = np.zeros(A.shape[1], int)
for i, j in wp: syn2real[i] = j          # dernière correspondance pour chaque trame de synthèse
rms = librosa.feature.rms(y=real, hop_length=HOP)[0]; thr = 0.15 * np.percentile(rms, 95)

res = []
for w, (a, b) in zip(words, bounds):
    s, e = syn2real[min(a // HOP, len(syn2real) - 1)], syn2real[min(b // HOP, len(syn2real) - 1)]
    while s < e and rms[s] < thr: s += 1   # caler le début sur l'attaque réelle du mot
    res.append({"word": w, "start": round(s * HOP / SR, 2), "end": round(max(e, s + 1) * HOP / SR, 2)})
json.dump(res, open(out, "w"), ensure_ascii=False, indent=1)
print(f"{len(res)} mots alignés sur {len(real)/SR:.1f} s")
