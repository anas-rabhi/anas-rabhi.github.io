# Plans des 4 articles à écrire

Recherches réalisées sur : LangChain, LlamaIndex, Weaviate, Qdrant, Pinecone, Anthropic, HuggingFace, Elasticsearch, Azure AI Search, JinaAI, Eugene Yan, Jason Liu, RAGAS, papiers arXiv.

---

## Article 1 — Agentic RAG vs RAG classique : quelle différence ?

**Mot-clé cible** : "agentic RAG" / "agent RAG différence" / "RAG agentique"
**Concurrence FR** : quasi nulle (seul Microsoft AI Agents for Beginners traduit existe)
**Longueur cible** : ~2 500 mots
**Lien interne pilier** : c-est-quoi-un-agent-ia.md, rag-trop-simple.md, cas-usage-rag-redaction-appels-offres-btp.md

### Angle différenciateur
Pas un article "comment implémenter", mais un article de **décision** : l'agentique est un spectre, pas un interrupteur. La plupart des articles FR traitent ça comme "RAG = simple, Agentique = avancé". La vraie question c'est : à partir de quel niveau de complexité l'overhead vaut le coup ?

### Plan

**H2 — Ce que fait un RAG classique (et pourquoi ça suffit souvent)**
- Le pipeline linéaire en 3 étapes : embed → retrieve → generate
- Ce que ça gère bien : FAQ, Q&A simple, recherche documentaire
- Ce que ça rate : questions multi-saut, sources hétérogènes, validation de la réponse
- Tableau : 5 cas d'échec typiques du RAG classique

**H2 — L'agentique, c'est un spectre (pas un interrupteur)**
- Framework HuggingFace : 4 niveaux d'agentisme (le plus utile pour comprendre)
  - Niveau 1 : LLM décide de retriever ou pas (routing)
  - Niveau 2 : LLM évalue la qualité des documents récupérés
  - Niveau 3 : LLM reformule sa requête si les résultats sont mauvais
  - Niveau 4 : LLM orchestre plusieurs sources, outils, agents
- Conséquence : on ne "passe pas" à l'agentique, on glisse sur ce spectre

**H2 — Les 5 patterns agentiques (avec schémas mermaid)**
Chaque pattern = 1 problème réel qu'il résout + schéma du flux

1. **Self-RAG** (Asai et al. 2023) : l'IA qui critique ses propres récupérations via des "reflection tokens". Cas d'usage : quand on veut éviter les hallucinations sans rajouter d'orchestration externe.

2. **Corrective RAG** (CRAG) : évalue la qualité des documents récupérés, déclenche une recherche web en fallback si score faible. Cas d'usage : base de connaissance incomplète.

3. **Adaptive RAG** : route les requêtes selon leur complexité — directement au LLM, RAG simple, ou pipeline multi-étapes. Cas d'usage : mix de questions simples et complexes.

4. **RAG avec outils** (ReAct) : le LLM décide quels outils appeler — vector DB, SQL, web search, API. Cas d'usage : données dans plusieurs systèmes hétérogènes.

5. **Multi-agent RAG** : agents spécialisés par source (base interne, emails, web), orchestrés par un agent maître. Cas d'usage : notre exemple BTP (4 index spécialisés).

**H2 — Le vrai coût de l'agentique**
Tableau comparatif sur 4 axes :

| | RAG classique | Advanced RAG | Agentic RAG | Multi-Agent |
|---|---|---|---|---|
| Latence | 1–3s | 2–5s | 5–30s | 30s–3min |
| Coût | 1 appel LLM | 2–3 appels | 3–10 appels | 10–50 appels |
| Fiabilité | Prévisible | Prévisible | Variable | Difficile |
| Complexité | Faible | Moyenne | Haute | Très haute |

- Principe Anthropic : "Commencez par la solution la plus simple. N'ajoutez de l'agentique que quand le workflow ne peut pas être prédéfini à l'avance."

**H2 — Comment décider : grille de décision pratique**
Arbre de décision :
- Tes questions ont toujours la même structure ? → RAG classique suffit
- La réponse nécessite de croiser plusieurs sources distinctes ? → Multi-sources (pas forcément agentique)
- Tu ne peux pas prédire les étapes à l'avance ? → Agentique
- La fiabilité doit être proche de 100% ? → Évite l'agentique

