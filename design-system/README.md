# abdoul.dev

Le système des vidéos explainer d'abdoul.dev (TikTok, Reels, Shorts, 9:16). Style **brutal papier, coins très arrondis** : fond papier quadrillé, blocs blancs à contour noir épais et ombre dure, un seul rouge accent pour ce dont la voix parle. **Chaque phrase devient un objet réel et concret ; le texte à l'écran se limite au sous-titre et aux étiquettes.**

Construit à partir de l'analyse de 5 vidéos de @ledevultime (Clients, Code, SaaS, SEO, Société) : mêmes cadrages, mêmes tailles, même logique ; habillage propre à abdoul.dev.

Ce système dit **ce que sont les pièces et à quoi elles ressemblent**. Quand et comment les utiliser dans une vidéo (choix du visuel, calage sur la voix, personnage, storyboard, rendu) : règles vidéo abdoul.dev, skill `abdoul-dev-video`.

## Fondations visuelles
- **Canevas** : 360 × 640 unités ; le rendu 1080 × 1920 multiplie tout par 3. Contenu centré au milieu ; rien sous y 560 (interface TikTok), sauf l'avatar.
- **Couleurs** : `paper` + quadrillage `grid-line` (pas de 12), blocs `tile`, contours et texte `ink`, `accent` rouge, `yes` / `no` pour les signes et chiffres seulement.
- **Blocs** : contour `border-frame` (3), ombre `shadow-hard` (4/4, sans flou), coins `radius-card` (22) ; étiquettes et boutons en pilule `radius-pill`.
- **Typo** : Satoshi partout (Black 900 pour les titres, Bold 700 pour le sous-titre), JetBrains Mono pour le code. Capitales pour les étiquettes et cartes. Fichiers dans `fonts/` : Satoshi Medium 500, Bold 700, Black 900 (Fontshare, ITF Free Font License, usage commercial libre).
- **Mise en page** : tout centré ; blocs pleine largeur à `space-edge` (30) des bords, lignes espacées de `space-row` (12).

## Organisation du système
Trois niveaux, du plus petit au plus grand :

1. **Briques** (17) : les pièces de base, sans contenu propre. Card, Tag, Badge, Button, WindowBar, TextLine, Bubble, Input, Checkbox, Mark, Arrow, Pin, Icon, LogoSlot, ProgressBar, Stars, Heading.
2. **Composants de scène** (50) : des assemblages de briques prêts à l'emploi, chacun lié à un cas de phrase. Chaque fiche liste ses briques.
3. **Règles d'assemblage** (ci-dessous) : de quoi fabriquer un composant qui manque sans sortir du style.

**Inventaire des composants de scène.**
Texte : Caption, PunchTitle, BigNumber.
Structure : Chapter, Slots, BadgeList, StepsChecklist, EndCard.
Cartes : LabelStack, ToolRow, CalcCards, Versus, PriceTable, GoalProgress, FeaturePriority, TodoList.
Interfaces : Window, GoogleResults, SearchBar, Chat, Counter, AdWindow, CodeEditor, PhoneScreen, Notification, BusinessCard, ReviewCard, EmailCard, WireframePages, AnalyticsBoard, AppStoreCard, SocialPost.
Schémas : MapPins, Detour, Referrer, BarChart, SplitShare, Timeline, Funnel, Donut, FlowStack, Network.
Objets : Tile, PeopleRow, Grid100, YouBlock, Calendar, Keyboard, FlagRow.
Personnages : Sticker.

