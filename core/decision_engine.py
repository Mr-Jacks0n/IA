import difflib
import re
from core.skills import SkillSet, SKILL_MAP

class DecisionEngine:
    def __init__(self, memory):
        self.memory = memory
        self.skills = SkillSet()
        # Contexte temporaire (mémoire courte durée)
        self.context = {}

    def analyze_input(self, user_input):
        """Analyse l'entrée pour détecter des commandes ou des faits."""
        text = user_input.lower().strip()

        # 1. RAISONNEMENT : Détection de patterns (Ex: "Je m'appelle X")
        if "je m'appelle" in text:
            name = text.split("je m'appelle")[-1].strip()
            self.memory.save_fact("user_name", name) # On sauvegarde dans la mémoire persistante
            return f"Enchanté {name}, je m'en souviendrai."

        # 2. RAISONNEMENT : Utilisation de la mémoire (Ex: "Quel est mon nom ?")
        if "mon nom" in text or "comment je m'appelle" in text:
            name = self.memory.get_fact("user_name")
            if name:
                return f"Tu t'appelles {name}."
            else:
                return "Je ne connais pas encore ton nom."

        # 3. CALCUL : Détection automatique de calculs (ex: "calcule 5+5" ou juste "5+5")
        if re.match(r'^[\d\s\+\-\*\/\(\)\.]+$', text):
            return self.skills.calculate(text)

        if text.startswith("calcule "):
            expression = text.replace("calcule ", "")
            return self.skills.calculate(expression)

        return None

    def find_best_match(self, user_input):
        """Cherche la meilleure réponse (Règles ou Compétences)."""
        
        # D'abord, on vérifie si c'est du raisonnement pur
        logic_response = self.analyze_input(user_input)
        if logic_response:
            return logic_response, "logic_event"

        # Sinon, on cherche dans la base de règles avec difflib
        rules = self.memory.get_rules()
        known_inputs = list(rules.keys())
        
        # cutoff=0.6 signifie qu'il faut 60% de ressemblance
        matches = difflib.get_close_matches(user_input.lower(), known_inputs, n=1, cutoff=0.6)
        
        if matches:
            best_key = matches[0]
            response_template = rules[best_key]
            
            # Vérification : Est-ce une compétence (CMD:) ?
            if response_template.startswith("CMD:"):
                cmd_key = response_template.split(" ")[0] # Récupère CMD:date
                if cmd_key in SKILL_MAP:
                    method_name = SKILL_MAP[cmd_key]
                    method = getattr(self.skills, method_name)
                    return method(), best_key
            
            return response_template, best_key
        
        return None, None