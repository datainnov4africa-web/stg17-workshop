# Avant l'atelier

L'agenda ne tient que si la préparation ci-dessous est faite. Cette section est
volontairement brève — six pages, et seule la première est de lecture obligatoire.

<div class="stg-cards" markdown>

<div markdown>
### :material-clipboard-check: Prérequis
La liste complète, déduite des neuf laboratoires. **Commencez ici.**

[Lire →](prerequisites.md)
</div>

<div markdown>
### :material-account-key: Comptes à créer
Six comptes, aucun payant. À quoi sert chacun et combien de temps il prend.

[Lire →](accounts.md)
</div>

<div markdown>
### :material-folder-table: Votre paquet de données national
Trois fichiers qui font que la semaine produit les indicateurs de *votre* pays.

[Lire →](data-pack.md)
</div>

<div markdown>
### :material-gpu: Quand Kaggle est nécessaire
Le plus souvent jamais. Deux laboratoires font exception.

[Lire →](kaggle.md)
</div>

<div markdown>
### :material-notebook-check: Vérification d'environnement
Un carnet, cinq minutes, une chaîne de diagnostic à nous envoyer.

[Exécuter →](environment-check.md)
</div>

<div markdown>
### :material-presentation: Gabarit des diapositives pays
Six diapositives pour l'échange du Jour 1. Soyez francs sur ce qui n'a pas marché.

[Lire →](country-slides.md)
</div>

</div>

## Le calendrier de préparation

| Quand | Qui | Quoi |
|---|---|---|
| T − 6 semaines | Secrétariat (BAD) | Confirmer dates, lieu, plateforme hybride et interprétation ; émettre les invitations portant la demande de contribution pays et la liste du paquet de données |
| T − 4 semaines | Points focaux pays | Confirmer les participants et désigner l'équipe pays qui portera le travail jusqu'au vendredi |
| T − 4 semaines | Animateur principal | Geler le jeu de carnets dans les deux versions, guidée et ouverte ; créer l'organisation GitHub et un dépôt par pays |
| T − 3 semaines | Assistants techniques | Copier en miroir les tuiles Ookla, les rasters WorldPop et les sous-ensembles NTL pour chaque pays participant ; préparer les extraits pré-découpés et le pays de référence |
| **T − 2 semaines** | **Participants** | **Envoyer les six diapositives pays ; créer un compte GitHub ; soumettre le paquet de données national** |
| T − 2 semaines | Secrétariat | Fournir les clés API LLM et Groq avec quotas par participant ; provisionner et charger le cluster Elasticsearch |
| T − 1 semaine | Assistants techniques | Animer la vérification d'environnement à distance — une heure, proposée deux fois dans deux fuseaux |
| T − 1 semaine | Animateur principal | Répétition à blanc de chaque laboratoire de bout en bout sur une machine aux spécifications de l'atelier, en chronométrant chaque étape |
| Jour 0 | Tous | Test de salle et de réseau ; distribution des clés USB contenant toutes les données, carnets et présentations |
| T + 1 semaine | Secrétariat | Publier enregistrements et carnets ; consolider le mur d'engagements en un calendrier de suivi daté |

## Risques connus, et leur traitement

**La bande passante** est la cause d'échec la plus fréquente des laboratoires,
d'où le fait que chaque jeu de données soit copié en miroir localement et
distribué sur clé USB plutôt que téléchargé pendant les séances — et que chaque
laboratoire géospatial dispose d'une variante Earth Engine qui ne télécharge rien.

**Les clés API en échec ou limitées** sont traitées par des quotas par participant
provisionnés à l'avance, et par un chemin de démonstration animé par le
facilitateur pour chaque étape dépendant d'une API.

**L'hétérogénéité des portables** est absorbée par le repli Colab, testé pendant
la vérification d'environnement plutôt que découvert au Jour 1.

**Les niveaux inégaux** sont traités par les carnets à deux pistes et par
l'appariement de participants de niveaux différents à partir du Jour 3.

**Les données nationales incomplètes** — fichier de frontières manquant,
indicateur disponible seulement au niveau national — sont traitées par le pays de
référence entièrement préparé, afin qu'aucune équipe ne perde une journée.
