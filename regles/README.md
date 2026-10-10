# Règles vidéo abdoul.dev

Comment transformer un script en vidéo explainer abdoul.dev. Ces règles disent **quand et comment** utiliser les pièces ; le [design system abdoul.dev](https://claude.ai/artifact/KpGSYjQxzaakj89X4J8t9e) dit **ce que sont les pièces et à quoi elles ressemblent** (couleurs, composants, poses, motion). On ne recopie jamais l'un dans l'autre.

| Fichier | Contenu |
| --- | --- |
| [01-principes.md](01-principes.md) | Les 8 principes qui guident chaque écran |
| [02-choisir-le-visuel.md](02-choisir-le-visuel.md) | Phrase → composant, les 3 niveaux, exemple vs liste, trouver un asset |
| [03-calage-voix.md](03-calage-voix.md) | Synchronisation au mot, rythme, continuer ou couper, son |
| [04-personnage.md](04-personnage.md) | Quand il apparaît, fréquence, choix de la pose |
| [05-storyboard-et-rendu.md](05-storyboard-et-rendu.md) | Format du storyboard, checklist, HyperFrames |
| [exemple-storyboard.json](exemple-storyboard.json) | Storyboard de 13 s qui passe toutes les règles |
| [check_storyboard.py](check_storyboard.py) | Vérification automatique avant rendu |
| [tokens2css.py](tokens2css.py) | tokens.json du design system → tokens.css |
| [scribe_words.py](scribe_words.py) | Temps de chaque mot avec ElevenLabs Scribe, recalé sur le script |
| [align_words.py](align_words.py) | Secours sans API (±0,3 à 0,5 s, à vérifier) |
| [detourage.py](detourage.py) | Détourage standard d'une nouvelle pose |

## Le process, dans l'ordre

1. **Horodater la voix** : `scribe_words.py voix.mp3 mots.json script.txt` (ElevenLabs Scribe), puis **découper** le script au mot près (03).
2. **Choisir le visuel** de chaque phrase (02).
3. **Caler** chaque élément sur son mot (03).
4. **Placer le personnage** (04).
5. **Écrire le storyboard**, le **vérifier** avec `check_storyboard.py` (05).
6. **Construire les scènes** avec le design system, **rendre** avec HyperFrames (05).

Les chiffres (rythme, fréquence) sont des valeurs de départ, à recaler sur les premières vidéos publiées.
