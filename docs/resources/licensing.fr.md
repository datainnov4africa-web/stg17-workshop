# Licences et éthique

Trois questions décident si une production de cet atelier peut être publiée, et
ce sont des questions distinctes. Réussir les deux premières et rater la
troisième est l'échec le plus courant.

## 1 · Quelle licence porte votre production ?

La licence d'un produit dérivé est déterminée par la licence la **plus stricte**
parmi ses intrants. Ce n'est pas une préférence.

| Source utilisée | Sa licence | Ce que votre produit dérivé peut porter |
|---|---|---|
| NASA Black Marble (VNP46A*) | Œuvre du gouvernement américain, de fait domaine public | N'importe quoi, y compris la licence ouverte de votre office |
| NOAA / EOG VNL annuel | Domaine public | N'importe quoi |
| WorldPop | CC BY 4.0 | CC BY 4.0 ou plus strict. Attribution obligatoire |
| geoBoundaries (gbOpen) | CC BY 4.0 | CC BY 4.0 ou plus strict |
| GADM | Usage académique seulement, **pas de rediffusion commerciale** | Inadapté à un produit national publié |
| **Ookla Open Data** | **CC BY-NC-SA 4.0** | **CC BY-NC-SA 4.0 uniquement** |

!!! danger "Le piège Ookla"

    Le « pas d'usage commercial » et le « partage dans les mêmes conditions » se
    propagent tous deux. Un indicateur de connectivité pondéré par la population
    dérivé des tuiles Ookla :

    - ne peut pas être utilisé à des fins commerciales,
    - doit lui-même être diffusé sous CC BY-NC-SA 4.0,
    - **ne peut pas** être diffusé sous la licence de données ouvertes standard de
      votre office si celle-ci autorise la réutilisation commerciale — ce qui est
      le cas de la plupart.

    Ce n'est pas une raison d'écarter la source. C'est une raison de l'indiquer
    sur le produit et de poser la question en interne *avant* que l'indicateur
    n'intègre une publication régulière. Plusieurs offices concluront qu'un accord
    négocié avec Ookla ou avec les opérateurs nationaux est la voie vers un
    indicateur librement réutilisable — c'est exactement la discussion sur les
    partenariats avec le secteur privé de l'activité 3.1 du Plan d'action.

**Gardez les tas séparés.** Si votre produit NTL doit être librement réutilisable
et que votre produit Ookla ne peut pas l'être, publiez-les comme deux produits
clairement séparés avec deux fichiers `LICENSE-DATA`. Un ensemble unique hérite
des conditions les plus strictes pour tout ce qu'il contient.

## 2 · Qu'est-ce qui peut sortir du bâtiment ?

| Donnée | Peut-elle aller vers une API LLM commerciale ? | Peut-elle aller dans un dépôt public ? |
|---|---|---|
| Un annuaire statistique publié | Oui | Oui |
| Des indicateurs agrégés déjà diffusés | Oui | Oui |
| Des chiffres officiels non diffusés | **Non** | **Non** |
| Des microdonnées, même anonymisées | **Non** | **Non** |
| Les fichiers de frontières que votre office publie | Oui | Oui |
| Des données personnelles, quelles qu'elles soient | **Non** | **Non** |

Le laboratoire du Jour 2 envoie un document à une API LLM. Apportez quelque chose
que votre office a **déjà publié**. Ce n'est pas une formalité : la requête quitte
votre réseau, et vous ne maîtrisez pas ce qu'il en advient ensuite.

## 3 · Que prétendez-vous ?

La question éthique propre à cet atelier ne porte pas sur la protection des
données — elle porte sur la sur-interprétation.

Une série de lumières nocturnes présentée comme « le PIB régional » est une
affirmation fausse, faite avec des données réelles, par une institution crédible.
C'est plus dommageable qu'une absence d'indicateur, car elle sera crue et elle
orientera des décisions.

**La discipline :**

- Dire ce que mesure l'indicateur, en une phrase, à côté de chaque figure.
- Dire les paramètres qu'un lecteur ne pourrait pas deviner — le seuil, le
  fichier de frontières, la version du produit, les années exclues.
- Dire la corrélation avec vos chiffres officiels, avec son coefficient, plutôt
  que d'affirmer une équivalence.
- Dire à quoi l'indicateur ne doit **pas** servir.

Le laboratoire du Jour 4 après-midi en fait un document formel, et le gabarit
pays en fait une section obligatoire du README. C'est un livrable, pas un
avertissement de forme.

## 4 · Frontières

La représentation des frontières est politiquement sensible dans plusieurs États
membres. geoBoundaries et FAO GAUL sont commodes pour un atelier et ne portent de
valeur juridique nulle part. Substituez les frontières officielles de votre office
avant de publier, et attendez-vous à ce que les chiffres infranationaux se
déplacent — parfois sensiblement à l'ADM2.

Ni cet atelier, ni la Banque africaine de développement, ni l'UA STATAFRIC ne
prennent position sur une quelconque délimitation. Un dépôt pays engage son propre
office.

## 5 · Une liste de contrôle avant publication

- [ ] Chaque intrant listé, avec sa licence et la date de récupération
- [ ] Licence de sortie déterminée par l'intrant le plus strict, non par préférence
- [ ] Rien de confidentiel, rien de non diffusé, aucune donnée personnelle — **y compris dans l'historique git**
- [ ] Aucune clé API, nulle part, y compris dans les sorties de notebooks
- [ ] Déclaration de limites présente, spécifique, et portant sur votre pays
- [ ] Source des frontières nommée
- [ ] Un mainteneur nommé avec une adresse institutionnelle
