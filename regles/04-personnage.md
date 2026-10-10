# Le personnage

Les poses disponibles, leur cadrage et leur rendu (classe `sticker edged`) sont dans le [design system abdoul.dev](https://claude.ai/artifact/KpGSYjQxzaakj89X4J8t9e), groupe Avatar.

## Quand il apparaît

L'accroche, une émotion, un verdict, une adresse directe (« toi »), une anecdote, l'appel à l'action. Il porte l'émotion, souvent avec un accessoire lié au sujet et de l'humour.

## Fréquence

- Environ **une apparition toutes les 8 à 12 s**, **15 à 25 %** du temps d'écran.
- **1 à 4 s** par apparition ; jamais moins de **4 s** entre deux apparitions ; jamais deux fois la même pose de suite.
- Présent dans l'accroche (0 à 3 s) et sur l'appel à l'action.
- Tête seule (réactions) pour une émotion ; buste (gestes) pour une adresse ou une explication ; `count_N` quand la voix dit un numéro (« 3 ») ; accessoire (money, laptop, phone, stopwatch, chart_up) quand la phrase en parle.
- Jamais avec un schéma ou une interface ; possible avec Caption, PunchTitle, BigNumber, une Tile ou EndCard.

## Choisir la pose

| La phrase… | Pose |
| --- | --- |
| interpelle, montre du doigt | point |
| explique, nuance | explain, present |
| compte, annonce un numéro | count_1 … count_10 |
| valide, recommande | thumbs_up |
| rejette, déconseille | thumbs_down, arms_crossed, stop |
| raconte une erreur, un échec | facepalm, sad |
| doute, « ça dépend » | shrug, skeptical, think |
| a l'idée, la solution | idea |
| célèbre un résultat | arms_up, star_eyes, chart_up |
| choque, révèle | shocked, mind_blown |
| confie un secret, une astuce | whisper |
| parle d'argent gagné / perdu | money / empty_pockets |
| parle de temps, de vitesse | stopwatch |
| parle de code, d'app | laptop, phone |
| s'énerve contre une pratique | angry |
| fait rire | laugh |
| remercie, appelle à s'abonner | hands_heart, wave |
| adore un outil, un résultat | heart_eyes |

Jamais deux fois la même pose de suite ; sur une vidéo, varier au maximum. Pose absente : la générer depuis l'image de référence et l'ajouter au groupe Avatar du design system.