**H2 — Un exemple concret : notre cas BTP**
Lier à l'article existant : pourquoi le RAG multi-sources du BTP est un Agentic RAG (niveau 3–4), et pas juste un RAG classique.

**H2 — FAQ**
- Quelle différence entre Agentic RAG et un agent IA classique ?
- Quels frameworks pour implémenter de l'Agentic RAG ? (LangGraph, LlamaIndex Workflows)
- L'Agentic RAG coûte-t-il vraiment beaucoup plus cher ?
- Puis-je convertir mon RAG classique en Agentic RAG ?

---

## Article 2 — Optimiser son RAG : les 8 techniques qui font vraiment la différence

**Mot-clé cible** : "optimiser RAG" / "améliorer performances RAG" / "RAG optimization"
**Concurrence FR** : très faible (articles existants sur tensoria.fr, paul.argoud.net sont superficiels)
**Longueur cible** : ~2 800 mots
**Lien interne pilier** : rag-trop-simple.md, les-4-causes-techniques-echec-rag.md, pourquoi-le-rag-ne-fonctionne-pas.md

### Angle différenciateur
Tous les articles d'optimisation RAG en FR listent des techniques dans le vide. Celui-ci est **orienté ROI** : pour chaque technique, on donne le gain mesuré, l'effort, et quand l'appliquer. Le point de départ vient du principe de Jason Liu : établir 97% de recall comme baseline avant d'optimiser quoi que ce soit.

### Plan

**H2 — Avant d'optimiser : comment mesurer ce que tu as vraiment**
- Le problème : la plupart des gens optimisent sans baseline
- L'approche Jason Liu : générer des questions synthétiques par chunk, mesurer le recall
- Les 3 métriques essentielles : Hit Rate, MRR (retrieval), Faithfulness (génération)
- RAGAS en 5 minutes (tool) — explication simple des formules
- Objectif : 97% recall en retrieval avant de toucher à la génération

**H2 — Phase 1 : Améliorer la requête avant la recherche (pre-retrieval)**

Technique 1 : **HyDE** (Hypothetical Document Embeddings)
- Mécanisme : le LLM génère un "document hypothétique" idéal, on l'utilise comme query
- Pourquoi ça marche : les requêtes sont courtes et ambiguës ; les documents sont longs et riches
- Implémentation : 3 lignes avec LangChain
- Gain : +5–15% sur les requêtes courtes ambiguës

Technique 2 : **Multi-Query + RAG-Fusion**
- Mécanisme : N reformulations en parallèle, fusion avec RRF
- Quand l'utiliser : quand les utilisateurs posent des questions "mal formulées"
- Coût : N appels embedding supplémentaires (faible)

Technique 3 : **Step-Back Prompting**
- Pour les questions très spécifiques qui nécessitent du contexte généraliste

**H2 — Phase 2 : Améliorer ce qu'on récupère (retrieval)**

Technique 4 : **Hybrid Search BM25 + Vectoriel**
- 1 paragraphe + lien vers l'article dédié
- Gain benchmark : +4–8% vs vectoriel seul (Microsoft, BEIR)
- Quand critique : jargon technique, acronymes, noms propres

Technique 5 : **Contextual Retrieval (Anthropic)**
- Le seul article FR à couvrir cette technique en détail
- Mécanisme : prépendre 50–100 tokens de contexte à chaque chunk avant embedding
- Benchmark dur : −35% à −67% de taux d'échec
- Coût : ~1,02€ par million de tokens (avec prompt caching)
- Code : le prompt exact d'Anthropic

**H2 — Phase 3 : Améliorer ce qu'on passe au LLM (post-retrieval)**

Technique 6 : **Reranking (cross-encoder)**
- Architecture 2 étapes : bi-encoder (rapide) + cross-encoder (précis)
- Benchmark LlamaIndex : JinaAI + bge-reranker-large = 0.938 hit rate
- Benchmark Azure : hybrid + reranker = +48% vs BM25 seul
- Options : bge-reranker-large (open-source), Cohere Rerank (API)
- Quand l'ajouter : quand le retrieval renvoie trop de docs corrects mais mal classés

