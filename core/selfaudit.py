"""Auto-audit ARIA : phases déterministes, rapport neutre.

Six phases condensées mais réelles, exécutables hors ligne :

  1. Reconnaissance : surface d'entrée, fichiers data, skills, config.
  2. Chasse guidée : secrets dans la mémoire, règles dangereuses, eval.
  3. Validation des candidats : chaque trouvaille doit être reproductible
     (fichier + extrait) ou elle est rejetée.
  4. Sortie structurée : findings.json (confirmed / rejected).
  5. Vérification indépendante : la source est relue une 2e fois.
  6. Rapport neutre : rien n'est déclaré vulnérable sans preuve reproductible.

Usage : python main.py --audit  (exit code 0 => rapport généré)
"""
import ast
import json
import os
import re
import sys
from datetime import datetime, timezone

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

_SECRET_PATTERNS = [
    ('mot de passe littéral', re.compile(r'(?i)\b(password|mot de passe)\s*[:=]\s*["\'][^"\']+["\']')),
    ('token littéral', re.compile(r'(?i)\btoken\b\s*[:=]\s*["\'][A-Za-z0-9_\-]{12,}["\']')),
    ('clé API littérale', re.compile(r'(?i)\b(api[_-]?key|secret[_-]?key)\b\s*[:=]\s*["\'][A-Za-z0-9_\-]{16,}["\']')),
]
_DANGEROUS_CALLS = ('eval(', 'exec(', '__import__(')


# ── Phase 1 · reconnaissance ─────────────────────────────────────────
def _survey():
    data_dir = os.path.join(_ROOT, 'data')
    surfaces = {
        'data_files': [f for f in os.listdir(data_dir)
                       if f.endswith('.json')] if os.path.isdir(data_dir) else [],
        'skills': [os.path.basename(os.path.dirname(p))
                   for p in _walk_skills()],
        'entrypoints': [f for f in os.listdir(_ROOT)
                        if f in ('main.py', 'config.py')],
    }
    return surfaces


def _walk_skills():
    skills_dir = os.path.join(_ROOT, 'skills')
    if not os.path.isdir(skills_dir):
        return []
    return [os.path.join(skills_dir, d, 'SKILL.md')
            for d in sorted(os.listdir(skills_dir))
            if os.path.isfile(os.path.join(skills_dir, d, 'SKILL.md'))]


# ── Phase 2 · chasse guidée ──────────────────────────────────────────
def _hunt():
    candidates = []
    # 2a. secrets dans data/ ou une règle héritée
    data_dir = os.path.join(_ROOT, 'data')
    if os.path.isdir(data_dir):
        for fname in os.listdir(data_dir):
            path = os.path.join(data_dir, fname)
            if not fname.endswith('.json') or not os.path.isfile(path):
                continue
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
            except OSError:
                continue
            for label, pat in _SECRET_PATTERNS:
                m = pat.search(content)
                if m:
                    candidates.append({'file': os.path.relpath(path, _ROOT),
                                       'kind': label,
                                       'match': m.group(0)[:60]})
    # 2b. eval / exec hors liste blanche réfléchie
    for pyfile in ('main.py', 'config.py',
                   *(os.path.join('core', f) for f in os.listdir(os.path.join(_ROOT, 'core'))
                     if f.endswith('.py'))):
        path = os.path.join(_ROOT, pyfile)
        if not os.path.isfile(path):
            continue
        try:
            with open(path, 'r', encoding='utf-8') as f:
                tree = ast.parse(f.read())
        except (OSError, SyntaxError):
            continue
        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) \
                    and ast.unparse(node.func) + '(' in _DANGEROUS_CALLS:
                candidates.append({'file': pyfile,
                                   'kind': f"appel {node.func.id}()",
                                   'match': f"ligne {node.lineno}"})
    return candidates


# ── Phase 3 + 5 · validation & vérification indépendante ─────────────
def _validate(candidate):
    """Rejoue la chasse sur le fichier et exige la même preuve."""
    path = os.path.join(_ROOT, candidate['file'])
    if not os.path.isfile(path):
        return 'rejected'
    try:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
    except OSError:
        return 'rejected'
    if candidate['kind'].startswith('appel '):
        name = candidate['kind'][len('appel '):].rstrip('()')
        return 'confirmed' if f"{name}(" in content else 'rejected'
    for label, pat in _SECRET_PATTERNS:
        if pat.search(content):
            return 'confirmed'
    return 'rejected'


# ── Phase 4 · sortie structurée ──────────────────────────────────────
def run_audit(verbose=False):
    t0 = datetime.now(timezone.utc).isoformat()
    surfaces = _survey()
    candidates = _hunt()
    findings = {
        'generated_at': t0,
        'kind': 'aria.self-audit.report',
        'surfaces': surfaces,
        'confirmed': [], 'rejected': [],
    }
    for c in candidates:
        status = _validate(c)
        findings['confirmed' if status == 'confirmed' else 'rejected'].append(c)

    out_path = os.path.join(_ROOT, 'data', 'findings.json')
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(findings, f, indent=2, ensure_ascii=False)

    # 6 · rapport neutre
    print("🔍 Audit de sécurité ARIA (auto, hors ligne)")
    print(f"   reconnaissance : {len(surfaces['data_files'])} fichier(s) data · "
          f"{len(surfaces['skills'])} compétences · exécution déterministe")
    if findings['confirmed']:
        print(f"   ⚠️ {len(findings['confirmed'])} trouvaille(s) confirmée(s) :")
        for c in findings['confirmed']:
            print(f"      · {c['file']} → {c['kind']} ({c['match']})")
        print("   action : retirer la valeur, la déplacer vers un gestionnaire "
              "de secrets, relancer l'audit.")
    else:
        print("   ✅ Aucun secret ni appel dangereux confirmé "
              f"({len(findings['rejected'])} candidat(s) rejeté(s)).")
    print(f"   rapport : data/findings.json ({t0})")
    if verbose:
        for rej in findings['rejected']:
            print(f"      (rejeté) {rej['file']} → {rej['kind']}")
    return findings


if __name__ == '__main__':
    run_audit(verbose='--verbose' in sys.argv)
    sys.exit(0)
