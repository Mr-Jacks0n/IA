import json
import os
from .rules import DEFAULT_RULES

class Memory:
    def __init__(self):
        self.rules = self._load("data/rules.json")
        if not self.rules:
            self.rules = DEFAULT_RULES
            self.save_rules()
        self.experiences = self._load("data/experiences.json")

    def _load(self, path):
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        return []

    def save_rules(self):
        with open("data/rules.json", "w", encoding="utf-8") as f:
            json.dump(self.rules, f, indent=2, ensure_ascii=False)

    def save_experiences(self):
        with open("data/experiences.json", "w", encoding="utf-8") as f:
            json.dump(self.experiences, f, indent=2, ensure_ascii=False)