Technique 7 : **Context Compression + LongContextReorder**
- "Lost in the Middle" (Liu et al. 2023) : l'info au milieu du contexte est ignorée
- Solution : réordonner les chunks les plus pertinents en début/fin
- Compression : ne garder que les phrases pertinentes de chaque chunk (LLM ou embedding-based)

**H2 — Phase 4 : Optimisations transversales (infrastructure)**

Technique 8 : **Semantic Caching**
- Mécanisme : cache vectoriel des requêtes similaires
- Benchmark Redis : 15x plus rapide sur les requêtes répétées, −50% coût LLM
- Seuil de similarité : 0.90–0.95 (régler selon la fraîcheur des données)

**H2 — Prioriser : tableau ROI par technique**

| Technique | Gain mesuré | Effort | Quand l'appliquer en premier |
|---|---|---|---|
| Hybrid Search | +4–8% Hit Rate | Faible | Dès que tu as du jargon/acronymes |
| Reranking | +15–24% NDCG | Moyen | Si le retrieval ramène du bruit |
| Contextual Retrieval | −35–67% échecs | Moyen | Si les chunks manquent de contexte |
| HyDE | +5–15% | Faible | Requêtes courtes/ambiguës |
| Multi-Query | +5–10% recall | Faible | Utilisateurs qui formulent mal |
| Semantic Cache | 15x latence | Moyen | Dès que le trafic répété >20% |

**H2 — FAQ**
- Par quoi commencer pour optimiser un RAG en production ?
- RAGAS est-il gratuit ?
- Quelle différence entre reranking et re-retrieval ?
- Est-ce que l'optimisation aide si mes données sont de mauvaise qualité ?

---

## Article 3 — RAG hybride BM25 + recherche vectorielle : comment l'implémenter

**Mot-clé cible** : "RAG hybride" / "hybrid search RAG" / "BM25 vectoriel RAG"
**Concurrence FR** : nulle (aucun article sérieux en FR)
**Longueur cible** : ~2 800 mots
**Lien interne pilier** : mais-que-es-le-rag.md, rag-trop-simple.md, les-4-causes-techniques-echec-rag.md

### Angle différenciateur
L'article de référence EN c'est Weaviate et Elasticsearch. En FR, rien. Angle unique : partir du **problème terrain** (le vocabulary mismatch que tout le monde vit sans mettre un nom dessus), expliquer pourquoi BM25 et vectoriel sont complémentaires (leurs erreurs ne sont pas corrélées), puis aller jusqu'à l'implémentation avec 3 stacks différentes et les benchmarks réels pour justifier.

### Plan

**H2 — Le problème que le hybrid search résout**
- Scénario : "Quelle est la procédure ISO-27001 ?" → 0 résultat en vectoriel pur
- Pourquoi : le vectoriel encode le sens, rate les correspondances exactes
- Vocabulaire : "vocabulary mismatch" — le problème qu'on vit sans l'avoir nommé
- Les 3 types de requêtes où le vectoriel seul échoue :
  1. Jargon métier (DTU 31.2, CSRD, IFRS 9)
  2. Noms propres, numéros de produit, codes erreur
  3. Requêtes mixtes (ex: "configurer Redis en cluster sur AWS")
- Et les 3 types où BM25 seul échoue (questions conceptuelles, synonymes, multilingue)

**H2 — Comment fonctionne BM25 (sans les mathématiques)**
- L'idée : un mot rare dans un document court = très pertinent
- Les 2 paramètres qui comptent :
  - k1 (défaut : 1.2) — la "saturation" : après la 5e occurrence d'un mot, ça n'apporte plus grand chose
  - b (défaut : 0.75) — la normalisation par longueur
- La vision moderne : BM25 comme vecteur creux (sparse vector) — pourquoi c'est important pour les architectures
- BM25 vs SPLADE vs BGE-M3 sparse : quand utiliser quoi (tableau)

