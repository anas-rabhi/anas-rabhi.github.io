---
title: "Pourquoi ton RAG ne marche pas (et comment l'améliorer)"
description: "Un RAG basique donne souvent 50 à 70 % de bonnes réponses. Voici les causes principales quand ça ne marche pas, et les pistes d'optimisation qui font la différence."
categories:
  - "Blog"
  - "IA"
  - "RAG"
tags:
  - "RAG"
  - "Optimisation"
  - "Retrieval"
  - "LLM"
date: 2026-02-05
comments: true
authors:
  - Anas
pin: true
math: true
mermaid: true
---

## Introduction

Un RAG "basique" est rapide à mettre en place, mais il plafonne souvent entre 50 et 70 % de bonnes réponses. En entreprise, ce n'est pas suffisant pour un usage fiable.

Si tu veux d'abord comprendre **pourquoi le RAG reste utile malgré les grandes fenêtres contextuelles**, j'ai un article dédié :  
[Le RAG est-il vraiment fini ?](/blog/2026/02/05/le-rag-est-il-vraiment-fini/)

Ici, on se concentre sur l'autre question : **pourquoi un RAG ne répond pas correctement, et comment l'améliorer**.

<!-- more -->

## 1) Le LLM n'est pas assez bon

Ce cas est le plus simple. En général, avec le bon contexte, les derniers LLMs savent répondre.

Quand le LLM est en cause ? Souvent quand il est noyé dans l'information : on récupère trop de chunks, parfois pas assez pertinents, et la vraie info se perd.

Comment corriger ? Soit on choisit un meilleur modèle, soit on optimise le nombre de chunks à extraire. Mais ça, c'est un autre chantier.

## 2) Le parsing des documents est insuffisant

Le parsing consiste à extraire correctement les informations des documents. Exemple : une facture doit être extraite de façon structurée. Les tableaux sont un cas classique : selon leur format, récupérer les colonnes et les lignes peut devenir très complexe. Même les images posent problème, sauf si on les décrit via un LLM et qu'on insère la description dans le texte.

Le parsing est l'un des plus gros problèmes du RAG. Il est difficile d'avoir un parsing propre, car chaque entreprise structure ses documents différemment (tableaux, images, formules, graphiques, etc.). Le parsing est donc spécifique à chaque type de document, même s'il existe des solutions qui tentent de généraliser (par exemple docling : https://www.docling.ai/).

## 3) L'information n'est pas dans le contexte fourni

Parfois, on ne récupère pas les bons documents : la requête est floue ou ne matche pas bien avec la base vectorielle.

Dans ce cas, le problème peut venir du **chunking**. Exemple : un PDF où le dernier paragraphe est coupé sur deux pages, et une méthode de chunking qui découpe par page. Résultat : le paragraphe est scindé en deux chunks, et le LLM ne trouve pas la bonne info.

Si c'est la cause (on peut le savoir en analysant les erreurs, voir cet [article](/blog/2025/06/04/mon-rag-ne-marche-pas-pourquoi-l-analyse-derreur-change-tout/)), il faut travailler le chunking : taille des chunks, méthode de découpage, overlap, etc.

## 4) L'information n'est pas dans les documents (et le chunking est bon)

Parfois, même avec un bon chunking, le problème vient du **retriever**. Le retriever récupère les chunks pertinents et les injecte dans le prompt. S'il ne trouve pas les bons chunks, le LLM ne pourra pas répondre.

Souvent, la recherche est sémantique. On utilise un modèle d'embeddings pour vectoriser les documents, puis la question de l'utilisateur, et on compare les vecteurs (avec le même modèle, sinon ça n'a pas de sens).

On peut optimiser l'embedding model, surtout si vous utilisez un modèle open source comme `BAAI/bge-m3` (https://huggingface.co/BAAI/bge-m3). Si vous utilisez un modèle comme `text-embedding-3-large` d'OpenAI, on est déjà sur du très performant, sauf si votre champ lexical est très spécifique (univers de niche). Dans ce cas, on peut imaginer un fine-tuning, mais c'est une option à privilégier après les autres.

Une méthode très efficace consiste à **combiner recherche sémantique et recherche par mots-clés**, via des techniques de type BM25 (https://en.wikipedia.org/wiki/Okapi_BM25). Dans certains cas, on observe des gains de 10 à 20 % de qualité. Exemple : sur un site e-commerce, une requête sur une couleur peut être mal gérée par la recherche sémantique ; ajouter la recherche par mots-clés force les chunks qui contiennent la couleur.

Enfin, même avec tout ça, le retriever peut ne pas atteindre les performances ciblées (viser 100 % de bonnes réponses n'est pas réaliste). Une cause fréquente : la recherche est basée sur la **question**, alors que ce qu'on veut extraire, c'est la **réponse**. La question peut être trop courte ou vague. Il existe des techniques pour ça (https://arxiv.org/pdf/2312.10997), comme HyDE (Hypothetical Document Embeddings), très utile quand la question est mal formulée.

## Conclusion

Un RAG qui marche bien, ce n'est pas un RAG "magique" : c'est un RAG **analysé, mesuré et optimisé**. La qualité dépend du parsing, du chunking, du retriever et du modèle.

Si tu veux, je peux aussi détailler une méthode simple d'audit pour identifier rapidement la vraie cause des erreurs.

***

Si mes articles vous intéressent et que vous avez des questions ou simplement envie de discuter de vos propres défis, n'hésitez pas à m'écrire à [anas0rabhi@gmail.com](mailto:anas0rabhi@gmail.com), j'aime échanger sur ces sujets !

Vous pouvez aussi vous abonner à ma newsletter :)


---

### À propos de moi

Je suis **Anas Rabhi**, consultant Data Scientist freelance. J'accompagne les entreprises dans leur stratégie et mise en œuvre de solutions d'IA (RAG, Agents, NLP). 

Découvrez mes services sur [tensoria.fr](https://tensoria.fr) ou testez notre solution d'agents IA [heeya.fr](https://heeya.fr).

<div style="text-align: center; margin: 40px 0;">
  <a href="https://anas-ai.kit.com/d8b1a255cc" target="_blank" style="display: inline-block; background-color: #222222; color: #ffffff; font-weight: bold; padding: 16px 32px; text-decoration: none; border-radius: 8px; font-size: 18px; letter-spacing: 0.8px; box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2); transition: all 0.3s ease; border: none;">
    <span style="margin-right: 10px;">✉️</span> S'abonner à ma newsletter
  </a>
</div>
