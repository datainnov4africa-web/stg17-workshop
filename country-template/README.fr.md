<!--
  Gabarit de dépôt pays STG17.
  Remplacez chaque <PLACEHOLDER> ci-dessous, supprimez ce commentaire, et
  supprimez toute section qui ne s'applique pas. Conservez la structure — c'est
  elle qui rend les travaux pays comparables à l'échelle du continent.
  English: see README.md
-->

# <Nom de l'indicateur> — <Pays>

🇫🇷 Français · [🇬🇧 English](README.md)

> Un paragraphe : ce que contient ce dépôt, qui l'a produit, et à quelle question
> il répond. Rédigé pour un collègue d'un autre office national de statistique
> qui dispose de cinq minutes.

**Produit par** <votre office> lors de l'atelier technique STG17
*Enjeux émergents, pratiques émergentes*, Banque africaine de développement et
UA STATAFRIC, <mois année>.

[![Site](https://img.shields.io/badge/site-en%20ligne-1B7A43)](https://<owner>.github.io/stg17-<iso3>/)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.XXXXXXX.svg)](https://doi.org/10.5281/zenodo.XXXXXXX)
[![Code : MIT](https://img.shields.io/badge/code-MIT-0B2545)](LICENSE)
[![Données : voir LICENSE-DATA](https://img.shields.io/badge/donn%C3%A9es-voir%20LICENSE--DATA-F2A900)](LICENSE-DATA)

---

## Résultats

> Deux ou trois figures, une phrase chacune. **Montrez la réponse avant la
> méthode.** La plupart des lecteurs s'arrêtent ici, et c'est très bien — cette
> section doit leur suffire pour savoir si la suite mérite leur temps.

![<Figure 1>](outputs/figures/<figure1>.png)

*<Une phrase disant ce que le lecteur doit retenir de cette figure.>*

| Chiffre phare | Valeur | Période |
|---|---|---|
| <ex. croissance de la Somme des lumières nationale> | <x,x % / an> | <2016-2024> |
| <ex. territoire au-dessus du seuil d'éclairement> | <xx %> | <2024> |
| <ex. corrélation avec l'indicateur officiel> | <r = 0,xx> | <2020> |

---

## Sources de données

| Source | Produit / version | Période | Licence | Récupéré le |
|---|---|---|---|---|
| NASA Black Marble | VNP46A4 collection 002 | <2016-2024> | Domaine public (gouvernement américain) | <AAAA-MM-JJ> |
| Ookla Open Data | Haut débit fixe, trimestriel | <T1-T4 2024> | **CC BY-NC-SA 4.0** | <AAAA-MM-JJ> |
| WorldPop | Contraint 100 m | <2024> | CC BY 4.0 | <AAAA-MM-JJ> |
| <Votre office> | Frontières ADM1 / ADM2 | <2024> | <votre licence> | — |
| <Votre office> | <indicateur infranational officiel> | <2020> | <votre licence> | — |

> Supprimez les lignes non utilisées. **Ne supprimez pas la colonne licence** —
> la licence de votre production est déterminée par la licence la plus stricte de
> ce tableau. Voir [LICENSE-DATA](LICENSE-DATA).

---

## Méthode

> Brève. Cinq à dix phrases. Renvoyez au carnet pour tout ce dont un lecteur
> aurait besoin pour reproduire, et non simplement pour comprendre.

1. <Acquisition>
2. <Découpage aux frontières nationales>
3. <Statistiques zonales à l'ADM2, agrégées en ADM1 et ADM0>
4. <Validation contre l'indicateur officiel>

Paramètres qu'un lecteur ne pourrait pas deviner et qui changent les chiffres :

| Paramètre | Valeur | Pourquoi |
|---|---|---|
| Seuil d'éclairement | <0,5> nW·cm⁻²·sr⁻¹ | <raison> |
| Niveau administratif | ADM<2> | <raison> |
| Années exclues | <aucune / 2018 (couverture de tuiles incomplète)> | <raison> |
| Fichier de frontières | <source> | <raison> |

Détail complet : [`notebooks/`](notebooks/).

---

## Limites

> **Cette section n'est ni optionnelle ni un avertissement de forme.** C'est elle
> qui rend le reste du dépôt crédible. Répondez à ces quatre questions
> spécifiquement pour votre pays — la version générique ci-dessous est un point
> de départ, pas une réponse.

**Ce que mesure réellement cet indicateur.** <ex. La radiance nocturne est un
indicateur indirect des infrastructures éclairées. Ce n'est ni le PIB, ni le taux
de raccordement des ménages.>

**Choix qu'un lecteur ne devinerait pas.** <Le seuil d'éclairement. Le fichier de
frontières. La version du produit. Les années éventuellement exclues.>

**Ce qui est connu comme faux ou incertain dans ce pays.** <ex. Les torchères de
<région> dominent le total de cette région. La capitale sature le capteur au-delà
de <valeur>. <n> années auxquelles il manque une tuile ont été exclues.>

**À quoi ceci ne doit pas servir.** <ex. Ceci ne doit pas servir à répartir un
budget entre districts sans vérification de terrain.>

---

## Reproduire

```bash
git clone https://github.com/<owner>/stg17-<iso3>.git
cd stg17-<iso3>
pip install -r requirements.txt
jupyter lab notebooks/
```

Chaque carnet est paramétré par une seule variable en tête :

```python
COUNTRY_ISO3 = "<ISO3>"
```

Changez-la et la chaîne s'exécute sur un autre pays. C'est délibéré : ces travaux
sont faits pour être réutilisés.

Les intrants bruts ne sont **pas** dans ce dépôt — ils sont volumineux et, dans
certains cas, ne nous appartiennent pas au point de pouvoir les rediffuser.
[`data/README.md`](data/README.md) indique d'où vient chacun et comment
le récupérer.

---

## Licence

| Quoi | Licence |
|---|---|
| Code et carnets | [MIT](LICENSE) |
| Contenus rédigés et figures | CC BY 4.0 |
| Données dérivées dans `data/processed/` et `outputs/` | [voir LICENSE-DATA](LICENSE-DATA) |

> ⚠️ **Si un intrant est une donnée ouverte Ookla**, la production dérivée hérite
> de la **CC BY-NC-SA 4.0** — le « pas d'usage commercial » et le « partage dans
> les mêmes conditions » se propagent tous deux. Elle ne peut pas être diffusée
> sous la licence de données ouvertes standard de votre office. Voir
> [le guide de publication](https://stg17-africa.github.io/stg17-workshop/fr/publish/).

## Citation

Voir [`CITATION.cff`](CITATION.cff), ou utilisez le bouton **Cite this
repository** en haut à droite de cette page.

## Maintenance

**Mainteneur :** <Nom>, <fonction>, <adresse institutionnelle>

Une personne, pas un département. S'il ou elle part, cette ligne est mise à jour.
Les issues et pull requests sont bienvenues, y compris d'autres offices nationaux
de statistique.

---

<sub>Produit au titre du Plan d'action STG17 2025-2030, paquet de travail 4.2,
avec la Banque africaine de développement comme Secrétariat du STG17 et
l'UA STATAFRIC. Ni la BAD ni l'UA STATAFRIC ne prennent position sur une
quelconque délimitation frontalière figurant dans ce dépôt.</sub>