**H2 — Reciprocal Rank Fusion : l'algorithme de fusion qui marche**
- Pourquoi on ne peut pas simplement additionner les scores (plages incompatibles)
- RRF : une formule simple — `1/(k + rang)` — et pourquoi elle est robuste
- Exemple numérique pas à pas (doc A dans les 2 listes vs doc B dans une seule)
- k = 60 (Elasticsearch/Azure) vs k = 2 (Qdrant) : quelle différence
- RelativeScoreFusion (Weaviate) : +6% recall vs RRF sur FIQA

**H2 — Les benchmarks qui justifient d'implémenter**
- Microsoft Azure (BEIR + données clients) :
  - BM25 seul : 40.6 NDCG@3
  - Vectoriel seul : 43.8 NDCG@3
  - Hybrid : 48.4 NDCG@3 (+12% vs BM25, +10% vs vectoriel)
  - Hybrid + reranker : 60.1 NDCG@3 (+48% vs BM25 !)
- Elasticsearch (BEIR) : hybrid +1.4% vs vectoriel, +18% vs BM25
- LlamaIndex : Hit Rate 0.938 avec la combo optimale (hybrid + reranker)

**H2 — Implémentation : 3 stacks en pratique**

*Option 1 — LangChain + FAISS/Chroma (stack minimal, open-source)*
```python
# EnsembleRetriever avec BM25 + FAISS
# 15 lignes de code, RRF natif, c=60
```

*Option 2 — LlamaIndex + QueryFusionRetriever*
```python
# QueryFusionRetriever avec BM25Retriever + VectorIndexRetriever
# alpha tuning, use_async=True
```

*Option 3 — Weaviate (production, tout en un)*
```python
# hybrid query avec alpha, RelativeScoreFusion
# BM25F avec query_properties^2, filtres métadonnées
```

**H2 — Quand utiliser hybrid vs vectoriel pur**

| Situation | Recommandation |
|---|---|
| Jargon métier, acronymes, noms propres | Hybrid (BM25 essentiel) |
| Questions conceptuelles/sémantiques pures | Vectoriel pur |
| Requêtes avec fautes d'orthographe | Vectoriel (plus robuste aux typos) |
| Recherche de code, regex, log patterns | BM25 pur |
| Corpus multilingue | Hybrid avec modèle multilingual (BGE-M3) |
| Prod généraliste sans profiling | Hybrid par défaut |

**H2 — Pour aller plus loin : SPLADE et BGE-M3**
- SPLADE : comme BM25 mais avec expansion de termes (comprend les synonymes)
- BGE-M3 : dense + sparse + ColBERT dans un seul modèle, 100 langues, 8192 tokens
- Quand les choisir à la place de BM25 "classique"

**H2 — FAQ**
- Hybrid search ralentit-il les requêtes ?
- Quelle base de données vectorielle choisir pour du hybrid search ?
- Faut-il fine-tuner BM25 pour mon domaine ?
- Est-ce que BM25 gère le français correctement ?

---

## Article 4 — Chunking optimal pour votre RAG : quelle stratégie choisir ?

**Mot-clé cible** : "chunking RAG" / "stratégie chunking" / "découpage documents RAG"
**Concurrence FR** : nulle (un article Medium.com basique, rien de sérieux)
**Longueur cible** : ~3 000 mots
**Lien interne pilier** : mais-que-es-le-rag.md, les-4-causes-techniques-echec-rag.md, rag-trop-simple.md

### Angle différenciateur
Tous les articles anglophones listent les stratégies. L'angle unique ici : partir des **benchmarks durs** (Chroma Research, LlamaIndex, Anthropic, JinaAI) pour dire ce qui marche VRAIMENT, et finir sur un arbre de décision pratique "quel chunking pour quelle situation". Le résultat contre-intuitif principal : les paramètres par défaut d'OpenAI (800 tokens, 400 overlap) sont parmi les PIRES selon Chroma Research.

### Plan

