---
title: "Le RAG est-il vraiment fini ?"
slug: le-rag-est-il-vraiment-fini
description: "Le RAG est-il remplacé par le long context LLM ? Analyse des coûts, de la pertinence et des cas d'usage qui montrent que le RAG reste incontournable en entreprise."
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

Le RAG s'est imposé depuis l'arrivée de ChatGPT parce qu'il répond à une problématique majeure : la connaissance des LLMs est limitée aux données vues pendant l'entraînement. Or, dans la plupart des cas d'usage en entreprise, on veut que l'IA réponde sur les données internes. C'est d'ailleurs le même principe qui est utilisé par les moteurs de recherche IA comme Perplexity pour [indexer et citer les contenus web](geo-comment-fonctionnent-les-moteurs-ia.md).

Le RAG a un côté "magique" : si on combine une base vectorielle qui stocke les documents de l'entreprise et un LLM, on peut permettre à l'IA de répondre à n'importe quelle question sur ces données.

### Comment ça marche ?

Un RAG a deux grandes étapes :

1) **Traitement & ingestion**  
On traite les documents, on les découpe en chunks, puis on les ingère dans une base vectorielle (exemple : https://www.cloudflare.com/fr-fr/learning/ai/what-is-vector-database/). Cette étape n'est pas visible par l'utilisateur et est faite au début du projet, puis mise à jour à chaque changement de document.

2) **Recherche & génération**  
À chaque requête, on récupère les chunks pertinents via la base vectorielle, puis on les injecte dans le prompt du LLM pour améliorer la réponse et réduire les hallucinations.

La mise en place d'un RAG "basique" est assez simple et rapide. Et comme l'humain généralise vite, on se dit : *c'est parfait, on met en prod, c'est fini*. Sauf que ça ne se passe jamais comme ça.

Un RAG rapide donne souvent 50 à 70 % de bonnes réponses. En entreprise, ça peut ne pas suffire pour l'exposer aux utilisateurs finaux.

Si ce sujet t'intéresse, j'ai détaillé les causes fréquentes d'un RAG qui ne répond pas bien, et comment les corriger dans cet article :
[Les 4 causes techniques d'échec d'un RAG (et comment les corriger)](les-4-causes-techniques-echec-rag.md)

## RAG vs Long Context LLM : le vrai débat

C'est là où le débat se concentre depuis 2024. Avec des fenêtres contextuelles qui explosent (Gemini à 1M tokens, Claude à 200K), on se dit : *"Si je peux tout mettre dans le contexte, pourquoi me compliquer avec un RAG ?"*

La question est légitime. Voilà ce que ça donne en pratique :

| | RAG | Long Context LLM |
|---|---|---|
| **Coût par requête** | Faible (3-5 chunks injectés) | Élevé (tout le corpus à chaque fois) |
| **Qualité sur grand corpus** | Bonne si le retrieval est bon | Se dégrade avec la taille |
| **Latence** | Rapide | Plus lente sur long contexte |
| **Mise à jour des données** | Ré-indexation partielle | Rechargement complet |
| **Adapté pour** | Corpus de 50+ documents | 5-20 documents courts |

Un effet souvent sous-estimé : le **"lost in the middle problem"**. Plus on injecte de contexte, plus le LLM a tendance à négliger ce qui est au milieu. Il retient mieux le début et la fin. Sur un corpus de 400 pages, cette dégradation est réelle et mesurable.

## Quand le Long Context est vraiment préférable

Il y a des cas où injecter tout le contexte est la bonne décision :

- **Un seul document long** : un contrat de 50 pages, un rapport annuel, un code source → pas besoin de RAG, on met tout dedans et on pose des questions.
- **Questions qui croisent tout un document** : "Quelles sont les contradictions dans ce texte ?" → le RAG peut rater des passages si la question est trop large.
- **Synthèse globale d'un document** : "Résume l'essentiel de ce livre blanc" → plus fiable qu'un retrieval partiel sur des chunks.
- **Corpus de moins de 20 documents courts** : si tout rentre sans exploser les coûts, la complexité d'un RAG n'est pas justifiée.