## Règles d'assemblage
- **Tout est centré.** Le groupe sous-titre + visuel a son centre au milieu de l'écran (x 180, y 320) ; quand le personnage est à l'écran, au milieu de l'espace au-dessus de lui (y 190). Rien sous y 560 (interface TikTok) sauf l'avatar ; un même composant qui revient garde sa position (pas de saut entre deux scènes) ; les blocs sont centrés sur l'axe vertical (pleine largeur : x 30 à 330). Rien n'est calé à gauche ou à droite, sauf à l'intérieur d'une carte (texte, badges). Seul l'avatar reste ancré en bas. Dans le code : le contenu va dans `.ad-stage`, décalé par `--dx` / `--dy` pour centrer son cadre.
- **Espacements verticaux** : sous-titre, puis 62 jusqu'au visuel.
- **Largeurs** : 300 (pleine), 144 + 12 + 144 (2 colonnes), 92 + 12 + 92 + 12 + 92 (3 colonnes), tuile carrée 100 à 140. Lignes de liste : 36 à 40 de haut, espacées de 12.
- **Hiérarchie** : 1 titre de bloc en capitales (card-label), du contenu réel au centre, des lignes simulées pour le reste.
- **Couleur** : un seul élément accent pour ce dont la voix parle ; yes / no seulement pour les signes et chiffres ; logos et objets réels gardent leurs couleurs.
- **Tailles par famille** (tokens `size`) : puce dans une interface 22 (`control-xs`), étiquette de scène / bouton / champ en ligne 28 (`control-sm`), ligne de liste à une ligne / champ de saisie / bouton principal d'un écran 36 (`control-md`), ligne à deux niveaux 52 (`control-lg`). Deux éléments de la même famille ont toujours la même hauteur, quel que soit le composant.
- **Maquettes d'appareil** (PhoneScreen) : 200 × 390, écran à 14 de marge intérieure ; le contenu de l'écran ne touche jamais la coque.
- **Espacements internes** : une carte se monte en colonne (flex), jamais en positions absolues. Marge intérieure 14 (20 pour une carte schéma), 14 entre deux groupes, 6 entre un libellé et ce qu'il annonce, 10 entre une icône ou un logo et son texte. Une ligne de liste fait 40 à 44 de haut. Étiquettes (Tag) et boutons : marge latérale 14 au moins, texte sur une ligne, largeur donnée par le texte (jamais une largeur fixe qui serre le texte contre le bord). La carte épouse son contenu : pas de hauteur fixe, pas de vide en bas ; ce qui arrive plus tard dans la voix agrandit la carte à la scène suivante.
- **Matière** : toute surface est une Card (contour 3, ombre dure 4/4, rayon 22) ou une pilule (Tag, Button) ; à l'intérieur d'une fenêtre, contours 2 et pas d'ombre.
- **Texte** : jamais de faux texte lisible ; un vrai mot ou une TextLine. Pas plus de 6 mots lisibles par bloc hors bulles.
- **Apparition** : un élément par mot qui le nomme (data-d dans l'ordre de la voix) ; le contenant juste avant son contenu.
- **Évolution** : un composant reste et change d'état (rang, coche, barre, chiffre) tant que l'idée dure.

## Construire un composant qui manque
Quand une phrase demande un visuel absent du système :

1. **Nommer l'objet réel** que la phrase désigne (une fiche, un ticket, un panier, un contrat…). S'il existe dans la vraie vie, on le montre ; sinon, on choisit une métaphore spatiale simple (pile, flèche, réseau, entonnoir).
2. **Partir du composant le plus proche** de la même famille (une fiche ressemble à Window, un ticket à Card + TextLine…).
3. **N'assembler que des briques**, avec les largeurs ci-dessus, et **centrer le groupe** sur le canevas. Pas de nouvelle couleur, pas de nouvelle ombre, pas de nouveau rayon.
4. **Mettre LE détail qui prouve** : un vrai texte, un vrai chiffre, « TOI » ou « TON … » quelque part.
5. **Choisir l'accent** : l'élément dont parle la voix, un seul.
6. **Décider l'ordre d'apparition** sur les mots du script, et ce qui évolue ensuite.
7. **Illustration impossible avec les briques** (un objet physique précis) : Sticker 3D généré avec le prompt ci-dessous, ajouté aux assets.
8. **L'ajouter au système** : dossier `components/<Nom>/` avec preview.html et README.md (Quand, Règles, À fournir, Briques), pour qu'il soit réutilisé.

Exemple : BusinessCard (fiche d'établissement) = WindowBar (« MA FICHE » + icône boutique) + Heading (nom en capitales) + Stars + Tag accent pour les mots-clés retenus, Tag blanc pour les autres. Aucune pièce nouvelle.

## Iconographie
Icônes au trait `ink`, épaisseur 7 sur 100, bouts arrondis, **une seule forme remplie en `accent`** (la tête d'une personne, le cœur). Source : Flat Icons, recolorées. Pas d'emoji.

**Logos : toujours le vrai.** Une marque citée se montre avec son logo officiel (fichier SVG ou PNG transparent), couleurs et proportions d'origine, via la brique LogoSlot. Jamais d'initiale, d'icône générique, de logo redessiné ou généré par IA. Logo introuvable : l'emplacement reste « LOGO REQUIS » en rouge et la vidéo ne s'exporte pas. Chaque logo récupéré rejoint le groupe d'assets Logos et sert ensuite à toutes les vidéos.

**Stickers 3D** (objet ou lieu, jamais une marque) : générés avec ce prompt, puis ajoutés aux assets.

```text
A single [OBJECT], stylized 3D cartoon render, clean rounded shapes, soft matte shading, three-quarter view,
limited palette: white, warm light grey, ink #121212 and red #B70000 as the only accent.
Transparent background, no outline, no shadow, no text, centered with empty space around.
```

## Le personnage
- Une seule identité (image de référence), déclinée en poses WebP transparentes qui ont déjà leur liseré ; Sticker ajoute l'ombre (classe `sticker edged`).
- Ancré en bas, coupé par le bord. Tête seule pour une réaction, buste pour un geste.
- 40 poses dans le groupe Avatar. Gestes : point, explain, count, present, thumbs_up, thumbs_down, arms_crossed, facepalm, shrug, think, idea, arms_up, stop, whisper, wave, hands_heart, money, empty_pockets (en pied), stopwatch, laptop, phone, chart_up. Réactions, tête seule : shocked, angry, laugh, sad, star_eyes, heart_eyes, skeptical, mind_blown. Compter : count_1 à count_10.
- Pose absente : génération IA depuis l'image de référence, détourage, nouvelle clé en anglais minuscule, ajout au groupe Avatar.

## Motion
- Apparition : montée de 12 + échelle 0,86 → 1, 0,3 s avec léger rebond.
- Coupes franches entre les scènes ; rien ne bouge entre deux événements.
- Texte de fenêtre tapé à ≈ 25 caractères par seconde ; nombres qui défilent en 0,8 s.

---

## Consuming this system (generated — do not edit)

Every path named below is under `project/` in this design system: read `project/api/tokens.md`, not `api/tokens.md`.

67 components are documented without a runnable `components/bundle.js`: read each component’s card, and its README where it has one (`components/<Comp>/README.md`), and build to those guidelines. Tokens: the values are on `api/tokens.md`; a Slides deck or Design canvas also takes `tokens.json` by file path.

**Read, per thing:** a component’s props, parts and examples: `api/components/<Comp>.md`; token values: `api/tokens.md`; stored assets and their paths: `api/assets/<Group>.md`. After this README, fetch the cards and fonts you need in ONE message as parallel calls — none depends on another.

**Two rules.** Before you use a thing — a component, a token group, an icon, an asset — read its card from the index below; a value you did not read from a card is a guess. `tokens.json`, `manifest.json` and `design-system.json` are sources for tools: hand them over. `components/<Comp>/README.md` and `assets/<Group>/README.md` are the long-form second read a card links to; `SKILL.md` and `artifact-type/` beside them are authoring guidance, not needed to consume the system.

## Index (generated — do not edit)

**Tokens**

- `api/tokens.md` — Every token: surface, text, fill, palette, type, spacing, radius, shadow, border. (5.8k)

**Icons and assets**

- `api/assets/Avatar.md` — 1 file, by asset id. (1.0k)

**Components** (`api/components/<Comp>.md`, 67)

- **Interfaces**: `AdWindow` — Fenêtre pub : l'audience d'un créateur, « VOTRE PUB », clic sur payer · `AnalyticsBoard` — Un tableau de bord : visites, inscrits, clients · `AppStoreCard` — La fiche d'une app dans le store · `BusinessCard` — La fiche d'établissement (Google Business) : nom, note, mots-clés · `Chat` — Chat / message : les bulles arrivent une à une ; la tienne en couleur · `CodeEditor` — Éditeur de code : le code se tape ligne à ligne ; la valeur clé en couleur · `Counter` — Compteur d'abonnés : le chiffre défile, le bouton passe à « Suivi » · `EmailCard` — Un e-mail : expéditeur, objet, et LE détail en bas · `GoogleResults` — Résultats Google : « TON SITE » surligné ; le rang et la page évoluent avec la voix · `Notification` — Une notification push qui tombe : vente, client, message · `PhoneScreen` — Un smartphone : l'app, l'écran d'accueil, ce que la cible voit · `ReviewCard` — Des avis clients avec leur note · `SearchBar` — Barre de recherche : le mot-clé se tape, l'autocomplétion apparaît · `SocialPost` — Une publication de réseau social et ses réactions · `Window` — Fenêtre de navigateur : fausse URL, le nom du produit et LE détail qui prouve · `WireframePages` — Des maquettes d'écrans côte à côte
- **Briques**: `Arrow` — La flèche qui relie deux blocs : cause, transfert, détour · `Badge` — Le petit carré numéroté ou coché qui ouvre une ligne · `Bubble` — La bulle de message ou de commentaire · `Button` — Le bouton d'interface : Payer, Suivre, Obtenir, Valider · `Card` — Le bloc de base : fond tile, contour noir, coins arrondis, ombre dure · `Checkbox` — La case à cocher d'une liste de tâches ou d'une option · `Heading` — Les textes de scène : sous-titre, titre choc, gros chiffre, étiquette de carte · `Icon` — Le jeu d'icônes : trait noir, une seule forme accent · `Input` — Le champ de saisie et la barre de recherche · `LogoSlot` — Le logo officiel d'une marque citée, et rien d'autre · `Mark` — Les signes de verdict : coche verte, croix rouge, barré · `Pin` — L'épingle de carte : une cible, toi · `ProgressBar` — La barre qui se remplit : un objectif, un taux · `Stars` — La note en étoiles · `Tag` — L'étiquette en pilule : une question, un état, un nom posé sur un objet · `TextLine` — Les lignes simulées qui remplissent une interface sans texte à lire · `WindowBar` — La barre de titre qui transforme une carte en fenêtre d'application
- **Structure**: `BadgeList` — Liste à badges : une ligne de plus par élément cité · `Chapter` — Carte « Numéro » : ouvre chaque chapitre ; une sous-étiquette au besoin · `EndCard` — Fin « Abonne-toi » : plein écran accent, puis carte de la plateforme · `Slots` — Grille de cases : le nombre annoncé devient N cases · `StepsChecklist` — Sommaire qui se coche : revient entre les parties ; ce qui est fait est coché
- **Schémas**: `BarChart` — Graphique : les barres montent mot après mot · `Detour` — Flèche de détournement : l'usage habituel est barré, le détour part vers toi · `Donut` — Une part d'un tout en pourcentage · `FlowStack` — Une hiérarchie qui découle : principe → méthodes → techniques · `Funnel` — Un entonnoir : combien passent d'une étape à la suivante · `MapPins` — Plan + épingles : le principe : va où est ta cible ; TOI se rapproche · `Network` — TOI au centre d'un réseau de partenaires · `Referrer` — Schéma apporteur : quelqu'un t'apporte un client, tu lui verses une commission · `SplitShare` — Une répartition entre deux personnes : parts, bénéfices · `Timeline` — Des étapes dans le temps, de gauche à droite
- **Texte**: `BigNumber` — Gros chiffre : un montant seul, très grand, avec son sens dessous · `Caption` — Sous-titre karaoké : 2 à 4 mots au-dessus du visuel, le mot prononcé en couleur · `PunchTitle` — Titre choc : remplace le sous-titre sur les mots martelés, en 2 temps
- **Cartes**: `CalcCards` — Cartes de calcul : le calcul se pose sous les yeux : + / − / = · `FeaturePriority` — Une liste longue réduite à l'essentiel · `GoalProgress` — Un objectif et l'avancement vers lui · `LabelStack` — Étiquette + pile de cartes : une étiquette pose la question, les cartes répondent · `PriceTable` — Des offres et leurs prix, l'offre conseillée mise en avant · `TodoList` — Une liste de tâches qui se cochent · `ToolRow` — Ligne outil : logo + nom de l'outil cité ; barré quand on l'écarte · `Versus` — Deux choses comparées côte à côte
- **Objets**: `Calendar` — Un mois, une date précise, une régularité · `FlagRow` — Des drapeaux : des pays, des marchés · `Grid100` — Grille de 100 : une quantité qu'on remplit · `Keyboard` — Un clavier : taper, une lettre, un raccourci · `PeopleRow` — Rangée de personnes : une foule, une seule en couleur : ta cible · `Tile` — Tuile icône + label : un objet simple, une marque ou une catégorie, le mot dans la tuile · `YouBlock` — Bloc « TOI » : le spectateur placé dans le schéma
- **Personnages**: `Sticker` — Avatar (sticker) : une pose par émotion, ancrée en bas, coupée par le bord
