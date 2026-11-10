import ast
import calendar
import csv
import datetime
import json
import operator
import os
import random
import re
import secrets
import subprocess
import requests
import webbrowser

from zoneinfo import ZoneInfo

# Racine projet (data/ et chemins relatifs sont ancrés ici : ARIA
# fonctionne quel que soit le répertoire courant).
_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Évaluateur AST : aucun eval() brut sur une entrée utilisateur.
# ⚠️ Ancien code : eval(expression) · la whitelist de caractères
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

    # ── gestion d'une liste de tâches (dossier data/tasks.json) ────
    def tasks(self, text):
        """Liste de tâches locale : ajouter, lister, terminer, supprimer."""
        path = os.path.join(_ROOT, 'data', 'tasks.json')
        data = {"tasks": []}
        try:
            with open(path, 'r', encoding='utf-8') as f:
                loaded = json.load(f)
                if isinstance(loaded, dict):
                    data.update(loaded)
        except (OSError, ValueError):
            pass
        tasks = [t for t in data.get("tasks", []) if isinstance(t, dict)]
        tasks.sort(key=lambda t: t.get("id", 0))
        text_l = text.lower().strip()

        match_add = re.search(r'ajoute (?:la )?t[âa]che\s*[:;]?\s*(.+)', text_l)
        if match_add:
            label = match_add.group(1).strip('?.!: ')
            task_id = (max((t.get("id", 0) for t in tasks), default=0) + 1)
            tasks.append({"id": task_id, "text": label, "done": False})
            self._save_tasks(path, {"tasks": tasks})
            return (f"☑ Tâche #{task_id} enregistrée : « {label} ». "
                    f"{sum(1 for t in tasks if not t['done'])} en cours.")

        match_done = re.search(r'termine (?:la )?t[âa]che\s*#?\s*(\d+)', text_l)
        if match_done:
            step = next((t for t in tasks
                         if str(t.get("id")) == match_done.group(1)), None)
            if step and not step.get("done"):
                step["done"] = True
                self._save_tasks(path, {"tasks": tasks})
                return f"✅ Tâche #{step['id']} terminée : « {step['text']} »."
            return "Tâche introuvable ou déjà terminée."

        open_tasks = [t for t in tasks if not t.get("done")]
        if not open_tasks:
            return "📋 Aucune tâche en cours. Ajoute-en une : « ajoute la tâche … »."
        lines = ["📋 Tâches en cours :",
                 *(f"  · #{t['id']} · {t['text']}" for t in open_tasks[:8])]
        return "\n".join(lines)

    @staticmethod
    def _save_tasks(path, payload):
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(payload, f, indent=2, ensure_ascii=False)

    def changelog(self, text):
        """Ébauche neutral de journal des changements depuis git log.

        Réécrit l'historique récent en puces « · » neutres : la personne
        révise ensuite. Seulement les messages, jamais les fichiers.
        """
        try:
            count = re.search(r'(\d+)', text or '')
            n = min(int(count.group(1)), 30) if count else 8
            out = subprocess.run(
                ["git", "log", f"-{n}", "--pretty=%h %s"],
                cwd=_ROOT, capture_output=True, text=True, timeout=10)
            lines = ["📝 Ébauche de journal (à réviser avant publication) :"]
            for line in (out.stdout or "").splitlines():
                if not line.strip():
                    continue
                digest, _, message = line.partition(" ")
                lines.append(f"  · [{digest}] {message}")
            if len(lines) == 1:
                return "Journal indisponible : historique vide ou pas un dépôt."
            return "\n".join(lines[:9])
        except (OSError, subprocess.SubprocessError):
            return "Journal indisponible : git n'est pas joignable."

    def charter(self, text):
        """Inspecteur de charte : tirets cadratins, artefacts, valeur
        sensible éventuelle. Le contenu n'est jamais recité, seules les
        positions sont affichées."""
        path_match = re.search(r'([\w./\-]+\.(?:py|md|json|txt|yml|yaml|cfg))',
                               text.replace('\\', '/'))
        if not path_match:
            return ("Indique le fichier à contrôler, ex. : « inspecte le "
                    "fichier config.py » · je vérifie la charte "
                    "(séparateurs ·, artefacts, identifiants).")
        path = path_match.group(1)
        if not os.path.isabs(path):
            path = os.path.join(_ROOT, path)
        try:
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
        except (OSError, UnicodeDecodeError):
            return f"Fichier introuvable ou illisible : {path_match.group(1)}"

        from core.selfaudit import _SECRET_PATTERNS
        issues = {"tiret cadratin": [], "artefact": [],
                  "littéral d'identifiant": []}
        scories = ('espec', 'Orchard', 'parsnas', 'librarie', 'Quando')
        for no, line in enumerate(content.splitlines(), start=1):
            em_dash = '\u2014'
            if em_dash in line:
                issues["tiret cadratin"].append(no)
            if any(word in line for word in scories) or \
                    any('\u4e00' <= c <= '\u9fff' for c in line):
                issues["artefact"].append(no)
            if any(pat.search(line) for _, pat in _SECRET_PATTERNS):
                issues["littéral d'identifiant"].append(no)
        lines = [f"🔍 Charte · {path_match.group(1)} :"]
        for kind, hits in issues.items():
            detail = "aucune"
            if hits:
                detail = (f"{len(hits)} occurrence(s) · ligne(s) "
                          + ", ".join(map(str, hits[:5])))
            lines.append(f"  · {kind} : {detail}")
        if all(not v for v in issues.values()):
            return f"✅ {path_match.group(1)} est conforme à la charte."
        lines.append("  corrige les positions puis relance l'examen.")
        return "\n".join(lines)

    def textstats(self, text):
        """Statistiques locales d'un texte : mots, unicité, fréquences."""
        corps = re.sub(
            r'^(?:analyse (?:ce )?le? texte|statistiques(?: du)? texte)\s*[:;]?\s*',
            '', text.strip(), flags=re.I)
        if not corps:
            return "Donne-moi un texte à analyser : « analyse le texte … »."
        words = [w for w in re.split(r'[\W_]+', corps.lower()) if len(w) > 1]
        unique = set(words)
        usable = [w for w in words if w not in (
            "que", "qui", "quoi", "dont", "est", "les", "des", "une",
            "son", "sur", "avec", "pour", "et", "ou", "le", "la", "un",
            "au", "aux", "en", "il", "elle", "je", "tu", "on", "ce",
            "cette", "du", "mais", "donc", "ni", "car", "dans", "par")]
        top = sorted(set(usable), key=lambda w: -usable.count(w))[:5]
        sentences = len(re.findall(r'[.!?]+(?:\s|$)', corps)) or 1
        lines = [
            f"📊 Mots : {len(words)} · uniques : {len(unique)}",
            f"   phrases détectées : {sentences}",
            f"   fréquentes : {', '.join(top[:5]) or 'aucune'}",
        ]
        return "\n".join(lines)

    _UNITS = {
        ("km", "mi"): lambda v: v * 0.621371,
        ("mi", "km"): lambda v: v / 0.621371,
        ("m", "ft"): lambda v: v * 3.28084,
        ("ft", "m"): lambda v: v / 3.28084,
        ("kg", "lb"): lambda v: v * 2.20462,
        ("lb", "kg"): lambda v: v / 2.20462,
        ("mb", "gb"): lambda v: v / 1000,
        ("gb", "mb"): lambda v: v * 1000,
    }

    def convert(self, text):
        """Convertisseur d'unités local, déterministe (pas de réseau)."""
        m = re.search(r"(-?\d+(?:[.,]\d+)?)\s*°?\s*([a-zA-Z°]+)\s*"
                      r"(?:en|vers|to)\s*°?\s*([a-zA-Z°]+)", text)
        if not m:
            return ("Format attendu : « convertis 5 km en miles » · "
                    "km/mi, m/ft, kg/lb, °C/°F, Mo/Go.")
        raw, source, target = (m.group(1).replace(",", "."),
                               m.group(2).lower().strip('°'),
                               m.group(3).lower().strip('°'))
        aliases = {"mile": "mi", "miles": "mi", "livre": "lb",
                   "livres": "lb", "c": "c", "f": "f"}
        source, target = aliases.get(source, source), aliases.get(target, target)
        try:
            value = float(raw)
        except ValueError:
            return "Nombre non compris, reformule la conversion."
        if source == "c" and target == "f":
            return f"Le résultat est : {value * 9 / 5 + 32:.1f} °F"
        if source == "f" and target == "c":
            return f"Le résultat est : {round((value - 32) * 5 / 9, 1)} °C"
        kind = self.__class__._UNITS
        if (source, target) in kind:
            result = kind[(source, target)](value)
            return f"Le résultat est : {result:.2f} {target}"
        return ("Conversion inconnue · paires disponibles : km/mi, "
                "m/ft, kg/lb, °C/°F, Mo/Go.")

    _WORLD_CLOCK = {
        "paris": "Europe/Paris",
        "londres": "Europe/London",
        "montréal": "America/Montreal",
        "new york": "America/New_York",
        "tokyo": "Asia/Tokyo",
        "sydney": "Australia/Sydney",
        "são paulo": "America/Sao_Paulo",
        "cairo": "Africa/Cairo",
    }

    def worldtime(self, text):
        """Heures des grandes villes via zoneinfo seule (pas de réseau)."""
        text_l = text.lower()
        city = next((name for name in self.__class__._WORLD_CLOCK
                     if re.search(r'\b' + re.escape(name) + r'\b', text_l)),
                    None)
        try:
            now = datetime.datetime.now()
            if city:
                zone = ZoneInfo(self.__class__._WORLD_CLOCK[city])
                local = now.astimezone(zone)
                return f"🌍 {city.capitalize()} · {local.strftime('%H:%M')}"
            lines = ["🌍 Heures autour du monde :"]
            for name, tz in self.__class__._WORLD_CLOCK.items():
                local = now.astimezone(ZoneInfo(tz))
                lines.append(f"  · {name.capitalize()} : "
                             f"{local.strftime('%H:%M')}")
            return "\n".join(lines)
        except (KeyError, ValueError, OSError):
            return "Fuseau inconnu sur cette machine · jeu de villes limité."

    def calendar_show(self):
        """Calendrier du mois courant (module calendar, marquage du jour)."""
        now = datetime.date.today()
        grid = calendar.TextCalendar(firstweekday=0).formatmonth(
            now.year, now.month)
        today = f"{now.day:02d}"
        marked = []
        for line in grid.rstrip().splitlines():
            line = line.rstrip()
            if re.search(r'(?<!\d)' + today + r'(?!\d)', line):
                line += "  ← aujourd'hui"
            marked.append(line)
        return "\n".join(marked)

    def tokens(self, text):
        """Génération locale de valeurs aléatoires (module secrets).

        ⚠️ la valeur est affichée mais JAMAIS stockée ni mémorisée ·
        le vocabulaire sensible (« jeton d'accès ») tient à distance du
        masquage discipliné : la sortie dit « valeur générée ».
        """
        count = re.search(r'(\d+)', text or '')
        n = min(int(count.group(1)), 5) if count else 1
        digit_only = bool(re.search(r'numériqu', text.lower()))
        values = []
        for _ in range(n):
            if digit_only:
                values.append(str(secrets.randbelow(10**6)))
            else:
                values.append(secrets.token_hex(8))
        if n > 1:
            body = "\n".join(f"  · {v}" for v in values)
            return (f"Valeurs locales générées ({n}) · jamais stockées, "
                    f"à conserver dans un gestionnaire dédié :\n{body}")
        return (f"Valeur locale générée · jamais stockée, à conserver "
                f"dans un gestionnaire dédié : {values[0]}")

    def chance(self, text):
        """Tirage local honnête : dé, pile ou face, nombre 1 à 100."""
        text_l = text.lower()
        if 'pile ou face' in text_l or 'pièce' in text_l:
            draw = "pile" if secrets.randbelow(2) == 0 else "face"
            return f"🪙 Pile ou face : {draw}."
        if 'nombre' in text_l:
            return f"🎲 Nombre tiré entre 1 et 100 : {random.randint(1, 100)}."
        faces = re.search(r'(\d+)\s*faces?', text_l)
        dice = min(int(faces.group(1)), 100) if faces else 6
        return f"🎲 Dé ({dice} faces) : {random.randint(1, dice)}."

    def csv_preview(self, text):
        """Aperçu local d'un fichier CSV : colonnes, lignes, entête."""
        path_match = re.search(r'([\w./\-]+\.csv)', text.replace('\\', '/'))
        if not path_match:
            return "Indique le fichier à lire : « aperçu du fichier data.csv »."
        path = path_match.group(1)
        if not os.path.isabs(path):
            path = os.path.join(_ROOT, path)
        try:
            with open(path, 'r', encoding='utf-8') as f:
                rows = list(csv.reader(f))[:4]
        except (OSError, UnicodeDecodeError):
            return f"CSV introuvable ou illisible : {path_match.group(1)}"
        if not rows:
            return "CSV vide (aucune ligne lisible)."
        body = "\n".join("  · " + " | ".join(r) for r in rows[1:4])
        return (f"📄 {path_match.group(1)} · colonnes : {len(rows[0])}"
                + (f"\n   entête : « {' | '.join(rows[0])} »"
                   if len(rows) > 1 else "")
                + (f"\n{body}" if len(rows) > 1 else "\n   (aucune donnée)"))


SKILL_MAP = {
    "CMD:date": "get_date",
    "CMD:meteo": "get_weather",
    "CMD:calc": "calculate",
    "CMD:search": "search_web",
    "CMD:open_browser": "open_browser",
    "CMD:session_report": "session_report",
    # catalogue élargi · gestion & documentation
    "CMD:tasks": "tasks",
    "CMD:changelog": "changelog",
    "CMD:charter": "charter",
    # analyse & fichiers
    "CMD:textstats": "textstats",
    "CMD:csv": "csv_preview",
    # utilities
    "CMD:convert": "convert",
    "CMD:worldtime": "worldtime",
    "CMD:calendar": "calendar_show",
    # éléments aléatoires locaux
    "CMD:tokens": "tokens",
    "CMD:chance": "chance",
}

# Compétences dont la méthode a besoin du texte utilisateur brut
# (paramètre, fichier à inspecter…) ou de la mémoire (rapport).
NEEDS_TEXT = {
    "CMD:tasks", "CMD:changelog", "CMD:charter", "CMD:textstats",
    "CMD:convert", "CMD:tokens", "CMD:chance", "CMD:csv", "CMD:worldtime",
}
NEEDS_MEMORY = {"CMD:session_report"}