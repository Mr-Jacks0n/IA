<p align="center">
  <img src="docs/banner.png" alt="ARIA · Symbolic, learning AI" width="100%">
</p>

# ARIA · Local Learnable Intelligence

ARIA is a **symbolic, adaptive AI**: a rule engine, a persistent memory and a
feedback loop · no LLM, no machine learning model, no cloud. It learns
exclusively from the conversations you have with it and runs **100% on your
machine**.

[![CI (Python 3.10 → 3.12)](https://github.com/Mr-Jacks0n/IA/actions/workflows/python-package.yml/badge.svg)](https://github.com/Mr-Jacks0n/IA/actions/workflows/python-package.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue)

> 🇫🇷 Une version française de ce README est disponible :
> **[README.fr.md](README.fr.md)**

## ✨ Features

- **IF/THEN rule learning** · answers are matched against learned rules;
  every unknown input is a teaching opportunity (`Réponse correcte ?` →
  new rule written to disk).
- **Persistent memory** · rules, facts, experiences and context are plain
  JSON files in `data/`, readable and editable by hand.
- **Fuzzy understanding** · `difflib.get_close_matches` maps typos and
  variants to known rules ("qu'elle heure" → "quelle heure est-il").
- **Automatic calculations** · detects expressions anywhere in the input
  ("1550 + 12500" → `Le résultat est : 14050`) through a **safe AST
  evaluator** (no raw `eval`, bounded exponents · see changelog).
- **Fact-based reasoning** · statements ("je m'appelle Martin") are stored
  as facts and later recalled ("quel est mon nom" → "Tu t'appelles martin.").
- **Web search** · "recherche python" triggers a real DuckDuckGo Instant
  Answer query over `requests` (the only network dependency).
- **Reflection** · a short-term memory of the last exchanges gives ARIA
  self-observations: it flags unknown answers, notices repeated topics,
  asks follow-up questions.
- **Special commands** · time/date, open browser, web search
  (skill mapping `CMD:*` handled by `core/skills.py`).
- **Two interfaces** · console (works without tkinter) and Tkinter GUI.
- **Debug mode** · `--debug` prints every decision step: fuzzy matches,
  memory loads, facts.

## 🖼 What it looks like

Real Tkinter window, captured during a genuine session · the "1550 + 12500"
calculation and the remembered name are live answers:

<p align="center">
  <img src="docs/gui_screenshot.png" alt="ARIA GUI, real session" width="420">
</p>

## 🚀 Getting started

```bash
git clone https://github.com/Mr-Jacks0n/IA.git
cd IA
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt        # requests is the only dependency

python main.py          # console mode
python main.py --gui    # graphical mode (needs python3-tk)
python main.py --debug  # console + decision logs
python utils/clean_data.py   # lowercase-normalize saved rules
```

Console works on servers with no tkinter installed; `--gui` prints
an actionable install hint (`sudo apt install python3-tk`) if Tk is absent.

## 🗂 Project structure

```
.
├── main.py                    # entry point: console | --gui | --debug
├── config.py                  # DEBUG_MODE + debug_print helper
├── core/
│   ├── decision_engine.py     # routing: reasoning → logic → rules → unknown
│   ├── rules.py               # DEFAULT_RULES (seed rules)
│   ├── memory.py              # persistent JSON memory (rules/facts/context)
│   ├── reflection.py          # short-term memory + self-observations
│   └── skills.py              # date, calculator (AST-safe), web search, browser
├── interface/
│   ├── console.py             # REPL + oui/non feedback loop
│   └── gui.py                 # Tkinter chat window
├── learning/feedback.py       # learn(rule) → Memory.add_rule
├── utils/clean_data.py        # normalize saved rule keys
├── data/*.json                # persistent state (defaults shipped)
├── docs/                      # banner + real GUI screenshot
└── .github/                   # CI + issue/PR templates
```

## 🧪 Quality & CI

Every push runs a **3-version CI (Python 3.10 → 3.12)** that:

1. lints the codebase (flake8, blocking),
2. runs a **scripted console session** (greet → teach confirmation →
   calculation → name memorization → recall → date command → clean exit)
   and asserts the exact expected answers,
3. launches ARIA from an unrelated working directory to guarantee the
   data paths are anchored to the project root,
4. fails if any `__pycache__/*.pyc` sneaks back into the index.

## 📜 Version history

- **1.0.0** · rule engine, fuzzy matching, persistent memory, feedback
  learning, facts, reflection, web search, GUI.
- **1.1.0** · reliability pass: fixed the reflection engine comparing an
  exchange with itself, the web-search routing that never fired, an
  `eval()` DoS in the calculator, the hard tkinter dependency, and
  CWD-relative data paths. See [CHANGELOG.md](CHANGELOG.md).

## 🗺 Roadmap

- [ ] Richer fact schemas (age, city, preferences) + follow-up reasoning
- [ ] Multi-shot learning: keep several candidate answers per rule
- [ ] Accent/diacritics normalization before fuzzy matching
- [ ] Export/import of a memory as shareable "knowledge pack"
- [ ] Voice input via `speech_recognition` (optional extra)

## 🤝 Contributing

Issues and PRs are welcome · see [CONTRIBUTING.md](CONTRIBUTING.md).
Templates are provided for bugs, ideas and pull requests.

## ⚖️ License

[MIT](LICENSE) · © 2026 Mr Jackson.