**H2 — Pourquoi le chunking est la décision la plus importante de ton RAG**
- Un mauvais chunking = impossible à corriger en aval (même avec le meilleur LLM)
- Les 3 problèmes fondamentaux :
  1. Limite de tokens du modèle d'embedding (512 tokens pour la plupart)
  2. "Lost in the Middle" : les LLMs ratent l'info au milieu des longs contextes
  3. Bruit vs signal : plus le chunk est grand, plus l'embedding est dilué
- La règle d'or (Pinecone) : "Si un humain comprend le chunk sans contexte extérieur, le LLM aussi"
- Résultat choc : les paramètres par défaut d'OpenAI Assistants (800 tokens, 400 overlap) sont **les pires** testés par Chroma Research

**H2 — Les 8 stratégies de chunking (de la plus simple à la plus avancée)**

**1. Fixed-size / Taille fixe**
- Ce que c'est, tailles typiques (256–1024 tokens), overlap recommandé (10%)
- Pour qui : point de départ universel
- Benchmark LlamaIndex : 1024 tokens = sweet spot sur docs financiers

**2. Recursive splitting (le vrai standard)**
- Hiérarchie de séparateurs : `\n\n` → `\n` → ` ` → `""`
- La règle souvent ignorée : mesurer en tokens, PAS en caractères (un token ≠ un caractère)
- Code LangChain avec tokenizer HuggingFace
- Pour qui : texte narratif homogène

**3. Structure-aware chunking (Markdown, HTML, code)**
- `MarkdownHeaderTextSplitter` : conserver la hiérarchie en métadonnées
- `HTMLHeaderTextSplitter` : balises sémantiques
- `CodeSplitter` avec tree-sitter : ne jamais couper une fonction au milieu
- Pour qui : documentation, sites web, codebase

**4. Semantic chunking**
- Mécanisme : cosine distance entre embeddings de phrases consécutives pour détecter les changements de sujet
- `breakpoint_percentile_threshold` : le paramètre clé
- Code LlamaIndex SemanticSplitterNodeParser
- Benchmark Chroma : meilleure précision et IoU des méthodes testées
- Pour qui : longs documents multi-sujets. Coût : 2–3x plus lent à l'ingestion

**5. Sentence Window Retrieval (petits chunks, grand contexte)**
- Dissocier ce qu'on indexe (une phrase) de ce qu'on retourne au LLM (±3 phrases autour)
- Résout le trade-off précision/contexte
- Code LlamaIndex (SentenceWindowNodeParser + MetadataReplacementPostProcessor)
- Pour qui : corpus où chaque phrase compte, Q&R précises

**6. Hierarchical / Parent-Child chunking**
- 3 niveaux : 2048 → 512 → 128 tokens
- Auto-merging : si 50%+ des feuilles d'un parent sont récupérées → retourner le parent
- Code LlamaIndex HierarchicalNodeParser + AutoMergingRetriever
- Pour qui : documents longs structurés (rapports, articles techniques)

**7. Late Chunking (JinaAI 2024) — la meilleure amélioration "gratuite"**
- L'idée inversée : d'abord passer tout le document dans le transformer, PUIS découper
- Résultat : chaque token est contextualisé par tout le document
- Benchmark BEIR : +6.5 points sur NFCorpus (long documents)
- Aucun gain sur les documents courts (<200 chars)
- Condition : nécessite un modèle long-context (8192 tokens) — jina-embeddings-v2, text-embedding-3
- Pour qui : tout le monde qui a des documents >800 caractères

**8. Contextual Retrieval (Anthropic 2024) — le plus grand gain mesurable**
- Mécanisme : avant d'embedder chaque chunk, un LLM génère 50–100 tokens de contexte ("ce chunk parle de X dans le document Y, section Z")
- Résout le problème des chunks anonymes ("le chiffre d'affaires a augmenté de 3%" → de qui, quand ?)
- Benchmarks :
  - Contextual Embedding seul : −35% taux d'échec
  - + BM25 contextuel : −49%
  - + Reranking : −67%
- Coût : ~1€ par million de tokens (avec prompt caching Claude)
- Code : le prompt exact à utiliser
- Pour qui : quand la précision est critique et le coût d'une mauvaise réponse est élevé

**H2 — Cas spéciaux : tableaux, PDFs, code**

