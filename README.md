# ARIA - Intelligence Apprenante Locale

ARIA est une IA symbolique et adaptative basée sur des règles logiques, conçue pour apprendre uniquement via l'interaction humaine. Sans modèles de machine learning ou LLM, elle utilise un moteur de décision, une mémoire persistante et un apprentissage par feedback.

## Fonctionnalités

- **Apprentissage par règles IF/THEN** : Répond basé sur des conditions apprises.
- **Mémoire persistante** : Stocke règles, faits, expériences et contexte dans des fichiers JSON.
- **Compréhension floue** : Utilise la similarité pour matcher les entrées (ex. "salut" ≈ "slt").
- **Commandes spéciales** : Peut exécuter des actions (heure, ouvrir navigateur, météo).
- **Calcul automatique** : Détecte et calcule des expressions mathématiques flexibles (ex. "5+5", "et 45*2").
- **Raisonnement contextuel** : Se souvient de faits personnels (nom, etc.) et répond en conséquence.
- **Conscience et Réflexion** : Mémoire courte terme, auto-réflexion sur réponses, résumé de contexte, questions pour approfondir.
- **Interface console** : Interaction simple via CLI.
- **Apprentissage humain** : Corrige et apprend de chaque interaction (sauf pour actions automatiques).

## Structure du Projet

```
aria_core/
├── core/
│   ├── decision_engine.py  # Moteur de décision avec raisonnement et fuzzy matching
│   ├── memory.py           # Gestion mémoire (règles, faits, contexte)
│   ├── rules.py            # Règles par défaut
│   ├── skills.py           # Compétences (calcul, date, météo)
│   └── reflection.py       # Conscience et réflexion (mémoire courte, auto-analyse)
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

Toi : calcule 15 + 15 * 2
ARIA : Le résultat est : 45

Toi : et 45*2
ARIA : Le résultat est : 90

Toi : résume
ARIA : Récemment, nous avons parlé de : je m'appelle Alice..., quel est mon nom, calcule 15 + 15 * 2.

Toi : comment vas-tu
ARIA : Je ne sais pas encore répondre à cela. Apprends-moi. Pour mieux t'aider, peux-tu me donner plus de détails ?
```

## Développement Futur

- Module Internet pour recherche.
- Spécialisation métier (ex. : assistant médical).
- Raisonnement avancé (chaînage logique).
- Interface graphique.

## Licence

Ce projet est open-source. Utilisez et modifiez librement.