---
name: tirage-hasard
description: "Tirages locaux honnêtes : dé à N faces, pile ou face, nombre 1 à 100"
category: divertissement
risk: none
command: CMD:chance
triggers: pile ou face, lance un dé, tirage, nombre aléatoire
---
# Local draws

## Quand l'utiliser
- demandes de hasard : « lance un dé », « pile ou face », « nombre
  aléatoire ».

## Comment ça marche
- dé : module `random` borné (faces du dé reconnues, 6 par défaut) ;
- pièce : `secrets.randbelow(2)` ;
- nombre : 1 à 100.

## Limitations
- aucun tirage attaché à des données personnelles ;
- tirages non reproductibles (c'est le but).
