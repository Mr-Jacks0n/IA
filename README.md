# ARIA - Intelligence Apprenante Locale

ARIA est une IA symbolique et adaptative basée sur des règles logiques, conçue pour apprendre uniquement via l'interaction humaine. Sans modèles de machine learning ou LLM, elle utilise un moteur de décision, une mémoire persistante et un apprentissage par feedback.

## Fonctionnalités

- **Apprentissage par règles IF/THEN** : Répond basé sur des conditions apprises.
- **Mémoire persistante** : Stocke règles, expériences et contexte dans des fichiers JSON.
- **Compréhension floue** : Utilise la similarité pour matcher les entrées (ex. "salut" ≈ "slt").
- **Commandes spéciales** : Peut exécuter des actions (heure, ouvrir navigateur).
- **Contexte utilisateur** : Se souvient du nom et d'autres infos.
- **Interface console** : Interaction simple via CLI.
- **Apprentissage humain** : Corrige et apprend de chaque interaction (sauf pour commandes).

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

Toi : quelle heure est-il
ARIA : 14:30

Toi : ouvre google
ARIA : J'ai ouvert Google pour toi.

Toi : je m'appelle Alice
ARIA : Enchantée Alice, je m'en souviendrai.

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