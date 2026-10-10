# Storyboard et rendu

## Format

Un fichier JSON par vidéo. Une scène par idée ; chaque événement porte son temps (secondes) et le mot qui le déclenche.

| Champ | Où | Sens |
| --- | --- | --- |
| `video`, `fps`, `duration`, `audio` | racine | nom, 30 i/s, durée totale, fichier de la voix |
| `id`, `start`, `end`, `say` | scène | les scènes se suivent sans trou |
| `component`, `props` | scène | le composant principal (nom du design system) et son contenu |
| `t`, `el`, `word` | événement | temps, élément du composant, mot déclencheur |
| `text`, `state`, `value`, `typing` | événement | contenu, état (« near »), valeur (rang, chiffre), texte tapé |
| `accent` | événement | `true` sur l'élément dont parle la voix (1 par scène hors badges) |
| `logo` | événement | chemin du logo officiel ; `null` = LOGO REQUIS, rendu bloqué |
| `pose`, `until` | événement `sticker` | la pose ; fin avant la fin de scène si besoin |

Exemple complet : [exemple-storyboard.json](exemple-storyboard.json). Le personnage y apparaît dans l'accroche puis sur le verdict (stop puis facepalm, 8,7 s d'écart, 24 % du temps) ; jamais plus de 2 s sans événement ; la carte et la fenêtre Google restent et évoluent.

## Checklist avant rendu

- [ ] Chaque phrase a un visuel ; chaque élément a un mot déclencheur et un temps.
- [ ] Rien de figé plus de 2,5 s ; pas d'événement sur un mot de liaison.
- [ ] Un seul élément `accent` par scène (hors badges).
- [ ] Tout est centré ; le tiers bas est libre (sauf avatar).
- [ ] Pas plus de 6 mots lisibles par bloc ; aucun faux texte lisible.
- [ ] Chaque marque citée a son vrai logo (aucun « LOGO REQUIS » restant).
- [ ] Personnage : fréquence, durée, écart de 4 s et poses différentes respectés ; jamais avec un schéma.
- [ ] TOI / TON … présent dans les exemples ; chiffres précis.

`python3 check_storyboard.py storyboard.json` vérifie tout ce qui est mesurable (rythme, accent, mots de liaison, 6 mots, logos, durée, écart et poses du personnage). Une ERREUR bloque le rendu ; une ALERTE se justifie ou se corrige. Le centrage et la présence de TOI se vérifient à l'œil sur les images clés.

## Rendu HyperFrames

Testé avec hyperframes 0.8.144 (Node ≥ 22, FFmpeg).

**Structure du projet**

```text
video/
  index.html          composition principale
  tokens.css          généré depuis tokens.json (tokens2css.py)
  bundle.css          components/bundle.css du design system
  gsap.min.js         copie locale (npm i gsap), jamais un CDN
  fonts/              Satoshi en woff2 (+ @font-face dans index.html)
  poses/<clé>.webp    poses utilisées, téléchargées du groupe Avatar
  logos/<marque>.svg  logos officiels
  voix.mp3
```

**index.html**

- `<html>` en 1080 × 1920 ; racine `<div id="root" data-composition-id="main" data-start="0" data-duration="…" data-width="1080" data-height="1920">`.
- La voix : `<audio id="voix" src="voix.mp3" data-start="0" data-duration="…" data-track-index="0">`. **L'`id` est obligatoire**, sinon la vidéo sort muette.
- Une scène = `<div id="s1" class="clip" data-start="…" data-duration="…" data-track-index="1">` qui contient un `.ad-scene.is-full` mis à l'échelle (`.clip .ad-scene{transform:scale(3)}`), avec le balisage du composant repris de sa preview dans le design system (et les `<symbol>` d'icônes dont il a besoin).
- Le personnage : `<img id="…" class="clip sticker edged" src="poses/<clé>.webp" data-start data-duration data-track-index="2">`, ancré en bas, coupé par le bord.
- Les apparitions : une timeline GSAP en pause, `window.__timelines["main"] = tl`. Chaque événement du storyboard = `tl.fromTo(el, {opacity:0, y:12, scale:.86}, {opacity:1, y:0, scale:1, duration:.3, ease:"back.out(2)"}, t)`. Les changements d'état (rang, page, épingle qui se rapproche) sont aussi des tweens placés à leur `t`. Pas d'animation CSS dans le rendu.

**Commandes**

```bash
npx hyperframes lint .                 # 0 erreur exigée (les avertissements de sous-composition sont acceptés)
npx hyperframes render . -o video.mp4
```

Dans un environnement sans Chrome HyperFrames, pointer `HYPERFRAMES_BROWSER_PATH` vers un headless shell Chromium existant.

**Contrôle** : extraire 3 images par scène (début, milieu, fin) avec ffmpeg et les regarder avant de livrer : centrage, accent unique, personnage coupé par le bord, rien de coupé par l'interface TikTok.
