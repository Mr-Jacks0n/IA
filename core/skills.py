import ast
import datetime
import operator
import requests
import webbrowser

# Évaluateur AST : aucun eval() brut sur une entrée utilisateur.
# ⚠️ Ancien code : eval(expression) — la whitelist de caractères
# autorisait '*', donc "9**9**9" (recursif, chiffres autorisés)
# figeait le process indéfiniment (testé : timeout). Un simple
# message pouvait bloquer ARIA.
_BINOPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
}
_MAX_EXPONENT = 100      # borne anti-DoS sur les puissances
_MAX_LENGTH = 100        # borne sur la taille de l'expression


def _safe_eval(node, depth=0):
    if depth > 50:
        raise ValueError("expression trop imbriquée")
    if isinstance(node, ast.Expression):
        return _safe_eval(node.body, depth + 1)
    if (isinstance(node, ast.Constant)
            and isinstance(node.value, (int, float))
            and not isinstance(node.value, bool)):
        return node.value
    if isinstance(node, ast.BinOp) and (
            type(node.op) in _BINOPS or isinstance(node.op, ast.Pow)):
        left = _safe_eval(node.left, depth + 1)
        right = _safe_eval(node.right, depth + 1)
        if isinstance(node.op, ast.Pow):
            if abs(right) > _MAX_EXPONENT:
                raise ValueError("exposant trop grand")
            return left ** right
        return _BINOPS[type(node.op)](left, right)
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.UAdd, ast.USub)):
        value = _safe_eval(node.operand, depth + 1)
        return value if isinstance(node.op, ast.UAdd) else -value
    raise ValueError("expression non autorisée")

class SkillSet:
    def get_date(self):
        """Retourne la date et l'heure actuelles."""
        now = datetime.datetime.now()
        return f"Nous sommes le {now.strftime('%d/%m/%Y')} et il est {now.strftime('%H:%M')}."

    def calculate(self, expression):
        """Calculatrice sécurisée (AST, sans eval brut)."""
        try:
            expression = expression.strip()
            if not expression or len(expression) > _MAX_LENGTH:
                return "Erreur de calcul. Vérifie ta formule."
            # Sécurité : on n'autorise que les chiffres et opérateurs mathématiques
            allowed = set("0123456789+-*/(). ")
            if not set(expression).issubset(allowed):
                return "Je ne peux calculer que des opérations mathématiques simples."
            tree = ast.parse(expression, mode="eval")
            result = _safe_eval(tree)
            return f"Le résultat est : {result}"
        except (ValueError, SyntaxError, ZeroDivisionError, OverflowError):
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

    def open_browser(self, url="https://www.google.com"):
        """Ouvre le navigateur par défaut avec l'URL spécifiée."""
        try:
            webbrowser.open(url)
            return f"Navigateur ouvert avec {url}."
        except Exception as e:
            return f"Erreur lors de l'ouverture du navigateur : {str(e)}"

    def session_report(self, memory):
        """Rapport de session : faits + rules, valeurs sensibles masquées.

        Défense en profondeur : même si une valeur sensible a échappé
        au filtre d'écriture (versione antérieure), elle est masquée à
        la sortie. Le secret n'est jamais recité.
        """
        from core.catalog import contains_secret
        facts = memory.facts
        lines = [f"📋 Bilan de session : {len(facts)} fait(s), "
                 f"{len(memory.rules)} règle(s) en mémoire."]
        if facts:
            shown = []
            for k, v in list(facts.items())[:5]:
                val = str(v)
                display = "(masqué : valeur sensible)" \
                    if contains_secret(k + " " + val) else val
                shown.append(f"{k}: {display}")
            lines.append("Faits récents : " + " · ".join(shown))
        learned = [q for q, a in memory.rules.items()
                   if not str(a).startswith("CMD:")]
        if learned:
            lines.append("Règles récentes : " +
                         " · ".join(learned[:3]) +
                         ("…" if len(learned) > 3 else ""))
        lines.append("Discipline : les secrets ne sont jamais stockés ;")
        lines.append("toute demande d'effacement est honorée.")
        return "\n".join(lines)

# Dictionnaire de mappage pour lier les textes aux fonctions
SKILL_MAP = {
    "CMD:date": "get_date",
    "CMD:meteo": "get_weather",
    "CMD:calc": "calculate",
    "CMD:search": "search_web",
    "CMD:open_browser": "open_browser",
    "CMD:session_report": "session_report",
}