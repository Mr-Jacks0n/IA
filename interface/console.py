import sys

from config import VERSION, DEBUG_MODE
from core.decision_engine import DecisionEngine
from core.memory import Memory, MemoryRefused

# Routes où une correction d'apprentissage crééait un doublon trompeur
# (réponse générée par une compétence dédiée ou une garde) : le
# feedback de correction n'a de sens que pour les règles apprises.
_LEARNABLE = ('rules.fuzzy', None)

# Couleurs ANSI : réservées à un terminal réel. La session CI scriptée
# passe par un pipe : couleur coupée, les greps restent fiables.
_IS_TTY = bool(getattr(sys.stdout, 'isatty', None) and sys.stdout.isatty())
_GOLD = '\033[38;5;178m' if _IS_TTY else ''
_DIM = '\033[2m' if _IS_TTY else ''
_RST = '\033[0m' if _IS_TTY else ''

_AIDE = """\nCommandes : aide · stats · audit · exit
Exemples de demandes :
  · quelle heure est-il · calendrier · heures du monde
  · convertis 5 km en miles · convertis 30 C en F
  · ajoute la tâche réviser la doc · termine la tâche 1
  · lance un dé · pile ou face · génère une valeur aléatoire
  · inspecte le fichier config.py · aperçu du fichier x.csv
  · analyse le texte … · journal · bilan
  · je m'appelle … · quel est mon nom · oublie …
  · recherche python
La question « Réponse correcte ? » ne se pose que pour les règles apprises.
"""


def _banner(memory):
    try:
        from core.catalog import SkillCatalog
        count = len(SkillCatalog().skills)
    except Exception:
        count = '?'
    print(f"{_GOLD}ARIA v{VERSION} · IA symbolique apprenante{_RST}")
    print(f"{_DIM}  {count} compétences · {len(memory.rules)} règles · "
          f"mémoire 100 % locale · tapez 'aide'{_RST}")
    print("ARIA est active. Tape 'exit' pour quitter.\n")


def start_console():
    memory = Memory()
    engine = DecisionEngine(memory)
    _banner(memory)

    while True:
        try:
            user_input = input("Toi : ").strip()
        except (EOFError, KeyboardInterrupt):
            memory.save_context()
            break
        if user_input.lower() in ("exit", "quitte", "au revoir"):
            memory.save_context()
            print(f"{_GOLD}ARIA :{_RST} Au revoir ! Contexte sauvegardé.")
            break

        low = user_input.lower()
        if low == "aide":
            print(_AIDE)
            continue
        if low == "stats":
            from main import run_stats
            run_stats()
            continue
        if low == "audit":
            from main import run_audit
            run_audit()
            continue

        response, route = engine.find_best_match(user_input)
        print(f"{_GOLD}ARIA :{_RST}", response)
        if DEBUG_MODE and engine.last_trace:
            print("  ⤷", engine.last_trace[0])

        if route not in _LEARNABLE:
            continue
        try:
            feedback = input("Réponse correcte ? (oui/non/exit) : ")
        except (EOFError, KeyboardInterrupt):
            memory.save_context()
            break
        if feedback.strip().lower() == "exit":
            memory.save_context()
            break
        if feedback.strip().lower() == "non":
            try:
                correction = input("Quelle aurait été la bonne réponse ? ").strip()
                if response.lower().strip() != correction.lower().strip():
                    _learn(engine, user_input, correction)
                    print(f"{_GOLD}ARIA :{_RST} Noté · je ferai mieux.")
                else:
                    print(f"{_GOLD}ARIA :{_RST} ok, rien à corriger.")
            except MemoryRefused as exc:
                print(f"{_GOLD}ARIA :{_RST} ⛔ je n'ai pas appris "
                      f"cette règle : {exc}")


def _learn(engine, question, correction):
    from learning.feedback import learn
    learn(engine.memory, question.lower(), correction)
