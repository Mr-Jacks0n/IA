# Contribuer à ARIA — L'IA Symbolique Apprenante

Merci de votre intérêt ! ARIA est un projet d'étude **100 % local** :
aucun LLM, aucun modèle d'apprentissage automatique — uniquement des
règles logiques, une mémoire JSON et votre feedback. Toutes les
contributions sont bienvenues.

## Pour commencer

```bash
git clone https://github.com/Mr-Jacks0n/IA.git
cd IA
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python main.py            # mode console
python main.py --gui      # mode graphique (nécessite python3-tk)
python main.py --debug    # console + logs de décision
```

Serveur Linux sans interface graphique ? La console fonctionne sans
tkinter — c'est voulu (voir le changelog 1.1.0).

## Règles du projet

- **Pas de secrets ni de données personnelles dans les commits.**
  Les fichiers `data/*.json` contiennent ce qu'ARIA a appris de
  *vous* : validez toujours `git status` et le contenu de `data/`
  avant de committer.
- **Restez symbolique.** Pas d'intégration d'API LLM dans le moteur
  principal ; les idées doivent tenir dans le paradigme règles +
  mémoire + feedback. Les compétences réseau existantes
  (`core/skills.py`) sont le seul endroit où du externe est accepté.
- **Style** : Python standard, docstrings courtes en français,
  pas de dépendance supplémentaire sans discussion dans une issue.
- **Lint** : la CI applique flake8 (syntaxe et noms non définis).
  Vérifiez avant de pousser :
  ```bash
  python -m flake8 . --count --select=E9,F63,F7,F82
  ```

## Comment proposer un changement

1. Ouvrez une **issue** en décrivant le problème ou l'idée
   (template fourni dans le dépôt).
2. Créez une branche : `git checkout -b feat/ma-fonctionnalite`
3. Testez votre changement en console **et**, si l'interface est
   touchée, en GUI.
4. Committez avec un message conventionnel
   (`fix:` / `feat:` / `docs:` / `refactor:` …).
5. Ouvrez une Pull Request — le template vous guide.

## Bonnes premières contributions

- Ajouter des règles par défaut utiles à `core/rules.py`.
- Améliorer le fuzzy matching (cutoff, normalisation des accents).
- Étendre la réflexion de `core/reflection.py` (aujourd'hui 4 cas).
- Lire/écrire les faits de raisonnement de façon plus riche
  (`je m'appelle X` → âge ? ville ? goûts ?).

Merci de faire grandir une IA qui apprend uniquement de son humain 🤖
