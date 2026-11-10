import json
import os
from difflib import get_close_matches

from .rules import DEFAULT_RULES
from .catalog import contains_secret
from config import debug_print

# Chemins ancrés à la racine du projet via ce fichier : ARIA fonctionne
# quel que soit le répertoire courant (python /chemin/IA/main.py aussi).
_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_DATA_DIR = os.path.join(_ROOT, 'data')

# bornes d'hygiène : une mémoire qui grossit sans limite finit en
# problème de performance et en surface de fuite.
_MAX_FACTS = 200
_MAX_RULES = 500
_MAX_CONTEXT = 50


class MemoryRefused(ValueError):
    """Écriture refusée par la discipline (secret, contenu critique…)."""


class Memory:
    def __init__(self, data_dir=_DATA_DIR):
        self.data_dir = data_dir
        self.rules_file = os.path.join(data_dir, 'rules.json')
        self.facts_file = os.path.join(data_dir, 'facts.json')
        self.rules = self._load_json(self.rules_file)
        if not self.rules:
            self.rules = dict(DEFAULT_RULES)
            self.save_rules()
        self.facts = self._load_json(self.facts_file)
        self.context = self._load_json(os.path.join(data_dir, 'context.json')) or {}
        debug_print(f"Mémoire chargée : {len(self.rules)} règles, {len(self.facts)} faits")

    def _load_json(self, filepath):
        if not os.path.exists(filepath):
            return {}
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (OSError, ValueError):
            return {}

    def save_rules(self):
        with open(self.rules_file, 'w', encoding='utf-8') as f:
            json.dump(self.rules, f, indent=4, ensure_ascii=False)

    def get_rules(self):
        return self.rules

    def add_rule(self, question, answer):
        """Apprentissage supervisé, avec discipline : une règle dont le
        texte contient un secret est refusée (le filtre vaut aussi pour
        la réponse : c'est justement là que l'utilisateur les colle)."""
        question = str(question).lower().strip()
        answer = str(answer).strip()
        if not question or not answer:
            raise MemoryRefused("question ou réponse vide")
        if contains_secret(question + " " + answer):
            raise MemoryRefused(
                "refus : la règle mentionne un secret (mot de passe, token, clé…)")
        if len(question) > 200 or len(answer) > 1000:
            raise MemoryRefused("règle trop longue")
        self.rules[question] = answer
        if len(self.rules) > _MAX_RULES:
            oldest = next(iter(self.rules))
            if oldest in dict(DEFAULT_RULES):
                # écrase le plus ancien ajouté *hors* valeurs par défaut
                for k in self.rules:
                    if k not in DEFAULT_RULES:
                        oldest = k
                        break
            self.rules.pop(oldest, None)
        self.save_rules()

    def save_fact(self, key, value):
        """Écriture filtrée : un secret n'entre JAMAIS en mémoire, même
        sur demande explicite de l'utilisateur. Renvoie True si écrit."""
        key, value = str(key).strip(), str(value).strip()
        if contains_secret(key + " " + value):
            debug_print(f"refus (secret) : {key}")
            return False
        self.facts[key] = value
        if len(self.facts) > _MAX_FACTS:
            # FIFO : les plus anciens faits partent d'abord
            for k in list(self.facts)[:-_MAX_FACTS]:
                self.facts.pop(k, None)
        with open(self.facts_file, 'w', encoding='utf-8') as f:
            json.dump(self.facts, f, indent=4, ensure_ascii=False)
        debug_print(f"Fait sauvegardé : {key} = {value}")
        return True

    def get_fact(self, key):
        value = self.facts.get(key)
        debug_print(f"Fait récupéré : {key} = {value}")
        return value

    def forget_from_hints(self, needle):
        """Suppression explicite, toujours honorée (pas de copie cachée).
        Accepte un fragment : matche la clé OU la valeur."""
        needle = str(needle).lower().strip()
        if not needle:
            return 0
        word = needle.split()[0]
        hits = [k for k, v in self.facts.items()
                if word in k.lower() or word in str(v).lower()]
        for k in hits:
            self.facts.pop(k, None)
        if hits:
            with open(self.facts_file, 'w', encoding='utf-8') as f:
                json.dump(self.facts, f, indent=4, ensure_ascii=False)
        return len(hits)

    def search_facts(self, hint):
        """Retrouve le fait le plus proche (difflib, déclencheur libre)."""
        hint = str(hint).lower().strip()
        if not self.facts or not hint:
            return None
        best = get_close_matches(hint, list(self.facts.keys()), n=1, cutoff=0.5)
        return (best[0], self.facts[best[0]]) if best else None

    def remember_session(self, user_input, ai_response):
        """Compaction : on ne garde que les derniers échanges complets,
        les plus anciens sont résumés (le détail n'est pas réinventé)."""
        self.context.setdefault('recent', [])
        self.context['recent'].append(
            {"user": user_input[:120], "ai": str(ai_response)[:120]})
        if len(self.context['recent']) > _MAX_CONTEXT:
            dropped = self.context['recent'][:-_MAX_CONTEXT]
            digest = [d['user'][:40] for d in dropped]
            self.context.setdefault('archived_topics', [])
            self.context['archived_topics'] = (
                self.context['archived_topics'][-20:] + digest)
            self.context['recent'] = self.context['recent'][-_MAX_CONTEXT:]

    def save_context(self):
        with open(os.path.join(self.data_dir, 'context.json'), 'w',
                  encoding='utf-8') as f:
            json.dump(self.context, f, indent=2, ensure_ascii=False)
