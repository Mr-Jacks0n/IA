---
name: analyse-texte
description: "Statistiques texte local : mots, uniques, phrases, fréquences"
category: analyse
risk: none
command: CMD:textstats
triggers: analyse le texte, analyse ce texte, statistiques du texte
---
# Text statistics

## Quand l'utiliser
- quand l'utilisateur donne un texte et veut des statistiques.

## Comment ça marche
- découpage par mots (regex), compte total vs uniques ;
- détection des phrases (finisseurs . ! ?) ;
- fréquences : les mots fréquents du français banal sont écartés.

## Limitations
- aucune sémantique : statistiques uniquement ;
- texte borné à la longueur du message console.
