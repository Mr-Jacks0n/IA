import datetime
import math
import requests

class SkillSet:
    def get_date(self):
        """Retourne la date et l'heure actuelles."""
        now = datetime.datetime.now()
        return f"Nous sommes le {now.strftime('%d/%m/%Y')} et il est {now.strftime('%H:%M')}."

    def calculate(self, expression):
        """Calculatrice sécurisée basique."""
        try:
            # Sécurité : on n'autorise que les chiffres et opérateurs mathématiques
            allowed = set("0123456789+-*/(). ")
            if not set(expression).issubset(allowed):
                return "Je ne peux calculer que des opérations mathématiques simples."
            
            result = eval(expression)
            return f"Le résultat est : {result}"
        except Exception:
            return "Erreur de calcul. Vérifie ta formule."

    def get_weather(self):
        """Simulation météo (nécessiterait une API pour du réel)."""
        # Pour l'instant, c'est statique, mais prêt à être connecté à une API
        return "Je n'ai pas encore accès à Internet, mais regarde par la fenêtre !"

    def search_web(self, query):
        """Recherche simple sur le web via DuckDuckGo Instant Answer API."""
        try:
            url = f"https://api.duckduckgo.com/?q={query}&format=json&no_html=1&skip_disambig=1"
            response = requests.get(url, timeout=10)
            data = response.json()
            
            if data.get("AbstractText"):
                return f"Voici ce que j'ai trouvé : {data['AbstractText']}"
            elif data.get("Answer"):
                return f"Réponse : {data['Answer']}"
            else:
                return "Je n'ai pas trouvé d'information précise. Essaie de reformuler ta question."
        except Exception as e:
            return f"Erreur de connexion Internet : {str(e)}"

# Dictionnaire de mappage pour lier les textes aux fonctions
SKILL_MAP = {
    "CMD:date": "get_date",
    "CMD:meteo": "get_weather",
    "CMD:calc": "calculate",
    "CMD:search": "search_web"
}