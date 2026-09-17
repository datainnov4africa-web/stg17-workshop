<!-- GENERATED from config/agenda.yml by tools/build_site.py. Do not edit. -->

# Glossary

The shared vocabulary of the week. These terms come from the `stg17` package itself, so a notebook, a slide and this page necessarily use the same wording.

!!! tip "Vocabulary discipline"

    The Day 1 morning talk exists to fix these words. An "agent" and a "RAG assistant" are not the same thing, and confusing the two in a terms of reference is expensive. When a term is used loosely during the week, come back here.

## Artificial intelligence

**Prompt engineering**  
*Ingénierie de prompt*

: Shaping a model's input — role, context, constraints, examples — to steer its output. The cheapest lever, and the one to exhaust first.

**Retrieval-Augmented Generation (RAG)**  
*Génération augmentée par récupération (RAG)*

: Retrieving relevant documents and putting them in the model's context, so it answers from your material rather than from memory.

**Fine-tuning**  
*Affinage (fine-tuning)*

: Changing a model's weights on your own examples. The heavy lever — try prompting and RAG first.

**Agent**  
*Agent*

: A model given tools and allowed to decide which to call, in what order. Powerful, and the reason human checkpoints matter.

**Hallucination**  
*Hallucination*

: A fluent, confident, false output. Not a bug to be patched — a property of the mechanism, to be managed by verification.

**Grounding**  
*Ancrage factuel*

: Tying an answer to a retrievable source, so a reader can check it.

**Inference**  
*Inférence*

: Running a trained model to produce output. Where the recurring cost of an AI system actually sits.

**Token**  
*Token*

: The sub-word unit a model reads and writes. Cost and context limits are counted in tokens, not words.

**Embedding**  
*Plongement (embedding)*

: A numeric vector representing meaning, so that similarity can be computed. The mechanism behind retrieval.

**Vector store**  
*Base vectorielle*

: The index that makes similarity search over embeddings fast.

## Night-time lights

**Sum of Lights**  
*Somme des lumières*

: The sum of radiance over an area. A proxy for lit activity — not GDP.

**Radiance**  
*Radiance*

: Light leaving the ground, in nW·cm⁻²·sr⁻¹, as measured by the sensor.

**Lit area**  
*Superficie éclairée*

: The share of territory whose radiance exceeds a chosen threshold. Moves when the threshold moves — always publish both.

**Mean radiance**  
*Radiance moyenne*

: Average radiance over valid pixels. Nearly meaningless alone, because the distribution is extremely skewed.

**Blooming**  
*Halo lumineux (blooming)*

: Light spilling beyond its physical source, so a city lights up more pixels than it occupies. Inflates urban totals.

**Saturation**  
*Saturation*

: The brightest cores exceed the sensor's usable range, so growth there stops appearing in the data.

**Gas flare**  
*Torchère de gaz*

: An industrial flame, extremely bright and constant, that can dominate a region's total while electrifying nobody.

**Cloud mask**  
*Masque nuageux*

: The layer marking pixels obscured by cloud, which must be excluded before any statistic is computed.

**Quality flag**  
*Indicateur de qualité*

: Per-pixel metadata describing how trustworthy that observation is.

## Geography

**National (ADM0)**  
*National (ADM0)*

: The national level.

**Region (ADM1)**  
*Région (ADM1)*

: The first subnational level — regions, provinces, states.

**District (ADM2)**  
*District (ADM2)*

: The second subnational level — districts, departments.

**Zonal statistics**  
*Statistiques zonales*

: Summarising a raster within polygon boundaries. The operation that turns satellite imagery into a statistical table.

**Administrative boundaries**  
*Frontières administratives*

: The polygons defining administrative units. Which file you use changes every subnational figure you publish.

## Connectivity

**Download speed**  
*Débit descendant*

: Measured throughput toward the user, in kbit/s in the Ookla tiles.

**Upload speed**  
*Débit montant*

: Measured throughput from the user.

**Latency**  
*Latence*

: Round-trip delay in milliseconds. Often more decisive than raw speed for whether a service is usable.

**Quadkey**  
*Quadkey*

: The identifier of a web-Mercator tile. Ookla publishes at zoom 16, about 611 m at the equator.

**Tests**  
*Tests*

: The number of speed tests behind a tile's average. A tile with three tests is not comparable with one built from three thousand.

## Statistical practice

**Proxy indicator**  
*Indicateur indirect (proxy)*

: A measurable quantity used to stand in for one you cannot measure directly. Its usefulness is an empirical question, not an assumption.

**Coverage bias**  
*Biais de couverture*

: Systematic under-representation of part of the population, characteristic of non-probabilistic sources. Ookla measures people who run speed tests, not people.

**Validation**  
*Validation*

: Establishing, with evidence, the relationship between a proxy and an official measure — before publishing either.

**Limitations**  
*Limites*

: The statement of what a result cannot support. In this workshop it is part of the deliverable, not an appendix.

**Reproducibility**  
*Reproductibilité*

: Whether someone else, with the same inputs, obtains the same numbers. Requires the parameters, not just the code.

**Metadata**  
*Métadonnées*

: The description that makes a dataset findable and interpretable by someone who was not in the room.

---

This glossary follows the vocabulary used during the week. A term missing? Tell the facilitation team.
