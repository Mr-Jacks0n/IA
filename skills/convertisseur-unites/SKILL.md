---
name: convertisseur-unites
description: "Conversions locales déterministes : km/mi, m/ft, kg/lb, °C/°F, Mo/Go"
category: utilites
risk: none
command: CMD:convert
triggers: convertis, convertis en, conversion
---
# Unit converter

## Quand l'utiliser
- quand une phrase contient une valeur à convertir (« convertis 5 km
  en miles »).

## Comment ça marche
- analyse par regex : nombre + unité source + « en » + unité cible ;
- paires fixes : km/mi, m/ft, kg/lb, °C/°F, Mo/Go (Go = 1000 Mo) ;
- calcul local, déterministe, sans réseau.

## Limitations
- unités monétaires et scientifiques non couvertes ;
- exposants et unités composées (m/s) non supportés.
