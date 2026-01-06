# ARIA - Intelligence Apprenante Locale

ARIA est une IA symbolique et adaptative basée sur des règles logiques, conçue pour apprendre uniquement via l'interaction humaine. Sans modèles de machine learning ou LLM, elle utilise un moteur de décision, une mémoire persistante et un apprentissage par feedback.

## Fonctionnalités

- **Apprentissage par règles IF/THEN** : Répond basé sur des conditions apprises.
- **Mémoire persistante** : Stocke règles, faits, expériences et contexte dans des fichiers JSON.
- **Compréhension floue** : Utilise la similarité pour matcher les entrées (ex. "salut" ≈ "slt").
- **Commandes spéciales** : Peut exécuter des actions (heure, ouvrir navigateur, météo, recherche web).
- **Calcul automatique** : Détecte et calcule des expressions mathématiques flexibles (ex. "5+5", "et 45*2").
- **Raisonnement contextuel** : Se souvient de faits personnels (nom, etc.) et répond en conséquence.
- **Raisonnement avancé** : Chaînage logique basé sur les faits (ex. météo d'une ville).
- **Module Internet** : Recherche web via API DuckDuckGo.
- **Conscience et Réflexion** : Mémoire courte terme, auto-réflexion sur réponses, résumé de contexte, questions pour approfondir.
- **Interface console** : Interaction simple via CLI.
- **Interface graphique** : GUI avec Tkinter pour une expérience visuelle.
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
│   ├── console.py          # Interface CLI
│   └── gui.py              # Interface graphique Tkinter
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
   python main.py  # Pour console
   python main.py --gui  # Pour interface graphique
   python main.py --debug  # Mode debug avec logs détaillés
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

Toi : recherche python
ARIA : Voici ce que j'ai trouvé : Python is a high-level, general-purpose programming language. Its design philosophy emphasizes code readability with the use of significant indentation.

Toi : quel temps fait-il à Paris
ARIA : Voici ce que j'ai trouvé : [Informations météo pour Paris]

Toi : résume
ARIA : Récemment, nous avons parlé de : recherche python, quel temps fait-il à Paris.

Toi : comment vas-tu
ARIA : Je ne sais pas encore répondre à cela. Apprends-moi. Pour mieux t'aider, peux-tu me donner plus de détails ?
```

## Mode Debug

Pour déboguer et voir les processus internes :
- Ajoutez `--debug` au lancement : `python main.py --debug`
- Affiche des logs détaillés sur :
  - Inputs utilisateur
  - Raisonnement avancé
  - Matches fuzzy
  - Règles utilisées
  - Faits sauvegardés/récupérés
  - Mémoire chargée

Exemple :
```
[DEBUG] Input utilisateur : 'bonjour'
[DEBUG] Matches fuzzy : ['bonjour']
```

## Licence

Ce projet est open-source. Utilisez et modifiez librement.