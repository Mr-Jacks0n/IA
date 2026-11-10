---
name: fuseaux-horaires
description: "Heures des grandes villes via zoneinfo (données de la machine, pas de réseau)"
category: utilites
risk: none
command: CMD:worldtime
triggers: fuseaux, heures du monde, heure à
---
# World clock

## Quand l'utiliser
- quand il faut l'heure locale d'une grande ville.

## Comment ça marche
- base de villes locale : Paris, Londres, Montréal, New York, Tokyo,
  Sydney, São Paulo, Le Caire ;
- conversion via `zoneinfo` (données système), jamais une API ;
- ville citée : une ligne · sinon : liste complète.

## Limitations
- ville inconnue du jeu : liste générale affichée ;
- données de fuseaux dépendantes de la machine (tzdata).
