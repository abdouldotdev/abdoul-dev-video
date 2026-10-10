# abdoul-dev-video

Skill Hermes pour transformer **la voix enregistrée d'Abdoul** en vidéo explainer verticale (TikTok, Reels, Shorts). Il relie transcription au mot, nettoyage des prises, storyboard, composants du design system abdoul.dev, effets sonores et rendu MP4.

> **Ce dépôt est un kit de production, pas une vidéo ni un service hébergé.** Il ne contient ni enregistrement vocal, ni clé API, ni vidéo rendue. Les exemples de texte/storyboard sont des données de démonstration.

## Ce qu'il contient

| Chemin | Rôle |
| --- | --- |
| [`SKILL.md`](SKILL.md) | Workflow, contraintes de montage et vérifications |
| [`design-system/`](design-system/) | Tokens, CSS, polices, 68 aperçus de composants, 40 poses d'avatar et logos de référence |
| [`regles/`](regles/) | Principes visuels, choix des scènes, calage voix et storyboard |
| [`scripts/`](scripts/) | Transcription ElevenLabs Scribe, nettoyage audio, calage, vérification et SFX |
| [`exemple/`](exemple/) | Script, storyboards et générateur HTML HyperFrames pour « Combien ça m'a coûté » |

Les ressources du design system sont **locales** : l'artifact Claude cité dans le skill n'est pas nécessaire pour lire les composants et les assets de cet export.

## Installer dans Hermes

Cloner le dépôt entier dans le dossier des skills pour conserver les assets et scripts (ne pas télécharger uniquement `SKILL.md`) :

```bash
git clone https://github.com/abdouldotdev/abdoul-dev-video.git ~/.hermes/skills/abdoul-dev-video
```

Dans une nouvelle session Hermes, demander une vidéo explainer abdoul.dev en fournissant **son fichier audio original** et, si disponible, son script. Le skill décrit le processus ; aucune publication TikTok n'est effectuée automatiquement.

## Prérequis pour produire une vidéo

- Python 3 et les modules `requests`, `Pillow`, `numpy`, `scipy` (selon les scripts utilisés) ; `ffmpeg` et `ffprobe` ; Node.js 22+.
- HyperFrames (version testée : `0.8.144`) et GSAP local pour le rendu HTML → MP4.
- Une clé **ElevenLabs** dans la variable d'environnement `ELEVENLABS_API_KEY` pour Scribe et les SFX. Ne jamais la mettre dans un commit, un argument de commande, un storyboard ou un fichier du projet.
- La voix brute en MP3/WAV **sans musique**. Les temps du storyboard proviennent des mots transcrits, pas des intervalles saisis à la main.

### Flux de travail

1. Transcrire l'audio avec [`scripts/scribe_words.py`](scripts/scribe_words.py) ; garder la réponse Scribe brute pour éviter un second appel facturé.
2. Examiner les faux départs, hésitations et prises répétées, puis nettoyer l'audio avec [`scripts/clean_voice.py`](scripts/clean_voice.py). Toujours contrôler les jointures et les noms propres sur l'enregistrement.
3. Construire des scènes avec les composants/poses de `design-system/`. Ancrer chaque événement à l'**index du mot** et calculer son temps depuis `mots.json`.
4. Exécuter [`scripts/check_storyboard.py`](scripts/check_storyboard.py) jusqu'à **0 erreur** ; justifier les alertes restantes.
5. Générer le HTML, y copier tokens/CSS, polices, poses, logos officiels et GSAP. Configurer les effets via [`scripts/sfx.config.json`](scripts/sfx.config.json), ou mettre `enabled: false`.
6. Vérifier avec `npx hyperframes lint .` (0 erreur), puis rendre avec `npx hyperframes render . -o video.mp4 --quality delivery`. Examiner plusieurs images par scène et écouter les jointures de la voix avant livraison.

Le dossier [`exemple/`](exemple/) montre la structure d'un montage complet, mais son générateur attend un `mots.json` **aligné sur son propre** `script_propre.txt`, ainsi qu'un dossier de travail `proj/` préparé avec les ressources. Ne pas lancer un rendu sur des mots d'un autre script sans réaligner les index.

## Vérification rapide sans API

```bash
python3 scripts/check_storyboard.py exemple/exemple-storyboard.json
node --check scripts/scan_composants.js
```

Le premier contrôle doit indiquer **0 erreur et 0 alerte**. Ces commandes ne transcrivent rien et ne produisent pas de vidéo ; un rendu de bout en bout nécessite la voix et les prérequis ci-dessus.

## Publication et droits

Le dépôt public expose les **poses d'avatar d'Abdoul**. Les logos de marques restent la propriété de leurs titulaires ; les polices Satoshi conservent leurs conditions d'utilisation d'origine. Aucune licence de réutilisation générale du contenu original n'est accordée par défaut. Pour utiliser l'identité visuelle ou les poses dans un autre projet, demander l'accord d'Abdoul.
