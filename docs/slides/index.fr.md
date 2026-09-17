# Présentations

**Aucune présentation n'est encore publiée.** Les diapositives de chaque séance
sont fournies par la personne qui l'anime, et apparaissent sur le site dès que le
fichier est en place.

---

## Comment une présentation apparaît

Chaque séance dispose déjà d'un gabarit vide qui l'attend, nommé d'après la
séance elle-même :

```
docs/downloads/Day1/1400_ai-infrastructure_FR-inactif.pdf
```

Nommez votre fichier exactement pareil, **sans `-inactif`**, déposez-le dans ce
dossier, et reconstruisez. Un bouton de téléchargement apparaît sous la séance,
sur la page de son jour.

```bash
python tools/downloads.py            # le nom attendu pour chaque séance
python tools/downloads.py --missing  # seulement ce qui manque encore
python tools/build_site.py           # publier ce que vous avez déposé
```

Le PDF et le PowerPoint sont acceptés tous les deux, en anglais et en français,
et n'importe quel sous-ensemble convient. Plusieurs fichiers pour une même séance
se distinguent par un numéro — la convention complète est dans
`docs/downloads/HOW-TO-ADD-FILES.txt`.

---

## Où les boutons apparaissent

Pas ici. Une présentation appartient à une séance : ses boutons s'affichent sur
la page du jour, juste sous la séance qu'elle accompagne.

[Jour 1](../day1/index.md){ .md-button } [Jour 2](../day2/index.md){ .md-button }
[Jour 3](../day3/index.md){ .md-button } [Jour 4](../day4/index.md){ .md-button }
[Jour 5](../day5/index.md){ .md-button }

Cette page reste le point d'entrée et listera les présentations une fois qu'elles
existeront.

---

## Notes pour les animateurs

!!! info "Les présentations reveal.js construites sont désactivées"

    Le dépôt porte aussi un petit système qui construit des présentations pour le
    navigateur à partir de sources bilingues, sous `slides/decks/`. Il est
    désactivé tant que l'atelier fonctionne avec des présentations fournies :

    ```yaml
    # config/workshop.yml
    site:
      publish_slides: false
    ```

    Passez la valeur à `true` puis lancez `python tools/build_slides.py` pour les
    publier. Les sources sont intactes — rien n'a été supprimé.

!!! tip "Présenter sans réseau"

    Un PDF ou un PowerPoint fourni n'a besoin que de lui-même. Si vous utilisez
    plutôt les présentations construites, lancez `python tools/vendor_reveal.py`
    au préalable pour qu'elles ne dépendent pas d'un CDN ; le réseau de la salle
    n'est pas une hypothèse sûre.
