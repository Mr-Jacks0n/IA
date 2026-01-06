import json
import os
from .rules import DEFAULT_RULES
from config import debug_print

class Memory:
    def __init__(self):
        self.rules_file = 'data/rules.json'
        self.facts_file = 'data/facts.json' # Nouveau fichier pour le raisonnement
        self.rules = self._load_json(self.rules_file)
        if not self.rules:
            self.rules = DEFAULT_RULES
            self.save_rules()
        self.facts = self._load_json(self.facts_file)
        self.context = self._load_json('data/context.json') or {}
        debug_print(f"Mémoire chargée : {len(self.rules)} règles, {len(self.facts)} faits")

    def _load_json(self, filepath):
        if not os.path.exists(filepath):
            return {}
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}

    def save_rules(self):
        with open(self.rules_file, 'w', encoding='utf-8') as f:
            json.dump(self.rules, f, indent=4, ensure_ascii=False)

    def get_rules(self):
        return self.rules

    def add_rule(self, question, answer):
        self.rules[question.lower()] = answer
        self.save_rules()

    # --- Nouvelles fonctions pour le Raisonnement ---
    def save_fact(self, key, value):
        self.facts[key] = value
        with open(self.facts_file, 'w', encoding='utf-8') as f:
            json.dump(self.facts, f, indent=4, ensure_ascii=False)
        debug_print(f"Fait sauvegardé : {key} = {value}")

    def get_fact(self, key):
        value = self.facts.get(key)
        debug_print(f"Fait récupéré : {key} = {value}")
        return value

    def save_context(self):
        with open('data/context.json', 'w', encoding='utf-8') as f:
            json.dump(self.context, f, indent=2, ensure_ascii=False)