# ARIA - Intelligence Apprenante Locale

ARIA est une IA symbolique et adaptative basée sur des règles logiques, conçue pour apprendre uniquement via l'interaction humaine. Sans modèles de machine learning ou LLM, elle utilise un moteur de décision, une mémoire persistante et un apprentissage par feedback.

## Fonctionnalités

- **Apprentissage par règles IF/THEN** : Répond basé sur des conditions apprises.
- **Mémoire persistante** : Stocke règles et expériences dans des fichiers JSON.
- **Interface console** : Interaction simple via CLI.
- **Apprentissage humain** : Corrige et apprend de chaque interaction.
- **Extensible** : Prêt pour ajout de modules (Internet, spécialisation métier, GUI).

## Structure du Projet

```
aria_core/
├── core/
│   ├── decision_engine.py  # Moteur de décision
│   ├── memory.py           # Gestion mémoire
│   └── rules.py            # Règles par défaut
├── learning/
│   └── feedback.py         # Apprentissage
├── interface/
│   └── console.py          # Interface CLI
├── data/
│   ├── rules.json          # Règles apprises
│   └── experiences.json    # Expériences (futur)
└── main.py                 # Point d'entrée
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

Toi : comment ça va
ARIA : Je ne sais pas encore répondre à cela. Apprends-moi.
Réponse correcte ? (oui/non) : non
Quelle aurait été la bonne réponse ? Ça va bien, merci !
```

## Développement Futur

- Module Internet pour recherche.
- Spécialisation métier (ex. : assistant médical).
- Raisonnement avancé (chaînage logique).
- Interface graphique.

## Licence

Ce projet est open-source. Utilisez et modifiez librement.