Tableaux :
- Règle absolue : ne jamais découper un tableau au milieu
- Pattern multi-vecteur : résumé textuel pour l'embedding, tableau brut pour la génération
- Unstructured.io en mode hi_res

PDFs complexes :
- La différence entre PDF "text-based" et PDF "scanné"
- LlamaParse pour les PDFs avec mise en page complexe
- Conserver les titres de section comme métadonnées

Code :
- tree-sitter : le seul bon choix (découpe au niveau AST, pas au niveau ligne)
- LlamaIndex CodeSplitter

**H2 — Quel chunk size choisir : le benchmark LlamaIndex**
- Tests sur un vrai document financier (Uber 10K) avec GPT-3.5-Turbo
- Résultats Faithfulness + Relevancy pour 128 / 256 / 512 / 1024 / 2048 tokens
- Conclusion : 1024 tokens gagne sur les deux métriques
- Nuance : dépend fortement du type de document et des requêtes

**H2 — L'overlap : 10%, pas 50%**
- Pourquoi l'overlap existe : information aux frontières de chunks
- Benchmark Chroma : l'overlap à 50% (défaut OpenAI) est le pire résultat testé
- Règle : 10% de la taille du chunk. Ex : 512 tokens → 51 tokens d'overlap
- Quand augmenter à 15–20% : si les évaluations montrent des miss aux frontières

**H2 — Arbre de décision : quelle stratégie pour quel cas**

```
Quel type de document ?
├── Texte narratif homogène → Recursive (512 tokens, 10% overlap)
├── Markdown/HTML/Docs → Structure-aware splitter
├── PDF avec tableaux → Unstructured hi_res + multi-vecteur
├── Code source → CodeSplitter (tree-sitter)
└── Documents longs multi-sujets → Semantic ou Hierarchical

Quel type de questions ?
├── Requêtes très précises (1 phrase répond) → Sentence Window
├── Questions nécessitant du contexte → Parent-Child / Hierarchical
└── Questions conceptuelles larges → Chunks 1024 tokens

Contraintes de production ?
├── Ingestion rapide → Fixed-size uniquement
├── Haute précision requise → + Contextual Retrieval (Anthropic)
└── Documents longs (>800 chars) → + Late Chunking (JinaAI)
```

**H2 — Comment valider son chunking : méthode en 3 étapes**
1. Générer des questions synthétiques par chunk (LlamaIndex DatasetGenerator)
2. Tester 3–5 tailles de chunk sur ces questions
3. Mesurer Hit Rate + Faithfulness + Relevancy → garder le meilleur

**H2 — FAQ**
- Quelle taille de chunk pour GPT-4 ? Pour Claude ? Pour Mistral ?
- Faut-il rechunker quand on change de modèle d'embedding ?
- Le chunking sémantique vaut-il vraiment le coût supplémentaire ?
- Comment gérer les documents qui se mettent à jour régulièrement ?

---

## Notes transversales

### Cohérence des exemples
- Chaque article peut s'appuyer sur nos 2 cas clients existants (BTP, assurance) pour illustrer le propos
- Les benchmarks cités ont tous des sources EN solides (Microsoft, Anthropic, LlamaIndex, Chroma Research)

### Ordre de publication recommandé
1. **Chunking** en premier (fondamental, lu avant d'aller chercher hybrid ou agentic)
2. **Hybrid Search** (complète le chunking, souvent co-implémenté)
3. **Optimisation RAG** (synthèse, s'appuie sur les deux précédents)
4. **Agentic RAG** (niveau avancé, vient après avoir maîtrisé les bases)

### Maillage entre les 4 articles
- Chunking → lien vers Hybrid Search (souvent implémentés ensemble)
- Hybrid Search → lien vers Optimisation (reranking mentionné dans les deux)
- Optimisation → lien vers Agentic (quand optimiser ne suffit plus)
- Agentic → lien vers les cas clients BTP/assurance (preuves concrètes)

### Éléments à inclure dans chaque article
- 1 schéma mermaid minimum
- 1 tableau comparatif
- 1 FAQ (4–6 questions, pour les featured snippets)
- Meta description ≤ 155 caractères
- Slug sans accents ni double tiret
