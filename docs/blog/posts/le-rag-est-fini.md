---
title: "Le RAG est-il vraiment fini ?"
description: "Avec des fenêtres contextuelles de plus en plus grandes, certains annoncent la fin du RAG. Pourtant, en entreprise, coûts, pertinence et qualité des réponses montrent qu'il reste incontournable."
categories:
  - "Blog"
  - "IA"
  - "RAG"
tags:
  - "RAG"
  - "Intelligence Artificielle"
  - "Stratégie"
  - "Coûts"
date: 2026-02-05
comments: true
authors:
  - Anas
pin: true
math: true
mermaid: true
---

## Introduction : le RAG, une méthode magique ?

À chaque sortie d'un nouveau modèle avec une fenêtre contextuelle plus grande, on annonce le RAG comme dépassé. Pourtant, le RAG est né d'un besoin très concret : on ne peut pas donner un document de 400 ou 500 pages à un LLM et lui poser des questions dessus.

En entreprise, on a souvent des dizaines (voire des centaines) de fichiers. Le RAG apporte une réponse simple : construire une base documentaire avec des petits morceaux (chunks) de documents, puis fournir dynamiquement les morceaux pertinents à l'IA à chaque question.

<!-- more -->


C'est une technique comme une autre : parfois adaptée, parfois non. Si vous avez un petit document de 10 pages, inutile de monter un RAG : on peut le charger directement dans un LLM et poser des questions. En revanche, 100 articles de 100 pages, même si c'est *possible* à charger, ce n'est pas toujours pertinent (ni rentable).

Même si les fenêtres contextuelles explosent (on atteint 1M de tokens, soit environ 700k mots sur certains modèles), charger 1M de tokens reste coûteux : parfois entre 2 et 10 euros par question. Il existe des techniques pour réduire ces coûts (cache, etc.), mais 0,20 € × 100 questions, ça fait quand même 20 €.

Et surtout : injecter trop d'information dégrade souvent la qualité des réponses. Plus on surcharge la fenêtre, plus le LLM se noie. Le RAG n'est donc pas près de disparaître.

Le RAG s'est imposé depuis l'arrivée de ChatGPT parce qu'il répond à une problématique majeure : la connaissance des LLMs est limitée aux données vues pendant l'entraînement. Or, dans la plupart des cas d'usage en entreprise, on veut que l'IA réponde sur les données internes.

Le RAG a un côté "magique" : si on combine une base vectorielle qui stocke les documents de l'entreprise et un LLM, on peut permettre à l'IA de répondre à n'importe quelle question sur ces données.

### Comment ça marche ?

Un RAG a deux grandes étapes :

1) **Traitement & ingestion**  
On traite les documents, on les découpe en chunks, puis on les ingère dans une base vectorielle (exemple : https://www.cloudflare.com/fr-fr/learning/ai/what-is-vector-database/). Cette étape n'est pas visible par l'utilisateur et est faite au début du projet, puis mise à jour à chaque changement de document.

2) **Recherche & génération**  
À chaque requête, on récupère les chunks pertinents via la base vectorielle, puis on les injecte dans le prompt du LLM pour améliorer la réponse et réduire les hallucinations.

La mise en place d'un RAG "basique" est assez simple et rapide. Et comme l'humain généralise vite, on se dit : *c'est parfait, on met en prod, c'est fini*. Sauf que ça ne se passe jamais comme ça.

Un RAG rapide donne souvent 50 à 70 % de bonnes réponses. En entreprise, ça peut ne pas suffire pour l'exposer aux utilisateurs finaux.

Si ce sujet t'intéresse, j'ai détaillé les causes fréquentes d'un RAG qui ne répond pas bien, et comment l'améliorer dans cet article :  
[Pourquoi ton RAG ne marche pas (et comment l'améliorer)](/blog/2026/02/05/pourquoi-ton-rag-ne-marche-pas-et-comment-l-ameliorer/)

## Conclusion : le RAG est-il vraiment fini ?

Le RAG n'est pas mort. Il reste une approche pragmatique pour rendre les LLMs utiles sur des données internes, avec un bon équilibre entre pertinence, coûts et qualité.

Plutôt que de se demander si le RAG est fini, la vraie question est : **à quel moment un RAG est utile (ou non) pour votre cas d'usage**.

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
