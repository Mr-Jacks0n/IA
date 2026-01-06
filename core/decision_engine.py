import difflib

class DecisionEngine:
    def decide(self, user_input, memory):
        user_input = user_input.lower()
        known_conditions = [rule["condition"] for rule in memory.rules]
        
        # Recherche exacte d'abord
        for rule in memory.rules:
            if rule["condition"] in user_input:
                return rule["action"]
        
        # Fuzzy matching si pas d'exacte
        matches = difflib.get_close_matches(user_input, known_conditions, n=1, cutoff=0.6)
        if matches:
            best_match = matches[0]
            for rule in memory.rules:
                if rule["condition"] == best_match:
                    return rule["action"]
        
        return "Je ne sais pas encore répondre à cela. Apprends-moi."