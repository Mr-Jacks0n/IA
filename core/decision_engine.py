class DecisionEngine:
    def decide(self, user_input, memory):
        user_input = user_input.lower()
        for rule in memory.rules:
            if rule["condition"] in user_input:
                return rule["action"]
        return "Je ne sais pas encore répondre à cela. Apprends-moi."