---
name: journal-changements
description: "Ébauche de journal des changements depuis l'historique git local (à réviser)"
category: documentation
risk: none
command: CMD:changelog
triggers: journal des changements, journal, changelog
---
# Change journal draft

## Quand l'utiliser
- quand il faut une ébauche de journal des changements à partir des
  derniers commits.

## Comment ça marche
- lit `git log` en local (nombre de messages borné, 8 par défaut) ;
- reformate en puces neutres « · » avec digest court ;
- la personne révise et reformule avant toute publication.

## Limitations
- aucun contenu de diff n'est écrit, seulement les messages ;
- hors dépôt git : message clair, pas d'échec.
