# Vérification de l'environnement

Un carnet. Environ cinq minutes. Il vous dit, point par point, si votre machine
peut exécuter les treize laboratoires — puis produit une courte chaîne de
diagnostic à envoyer aux assistants techniques.

Le carnet de vérification d'environnement est distribué avec le matériel de l'atelier. Votre animateur vous enverra le lien.

!!! tip "Exécutez-le deux fois"
    Une fois chez vous, dès réception de votre invitation, et une fois pendant la
    séance de vérification à distance à T − 1 semaine. La première exécution vous
    dit quoi corriger ; la seconde confirme que c'est corrigé.

## Ce qu'il vérifie

| Section | Ce qu'elle établit |
|---|---|
| **1 · Boîte à outils** | Si le paquet `stg17` s'installe sur votre machine |
| **2 · Carte des laboratoires** | Ce dont chaque laboratoire a besoin — pour ne corriger que ce que vous utiliserez |
| **3 · Votre machine** | Version de Python, RAM, disque libre, présence d'un GPU, plateforme détectée |
| **4 · Bibliothèques** | Importe réellement chaque bibliothèque — un `rasterio` installé mais cassé apparaît comme présent dans `pip list` et échoue à l'import |
| **5 · Comptes et réseau** | Quelles clés API sont visibles (présence seulement, jamais la clé) et quels points d'accès votre réseau atteint |
| **6 · Votre pays** | Résout votre code ISO3 en tuiles satellitaires, projection et volume de téléchargement estimé, puis charge réellement vos frontières |
| **7 · Une première figure** | Confirme que la pile graphique s'affiche à l'identité de l'atelier |
| **8 · Chaîne de diagnostic** | Un résumé compact et partageable — aucune clé, aucun chemin personnel |

## Lire le résultat

La vérification est volontairement généreuse sur ce qui compte comme un problème.

**Du rouge dans le groupe *bibliothèques cœur*** doit être corrigé avant le
Jour 3. Le carnet affiche la ligne `pip install` exacte pour ce qui manque.

**De l'orange sur une clé API** n'est pas un échec. Chaque laboratoire utilisant
une clé dispose aussi d'un chemin documenté fonctionnant sans clé.

**De l'orange sur un point d'accès réseau** n'est pas davantage un échec. Les
points bloqués sont fréquents sur les réseaux institutionnels, et chaque jeu de
données est préparé à l'avance par l'équipe d'animation.

**Du rouge sur le chargement des frontières** mérite d'être signalé. Cela signifie
généralement que geoBoundaries ne publie pas le niveau demandé, ce qu'il est utile
de savoir avant jeudi.

## La chaîne de diagnostic

La section 8 affiche quelque chose comme ceci :

```
STG17 ENVIRONMENT CHECK
platform   : local / Windows 11 / py3.11.9
device     : CPU only
country    : CIV (2 VIIRS tiles)
boundaries : ok - 33 ADM1 units
core missing  : rasterio, h5py
optional ok   : 9/17
network fail  : NASA Earthdata (CMR)
keys present  : GROQ_API_KEY
```

Copiez-la et envoyez-la aux assistants techniques, ou collez-la dans le fil de
discussion pendant la séance de vérification. **Elle ne contient aucune clé, aucun
chemin issu de vos dossiers personnels et aucune donnée personnelle** — uniquement
ce qui est nécessaire pour vous aider.

## Si le carnet lui-même refuse de s'exécuter

C'est déjà un diagnostic, et un diagnostic fréquent. Prenez le badge Colab en haut
de cette page : il exécute le même carnet sur les machines de Google, sans rien
installer sur la vôtre. Si Colab fonctionne et que votre portable non, votre
chemin de repli pour toute la semaine est Colab — ce qui est une réponse
parfaitement valable. Signalez-le à la séance de vérification et les animateurs
vous appareilleront en conséquence.
