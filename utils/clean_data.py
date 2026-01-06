import json
import os

def clean_rules():
    path = '../data/rules.json'
    
    if not os.path.exists(path):
        print("Fichier rules.json introuvable.")
        return

    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Conversion des clés en minuscules pour liste de dicts
    if isinstance(data, list):
        for item in data:
            if "condition" in item:
                item["condition"] = item["condition"].lower().strip()
    else:
        data = {k.lower().strip(): v for k, v in data.items()}

    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    
    print("✅ Nettoyage terminé : toutes les clés sont en minuscules.")

if __name__ == "__main__":
    clean_rules()