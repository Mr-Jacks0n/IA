from core.decision_engine import DecisionEngine
from core.memory import Memory
from learning.feedback import learn

def start_console():
    memory = Memory()
    engine = DecisionEngine(memory)

    print("ARIA est active. Tape 'exit' pour quitter.\n")

    while True:
        user_input = input("Toi : ")
        if user_input.lower() == "exit":
            memory.save_context()
            break

        response, key = engine.find_best_match(user_input)
        
        if response:
            print("ARIA :", response)
            # Pas de feedback pour les événements logiques ou commandes
            if key != "logic_event" and not response.startswith("Le résultat est") and not "Nous sommes le" in response:
                feedback = input("Réponse correcte ? (oui/non) : ")
                if feedback.lower() == "non":
                    correction = input("Quelle aurait été la bonne réponse ? ")
                    learn(memory, user_input.lower(), correction)
        else:
            print("ARIA : Je ne sais pas encore répondre à cela. Apprends-moi.")
            correction = input("Quelle serait la bonne réponse ? ")
            learn(memory, user_input.lower(), correction)