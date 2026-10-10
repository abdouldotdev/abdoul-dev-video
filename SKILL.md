---
name: abdoul-dev-video
description: Monte la voix d'Abdoul en vidéo explainer verticale.
---

# abdoul-dev-video

Du script au MP4 pour les vidéos explainer abdoul.dev (TikTok, Reels, Shorts, 9:16).

**Responsabilités séparées.** Ce skill dit **quand et comment** utiliser les pièces. Le design system abdoul.dev (artifact `https://claude.ai/artifact/KpGSYjQxzaakj89X4J8t9e`) dit **ce que sont les pièces et à quoi elles ressemblent** : tokens (couleurs, typo, tailles par famille), composants, briques, poses, iconographie, motion, centrage, espacements. Ne jamais recopier ni réinventer un style : toujours le lire dans le design system.

**Copie locale (export).** Ce dossier contient tout ce qu'il faut sans accès à l'artifact : `design-system/` (README, tokens.json, components/ avec bundle.css et les previews, fonts/, assets/Avatar = les 40 poses, assets/Logos), `scripts/` (les scripts ci-dessous, prêts à lancer), `regles/` (les règles en fichiers séparés), `exemple/` (storyboard et build de la vidéo « Combien ça coûte »). Si l'artifact n'est pas joignable, lire `design-system/` à la place.

**Hors périmètre** : écrire le script ou l'accroche (AutoViral), générer la voix, publier.

## Entrées

- La voix enregistrée par Abdoul (mp3/wav, sans musique). Elle peut contenir hésitations, mots de remplissage, faux départs et prises répétées : le skill les retire.
- Le script ou sa transcription, si fourni (sinon, la transcription Scribe sert de base).
- Une clé ElevenLabs (`ELEVENLABS_API_KEY`), pour Scribe (horodatage) et les effets sonores. Ne jamais l'écrire dans un fichier. Le domaine `api.elevenlabs.io` doit être joignable ; sinon, demander à l'utilisateur de l'autoriser dans ses réglages réseau ou de lancer les scripts chez lui. On ne cale rien à l'oreille.
- `sfx.config.json` : interrupteur `enabled`, sons (prompt, durée, influence), déclencheurs. Rien n'est codé en dur.
- Si fournies : clés d'API d'image (poses et stickers 3D manquants).

## Étapes

