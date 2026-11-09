# Changelog

Format inspiré de [Keep a Changelog](https://keepachangelog.com/fr/1.1.0/).

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
