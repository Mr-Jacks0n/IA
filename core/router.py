"""Routeur d'intents ARIA : candidats, scores, route gagnante + preuve.

À la différence d'une cascade d'`if` dur-codée, build_routes(text, memory,
catalog, skillset) construit des routes candidates :

    · nom de la route ;
    · chargeur (closure sans argument) · la réponse est générée
      seulement si la route gagne (exécution lazy) ;
    · risque (du frontmatter, `none` par défaut) ;
    · confiance (score déterministe du déclencheur + heuristiques).

Le moteur sélectionne la route de confiance max. Une discipline de
mémoire passe en tête si l'entrée mentionne un secret. Chaque décision
renvoie aussi la preuve du routage (candidats perdants).
"""
import difflib
import re

from core.catalog import contains_secret


class Route:
    def __init__(self, name, run, risk='none', confidence=0.0, source='catalog'):
        self.name = name
        self.run = run          # closure -> str, exécutée seulement si gagnante
        self.risk = risk
        self.confidence = confidence
        self.source = source

    @staticmethod
    def evidence(winner):
        return (f"[route: {winner.name} · risque: {winner.risk} · "
                f"confiance: {winner.confidence:.2f} · source: {winner.source}]")


# heuristiques déterministes, évaluables dans le moteur :
_FACT_FORGET = re.compile(r"^(?:oublie|j'oublie|supprime le fait)\s*(?:que)?\s*(.+)$", re.I)
_FACT_RECALL = re.compile(r"as[- ]tu not[ée]|connais[\w\s]*(?:\bsur\b|\bà propos\b)", re.I)


def build_routes(text, memory, catalog, skillset):
    """Construit les routes candidates (sans les exécuter)."""
    routes = []
    text_l = text.lower().strip()

    # 0. garde : jamais de secret → refus de discipline avant tout
    if contains_secret(text_l):
        routes.append(Route(
            'memory.secret-guard',
            lambda: ("⛔ Discipline de mémoire : je ne stocke pas "
                     "d'identifiants sensibles, même sur demande. Ils ne "
                     "quittent jamais cette machine · passez par un "
                     "gestionnaire dédié."),
            risk='none', confidence=2.5, source='guard'))

    # 1. appropriation : « je m'appelle X » → fait persistant
    match_name = re.match(r"^je m'appelle[,\s:]+(.+)$", text_l)
    if match_name:
        name = match_name.group(1).strip()
        routes.append(Route(
            'memory.save_name',
            lambda: (memory.save_fact('user_name', name) and
                     f"Enchanté {name}, je m'en souviendrai.") or
                    "Ce prénom contient un secret : refusé par la discipline.",
            risk='none', confidence=2.0, source='logic'))

    # 2. rappel du nom
    if re.search(r"mon nom|comment je m['’]appelle", text_l):
        routes.append(Route(
            'memory.recall_name',
            lambda: _recall_name(memory),
            risk='none', confidence=2.0, source='logic'))

    # 3. calcul automatique
    if any(c in text for c in '+-*/') and re.search(r'\d', text):
        expression = re.sub(r'[^\d+\-*/().\s]', '', text).strip()
        if expression:
            routes.append(Route(
                'skills.calculator',
                lambda: skillset.calculate(expression),
                risk='safe', confidence=1.6, source='catalog'))

    # 4. résumé / bilan / contexte
    if re.search(r"\b(résume|contexte|récapitulatif|bilan|que sais[- ]tu)", text_l):
        routes.append(Route(
            'skills.session_report',
            lambda: skillset.session_report(memory),
            risk='none', confidence=1.4, source='catalog'))

    # 5. recherche web explicite
    match_search = re.match(r"^(?:recherche|cherche|recherche sur le web)\s+(.+)$", text_l)
    if match_search:
        query = match_search.group(1).strip()
        routes.append(Route(
            'skills.search-web',
            lambda: skillset.search_web(query),
            risk='safe', confidence=1.5, source='catalog'))

    # 6. météo d'une ville
    if re.search(r"\bm[ée]t[ée]o\b|\bquel temps\b", text_l):
        city = next((w for w in text.split() if w[:1].isupper()), None)
        routes.append(Route(
            'skills.web-weather',
            lambda: skillset.search_web(f"météo {city or 'France'}"),
            risk='safe', confidence=1.0, source='catalog'))

    # 7. oubli · suppression de fait explicite, toujours honorée
    match_forget = _FACT_FORGET.match(text_l)
    if match_forget:
        needle = match_forget.group(1).strip().strip('?.! ')
        routes.append(Route(
            'memory.forget',
            lambda: _forget(memory, needle),
            risk='safe', confidence=1.2, source='logic'))

    # 8. rappel ciblé (« as-tu noté … ? »)
    if _FACT_RECALL.search(text_l):
        routes.append(Route(
            'memory.search_facts',
            lambda: _search_facts(memory),
            risk='none', confidence=1.1, source='logic'))

    # 9. routes déclaratives du catalogue (frontmatter SKILL.md)
    seen = {r.name for r in routes}
    for s, trigger, score in catalog.candidates(text_l):
        if not s.command or s.risk == 'unknown':
            continue
        key = f"skills.{s.name}"
        if key in seen:
            continue
        seen.add(key)
        routes.append(Route(
            key,
            (lambda skill=s: _run_skill(skill, text, memory, skillset)),
            risk=s.risk, confidence=score, source='catalog'))

    # 10. règles apprises (difflib, cutoff 0.6)
    rules = memory.get_rules()
    if rules:
        matches = difflib.get_close_matches(text_l, list(rules.keys()), n=1, cutoff=0.6)
        if matches:
            template = rules[matches[0]]
            routes.append(Route(
                'rules.fuzzy',
                lambda: _run_rule(template, text, memory, skillset),
                risk='safe', confidence=0.6, source='rules'))

    return routes


