---
name: rapport-session
description: "Répond avec un résumé de la session : faits connus, règles, réponses apprises"
category: utilites
risk: none
command: CMD:session_report
triggers: rapport de session, bilan, que sais-tu, récapitulatif
---
# Session report

## Quand l'utiliser
- quand l'utilisateur demande un bilan, ses données connues ou un récapitulatif.

## Comment ça marche
- liste des faits en mémoire persistante (clé = valeur), faits mentionnés paresseux ;
- nombre de règles apprises + les X dernières ;
- rappel de la discipline : les secrets sont refusés à l'entrée, jamais stockés ;
- cacher les valeurs sensibles même si elles ont passé le filtre (défense en profondeur).

## Limitations
- aucune écriture pendant le rapport ;
- ne cite jamais un secret littéralement, même s'il apparaissait dans une règle
  héritée d'une autre version.