Le RAG reste le bon choix dès que le corpus est grand, les requêtes sont ciblées, le coût est une contrainte, ou les données changent souvent.

## Ce que les partisans du "RAG c'est fini" oublient

Deux contraintes que le Long Context LLM ne résout pas :

**La confidentialité des données.** En entreprise, les documents RH, juridiques, techniques ne peuvent pas toujours partir vers un LLM cloud. Un RAG on-premise avec un LLM local (Llama, Mistral) reste la seule option dans ce cas. Le Long Context n'y change rien.

**Le coût à l'échelle.** 100 utilisateurs × 10 questions/jour = 1000 requêtes. À 2€ la requête en Long Context (corpus de 500 pages), c'est 2000€/jour. Avec un RAG, on injecte 3-5 chunks pertinents par requête — le coût chute de 90%+. En entreprise, ça compte énormément.

## Le RAG évolue : vers l'Agentic RAG

Le vrai mouvement, c'est que le RAG n'est plus "juste" du retrieval vectoriel. Il intègre des capacités d'agent : reformulation de requête, recherche multi-sources, vérification des résultats, itération.

L'**Agentic RAG**, c'est un RAG où l'IA décide elle-même de relancer une recherche si les premiers résultats ne suffisent pas, de combiner plusieurs sources, ou d'adapter sa stratégie de recherche. C'est une réponse directe aux limites du RAG classique sur les requêtes complexes.

J'en parle concrètement dans [le cas client BTP](cas-usage-rag-redaction-appels-offres-btp.md) où un RAG multi-sources couplé à un agent rédacteur a permis de gagner 83% du temps sur la rédaction d'appels d'offres. Et dans [c'est quoi un agent IA](c-est-quoi-un-agent-ia.md) si vous voulez comprendre la différence fondamentale entre les deux approches.

## Conclusion : le RAG est-il vraiment fini ?

Le RAG n'est pas mort. Il reste une approche pragmatique pour rendre les LLMs utiles sur des données internes, avec un bon équilibre entre pertinence, coûts et qualité.

Le Long Context LLM est un outil complémentaire, pas un remplacement. Chacun a ses cas d'usage. Et l'Agentic RAG représente l'évolution naturelle pour les cas où le RAG classique atteint ses limites.

Plutôt que de se demander si le RAG est fini, la vraie question est : **à quel moment un RAG est utile (ou non) pour votre cas d'usage** — et comment l'optimiser quand c'est le bon choix.

***

Si mes articles vous intéressent et que vous avez des questions ou simplement envie de discuter de vos propres défis, n'hésitez pas à m'écrire à [anas0rabhi@gmail.com](mailto:anas0rabhi@gmail.com), j'aime échanger sur ces sujets !

Vous pouvez aussi [réserver un créneau d'échange](https://cal.eu/anas-rabhi/rendez-vous-ianas) ou vous abonner à ma newsletter :)


---

### À propos de moi

Je suis **Anas Rabhi**, consultant Data Scientist freelance. J'accompagne les entreprises dans leur stratégie et mise en œuvre de solutions d'IA (RAG, Agents, NLP). 

Découvrez mes services sur [tensoria.fr](https://tensoria.fr) ou testez notre solution d'agents IA [heeya.fr](https://heeya.fr).

<div style="text-align: center; margin: 40px 0; gap: 16px; display: flex; flex-wrap: wrap; justify-content: center;">
  <a href="https://cal.eu/anas-rabhi/rendez-vous-ianas" target="_blank" style="display: inline-block; background-color: #4F46E5; color: #ffffff; font-weight: bold; padding: 16px 32px; text-decoration: none; border-radius: 8px; font-size: 18px; letter-spacing: 0.8px; box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2); transition: all 0.3s ease; border: none;">
    Réserver un créneau
  </a>
  <a href="https://anas-ai.kit.com/d8b1a255cc" target="_blank" style="display: inline-block; background-color: #222222; color: #ffffff; font-weight: bold; padding: 16px 32px; text-decoration: none; border-radius: 8px; font-size: 18px; letter-spacing: 0.8px; box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2); transition: all 0.3s ease; border: none;">
    <span style="margin-right: 10px;">✉️</span> S'abonner à ma newsletter
  </a>
</div>
