---
name: recherche-web
description: "Recherche Instant Answer sur le web (réseau requis) et cite la source"
category: utilites
risk: safe
command: CMD:search
triggers: recherche, cherche, recherche sur le web
---
# Web search (network)

## Quand l'utiliser
- seulement quand l'utilisateur demande explicitement une recherche ;
- jamais en ambigue ou en tâche de fond (économie de réseau).

## Comment ça marche
- requête GET vers l'API Instant Answer DuckDuckGo (choix volontaire :
  response JSON légère, pas de page extraite) ;
- timeout dur : 10 s ; en échec, répondre proprement sans casser la session ;
- la réponse cite toujours le domaine de la source utilisée.

## Limitations
- réseau requis : si offline, dire "Aucune connexion" sans réessayer en boucle ;
- aucune clé réseau stockée, aucun cookie, aucune donnée envoyée ;
- sortie tronquée : les résultats longs sont résumés, pas recopiés.

## Cas numérique
- reconnaissance ville/météo supportée : relayer vers la même API.
