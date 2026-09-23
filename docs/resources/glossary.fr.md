<!-- GÉNÉRÉ depuis config/agenda.yml par tools/build_site.py. Ne pas modifier. -->

# Glossaire

Le vocabulaire commun de la semaine. Ces termes sont tirés du paquet `stg17` lui-même : un notebook, une diapositive et cette page emploient nécessairement la même formulation.

!!! tip "Discipline de vocabulaire"

    L'exposé du Jour 1 matin existe pour fixer ces mots. Un « agent » et un « assistant RAG » ne sont pas la même chose, et confondre les deux dans un cahier des charges coûte cher. Quand un terme est employé de travers pendant la semaine, revenez ici.

## Intelligence artificielle

**Ingénierie de prompt**  
*Prompt engineering*

: Façonner l'entrée d'un modèle — rôle, contexte, contraintes, exemples — pour orienter sa sortie. Le levier le moins coûteux, et le premier à épuiser.

**Génération augmentée par récupération (RAG)**  
*Retrieval-Augmented Generation (RAG)*

: Récupérer les documents pertinents et les placer dans le contexte du modèle, pour qu'il réponde depuis votre matériel plutôt que depuis sa mémoire.

**Affinage (fine-tuning)**  
*Fine-tuning*

: Modifier les poids d'un modèle sur vos propres exemples. Le levier lourd — essayez d'abord le prompt et le RAG.

**Agent**  
*Agent*

: Un modèle doté d'outils, autorisé à décider lesquels appeler et dans quel ordre. Puissant, et la raison pour laquelle les points de contrôle humains comptent.

**Hallucination**  
*Hallucination*

: Une sortie fluide, assurée et fausse. Pas un défaut à corriger — une propriété du mécanisme, à gérer par la vérification.

**Ancrage factuel**  
*Grounding*

: Rattacher une réponse à une source récupérable, pour qu'un lecteur puisse la vérifier.

**Inférence**  
*Inference*

: Exécuter un modèle entraîné pour produire une sortie. C'est là que se trouve réellement le coût récurrent d'un système d'IA.

**Token**  
*Token*

: L'unité sous-lexicale que le modèle lit et écrit. Les coûts et les limites de contexte se comptent en tokens, pas en mots.

**Plongement (embedding)**  
*Embedding*

: Un vecteur numérique représentant le sens, afin de pouvoir calculer une similarité. Le mécanisme derrière la récupération.

**Base vectorielle**  
*Vector store*

: L'index qui rend rapide la recherche par similarité sur les plongements.

## Lumières nocturnes

**Somme des lumières**  
*Sum of Lights*

: La somme de la radiance sur une zone. Un indicateur indirect de l'activité éclairée — pas le PIB.

**Radiance**  
*Radiance*

: La lumière quittant le sol, en nW·cm⁻²·sr⁻¹, telle que mesurée par le capteur.

**Superficie éclairée**  
*Lit area*

: La part du territoire dont la radiance dépasse un seuil choisi. Varie avec le seuil — publiez toujours les deux.

**Radiance moyenne**  
*Mean radiance*

: Radiance moyenne sur les pixels valides. Presque dénuée de sens seule, car la distribution est très asymétrique.

**Halo lumineux (blooming)**  
*Blooming*

: La lumière débordant de sa source physique : une ville éclaire plus de pixels qu'elle n'en occupe. Gonfle les totaux urbains.

**Saturation**  
*Saturation*

: Les cœurs les plus lumineux dépassent la plage exploitable du capteur : leur croissance n'apparaît plus dans les données.

**Torchère de gaz**  
*Gas flare*

: Une flamme industrielle, très lumineuse et constante, qui peut dominer le total d'une région sans électrifier personne.

**Masque nuageux**  
*Cloud mask*

: La couche marquant les pixels masqués par les nuages, à exclure avant tout calcul statistique.

**Indicateur de qualité**  
*Quality flag*

: Métadonnée par pixel décrivant la fiabilité de l'observation.

## Géographie

**National (ADM0)**  
*National (ADM0)*

: Le niveau national.

**Région (ADM1)**  
*Region (ADM1)*

: Le premier niveau infranational — régions, provinces, États.

**District (ADM2)**  
*District (ADM2)*

: Le deuxième niveau infranational — districts, départements.

**Statistiques zonales**  
*Zonal statistics*

: Résumer un raster à l'intérieur de polygones. L'opération qui transforme l'imagerie satellitaire en tableau statistique.

**Frontières administratives**  
*Administrative boundaries*

: Les polygones définissant les unités administratives. Le fichier retenu change chaque chiffre infranational publié.

## Connectivité

**Débit descendant**  
*Download speed*

: Débit mesuré vers l'utilisateur, en kbit/s dans les tuiles Ookla.

**Débit montant**  
*Upload speed*

: Débit mesuré depuis l'utilisateur.

**Latence**  
*Latency*

: Délai aller-retour en millisecondes. Souvent plus déterminant que le débit brut pour savoir si un service est utilisable.

**Quadkey**  
*Quadkey*

: L'identifiant d'une tuile Mercator web. Ookla publie au zoom 16, environ 611 m à l'équateur.

**Tests**  
*Tests*

: Le nombre de tests de débit derrière la moyenne d'une tuile. Une tuile de trois tests n'est pas comparable à une tuile de trois mille.

## Pratique statistique

**Indicateur indirect (proxy)**  
*Proxy indicator*

: Une grandeur mesurable utilisée à la place d'une grandeur qu'on ne peut pas mesurer directement. Son utilité est une question empirique, pas une hypothèse.

**Biais de couverture**  
*Coverage bias*

: Sous-représentation systématique d'une partie de la population, propre aux sources non probabilistes. Ookla mesure ceux qui lancent des tests de débit, pas la population.

**Validation**  
*Validation*

: Établir, preuves à l'appui, la relation entre un indicateur indirect et une mesure officielle — avant de publier l'un ou l'autre.

**Limites**  
*Limitations*

: L'exposé de ce qu'un résultat ne peut pas soutenir. Dans cet atelier, c'est une partie du livrable, pas une annexe.

**Reproductibilité**  
*Reproducibility*

: Le fait qu'une autre personne, avec les mêmes intrants, obtienne les mêmes nombres. Exige les paramètres, pas seulement le code.

**Métadonnées**  
*Metadata*

: La description qui rend un jeu de données trouvable et interprétable par quelqu'un qui n'était pas dans la salle.

---

Ce glossaire suit le vocabulaire employé pendant la semaine. Un terme vous manque ? Signalez-le à l'équipe d'animation.
