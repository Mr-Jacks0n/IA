# Changelog

Format inspiré de [Keep a Changelog](https://keepachangelog.com/fr/1.1.0/).

## [1.3.1] · 2026-11

### Changed · interfaces
- **Console** : bannière de marque (version, compteur de compétences,
  mémoire), commandes intégrées `aide` · `stats` · `audit`, messages
  « ARIA : » or de marque sur un terminal réel (ANSI), traces de
  routage (`⤷ [route: …]`) réservées au `--debug` · la session scriptée
  CI reste inchangée (les 4 réponses attendues, greps identiques).
- **GUI** : barre de marque or (`#bc9c22`) portant la version et
  « mémoire locale · aucun cloud », zone de chat sombre avec émetteurs
  colorés, barre d'état montrant la route gagnante du dernier tour,
  bouton « Effacer la discussion », géométrie minimale imposée, focus
  de saisie automatique, fenêtres de correction rattachées
  (`transient`), `MemoryRefused` géré.

## [1.3.0] · 2026-11

### Added
- **Catalogue élargi à 14 compétences déclaratives** (de 4) · les
  catégories couvertes rejoignent le quotidien :
  · gestion : `gestion-taches` (liste locale persistée, ajouter /
    lister / terminer) ;
  · documentation : `journal-changements` (ébauche de journal depuis
    l'historique git local, révisable) ;
  · révision : `inspecteur-charte` (scan d'un fichier : tirets
    cadratins, artefacts, littéraux d'identifiant · positions
    seulement, jamais le contenu) ;
  · analyse : `analyse-texte` (mots, uniques, phrases, fréquences),
    `apercu-csv` (colonnes, entête, premières lignes) ;
  · utilities : `convertisseur-unites` (km/mi, m/ft, kg/lb, °C/°F,
    Mo/Go), `fuseaux-horaires` (zoneinfo, 8 villes), `calendrier-mois`
    (grille du mois, jour marqué) ;
  · éléments aléatoires locaux : `generateur-jetons` (module
    `secrets`, affichés · JAMAIS stockés ni mémorisés),
    `tirage-hasard` (dé N faces, pile ou face, 1 à 100).
- Compétences à entrée : le routeur transmet le texte utilisateur aux
  compétences qui l'attendent (`NEEDS_TEXT`), et la mémoire au bilan
  (`NEEDS_MEMORY`).
- Réflexion : les observations suivent leur propre ligne (« 💬 »)
  pour les réponses multi-lignes.
- CI : le smoke vérifie en plus que le catalogue charge 14
  compétences avec 0 invalide.

## [1.2.0] · 2026-11

### Added
- **Catalogue déclaratif de compétences** (`skills/*/SKILL.md`,
  `core/catalog.py`) : chaque compétence vit dans un fichier avec
  frontmatter `name / description / category / risk (none·safe·critical) /
  command / triggers` (déclencheurs explicites). Le catalogue valide la
  cohérence nom-de-dossier, la taille de description, le niveau de risque ·
  les compétences invalides sont listées pour l'audit, jamais chargées.
- **Routeur d'intents à preuve** (`core/router.py`, `core/decision_engine.py`,
  rewire) : les compétences, les heuristiques de raisonnement et les règles
  apprises sont toutes des routes candidates avec un score de confiance ; la
  meilleure route seule est exécutée (lazy), et son choix est traçable
  (`[route: … · risque: … · confiance: …]`, affiché en console, debug possible).
- **Discipline de mémoire** (`core/memory.py`) : jamais un secret en
  mémoire (filtre sur `save_fact` ET `add_rule` · refus explicite), bornes
  d'hygiène (200 faits / 500 règles), toute demande d'effacement explicite
  (« oublie … ») est honorée sans copie cachée, retrieval flou des faits,
  compaction de session (`remember_session`) avec archives de sujets.
- **Masquage en sortie** (`core/decision_engine.py`) : toute valeur
  sensible qui serait renvoyée est masquée ligne à ligne (défense en
  profondeur, au cas où une règle héritée d'une ancienne version en
  contienne une).
- **Auto-audit de sécurité** (`core/selfaudit.py`, `python main.py --audit`)
  : six phases hors ligne · reconnaissance de surface, chasse guidée
  (secrets dans `data/`, appels `eval()/exec()/__import__()`), validation
  reproductible de chaque candidat, sortie structurée `data/findings.json`
  (confirmed / rejected), relecture indépendante de la source, rapport
  neutre. Ajouté comme étape de CI (breakage-détection continue).
- `python main.py --stats` : état mémoire + résumé du catalogue.
- Console : EOF propre (^D) sans traceback, prompt de correction gère le
  refus de discipline (message, pas un crash).

### Changed
- L'apprentissage visible (`Réponse correcte ?`) ne concerne plus que les
  routes « règles apprises » et les inconnues · les réponses de
  compétences dédiées (date, calcul, bilan, garde) ne polluent plus la
  base de règles avec des doublons.

## [1.1.0] · 2026-11

### Fixed
- **Réflexion qui se comparait à elle-même** (`core/reflection.py`) :
  `add_to_memory()` est appelé avant `reflect()` dans le moteur, donc
  « réflexion 2 » comparait l'échange courant **avec lui-même** ·
  « nom » était toujours présent des deux côtés. La réflexion compare
  désormais l'échange courant au **précédent** (`short_term_memory[-2]`).
- **Module Internet jamais déclenché** (`core/decision_engine.py`) :
  la règle `"recherche": "CMD:search"` existait, mais difflib ne matche
  un input complet comme « recherche python » contre la clé
  « recherche » qu'au cutoff 0.6 → jamais. Un routage explicite
  (regex `recherche … / cherche …`) est ajouté **avant** la recherche
  de règles, comme celui de « météo ». Vérifié sur l'API réelle :
  « recherche python » renvoie une vraie réponse DuckDuckGo.
- **Évaluateur de calculs non sécurisé** (`core/skills.py`) : `eval()`
  brut sur l'entrée utilisateur ; la whitelist de caractères autorise
  `*`, donc « 9**9**9 » **figeait le process indéfiniment** (testé :
  timeout). Remplacé par un évaluateur AST qui n'accepte que nombres,
  `+ - * / // % **` unaires, avec une borne anti-DoS sur les exposants.
- **Import tkinter bloquant** (`main.py`) : tkinter est importé au
  début du fichier → le mode console plantait sur une machine sans
  Tk. Import *lazy* : la console fonctionne sans tkinter, et
  `--gui` affiche un message d'installation clair si absent.
- **Chemins relatifs au CWD** (`core/memory.py`, `utils/clean_data.py`)
  : ARIA ne fonctionnait que si le répertoire courant était la racine
  du projet. Tous les chemins `data/` sont ancrés à la racine via
  `__file__` · vérifié en lançant ARIA depuis `/tmp`.
- **Nettoyage du dépôt** : 9 fichiers `__pycache__/*.pyc` versionnés
  retirés de l'index, `.gitignore` cohérent, `data/` réinitialisé aux
  valeurs par défaut (règles initiales, dictionnaires vides) · aucune
  donnée d'apprentissage d'utilisateur n'est publiée.

### Added
- `requirements.txt` explicite (la CI plantait car `requests` n'était
  déclaré nulle part).
- `LICENSE` (MIT), documentation bilingue, captures réelles
  (`docs/banner.png`, `docs/gui_screenshot.png`), templates GitHub,
  CI robuste (Python 3.10–3.12, session console scriptée sans pytest).

## [1.0.0] · 2026-02

### Added
- Version initiale d'ARIA : moteur de règles IF/THEN avec fuzzy
  matching, mémoire persistante JSON, feedback d'apprentissage
  (`Réponse correcte ?`), calculs automatiques, mémoire de faits,
  raisonnement contextuel, réflexion, module Internet, GUI Tkinter,
  mode `--debug`.
