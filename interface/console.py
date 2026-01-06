from core.decision_engine import DecisionEngine
from core.memory import Memory
from core.skills import execute_command
from learning.feedback import learn

def start_console():
    memory = Memory()
    engine = DecisionEngine()

    print("ARIA est active. Tape 'exit' pour quitter.\n")

    while True:
        user_input = input("Toi : ")
        if user_input.lower() == "exit":
            memory.save_context()
            break

        # Gestion du contexte : extraction du nom
        if "je m'appelle" in user_input.lower():
            name = user_input.split("appelle")[-1].strip()
            memory.context["user_name"] = name
            print(f"ARIA : Enchantée {name}, je m'en souviendrai.")
            continue  # Pas de feedback pour cette interaction

        response = engine.decide(user_input, memory)
        
        if response.startswith("CMD:"):
            action = response.split(":", 1)[1]
            print("ARIA :", execute_command(action))
            # Pas de feedback pour les commandes automatiques
        else:
            print("ARIA :", response)

            feedback = input("Réponse correcte ? (oui/non) : ")
            if feedback.lower() == "non":
                correction = input("Quelle aurait été la bonne réponse ? ")
                learn(memory, user_input.lower(), correction)