def _recall_name(memory):
    n = memory.get_fact('user_name')
    return f"Tu t'appelles {n}." if n else "Je ne connais pas encore ton nom."


def _forget(memory, needle):
    removed = memory.forget_from_hints(needle)
    return (f"🗑️ {removed} fait(s) supprimé(s) : {needle}."
            if removed else
            f"Aucun fait correspondant à « {needle} » dans ma mémoire.")


def _search_facts(memory):
    if not memory.facts:
        return "Ma mémoire ne contient encore rien de noté."
    return ("Voici ce que je sais : " +
            " · ".join(f"{k}: {v}" for k, v in list(memory.facts.items())[:5]))


def _run_skill(decl, text, memory, skillset):
    from core.skills import SKILL_MAP   # import tardif, évite un cycle
    method_name = SKILL_MAP.get(decl.command, '')
    method = getattr(skillset, method_name, None)
    if method is None:
        return "Cette compétence n'est pas encore câblée."
    # signature spéciale : le rapport de session a besoin de la mémoire
    if method_name == 'session_report':
        return method(memory)
    return method()


def _run_rule(template, text, memory, skillset):
    if not template.startswith("CMD:"):
        return template
    cmd_key, _, arg = template.partition(' ')
    from core.skills import SKILL_MAP
    method = getattr(skillset, SKILL_MAP.get(cmd_key, ''), None)
    if method is None:
        return template
    if cmd_key == 'CMD:search':
        q = text.lower().replace('recherche', '').strip()
        return method(q) if q else "Quelle est ta question de recherche ?"
    if cmd_key == 'CMD:open_browser':
        return method(arg.strip() or "https://www.google.com")
    return method()


def route_input(memory, catalog, skillset, text):
    """Sélectionne le meilleur candidat et renvoie (Route, preuves)."""
    routes = build_routes(text, memory, catalog, skillset)
    if not routes:
        return None, routes
    best = max(routes, key=lambda r: r.confidence)
    return best, routes
