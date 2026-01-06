# ARIA - Intelligence Apprenante Locale

ARIA est une IA symbolique et adaptative basée sur des règles logiques, conçue pour apprendre uniquement via l'interaction humaine. Sans modèles de machine learning ou LLM, elle utilise un moteur de décision, une mémoire persistante et un apprentissage par feedback.

## Fonctionnalités

- **Apprentissage par règles IF/THEN** : Répond basé sur des conditions apprises.
- **Mémoire persistante** : Stocke règles, faits, expériences et contexte dans des fichiers JSON.
- **Compréhension floue** : Utilise la similarité pour matcher les entrées (ex. "salut" ≈ "slt").
- **Commandes spéciales** : Peut exécuter des actions (heure, ouvrir navigateur, météo).
- **Calcul automatique** : Détecte et calcule des expressions mathématiques (ex. "5+5").
- **Raisonnement contextuel** : Se souvient de faits personnels (nom, etc.) et répond en conséquence.
- **Interface console** : Interaction simple via CLI.
- **Apprentissage humain** : Corrige et apprend de chaque interaction (sauf pour actions automatiques).

## Structure du Projet

```
aria_core/
├── core/
│   ├── decision_engine.py  # Moteur de décision avec raisonnement et fuzzy matching
│   ├── memory.py           # Gestion mémoire (règles, faits, contexte)
│   ├── rules.py            # Règles par défaut
│   └── skills.py           # Compétences (calcul, date, météo)
├── learning/
│   └── feedback.py         # Apprentissage par feedback
├── interface/
│   └── console.py          # Interface CLI
├── utils/
│   └── clean_data.py       # Outil de nettoyage des données
├── data/
│   ├── rules.json          # Règles apprises
│   ├── facts.json          # Faits mémorisés (nom, etc.)
│   ├── experiences.json    # Expériences (futur)
│   └── context.json        # Contexte utilisateur
└── main.py & README.md
```

## Installation et Lancement

1. Clonez le dépôt :
   ```bash
   git clone https://github.com/bindedouworker-hub/IA.git
   cd IA/aria_core
   ```

2. Lancez l'IA :
   ```bash
   python main.py
   ```

3. Interagissez :
   - Tapez un message.
   - Répondez "oui" ou "non" au feedback.
   - Si "non", fournissez la correction pour apprendre.

## Exemple d'Interaction

```
ARIA est active. Tape 'exit' pour quitter.

Toi : bonjour
ARIA : Bonjour. Je suis ARIA, une intelligence apprenante.
Réponse correcte ? (oui/non) : oui

Toi : 1578 + 4500
ARIA : Le résultat est : 6078

Toi : je m'appelle Alice
ARIA : Enchanté Alice, je m'en souviendrai.

Toi : quel est mon nom
ARIA : Tu t'appelles Alice.

Toi : quelle heure est-il
ARIA : Nous sommes le 06/01/2026 et il est 15:45

Toi : comment vas-tu
ARIA : Je ne sais pas encore répondre à cela. Apprends-moi.
Réponse correcte ? (oui/non) : non
Quelle aurait été la bonne réponse ? Très bien, merci !
```

## Développement Futur

- Module Internet pour recherche.
- Spécialisation métier (ex. : assistant médical).
- Raisonnement avancé (chaînage logique).
- Interface graphique.

## Licence

Ce projet est open-source. Utilisez et modifiez librement.