# Caler sur la voix

## Découper

- La voix (enregistrée par Abdoul) est horodatée au mot avec ElevenLabs Scribe : `ELEVENLABS_API_KEY=… python3 scribe_words.py voix.mp3 mots.json script.txt`. Le script recale la transcription sur le texte exact ; les mots marqués `guess` se vérifient à l'écoute.
- Une phrase = une scène possible.
- **Mots déclencheurs** : les noms, chiffres, marques, et « toi / ton / ta ». Chacun peut faire apparaître ou changer un élément.
- **Mots de liaison** (« alors », « en fait », « donc », « du coup ») : rien de nouveau, seul le sous-titre change.

## Synchroniser

- Un élément apparaît au **début du mot qui le nomme, 0,08 s avant** (2 images d'anticipation à 30 i/s).
- Le contenant arrive juste avant son contenu (la fenêtre, puis le texte tapé).
- Texte tapé à ≈ 25 caractères par seconde ; nombres qui défilent en 0,8 s (vitesses définies dans Motion du design system).
- Le sous-titre suit la voix phrase par phrase ; le mot dit en ce moment peut passer en accent.

## Rythme

- Un nouvel élément ou un changement d'état toutes les **0,8 à 1,5 s**.
- Rien de figé plus de **2,5 s** (un texte en train de se taper compte comme du mouvement).

## Continuer ou couper

- **Même idée** : le composant reste et change d'état (rang, coche, chiffre, barre, épingle qui se rapproche).
- **Idée nouvelle** : coupe franche, en général toutes les **3 à 6 s**.
- Un motif récurrent (MapPins « va où est ta cible ») revient au début, au milieu et à la fin.

## Son

- « Tap » sur Chapter, pop discret sur PunchTitle et à chaque apparition du personnage.
- Jamais de son de transition (whoosh, swipe, swoosh) aux changements de scène : un son marque un objet qui apparaît, pas le passage d'une scène à l'autre.
- Musique très basse sous la voix.
