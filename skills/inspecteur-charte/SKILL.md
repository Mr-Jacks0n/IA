---
name: inspecteur-charte
description: "Contrôle un fichier contre la charte : tirets cadratins, artefacts, identifiants (positions only)"
category: revision
risk: safe
command: CMD:charter
triggers: inspecte, vérifie la charte, contrôle la charte
---
# Charter inspector

## Quand l'utiliser
- quand un texte source doit être vérifié contre la charte du projet.

## Comment ça marche
- scan ligne à ligne : tiret cadratin, artefacts connus, identifiants
  sensibles détectés par le filtre de discipline ;
- sortie = comptes + numéros de ligne, JAMAIS le contenu repris.

## Limitations
- lecture seule : aucune correction automatique ;
- langues : artefacts connus seulement (liste évolutive).
