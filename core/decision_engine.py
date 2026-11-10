from core.router import route_input, Route
from core.catalog import SkillCatalog
from core.skills import SkillSet
from core.reflection import ReflectionEngine
from config import debug_print


class DecisionEngine:
    """Cœur ARIA : routage score-based, plan présenté, résultat vérifié.

    Pipeline de chaque tour :
      1. construire les routes candidates (règles + compétences + logique) ;
      2. choisir la route de meilleure confiance ;
      3. exécuter (lazy : seul le gagnant tourne) ;
      4. VÉRIFIER le résultat (longueur sensée, pas de fuite de secret) ;
      5. mémoriser l'échange (compaction) et réfléchir si utile.

    find_best_match(input) → (réponse, clé) reste l'API publique
    (console + GUI), la clé est désormais le NOM DE ROUTE.
    """

    def __init__(self, memory, catalog=None):
        self.memory = memory
        self.skills = SkillSet()
        self.catalog = catalog or SkillCatalog()
        self.reflection = ReflectionEngine(memory)
        self.last_trace = []      # preuve du dernier routage

    # ── pipeline principal ────────────────────────────────────────
    def respond(self, user_input):
        """Tour complet + trace. Retourne (réponse, nom_route, trace)."""
        winner, all_routes = route_input(
            self.memory, self.catalog, self.skills, user_input)
        self.last_trace = [winner.evidence(winner)] if winner else \
            [f"candidats : {[r.name for r in all_routes]}"]
        debug_print("[route] " + (self.last_trace[0] if winner else "aucune route"))

        if winner is None:
            response = "Je ne sais pas encore répondre à cela. Apprends-moi."
            self._record(user_input, response)
            return response, None, self.last_trace

        response = winner.run()          # exécution lazy du vainqueur
        response = self._verify(response)
        self._record(user_input, response)
        reflechie = self.reflection.reflect(user_input, response)
        if reflechie:
            if "\n" in response:
                response += "\n💬 " + reflechie
            else:
                response += " 💬 " + reflechie
        return response, winner.name, self.last_trace

    def find_best_match(self, user_input):
        """Compatibilité console/GUI : (réponse, clé[, route])."""
        response, route, _ = self.respond(user_input)
        return response, route

    # ── phase de vérification (plan → exécuter → vérifier) ────────
    def _verify(self, response):
        from core.catalog import contains_secret
        if not isinstance(response, str):
            response = str(response)
        text = response.strip()
        # fuite : une valeur secrète qui aurait échappé au filtre
        # d'écriture est masquée à la sortie (défense en profondeur).
        if contains_secret(text):
            text = "\n".join(
                "(masqué : valeur sensible)" if contains_secret(l) else l
                for l in text.splitlines())
        # réponses vides ou erratiques → réponse honnête
        if not text:
            text = "Je n'ai rien trouvé de concluant. Apprends-moi."
        return text

    # ── mémorisation + réflexion ──────────────────────────────────
    def _record(self, user_input, response):
        self.reflection.add_to_memory(user_input, response)
        self.memory.remember_session(user_input, response)
