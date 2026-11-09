<p align="center">
  <img src="docs/banner.png" alt="ARIA · IA symbolique apprenante" width="100%">
</p>

# ARIA · Intelligence Apprenante Locale

ARIA est une IA **symbolique et adaptative** : un moteur de règles, une
mémoire persistante et une boucle de feedback · aucun LLM, aucun modèle
d'apprentissage automatique, aucun cloud. Elle apprend exclusivement des
conversations que vous avez avec elle et fonctionne **100 % sur votre
machine**.

[![CI (Python 3.10 → 3.12)](https://github.com/Mr-Jacks0n/IA/actions/workflows/python-package.yml/badge.svg)](https://github.com/Mr-Jacks0n/IA/actions/workflows/python-package.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue)

> 🇬🇧 Une version anglaise de ce README est disponible :
> **[README.md](README.md)**

## ✨ Fonctionnalités

- **Apprentissage par règles IF/THEN** · les réponses sont comparées aux
  règles apprises ; chaque entrée inconnue est une occasion d'apprendre
  (`Réponse correcte ?` → nouvelle règle écrite sur disque).
- **Mémoire persistante** · règles, faits, expériences et contexte sont des
  fichiers JSON lisibles et éditables à la main dans `data/`.
- **Compréhension floue** · `difflib.get_close_matches` rattache les
  coquilles et variantes aux règles connues ("qu'elle heure" →
  "quelle heure est-il").
- **Calculs automatiques** · détecte les expressions où qu'elles soient
  ("1550 + 12500" → `Le résultat est : 14050`) via un **évaluateur AST
  sécurisé** (pas de `eval` brut, exposants bornés · voir changelog).
- **Raisonnement sur faits** · « je m'appelle Martin » est mémorisé comme
  un fait et restitué plus tard (« quel est mon nom » →
  « Tu t'appelles martin. »).
- **Recherche web** · « recherche python » déclenche une vraie requête
  DuckDuckGo Instant Answer via `requests` (la seule dépendance réseau).
- **Réflexion** · une mémoire courte terme des derniers échanges donne à
  ARIA des auto-observations : elle signale les réponses inconnues,
  remarque les sujets répétés et pose des questions de relance.
- **Commandes spéciales** · heure/date, ouvrir le navigateur, recherche
  web (mappage `CMD:*` géré par `core/skills.py`).
- **Deux interfaces** · console (fonctionne sans tkinter) et GUI Tkinter.
- **Mode debug** · `--debug` affiche chaque étape de décision : matches
  flous, chargements mémoire, faits.

## 🖼 À quoi ça ressemble

Fenêtre Tkinter réelle, capturée pendant une vraie session · le calcul
«1550 + 12500» et le nom retenu sont des réponses en direct :

<p align="center">
  <img src="docs/gui_screenshot.png" alt="GUI ARIA, session réelle" width="420">
</p>

## 🚀 Démarrage

```bash
git clone https://github.com/Mr-Jacks0n/IA.git
cd IA
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt        # requests est la seule dépendance

python main.py          # mode console
python main.py --gui    # mode graphique (nécessite python3-tk)
python main.py --debug  # console + logs de décision
python utils/clean_data.py   # normalise les clés de règles en minuscules
```

La console fonctionne sur un serveur sans tkinter ; `--gui` affiche
une consigne d'installation claire (`sudo apt install python3-tk`)
si Tk est absent.

## 🗂 Structure du projet

```
.
├── main.py                    # point d'entrée : console | --gui | --debug
├── config.py                  # DEBUG_MODE + utilitaire debug_print
├── core/
│   ├── decision_engine.py     # routage : raisonnement → logique → règles → inconnu
│   ├── rules.py               # DEFAULT_RULES (règles initiales)
│   ├── memory.py              # mémoire JSON persistante (règles/faits/contexte)
│   ├── reflection.py          # mémoire courte terme + auto-observations
│   └── skills.py              # date, calculatrice (AST sûr), recherche web, navigateur
├── interface/
│   ├── console.py             # REPL + boucle de feedback oui/non
│   └── gui.py                 # fenêtre de chat Tkinter
├── learning/feedback.py       # learn(règle) → Memory.add_rule
├── utils/clean_data.py        # normalise les clés de règles
├── data/*.json                # état persistant (valeurs par défaut fournies)
├── docs/                      # bannière + capture GUI réelle
└── .github/                   # CI + templates issues/PR
```

## 🧪 Qualité & CI

Chaque push exécute une **CI sur 3 versions (Python 3.10 → 3.12)** qui :

1. lint le code (flake8, bloquant),
2. lance une **session console scriptée** (accueil → confirmation
   d'apprentissage → calcul → mémorisation du nom → rappel → commande
   date → sortie propre) et vérifie les réponses exactes attendues,
3. lance ARIA depuis un autre répertoire courant pour garantir que les
   chemins de `data/` sont ancrés à la racine du projet,
4. échoue si un `__pycache__/*.pyc` se glisse à nouveau dans l'index.

## 📜 Historique des versions

- **1.0.0** · moteur de règles, fuzzy matching, mémoire persistante,
  apprentissage par feedback, faits, réflexion, recherche web, GUI.
- **1.1.0** · passe de fiabilité : correction du moteur de réflexion qui
  comparait un échange à lui-même, du routage de recherche web jamais
  déclenché, d'un DoS `eval()` dans la calculatrice, de la dépendance
  dure à tkinter et des chemins relatifs au CWD.
  Voir [CHANGELOG.md](CHANGELOG.md).

## 🗺 Feuille de route

- [ ] Schémas de faits plus riches (âge, ville, préférences) +
      raisonnement en relance
- [ ] Apprentissage multi-réponses : garder plusieurs candidats par règle
- [ ] Normalisation des accents avant le fuzzy matching
- [ ] Export/import de la mémoire en « kit de connaissances » partageable
- [ ] Entrée vocale via `speech_recognition` (dépendance optionnelle)

## 🤝 Contribuer

Issues et PRs bienvenues · voir [CONTRIBUTING.md](CONTRIBUTING.md).
Des templates sont fournis pour les bugs, les idées et les pull requests.

## ⚖️ Licence

[MIT](LICENSE) · © 2026 Mr Jackson.
