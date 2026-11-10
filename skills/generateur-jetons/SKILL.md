---
name: generateur-jetons
description: "Génère localement des valeurs aléatoires (module secrets) · affichées, jamais stockées"
category: securite
risk: safe
command: CMD:tokens
triggers: génère une valeur, valeur aléatoire, identifiant aléatoire
---
# Local random values

## Quand l'utiliser
- quand l'utilisateur veut une valeur aléatoire solide (identifiant,
  code numérique) sans réseau.

## Comment ça marche
- module `secrets` : hex 16 caractères par défaut ;
- « numérique » : code à 6 chiffres ;
- répétition supportée : « génère 3 valeurs ».

## Limitations
- la valeur est AFFICHÉE SEULEMENT : jamais écrite sur disque ni en
  mémoire (la discipline refuserait d'ailleurs toute écriture) ;
- prévoyez un gestionnaire dédié pour la conserver.