1. **Lire le design system** avec l'outil Artifact (`action: read`) : `project/README.md`, `project/tokens.json`, `project/components/bundle.css`, `project/design-system.json` (ids des poses dans `assetGroups.Avatar.files`), les polices `project/fonts/*.woff2`. Puis, pour chaque composant retenu, `project/components/<Nom>/README.md` et `preview.html` (le balisage à reprendre).
2. **Transcrire** : `ELEVENLABS_API_KEY=… python3 scribe_words.py voix_brute.mp3 mots_bruts.json` → `mots_bruts.scribe.json` (réponse brute, au mot).
3. **Nettoyer la voix** (règles « Nettoyer la voix ») : `python3 clean_voice.py suggest mots_bruts.scribe.json` marque les remplissages, phrases coupées et passages répétés ; écrire `script_propre.txt` ; puis `python3 clean_voice.py cut mots_bruts.scribe.json voix_brute.mp3 script_propre.txt propre/` → `propre/voix.mp3`, `propre/mots.json` (temps recalés sur l'audio coupé), `propre/coupes.json`. Annoncer en une ligne ce qui a été retiré. Puis **découper** au mot près ; repérer mots déclencheurs et mots de liaison.
4. **Choisir le visuel** de chaque phrase (« Choisir le visuel »). Composant absent : le construire selon « Construire un composant qui manque » du design system, le passer au scan (`scan_composants.js`), puis l'ajouter au design system (dossier `components/<Nom>/` avec README.md + preview.html ; relire `design-system.json` juste avant de publier).
5. **Placer le personnage** (« Le personnage »).
6. **Écrire `storyboard.json`** (« Storyboard et rendu ») : chaque événement est accroché à l'INDEX du mot dans `mots.json` (temps = début du mot − 0,08 s), jamais à un temps tapé à la main, pour qu'une nouvelle transcription recale tout. Lancer `check_storyboard.py` ; corriger jusqu'à 0 ERREUR ; justifier chaque ALERTE restante.
7. **Récupérer les assets** : poses utilisées (Artifact `read` avec `path` = id du blob ; une pose nouvelle passe par `detourage.py` avant d'être ajoutée au groupe Avatar), logos officiels (site ou kit presse de la marque, ou Simple Icons pour les marques connues ; jamais redessinés ni générés : introuvable = s'arrêter et demander ; si l'utilisateur veut quand même la vidéo, montrer le nom de la marque en texte seul, sans faux logo, et le dire), stickers 3D (prompt du design system, API fournie, sinon demander).
8. **Construire le projet HyperFrames** (structure plus bas) : `tokens2css.py` pour tokens.css, bundle.css copié, GSAP en local, balisage des previews dans des `.ad-scene.is-full` à l'échelle × 3, une timeline GSAP dont chaque tween suit un événement du storyboard. **Centrer** : mesurer l'emprise de chaque scène (navigateur, tout visible, sans animation) et figer le décalage de son `.ad-stage` pour placer le groupe au milieu de l'écran (y 320 ; y 190 quand le personnage est là) ; un composant qui revient d'une scène à l'autre garde le même décalage ; un fond plein écran est exclu de la mesure. **Espacer** : cartes en colonne flex, marges du design system (« Espacements internes », « Maquettes d'appareil »), hauteurs par famille (tokens `size` : 22 / 28 / 36 / 52).
9. **Sons** : `ELEVENLABS_API_KEY=… python3 sfx_eleven.py sfx.config.json` génère et met en cache les sons utilisés ; `python3 sfx_eleven.py sfx.config.json --plan storyboard.json` donne les sons à placer (un `<audio>` chacun). `"enabled": false` : aucun son.
10. **Faire valider** : une planche d'images clés (une par scène) puis un brouillon MP4 (le rendu prend 1 à 3 min). Une page HTML jouable ne lit pas son audio dans l'aperçu de la conversation : ne pas s'en servir pour valider.
11. **Rendre** : `npx hyperframes lint .` (0 erreur) puis `npx hyperframes render . -o video.mp4 --quality delivery`.
12. **Contrôler** 3 images par scène (ffmpeg), les regarder, corriger, re-rendre.
13. **Livrer** le MP4 et le `storyboard.json` ; signaler en une ligne ce qui a été ajouté au design system (composant, pose, logo).

Les chiffres de rythme et de fréquence sont des valeurs de départ : si l'utilisateur les recale, mettre à jour ce skill.

## Règles

### Principes

Ce qui guide chaque écran. Le style visuel (couleurs, blocs, typo) est dans le [design system abdoul.dev](https://claude.ai/artifact/KpGSYjQxzaakj89X4J8t9e).

1. **Un écran = un sous-titre + un seul visuel, centrés.** Le sous-titre est au-dessus du visuel ; le groupe entier est centré au milieu de l'écran (au-dessus du personnage quand il est là). Un Titre choc remplace le sous-titre sur les mots martelés.
2. **L'objet réel le plus concret de la phrase.** « Référencement » montre une vraie page Google, « payer une pub » une vraie fenêtre de pub, « l'entreprise » un vrai bâtiment.
3. **Un composant raconte une mini-histoire.** Il reste à l'écran et évolue avec la voix (rang 3 → page 20 → page 1, une ligne de plus au reçu) au lieu d'être remplacé. On ne coupe que quand l'idée change.
4. **Le spectateur est dans chaque exemple** : TOI, TON SITE, TA CIBLE, TON APP.
5. **Des données précises, jamais vagues** : « plombier paris 14 », « 12 401 abonnés », « 100 000 € ».
6. **Le personnage porte l'émotion**, souvent avec un accessoire lié au sujet et de l'humour.
7. **La structure est numérotée** : nombre annoncé (Slots) → carte Numéro par chapitre → sommaire qui se coche.
8. **L'accent n'a qu'un rôle** : `accent` marque l'élément dont on parle maintenant.

### Choisir le visuel

Pour chaque phrase : trouver le cas ci-dessous, puis l'objet réel le plus concret. Les fiches des composants (props, rendu) sont dans le [design system abdoul.dev](https://claude.ai/artifact/KpGSYjQxzaakj89X4J8t9e).

#### Les 3 niveaux d'illustration

| Niveau | Quand | Exemples | Composants |
| --- | --- | --- | --- |
| Sticker | Personnage, objet physique ou lieu à reconnaître | avatar, bâtiment, boutique, billets | Sticker |
| Tuile ou ligne | Nom simple, canal, marque, outil | e-mail, réseaux, Ubersuggest | Tile, ToolRow, YouBlock |
| Interface ou schéma | Action concrète ou relation entre idées | Google, pub, chat, plan, détour | Window, GoogleResults, SearchBar, Chat, Counter, AdWindow, CodeEditor, MapPins, Detour, Referrer, BarChart |

#### Cas de phrase → composant

| La phrase… | Composant |
| --- | --- |
| est dite (toujours) | Caption |
| martèle un mot | PunchTitle |
| donne un montant ou un pourcentage | BigNumber |
| annonce un nombre (« il y a 7… ») | Slots |
| ouvre un chapitre | Chapter |
| fait le point sur le plan | StepsChecklist |
| énumère | BadgeList, ou Tile si chaque élément a une icône |
| pose une question et ses réponses | LabelStack |
| cite des outils | ToolRow |
| détaille ce que quelque chose a coûté | Reçu (Card + WindowBar + lignes logo / nom / montant + total), qui se remplit au fil de la voix |
| additionne des ingrédients d'un résultat | CalcCards (✓ A, + B, = résultat en accent) |
| dit « tout » ou une part d'un budget | GoalProgress / ProgressBar qui se remplit |
| montre une page, un produit | Window |
| parle de référencement | GoogleResults, SearchBar |
| parle d'un contact, d'un message | Chat |
| parle d'audience | Counter |
| parle de payer pour être vu | AdWindow |
| parle de code | CodeEditor |
| énonce le principe « va où est ta cible » | MapPins (motif récurrent) |
| parle de détourner | Detour |
| parle d'apporteur, de commission | Referrer |
| parle de croissance, d'effet, de résultats qui montent | BarChart |
| désigne une cible dans une foule | PeopleRow |
| donne une quantité à remplir | Grid100 |
| pose un calcul | CalcCards |
| s'adresse à « toi » dans un schéma | YouBlock |
| montre une app sur mobile, ou son échec (0 utilisateur) | PhoneScreen, AppStoreCard |
| annonce un résultat qui tombe | Notification |
| parle de fiche, de référencement local | BusinessCard |
| compare deux choses, ou oppose « pas cher » à « ce qui change tout » | Versus |
| partage entre associés | SplitShare |
| parle de prix, d'offres | PriceTable |
| donne un objectif | GoalProgress |
| parle d'avis clients | ReviewCard |
| parle d'e-mail, de signature | EmailCard |
| parle de maquettes, d'écrans | WireframePages |
| demande de prioriser | FeaturePriority |
| décrit des étapes dans le temps | Timeline |
| parle de conversion | Funnel |
| donne une date, une régularité | Calendar |
| parle de taper, d'une lettre | Keyboard |
| cite des pays | FlagRow |
| parle de mesurer, d'analytics | AnalyticsBoard |
| parle d'un post, de viralité | SocialPost |
| liste des choses à faire | TodoList |
| donne une part en % | Donut |
| décrit une hiérarchie qui découle | FlowStack |
| parle de réseau, de partenaires | Network |
| ne correspond à aucun composant | nouveau composant (voir « Construire un composant qui manque ») |
| exprime une émotion, un verdict | Sticker |
| conclut, appelle à s'abonner | EndCard (plein écran accent, texte blanc) |
| lie sans contenu (« alors », « en fait ») | rien de nouveau : seul Caption change |

**Un exemple** se raconte en 3 temps : qui (Tile ou Sticker) → comment (interface avec LE détail) → résultat (BigNumber, Counter ou avatar). **Une liste d'exemples** s'empile (ToolRow, Tile), 1 par seconde, sans détail.

#### Où trouver un asset

Dans cet ordre :

1. Un composant du design system.
2. Une icône Flat Icons recolorée (style : Iconographie du design system).
3. **Le logo officiel** si une marque est citée : obligatoire, jamais remplacé. Introuvable : « LOGO REQUIS », le rendu est bloqué. Marques connues : Simple Icons (`cdn.jsdelivr.net/npm/simple-icons@<version>/icons/<nom>.svg`) avec la couleur officielle de la marque.
4. Sinon (objet ou lieu, jamais une marque) : un sticker 3D généré avec le prompt du design system, ajouté aux assets ; jamais deux fois le même objet.

Aucun composant ne colle : en construire un selon « Construire un composant qui manque » du design system, puis l'y ajouter pour qu'il serve aux vidéos suivantes.

### Nettoyer la voix

- Retirer : mots de remplissage (« euh », « hum », « bah », « ben »…), faux départs (phrase coupée « qui se-- », « il y a… »), prises répétées : quand une phrase est redite, garder la **dernière prise complète** et retirer les précédentes en entier.
- Ne jamais reformuler ni résumer : `script_propre.txt` reprend les mots dits, dans l'ordre. Seules corrections permises : l'orthographe des noms et marques mal reconnus (« Cloud Code » → « Claude Code », « Abdul » → « Abdoul », « Nana Pay » → « NanaPay ») et les nombres en chiffres.
- Le nom d'une marque se prend dans l'audio, pas dans une transcription fournie : si les deux diffèrent, l'audio gagne ; le doute se signale.
- `suggest` propose, il ne décide pas : « de ce genre » n'est pas un remplissage, une suite répétée peut être voulue. Trancher à la lecture.
- Les coupes se font entre deux mots, avec un fondu de 15 ms ; écouter les jointures sur le brouillon.

### Caler sur la voix

#### Découper

- La voix est horodatée au mot (début et fin de chaque mot) avec ElevenLabs Scribe, nettoyée, puis recalée sur le texte exact du script propre.
- Une phrase = une scène possible.
- **Mots déclencheurs** : les noms, chiffres, marques, et « toi / ton / ta ». Chacun peut faire apparaître ou changer un élément.
- **Mots de liaison** (« alors », « en fait », « donc », « mais », « et », « du coup ») : rien de nouveau, seul le sous-titre change ; accrocher l'événement au mot suivant.

#### Synchroniser

- Un élément apparaît au **début du mot qui le nomme, 0,08 s avant** (2 images d'anticipation à 30 i/s).
- Le contenant arrive juste avant son contenu (la fenêtre, puis le texte tapé).
- Texte tapé à ≈ 25 caractères par seconde ; nombres qui défilent en 0,8 s (vitesses définies dans Motion du design system).
- Le sous-titre suit la voix phrase par phrase, court (une ligne de préférence) ; le mot dit en ce moment peut passer en accent.

#### Rythme

- Un nouvel élément ou un changement d'état toutes les **0,8 à 1,5 s**.
- Rien de figé plus de **2,5 s** (un texte en train de se taper compte comme du mouvement).

#### Continuer ou couper

- **Même idée** : le composant reste et change d'état (rang, coche, chiffre, barre, épingle qui se rapproche, ligne qui s'ajoute au reçu).
- **Idée nouvelle** : coupe franche, en général toutes les **3 à 6 s**.
- Un motif récurrent (MapPins « va où est ta cible ») revient au début, au milieu et à la fin.

#### Son

- Les sons et ce qui les déclenche sont dans `sfx.config.json` (par défaut : pop sur le personnage et PunchTitle, tap sur Chapter, cash sur BigNumber). Deux sons au même instant : un seul.
- **Jamais de son de transition** (whoosh, swipe, swoosh) aux changements de scène : un son marque un objet qui apparaît, jamais le passage d'une scène à l'autre. `sfx_eleven.py` refuse ces sons.
- La voix prime : volume des sons 0,5 au plus ; musique très basse sous la voix.

### Le personnage

Les poses disponibles, leur cadrage et leur rendu (classe `sticker edged`) sont dans le [design system abdoul.dev](https://claude.ai/artifact/KpGSYjQxzaakj89X4J8t9e), groupe Avatar.

#### Quand il apparaît

L'accroche, une émotion, un verdict, une adresse directe (« toi »), une anecdote, l'appel à l'action. Il porte l'émotion, souvent avec un accessoire lié au sujet et de l'humour.

#### Fréquence

- Environ **une apparition toutes les 8 à 12 s**, **15 à 25 %** du temps d'écran.
- **1 à 4 s** par apparition ; jamais moins de **4 s** entre deux apparitions ; jamais deux fois la même pose de suite.
- Présent dans l'accroche (0 à 3 s) et sur l'appel à l'action.
- Tête seule (réactions) pour une émotion ; buste (gestes) pour une adresse ou une explication ; `count_N` quand la voix dit un numéro (« 3 ») ; accessoire (money, laptop, phone, stopwatch, chart_up) quand la phrase en parle.
- Jamais avec un schéma ou une interface ; possible avec Caption, PunchTitle, BigNumber, une Tile ou EndCard. Une longue suite d'interfaces sans personnage se signale en ALERTE et se justifie.

#### Choisir la pose

| La phrase… | Pose |
| --- | --- |
| interpelle, montre du doigt | point |
| explique, nuance | explain, present |
| compte, annonce un numéro | count_1 … count_10 |
| valide, recommande, « c'est pas cher » | thumbs_up |
| rejette, déconseille, « pas de négociation » | thumbs_down, arms_crossed, stop |
| raconte une erreur, un échec | facepalm, sad |
| doute, « ça dépend » | shrug, skeptical, think |
| a l'idée, la solution | idea |
| célèbre un résultat, une croissance | arms_up, star_eyes, chart_up |
| choque, révèle | shocked, mind_blown |
| confie un secret, une astuce | whisper |
| parle d'argent gagné / perdu / demande combien | money / empty_pockets |
| parle de temps, de vitesse | stopwatch |
| parle de code, d'app | laptop, phone |
| s'énerve contre une pratique | angry |
| fait rire | laugh |
| se présente, remercie, appelle à s'abonner | wave, hands_heart |
| adore un outil, un résultat, un prix bas | heart_eyes, star_eyes |

Jamais deux fois la même pose de suite ; sur une vidéo, varier au maximum. Pose absente : la générer depuis l'image de référence, lui appliquer `detourage.py` (bande blanche + trait encre, identique aux 40 poses), puis l'ajouter au groupe Avatar du design system.

### Storyboard et rendu

#### Format

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

Exemple complet : l'exemple plus bas. Le personnage y apparaît dans l'accroche puis sur le verdict (stop puis facepalm, 8,7 s d'écart, 24 % du temps) ; jamais plus de 2 s sans événement ; la carte et la fenêtre Google restent et évoluent.

#### Checklist avant rendu

- [ ] Chaque phrase a un visuel ; chaque élément a un mot déclencheur et un temps.
- [ ] Rien de figé plus de 2,5 s ; pas d'événement sur un mot de liaison.
- [ ] Un seul élément `accent` par scène (hors badges) ; jamais de texte accent posé sur un fond accent.
- [ ] Tout est centré au milieu de l'écran ; rien sous y 560 sauf l'avatar ; un composant qui revient ne saute pas.
- [ ] Espacements internes réguliers ; rien ne touche un bord de carte ou de téléphone ; hauteurs par famille respectées.
- [ ] Pas plus de 6 mots lisibles par bloc ; aucun faux texte lisible ; un titre choc tient sur ses lignes sans se chevaucher.
- [ ] Chaque marque citée a son vrai logo (aucun « LOGO REQUIS » restant).
- [ ] Personnage : fréquence, durée, écart de 4 s et poses différentes respectés ; jamais avec un schéma.
- [ ] TOI / TON … présent dans les exemples ; chiffres précis.

`python3 check_storyboard.py storyboard.json` (script plus bas) vérifie tout ce qui est mesurable (rythme, accent, mots de liaison, 6 mots, logos, durée, écart et poses du personnage). Une ERREUR bloque le rendu ; une ALERTE se justifie ou se corrige. Le centrage, les espacements et la présence de TOI se vérifient à l'œil sur les images clés.

#### Rendu HyperFrames

Testé avec hyperframes 0.8.144 (Node ≥ 22, FFmpeg), sur une vidéo de 68 s (rendu ≈ 3 min).

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
  sfx/<son>.mp3       sfx_eleven.py (cache, index.json)
  voix.mp3            la voix nettoyée (clean_voice.py)
```

**index.html**

- `<html>` en 1080 × 1920 ; racine `<div id="root" data-composition-id="main" data-start="0" data-duration="…" data-width="1080" data-height="1920">`.
- La voix : `<audio id="voix" src="voix.mp3" data-start="0" data-duration="…" data-track-index="0">`. **L'`id` est obligatoire**, sinon la vidéo sort muette. Les sons : un `<audio id="sfxN">` par entrée du plan, `data-volume` du config, chacun sur sa piste.
- Une scène = `<div id="s1" class="clip" data-start="…" data-duration="…" data-track-index="1">` qui contient un `.ad-scene.is-full` mis à l'échelle (`.clip .ad-scene{transform:scale(3)}`), son contenu dans un `.ad-stage` dont le décalage de centrage est figé, avec le balisage du composant repris de sa preview dans le design system (et les `<symbol>` d'icônes dont il a besoin).
- Le personnage : `<img id="…" class="clip sticker edged" src="poses/<clé>.webp" data-start data-duration data-track-index="2">`, ancré en bas, coupé par le bord.
- Les apparitions : une timeline GSAP en pause, `window.__timelines["main"] = tl`. Chaque événement du storyboard = `tl.fromTo(el, {opacity:0, y:12, scale:.86}, {opacity:1, y:0, scale:1, duration:.3, ease:"back.out(2)"}, t)`. Les changements d'état (rang, page, épingle qui se rapproche) sont aussi des tweens placés à leur `t`. Pas d'animation CSS dans le rendu.
- Sous-titres ancrés par le bas (`bottom` = haut prévu + 30) : un sous-titre sur deux lignes monte au lieu de toucher le visuel.
- Un bloc seul qui sera rejoint par un second (Versus) démarre centré (`x` décalé), puis glisse à sa place quand le second arrive.
- Barres et jauges : tween de `width` / `height` depuis 0.
- Texte qui se tape : animer `clip-path` (`inset(0 100% 0 0)` → `inset(0 0 0 0)`, `ease: steps(n)`), jamais un `onUpdate` : HyperFrames déplace la tête de lecture sans déclencher les callbacks. Changer un texte : `tl.set(el, {textContent})`. Sous-titres successifs : chacun son élément, le précédent masqué par `tl.set(opacity 0)`.

**Commandes**

```bash
npx hyperframes lint .                 # 0 erreur exigée (les avertissements de sous-composition sont acceptés)
npx hyperframes render . -o video.mp4 --quality delivery
```

Dans un environnement sans Chrome HyperFrames, pointer `HYPERFRAMES_BROWSER_PATH` vers un headless shell Chromium existant.

**Contrôle** : extraire 3 images par scène (début, milieu, fin) avec ffmpeg et les regarder avant de livrer : centrage, espacements, accent unique, personnage coupé par le bord, rien de coupé par l'interface TikTok.

## Exemple de storyboard (13 s, 0 erreur)

```json
{
  "video": "premiers-clients",
  "fps": 30,
  "duration": 12.9,
  "audio": "voix.mp3",
  "scenes": [
    { "id": "s1", "start": 0.0, "end": 2.3,
      "say": "Tes premiers clients ? Arrête de poster partout.",
      "component": "Sticker",
      "events": [
        { "t": 0.0,  "el": "caption", "text": "Tes premiers <em>clients</em> ?" },
        { "t": 1.12, "el": "sticker", "pose": "stop", "word": "Arrête" },
        { "t": 1.12, "el": "caption", "text": "Arrête de poster <em>partout</em>" }
      ] },
    { "id": "s2", "start": 2.3, "end": 5.2,
      "say": "Va là où ta cible est déjà.",
      "component": "MapPins", "props": { "target": "TA CIBLE" },
      "events": [
        { "t": 2.3, "el": "map" },
        { "t": 2.5, "el": "pin.you", "word": "Va", "state": "far", "accent": true },
        { "t": 3.3, "el": "pin.target", "word": "cible", "text": "TA CIBLE" },
        { "t": 4.3, "el": "pin.you", "word": "déjà", "state": "near" }
      ] },
    { "id": "s3", "start": 5.2, "end": 10.3,
      "say": "Ta cible tape « plombier paris 14 ». Ton site ? Page 3.",
      "component": "GoogleResults", "props": { "query": "plombier paris 14", "rank": 27, "page": 3 },
      "events": [
        { "t": 5.2,  "el": "window" },
        { "t": 5.72, "el": "query", "word": "tape", "text": "plombier paris 14", "typing": true },
        { "t": 8.0,  "el": "result.you", "word": "site", "text": "TON SITE", "accent": true },
        { "t": 8.9,  "el": "page", "word": "Page", "value": 3 }
      ] },
    { "id": "s4", "start": 10.3, "end": 12.9,
      "say": "Personne ne va en page 3.",
      "component": "Sticker",
      "events": [
        { "t": 10.3, "el": "caption", "text": "Personne ne va en <em>page 3</em>" },
        { "t": 11.0, "el": "sticker", "pose": "facepalm", "word": "Personne" }
      ] }
  ]
}
```

## Scripts

Les écrire dans le dossier de travail avant usage.

### check_storyboard.py

```python
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
```

### tokens2css.py

```python
#!/usr/bin/env python3
"""tokens.json du design system abdoul.dev -> tokens.css (variables CSS sur :root). Usage : python3 tokens2css.py tokens.json tokens.css"""
import json, sys
t = json.load(open(sys.argv[1])); out = [":root{"]
def val(v): return v.get("video", next(iter(v.values()))) if isinstance(v, dict) else v
for fam in ("color", "spacing", "radius", "shadow", "border", "size"):
    for tok in t.get(fam, {}).get("tokens", []):
        out.append(f"  --{tok['name']}:{val(tok['value'])};")
for k, v in t.get("type", {}).get("families", {}).items():
    out.append(f"  --font-{k}:{v};")
out.append("}")
open(sys.argv[2], "w").write("\n".join(out) + "\n")
print(f"{len(out)-2} variables")
```

### scribe_words.py

```python
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
```

### clean_voice.py

```python
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
```

### detourage.py

```python
"""Épaissit le détourage des poses : retire le fin liseré d'origine, pose une bande blanche épaisse + un trait encre."""
import sys, numpy as np
from PIL import Image
from scipy import ndimage
src, dst = sys.argv[1], sys.argv[2]
WHITE, INK, TRIM, PAD = 16, 5, 4, 24   # px pour une pose de ~900 px
im = Image.open(src).convert("RGBA")
src_a = np.array(im)
cut = src_a[-3:, :, 3].max() > 127                # la pose est coupée par le bas de l'image
bottom = 0 if cut else PAD
arr0 = np.pad(src_a, ((PAD, bottom), (PAD, PAD), (0, 0)))
im = Image.fromarray(arr0)
a = arr0[..., 3] > 127
if cut:  # prolonger le masque vers le bas pour ne pas détourer la coupe
    ext = np.vstack([a, np.repeat(a[-1:], PAD, 0)])
    a_calc = ext
else:
    a_calc = a
d_out = ndimage.distance_transform_edt(~a_calc)[:a.shape[0]]   # distance à l'extérieur
d_in = ndimage.distance_transform_edt(a_calc)[:a.shape[0]]     # distance à l'intérieur
core = d_in > TRIM                               # contenu sans l'ancien liseré
white = d_out <= WHITE                           # tout ce qui est à moins de WHITE px
ink = (d_out > WHITE) & (d_out <= WHITE + INK)
out = np.zeros((*a.shape, 4), np.uint8)
out[white] = (255, 255, 255, 255)
out[ink] = (18, 18, 18, 255)
arr = np.array(im)
out[core] = arr[core]
# anti-crénelage léger du bord extérieur
edge = (d_out > WHITE + INK) & (d_out <= WHITE + INK + 1.5)
out[edge] = (18, 18, 18, 110)
res = Image.fromarray(out)
bbox = res.getbbox(); res = res.crop(bbox)
print('coupée en bas' if cut else 'entière', end=' ')
res.save(dst, "WEBP", quality=88, method=6)
print(dst, res.size)
```

### sfx_eleven.py

```python
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
```

### sfx.config.json

```json
{
  "enabled": true,
  "provider": "elevenlabs",
  "model_id": "eleven_text_to_sound_v2",
  "output_format": "mp3_44100_128",
  "dir": "sfx",
  "volume": 0.5,
  "sounds": {
    "pop":   { "prompt": "short soft cartoon pop, bubbly UI appear sound, clean, no reverb", "duration": 0.5, "influence": 0.6 },
    "tap":   { "prompt": "single crisp wooden tap, minimal UI click, dry", "duration": 0.5, "influence": 0.6 },
    "cash":  { "prompt": "short cash register ching, bright and clean", "duration": 0.8, "influence": 0.6 }
  },
  "triggers": {
    "sticker": "pop",
    "PunchTitle": "pop",
    "Chapter": "tap",
    "BigNumber": "cash"
  }
}
```

### scan_composants.js

À lancer dans un dossier de previews (tokens.css, bundle.css et polices injectés), avec Playwright : `node scan_composants.js`.

```js
const {chromium}=require('playwright');const fs=require('fs');(async()=>{
 const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium'});const p=await b.newPage({viewport:{width:300,height:400}});
 const files=fs.readdirSync('.').filter(f=>f.endsWith('.html')).sort();const rep={};
 for(const f of files){await p.goto('file://'+process.cwd()+'/'+f);await p.waitForTimeout(120);
  const r=await p.evaluate(()=>{const out=[];const sc=document.querySelector('.ad-scene');if(!sc)return out;const R0=sc.getBoundingClientRect(),k=R0.width/360;
   const U=x=>+(x/k).toFixed(1);const rect=e=>{const q=e.getBoundingClientRect();return {l:(q.left-R0.left)/k,t:(q.top-R0.top)/k,r:(q.right-R0.left)/k,b:(q.bottom-R0.top)/k,w:q.width/k,h:q.height/k}};
   const isBox=e=>{const s=getComputedStyle(e);return parseFloat(s.borderLeftWidth)>=2||e.classList.contains('phone')||e.classList.contains('scr')};
   const lab=e=>(e.className&&e.className.baseVal===undefined?e.className:'')+':'+(e.textContent||'').trim().slice(0,18);
   // 1 débordement : un descendant sort de sa boîte (hors ombre)
   sc.querySelectorAll('*').forEach(e=>{if(e.closest('svg')&&e.tagName!=='svg')return;const box=e.parentElement&&e.parentElement.closest('.bx,.phone,.scr,.tg,.btn,.row[style*="border"]');if(!box||!sc.contains(box)||box===e)return;
     const a=rect(e),c=rect(box);if(!a.w||!a.h)return;const ov=Math.max(c.l-a.l,a.r-c.r,c.t-a.t,a.b-c.b);
     if(ov>1.5&&getComputedStyle(box).overflow!=='hidden')out.push({k:'déborde',el:lab(e),box:lab(box),px:U(ov*k)});});
   // 2 texte coupé
   sc.querySelectorAll('*').forEach(e=>{if(e.children.length||!(e.textContent||'').trim())return;if(e.scrollWidth>e.clientWidth+1&&getComputedStyle(e).overflow!=='visible')out.push({k:'texte coupé',el:lab(e)})});
   // 3 marge texte / bord
   const w=document.createTreeWalker(sc,NodeFilter.SHOW_TEXT);let n;while(n=w.nextNode()){const t=n.textContent.trim();if(t.length<2)continue;const el=n.parentElement;if(el.closest('.cap,.t,.big,svg'))continue;
     let c=el;while(c&&c!==sc&&!isBox(c))c=c.parentElement;if(!c||c===sc)continue;const rg=document.createRange();rg.selectNodeContents(n);const q=rg.getBoundingClientRect();if(!q.width)continue;const cr=c.getBoundingClientRect(),s=getComputedStyle(c);
     const L=(q.left-cr.left-parseFloat(s.borderLeftWidth))/k,Rr=(cr.right-parseFloat(s.borderRightWidth)-q.right)/k;if(Math.min(L,Rr)<6)out.push({k:'marge',el:lab(el),L:+L.toFixed(1),R:+Rr.toFixed(1)})}
   // 4 chevauchement entre blocs frères à contour
   const boxes=[...sc.querySelectorAll('.bx,.tg,.btn,.phone')].filter(e=>getComputedStyle(e).opacity!=='0');
   for(let i=0;i<boxes.length;i++)for(let j=i+1;j<boxes.length;j++){const A=boxes[i],B=boxes[j];if(A.contains(B)||B.contains(A))continue;const a=rect(A),c=rect(B);
     const x=Math.min(a.r,c.r)-Math.max(a.l,c.l),y=Math.min(a.b,c.b)-Math.max(a.t,c.t);if(x>2&&y>2)out.push({k:'chevauche',a:lab(A),b:lab(B),x:+x.toFixed(1),y:+y.toFixed(1)})}
   // 5 centrage horizontal du groupe
   const st=sc.querySelector('.ad-stage')||sc;let l=1e9,r=-1e9;[...st.children].forEach(c=>{if(c.classList.contains('cap')||c.classList.contains('t')||c.classList.contains('big'))return;const q=rect(c);if(!q.w)return;l=Math.min(l,q.l);r=Math.max(r,q.r)});
   if(r>l){const cx=(l+r)/2;if(Math.abs(cx-180)>4)out.push({k:'décentré',dx:+(180-cx).toFixed(1)})}
   // 6 tailles par famille
   sc.querySelectorAll('.tg,.btn,.inp').forEach(e=>{const h=rect(e).h;const ok=e.classList.contains('tg')?[22,28,32]:[28];if(!ok.some(v=>Math.abs(v-h)<1.5))out.push({k:'taille',el:lab(e),h:+h.toFixed(1)})});
   return out});
  if(r.length)rep[f.replace('.html','')]=r}
 fs.writeFileSync('scan.json',JSON.stringify(rep,null,1));
 const cnt={};Object.values(rep).flat().forEach(x=>cnt[x.k]=(cnt[x.k]||0)+1);console.log(JSON.stringify(cnt),Object.keys(rep).length,'composants');
 for(const [k,v] of Object.entries(rep))console.log(k,'→',v.map(x=>x.k+' '+(x.el||x.a||'')+(x.box?' ⊄ '+x.box:'')+(x.b?' ∩ '+x.b:'')+(x.px!==undefined?' '+x.px:'')+(x.h?' h'+x.h:'')+(x.dx!==undefined?' dx'+x.dx:'')+(x.L!==undefined?` L${x.L}/R${x.R}`:'')).join(' | ').slice(0,600));
 await b.close()})()
```
