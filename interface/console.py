from core.decision_engine import DecisionEngine
from core.memory import Memory
from learning.feedback import learn

def start_console():
    memory = Memory()
    engine = DecisionEngine()

    print("ARIA est active. Tape 'exit' pour quitter.\n")

    while True:
        user_input = input("Toi : ")
        if user_input.lower() == "exit":
            break

        response = engine.decide(user_input, memory)
        print("ARIA :", response)

        feedback = input("Réponse correcte ? (oui/non) : ")
        if feedback.lower() == "non":
            correction = input("Quelle aurait été la bonne réponse ? ")
            learn(memory, user_input.lower(), correction)