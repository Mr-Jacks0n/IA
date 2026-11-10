---
name: annonce-date
description: "Annonce la date et l'heure selon l'horloge de la machine, jamais du réseau"
category: utilites
risk: none
command: CMD:date
triggers: quelle heure, date du jour, jour, heure
---
# Announce the date

## Quand l'utiliser
- quand la demande porte sur la date, l'heure ou le jour actuel.

## Comment ça marche
- la source unique est l'horloge locale de la machine, jamais un service réseau ;
- la sortie est toujours en français, format JJ/MM/AAAA + HH:MM.

## Limitations
- aucune physique de fuseau : on suit la machine locale ;
- aucune donnée personnelle n'est lue ni stockée pour cette réponse.
