---
name: gestion-taches
description: "Liste de tâches locale : ajouter, lister, terminer · persistée dans data/tasks.json"
category: gestion
risk: safe
command: CMD:tasks
triggers: tâche, mes tâches, ajoute la tâche
---
# Task list

## Quand l'utiliser
- quand la demande concerne des tâches : ajouter, lister, terminer.

## Comment ça marche
- stockage local unique : `data/tasks.json` (id, texte, statut) ;
- phrases reconnues : « ajoute la tâche … », « termine la tâche N »,
  toute autre mention liste les tâches en cours ;
- aucun réseau, aucune synchronisation cloud.

## Limitations
- pas de dates d'échéance (proposition bienvenue) ;
- la liste est personnelle : jamais commitée.
