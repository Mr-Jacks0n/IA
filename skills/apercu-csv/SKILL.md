---
name: apercu-csv
description: "Aperçu local d'un CSV : colonnes, entête, 3 premières lignes"
category: analyse
risk: safe
command: CMD:csv
triggers: aperçu du fichier, aperçu csv, csv
---
# CSV preview

## Quand l'utiliser
- quand un fichier .csv doit être survolé avant usage.

## Comment ça marche
- module `csv` : nombre de colonnes, entête, 3 premières lignes ;
- lecture seule, chemin relatif ancré à la racine du projet.

## Limitations
- très gros fichiers : lecture tronquée volontaire (4 lignes) ;
- délimiteurs exotiques non détectés (compte fait sur les virgules).
