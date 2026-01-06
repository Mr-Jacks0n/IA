import difflib
import re
from core.skills import SkillSet, SKILL_MAP
from core.reflection import ReflectionEngine
from config import debug_print

class DecisionEngine:
    def __init__(self, memory):
        self.memory = memory
        self.skills = SkillSet()
        self.reflection = ReflectionEngine(memory)
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
        # Cherche si l'input contient principalement des chiffres et opérateurs
        if any(char in text for char in '+-*/()') and re.search(r'\d', text):
            # Nettoie l'input pour extraire l'expression
            expression = re.sub(r'[^\d\+\-\*\/\(\)\.\s]', '', text)
            if expression.strip():
                calc_result = self.skills.calculate(expression.strip())
                self.reflection.add_to_memory(user_input, calc_result)
                reflection = self.reflection.reflect(user_input, calc_result)
                if reflection:
                    calc_result += " " + reflection
                return calc_result

        # 4. CONTEXTE : Résumer la conversation récente
        if "résume" in text or "contexte" in text:
            return self.reflection.get_context_summary()

    def advanced_reasoning(self, user_input):
        """Raisonnement avancé : chaînage logique basé sur les faits."""
        text = user_input.lower()
        facts = self.memory.facts
        
        # Exemple : Si l'utilisateur mentionne une ville et demande la météo
        if "météo" in text or "temps" in text:
            # Chercher si une ville est mentionnée ou stockée
            city = None
            for word in text.split():
                if word[0].isupper():  # Ville souvent en majuscule
                    city = word
                    break
            if not city and "ville" in facts:
                city = facts["ville"]
            
            if city:
                return self.skills.search_web(f"météo {city}")
        
        # Autre exemple : Si nom connu et question personnelle
        if "mon" in text and self.memory.get_fact("user_name"):
            name = self.memory.get_fact("user_name")
            if "âge" in text:
                return f"Je ne connais pas ton âge, {name}."
        
        return None

    def find_best_match(self, user_input):
        """Cherche la meilleure réponse (Règles ou Compétences)."""
        debug_print(f"Input utilisateur : '{user_input}'")
        
        # D'abord, raisonnement avancé
        advanced_response = self.advanced_reasoning(user_input)
        if advanced_response:
            debug_print(f"Raisonnement avancé activé : {advanced_response}")
            self.reflection.add_to_memory(user_input, advanced_response)
            reflection = self.reflection.reflect(user_input, advanced_response)
            if reflection:
                return advanced_response + " " + reflection, "advanced_reasoning"
            return advanced_response, "advanced_reasoning"
        
        # Ensuite, on vérifie si c'est du raisonnement pur
        logic_response = self.analyze_input(user_input)
        if logic_response:
            self.reflection.add_to_memory(user_input, logic_response)
            reflection = self.reflection.reflect(user_input, logic_response)
            if reflection:
                return logic_response + " " + reflection, "logic_event"
            return logic_response, "logic_event"

        # Sinon, on cherche dans la base de règles avec difflib
        rules = self.memory.get_rules()
        known_inputs = list(rules.keys())
        
        # cutoff=0.6 signifie qu'il faut 60% de ressemblance
        matches = difflib.get_close_matches(user_input.lower(), known_inputs, n=1, cutoff=0.6)
        debug_print(f"Matches fuzzy : {matches}")
        
        if matches:
            best_key = matches[0]
            response_template = rules[best_key]
            
            # Vérification : Est-ce une compétence (CMD:) ?
            if response_template.startswith("CMD:"):
                parts = response_template.split(" ", 1)
                cmd_key = parts[0] # Récupère CMD:date
                if cmd_key in SKILL_MAP:
                    method_name = SKILL_MAP[cmd_key]
                    method = getattr(self.skills, method_name)
                    if cmd_key == "CMD:search":
                        # Extraire la query de l'input utilisateur
                        query = user_input.lower().replace("recherche", "").strip()
                        response = method(query) if query else "Quelle est ta question de recherche ?"
                    elif cmd_key == "CMD:open_browser":
                        # Extraire l'URL du template
                        url = parts[1] if len(parts) > 1 else "https://www.google.com"
                        response = method(url)
                    else:
                        response = method()
                    self.reflection.add_to_memory(user_input, response)
                    reflection = self.reflection.reflect(user_input, response)
                    if reflection:
                        response += " " + reflection
                    return response, best_key
            
            self.reflection.add_to_memory(user_input, response_template)
            reflection = self.reflection.reflect(user_input, response_template)
            if reflection:
                response_template += " " + reflection
            return response_template, best_key
        
        # Si rien trouvé
        unknown_response = "Je ne sais pas encore répondre à cela. Apprends-moi."
        self.reflection.add_to_memory(user_input, unknown_response)
        reflection = self.reflection.reflect(user_input, unknown_response)
        if reflection:
            unknown_response += " " + reflection
        return unknown_response, None