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
        self.context = self._load("data/context.json") or {}

    def _load(self, path):
        if os.path.exists(path):
            data = json.load(open(path, "r", encoding="utf-8"))
            # Normaliser les conditions en minuscules
            if isinstance(data, list):
                for item in data:
                    if "condition" in item:
                        item["condition"] = item["condition"].lower()
            return data
        return []

    def save_rules(self):
        with open("data/rules.json", "w", encoding="utf-8") as f:
            json.dump(self.rules, f, indent=2, ensure_ascii=False)

    def save_experiences(self):
        with open("data/experiences.json", "w", encoding="utf-8") as f:
            json.dump(self.experiences, f, indent=2, ensure_ascii=False)

    def save_context(self):
        with open("data/context.json", "w", encoding="utf-8") as f:
            json.dump(self.context, f, indent=2, ensure_ascii=False)