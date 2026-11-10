"""Catalogue local de compétences déclaratives (ARIA v0.3).

Chaque compétence vit dans skills/<dir>/SKILL.md avec un frontmatter :

    ---
    name: nom-short
    description: "... (< 200 caractères)"
    category: utilites
    risk: none | safe | critical
    command: CMD:date        (clé de SKILL_MAP côté skills.py)
    triggers: a, b, c        (déclencheurs explicites)
    ---

Le catalogue est la source unique pour :
  · l'indexation des routes disponibles (déclencheurs → routes) ;
  · le niveau de risque (aucune compétence critical ne s'exécute
    sans confirmation explicite de l'utilisateur) ;
  · le rapport d'audit (compétences non valides = trouvailles).

Les fichiers sont lus au démarrage, jamais reliés au réseau.
"""
import os
import re
from config import debug_print

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_SKILLS_DIR = os.path.join(_ROOT, 'skills')

_VALID_RISK = ('none', 'safe', 'critical')
_SECRET_RE = re.compile(
    r'\b(password|passwd|mot de passe|secret|token|api[_ -]?key|'
    r'clé privée|credential|cvv|carte bancaire)\b', re.I)

_FRONTMATTER_RE = re.compile(r'^---\n(.*?)\n---', re.S)


class SkillDecl:
    """Compétence déclarée + sa provenance."""

    def __init__(self, data, path):
        self.data = data
        self.path = path

    def __getattr__(self, k):
        return self.data.get(k)

    def label(self):
        return f"{self.name} ({self.risk})"


class SkillCatalog:
    def __init__(self, skills_dir=_SKILLS_DIR):
        self.skills = []      # SkillDecl valides
        self.broken = []      # (chemin, raison)  → sujets d'audit
        self.load(skills_dir)

    # ── chargement ────────────────────────────────────────────────
    def load(self, directory):
        if not os.path.isdir(directory):
            debug_print(f"catalogue absent : {directory}")
            return
        for sub in sorted(os.listdir(directory)):
            path = os.path.join(directory, sub, 'SKILL.md')
            if not os.path.isfile(path):
                continue
            decl = self._parse(path)
            if decl is None:
                continue
            if not decl.name:
                decl.data['name'] = sub

            ok, reason = self._validate(decl, sub)
            if ok:
                self.skills.append(decl)
            else:
                self.broken.append((path, reason))
                debug_print(f"SKILL.md invalide : {path} → {reason}")

    @staticmethod
    def _parse(path):
        try:
            with open(path, 'r', encoding='utf-8') as f:
                raw = f.read()
        except OSError:
            return SkillDecl({}, path)
        m = _FRONTMATTER_RE.match(raw)
        data = {}
        if m:
            for line in m.group(1).splitlines():
                if ':' not in line:
                    continue
                key, _, val = line.partition(':')
                key, val = key.strip(), val.strip().strip('"')
                data[key] = [v.strip() for v in val.split(',')] \
                    if key == 'triggers' else val
        else:
            data['_broken'] = True
        return SkillDecl(data, path)

    @staticmethod
    def _validate(decl, folder):
        if decl.data.get('_broken'):
            return False, 'frontmatter illisible'
        if decl.name != folder:
            return False, f"name ({decl.name}) != dossier ({folder})"
        if decl.risk not in _VALID_RISK:
            return False, f"risk inconnu: {decl.risk}"
        desc = decl.description or ''
        if len(desc) > 200:
            return False, 'description > 200'
        if not decl.description:
            return False, 'description vide'
        return True, ''

    # ── recherche de routes (index sur les déclencheurs) ──────────
    def candidates(self, text_lower):
        """Retourne [(SkillDecl, phrase_déclencheur, score), ...] trié.

        Score déterministe : correspondance sur frontière de mots
        (un fragment comme « jour » dans « bonjour » ne déclenche
        rien). Phrase complète = 1.0, mot isolé = 0.8.
        """
        out = []
        for s in self.skills:
            for trig in s.triggers:
                t = trig.strip().lower()
                if not t:
                    continue
                if re.search(r'(^|\W)' + re.escape(t) + r'(\W|$)', text_lower):
                    score = 1.0 if len(t.split()) > 1 else 0.8
                    out.append((s, t, score))
        out.sort(key=lambda x: -x[2])
        return out

    def get(self, command_key):
        for s in self.skills:
            if s.command == command_key:
                return s
        return None

    def by_name(self, name):
        for s in self.skills:
            if s.name == name:
                return s
        return None

    def risk_of_command(self, command_key):
        s = self.get(command_key)
        return s.risk if s else 'unknown'

    def summary(self):
        ok = len(self.skills)
        risks = {r: sum(1 for s in self.skills if s.risk == r)
                 for r in _VALID_RISK}
        return f"{ok} compétences chargées {risks} · {len(self.broken)} invalides"

    def report_lines(self):
        yield f"Compétences valides : {len(self.skills)}"
        for s in self.skills:
            yield f"  · {s.label():28s} {s.command or '(inactivée)'}  déclencheurs={list(s.triggers)}"
        if self.broken:
            yield "Compétences invalides (à corriger) :"
            for path, reason in self.broken:
                yield f"  ! {path}  {reason}"


# Filtre secret partagé (discipline de mémoire ET catalogue)
def contains_secret(text):
    return bool(_SECRET_RE.search(text))
