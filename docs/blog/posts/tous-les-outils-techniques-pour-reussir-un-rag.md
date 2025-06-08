---
title: "Tous les outils et techniques pour réussir un RAG"
description: "Vous avez intégré un RAG, mais les résultats ne sont pas à la hauteur ? Découvrez pourquoi l’analyse d’erreur est la clé pour comprendre et améliorer votre projet, avec des exemples concrets et des conseils issus du terrain."
categories:
  - "Blog"
  - "IA"
tags:
  - "RAG"
  - "Intelligence Artificielle"
  - "Conseils Pratiques"
  - "Optimisation"
date: 2025-06-10
comments: true
authors:
  - Anas
pin: true
math: true
mermaid: true
---

## Et si on reparlait... RAG ? 

Bon, l'idée de départ de ce blog n'était pas d'écrire que sur le RAG. Je voulais faire des articles sur l'IA générative, différents cas d'usages, des agents, les MCP, bref un peu tout ce qui sort. Mais comme je suis amené souvent à intervenir sur des sujets RAG, je me dit : "AH c'est vrai que j'ai oublié de parler de ça, de ci ou de ce sujet". Donc je ne pense pas que je vais arrêter de parler de RAG d'aussi tôt. Dans cet article je vais essayer de donner brique par brique ce qui permettrait de réussir un RAG.

Etant dans un univers très vaste, beaucoup d'outils apparaissent chaque jour, beaucoup de personnes en parlent de partout. Donc c'est très compliqué d'identifier ce qui est vraiment utile dans tout cet océan d'information. 

Donc je vais essayer de passer brique par brique dans le RAG et proposer différents outils et méthodes pour aborder et améliorer tout ça.

<!-- more -->

## Le problème des outils RAG

Vu qu'on parle d'un cas d'usage vu, revu et revu. Tous les outils de développement proposent à leur façon d'aider à faire du RAG. On est plus obligé d'être spécialiste en IA pour dire qu'on a fait un RAG. On peut en faire sur des outils No-code comme n8n, ou en faisant du code avec python en utilisant des librairies comme langchain, llamaindex, haystack, j'ai vu facilement passer une vingtaine d'outils assez sérieux, et dans la réalité il doit y en avoir plus d'une centaine chacune avec sa specificité ou pas.

Ces outils présentent des avantages mais aussi pas mal d'inconvenient. L'avantage premier et evident c'est que ça facilite le développement donc on a pas besoin de tout comprendre à l'IA pour faire du RAG. L'inconvenient c'est que ça facilite le développement et donc on ne comprend pas ce qu'on fait réellement, donc au moment où il faut améliorer le RAG, c'est la douche froide, on commence par ou ? Est-ce que l'outil qu'on a utilisé permet assez de flexibilité pour pouvoir faire des amélioration, ou on doit encore changer d'outil. 

Donc vous avez bien compris, le choix des outils principaux conditionne completement le reste du projet, surtout que vous n'aurez pas de RAG parfait du premier coup, en tout cas si vous cherchez à le déployer à d'autres utilisateurs.

D'autant plus que le RAG peut être decomposé en plusieurs briques donc chaque brique peut nécessiter un outil différent, donc l'investissement en temps à monter en compétence sur chaque outil est important.

## Les briques RAG

Dans le RAG il y a plein de choses à optimiser et pendant ce blog j'en parlerait pas de toutes les briques, en tout cas je vais m'attarder sur les plus importantes pour avoir un début de RAG qui tient la route.

=====> OUTILS + HOW TO IMPROVE + PAPERS

- Doc ingestion, text, image, type de document : textract, ocr, pdf docx, images etc (open ai envoi txt +img) , ajouter les outils textract, pixtral etc, docstring ibm

- Chunking : token chunk, semantic chunking, etc... llamaindex, llamadoc parsing, langchain, => 

- indexing : vectordb chroma pinecone etc, word search bm25..., ... graph indexing etc

- retrieving : embedding pb openai, opensource snowflake, mais pas que l'embeddings il y a aussi le querying aller chercher le bon truc
      -> reranking avec jinai, ou llm rerank, cf dspy

- prompt engineering => dspy, vanilla, llamaindex peutetre

- résponse LLM => llamaindex, langchain openai, ....

- monitoring => langfuse, chaque brique





---------

Si mes articles vous intéressent et que vous avez des questions ou simplement envie de discuter de vos propres défis, n'hésitez pas à m'écrire à anas0rabhi@gmail.com, j'aime échanger sur ces sujets !

Vous pouvez aussi vous abonner à ma newsletter :)

<div style="text-align: center; margin: 40px 0;">
  <a href="https://anas-ai.kit.com/d8b1a255cc" target="_blank" style="display: inline-block; background-color: #222222; color: #ffffff; font-weight: bold; padding: 16px 32px; text-decoration: none; border-radius: 8px; font-size: 18px; letter-spacing: 0.8px; box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2); transition: all 0.3s ease; border: none;">
    <span style="margin-right: 10px;">✉️</span> S'abonner à ma newsletter
  </a>
</div>
