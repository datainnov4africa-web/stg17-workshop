# Pour les animateurs

Un animateur principal, deux assistants techniques, environ un assistant pour dix
participants. Les participants à distance sont regroupés en équipes virtuelles,
chacune avec un assistant dédié. Une personne-ressource appuie l'atelier identité
visuelle et génération d'images du Jour 2.

## La mécanique des deux pistes

Chaque carnet de laboratoire existe en version **guidée** et **ouverte**, dans les
deux langues. Les équipes choisissent au début de chaque laboratoire et peuvent
basculer en cours de route. Le livrable est identique, ce qui garde les
présentations du vendredi comparables.

Annoncez-le une fois, au début du Jour 1 après-midi, puis n'y revenez plus. Les
participants qui ont besoin de la piste guidée ne devraient pas avoir à la
demander devant la salle.

## Animer un laboratoire

1. **Deux minutes sur l'objectif et le livrable.** Pas sur la méthode — le carnet
   le fait mieux que vous ne le ferez depuis le pupitre.
2. **Nommez le repli avant que quiconque en ait besoin.** « Si votre
   téléchargement bloque, prenez la variante Earth Engine, ou mettez le pays à
   CIV. » Dit à l'avance, c'est un élément de conception ; dit après vingt minutes
   de silence, c'est un sauvetage.
3. **Circulez.** Les assistants traitent les pannes individuelles ; l'animateur
   principal guette le *même* problème apparaissant à trois tables, signal qu'il
   faut arrêter la salle et le traiter une fois.
4. **Dix minutes avant la fin, réclamez le livrable.** Les équipes qui n'ont rien
   enregistré ont besoin de ces dix minutes.

## Quand déclencher un repli

| Signal | Action |
|---|---|
| Trois équipes ou plus bloquées sur la même étape depuis 10 minutes | Arrêtez la salle. Démontrez depuis le pupitre. |
| Les données nationales d'une équipe s'avèrent inexploitables | Basculez-la immédiatement sur le pays de référence. Ne la laissez pas déboguer un problème de données pendant un laboratoire de méthode. |
| Le cluster Elasticsearch est injoignable | Annoncez la voie DuckDB pour tout le monde en une fois, pas équipe par équipe. |
| Clés API limitées | Chemin de démonstration animé. Ne consacrez pas la séance à l'administration des quotas. |
| Réseau totalement coupé | Miroir de la clé USB. Chaque laboratoire fonctionne depuis elle. |

## Le mur

Ouvert lors de la synthèse du Jour 1 et gardé visible toute la semaine. Quatre
colonnes :

- **Cas d'usage récurrents** — ce que plus d'un pays tente
- **Partenariats réplicables** — accords de données qu'un autre office pourrait copier
- **Obstacles partagés** — la matière du Plan d'action
- **Où la mutualisation serait payante** — projets conjoints candidats

Consolidé le vendredi dans la session des enseignements clés puis, à T+1 semaine,
dans le calendrier de suivi daté transmis au Bureau.

## Risques de minutage

**Les présentations pays du Jour 1 matin** sont la session la plus susceptible de
déborder. Désignez un chronométreur. Huit minutes chacune, six diapositives
maximum, et le créneau de synthèse absorbe le débordement — c'est sa raison d'être.

**Le Jour 3 après-midi** comporte trois sessions en trois heures avec une pause
café. Si l'indexation Elasticsearch traîne, coupez le second jeu de requêtes
plutôt que le créneau de publication de 16h45 : les équipes qui ne versent rien le
mercredi arrivent au vendredi sans rien à montrer.

**Le Jour 4** est une journée entière sur un seul sujet. Surveillez la fatigue
d'après-déjeuner ; le laboratoire d'analyse de 14h00 est l'heure la plus dense de
la semaine.

## Avant la semaine

- [ ] Répétition à blanc de chaque laboratoire de bout en bout sur une machine aux spécifications de l'atelier, en chronométrant chaque étape
- [ ] Confirmer que le cluster Elasticsearch est chargé, un index par pays participant
- [ ] Confirmer que le pays de référence s'exécute de bout en bout depuis une machine propre
- [ ] Embarquer reveal.js pour la présentation hors ligne : `python tools/vendor_reveal.py`
- [ ] Vérifier que chaque badge Colab se résout
- [ ] Préparer les clés USB — voir `prep/usb-manifest.md`
