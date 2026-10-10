# Choisir le visuel

Pour chaque phrase : trouver le cas ci-dessous, puis l'objet réel le plus concret. Les fiches des composants (props, rendu) sont dans le [design system abdoul.dev](https://claude.ai/artifact/KpGSYjQxzaakj89X4J8t9e).

## Les 3 niveaux d'illustration

| Niveau | Quand | Exemples | Composants |
| --- | --- | --- | --- |
| Sticker | Personnage, objet physique ou lieu à reconnaître | avatar, bâtiment, boutique, billets | Sticker |
| Tuile ou ligne | Nom simple, canal, marque, outil | e-mail, réseaux, Ubersuggest | Tile, ToolRow, YouBlock |
| Interface ou schéma | Action concrète ou relation entre idées | Google, pub, chat, plan, détour | Window, GoogleResults, SearchBar, Chat, Counter, AdWindow, CodeEditor, MapPins, Detour, Referrer, BarChart |

## Cas de phrase → composant

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
| montre une page, un produit | Window |
| parle de référencement | GoogleResults, SearchBar |
| parle d'un contact, d'un message | Chat |
| parle d'audience | Counter |
| parle de payer pour être vu | AdWindow |
| parle de code | CodeEditor |
| énonce le principe « va où est ta cible » | MapPins (motif récurrent) |
| parle de détourner | Detour |
| parle d'apporteur, de commission | Referrer |
| parle de croissance, d'effet | BarChart |
| désigne une cible dans une foule | PeopleRow |
| donne une quantité à remplir | Grid100 |
| pose un calcul | CalcCards |
| s'adresse à « toi » dans un schéma | YouBlock |
| montre une app sur mobile | PhoneScreen, AppStoreCard |
| annonce un résultat qui tombe | Notification |
| parle de fiche, de référencement local | BusinessCard |
| compare deux choses | Versus |
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
| conclut | EndCard |
| lie sans contenu (« alors », « en fait ») | rien de nouveau : seul Caption change |

**Un exemple** se raconte en 3 temps : qui (Tile ou Sticker) → comment (interface avec LE détail) → résultat (BigNumber, Counter ou avatar). **Une liste d'exemples** s'empile (ToolRow, Tile), 1 par seconde, sans détail.

## Où trouver un asset

Dans cet ordre :

1. Un composant du design system.
2. Une icône Flat Icons recolorée (style : Iconographie du design system).
3. **Le logo officiel** si une marque est citée : obligatoire, jamais remplacé. Introuvable : « LOGO REQUIS », le rendu est bloqué.
4. Sinon (objet ou lieu, jamais une marque) : un sticker 3D généré avec le prompt du design system, ajouté aux assets ; jamais deux fois le même objet.

Aucun composant ne colle : en construire un selon « Construire un composant qui manque » du design system, puis l'y ajouter pour qu'il serve aux vidéos suivantes.
