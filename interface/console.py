from core.decision_engine import DecisionEngine
from core.memory import Memory, MemoryRefused
from config import set_debug

# Routes où une correction d'apprentissage crééait un doublon trompeur
# (réponse générée par une compétence dédiée ou une garde) : le
# feedback de correction n'a de sens que pour les règles apprises.
_LEARNABLE = ('rules.fuzzy', None)


def start_console():
    memory = Memory()
    engine = DecisionEngine(memory)

    print("ARIA est active. Tape 'exit' pour quitter.\n")

    while True:
        try:
            user_input = input("Toi : ").strip()
        except (EOFError, KeyboardInterrupt):
            memory.save_context()
            break
        if user_input.lower() in ("exit", "quitte", "au revoir"):
            memory.save_context()
            print("ARIA : Au revoir ! Contexte sauvegardé.")
            break

        response, route = engine.find_best_match(user_input)
        print("ARIA :", response)
        if engine.last_trace:
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
                    print("ARIA : Noté · je ferai mieux.")
                else:
                    print("ARIA : ok, rien à corriger.")
            except MemoryRefused as exc:
                print(f"ARIA : ⛔ je n'ai pas appris cette règle : {exc}")


def _learn(engine, question, correction):
    from learning.feedback import learn
    learn(engine.memory, question.lower(), correction)
