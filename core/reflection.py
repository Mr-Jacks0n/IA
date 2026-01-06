class ReflectionEngine:
    def __init__(self, memory):
        self.memory = memory
        self.short_term_memory = []  # Liste des derniers échanges

    def add_to_memory(self, user_input, ai_response):
        """Ajoute un échange à la mémoire courte."""
        self.short_term_memory.append({"user": user_input, "ai": ai_response})
        if len(self.short_term_memory) > 5:  # Garde seulement les 5 derniers
            self.short_term_memory.pop(0)

    def reflect(self, user_input, ai_response):
        """Analyse la réponse et ajoute une réflexion si nécessaire."""
        reflection = None

        # Réflexion 1 : Si la réponse est inconnue, proposer d'apprendre
        if "Je ne sais pas" in ai_response:
            reflection = "Je pourrais apprendre cela si tu me le dis."

        # Réflexion 2 : Cohérence avec la mémoire
        if self.short_term_memory:
            last_exchange = self.short_term_memory[-1]
            if "nom" in user_input.lower() and "nom" in last_exchange["user"].lower():
                reflection = "Je me souviens que nous parlions de noms."

        # Réflexion 3 : Auto-évaluation
        if len(user_input.split()) > 10:
            reflection = "Ta question est détaillée, je vais essayer de bien répondre."

        # Réflexion 4 : Poser une question pour approfondir
        if "comment" in user_input.lower():
            reflection = "Pour mieux t'aider, peux-tu me donner plus de détails ?"

        return reflection

    def get_context_summary(self):
        """Résume le contexte récent."""
        if not self.short_term_memory:
            return "C'est le début de notre conversation."
        summary = "Récemment, nous avons parlé de : "
        topics = []
        for exchange in self.short_term_memory[-3:]:
            topics.append(exchange["user"][:20] + "...")
        return summary + ", ".join(topics) + "."