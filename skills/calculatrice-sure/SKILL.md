---
name: calculatrice-sure
description: "Calcule une expression arithmétique via un parseur AST à liste blanche, sans eval"
category: utilities
risk: safe
command: CMD:calc
triggers: calcule, résultat, expression, +, -, *, /
---
# Safe calculator

## Quand l'utiliser
- quand l'entrée contient une expression arithmétique (chiffres + opérateurs).

## Comment ça marche
- parseur AST : uniquement les nœuds BinOp/UnaryOp/Constant ;
- parenthèses, + - * / // % et ** (borne d'exposant : 100) ;
- borne de longueur : 100 caractères, profondeur : 50 ;
- tout le reste est refusé : jamais d'eval brut sur une entrée utilisateur.

## Limitations
- pas de fonctions (sin, log…), pas de variables ;
- les entiers arbitrairement grands sont acceptés côté Python mais
  rendus tels quels ;

## Historique de sécurité
- DoS corrigé : un ancien eval() avec "*" autorisé permettait
  "9**9**9" de figer le process → remplacement par l'AST avec
  borne d'exposant et de profondeur.
