# LogoSlot

Le logo officiel d'une marque citée, et rien d'autre.

## Règle absolue
- Une marque citée = son **vrai logo**, fichier officiel (SVG de préférence, sinon PNG transparent), couleurs et proportions d'origine.
- Interdit : une initiale, une icône générique, un logo redessiné, recoloré ou généré par IA.
- Logo introuvable : l'emplacement reste en `.lg.miss` (hachuré rouge « LOGO REQUIS »). **La vidéo ne s'exporte pas** tant qu'il en reste un.

## Où prendre le logo
1. La page presse ou « brand » officielle de la marque.
2. Le site officiel (favicon haute définition, fichier SVG).
3. Le store officiel (icône de l'app, App Store ou Google Play).
Le fichier est ensuite ajouté au groupe d'assets Logos sous le nom de la marque (`ubersuggest.svg`) et réutilisé.

## Mise en forme
- `.lg.real` avec une balise `img` du fichier : fond blanc, marge 4, le logo n'est jamais déformé (`object-fit: contain`).
- Taille 40 dans une ligne (ToolRow), 56 à 80 dans une tuile (Tile).
- Le nom de la marque à côté, écrit comme la marque l'écrit.

## Utilisée par
ToolRow, Tile, AppStoreCard, et tout composant qui cite une marque.
