---
title: "Les 7 mauvais réflexes des équipes RAG (et comment les corriger)"
slug: mauvais-reflexes-equipes-rag
description: "Les 7 réflexes contre-productifs observés sur 20+ projets RAG : retoucher le prompt en premier, juger sur 3 exemples, blâmer le LLM... Les biais qui font perdre des semaines, et leurs corrections."
categories:
  - "Blog"
  - "IA"
  - "RAG"
tags:
  - "RAG"
  - "Méthode"
  - "Retour d'expérience"
  - "Conseils Pratiques"
  - "Anti-patterns"
date: 2026-05-23
comments: true
authors:
  - Anas
pin: true
math: true
mermaid: true
---

## Introduction

Quand un projet RAG patine, ce n'est presque jamais à cause d'une techno manquante. C'est à cause d'un enchaînement de **réflexes contre-productifs** que les équipes adoptent sans s'en rendre compte. On retouche le prompt alors que le problème est dans le retrieval. On juge "ça marche" sur quatre essais à la main. On empile les techniques avancées avant d'avoir compris où ça bloque.

Après une vingtaine de projets RAG en mission ou en audit, je retrouve toujours les mêmes 7 réflexes. Ce ne sont pas des erreurs techniques, ce sont des biais cognitifs. Mais ils sabotent les performances aussi sûrement qu'un mauvais chunking. Voici la liste, et à chaque fois le réflexe à substituer.

<!-- more -->

> Cet article complète les [5 erreurs récurrentes en projet RAG](les-5-erreurs-rag.md) côté posture et méthode. Pour le panorama complet du RAG, voir le [guide RAG](/rag/).

## Réflexe 1 : Modifier le prompt avant de regarder le retrieval

C'est le réflexe le plus fréquent. Quand une réponse est mauvaise, on relit le prompt, on le retouche, on rajoute une consigne. C'est ce qu'on contrôle visuellement, ce qui change instantanément la sortie. C'est rassurant. Et dans **80 % des cas, ce n'est pas la cause du problème**.

Un RAG est un pipeline. La réponse finale dépend de tout ce qui se passe avant : parsing, chunking, retrieval. Si l'information dont vous avez besoin n'a pas été récupérée par le retriever, le LLM ne pourra pas l'inventer. Vous pouvez tordre le prompt dans tous les sens, vous tournerez en rond.

**Le bon réflexe** : avant de toucher au prompt, ouvrir les **chunks effectivement injectés** pour la requête qui échoue. Si l'information n'y est pas, le prompt n'est pas le problème. C'est tout l'enjeu de l'[analyse d'erreur d'un RAG](pourquoi-le-rag-ne-fonctionne-pas.md), méthode que je détaille dans un article dédié.

## Réflexe 2 : Tester sur 3-4 exemples et conclure "ça marche"

On modifie le chunking, on relance 4 questions, ça semble mieux, on valide. C'est typique d'un biais de disponibilité : ce qu'on a vu remplace ce qu'on n'a pas vu. Une "amélioration" sur 4 cas peut très bien être une dégradation sur 50.

J'ai vu un cas concret où passer la taille de chunk de 1024 à 512 améliorait visiblement les questions courtes (les seules testées par l'équipe). Sur le dataset complet, c'était une dégradation de 12 points : les questions longues, sous-représentées dans les tests à la main, perdaient leur contexte.

**Le bon réflexe** : un **dataset d'évaluation fixe** de 30 à 50 paires question-réponse représentatives, à passer avant et après chaque modification. C'est non négociable. Sans ça, vous n'améliorez pas un système, vous tâtonnez. La méthode complète de construction du dataset et de mesure est ici : [évaluer un RAG en production](evaluer-rag-production-metriques-ragas.md). Une partie de ce contrôle s'automatise avec des [tests unitaires sur le LLM](tester-llm-tests-unitaires.md) (format, longueur, entités), qui remplacent les vérifications à la main.

## Réflexe 3 : Empiler les techniques avancées avant le diagnostic

HyDE, reranker, contextual retrieval, query expansion : ajoutés en cascade "parce qu'on a lu un article qui dit que c'est bien". Sauf que chaque technique a un coût (latence, complexité, dette technique) et un gain **conditionnel**. Si votre problème est le parsing, HyDE n'y changera rien. Si votre problème est la formulation des requêtes, ajouter un reranker masque le symptôme sans traiter la cause.

J'ai audité un système qui empilait 4 techniques avancées et performait à 58 %. Après désactivation de tout sauf le retrieval de base, on était à 61 %. Les techniques avaient été ajoutées sans diagnostic préalable, certaines se compensaient, d'autres se nuisaient mutuellement.

**Le bon réflexe** : diagnostiquer d'abord, ajouter ensuite. Chaque technique doit répondre à une cause identifiée. L'ordre est toujours le même : analyse d'erreur, hypothèse, test isolé sur dataset fixe, décision. Pour le panorama des techniques et le gain typique de chacune : [techniques pour optimiser son RAG](optimiser-rag-techniques.md).

## Réflexe 4 : Blâmer le LLM par défaut

"Le LLM ne comprend pas ma question." Pratiquement jamais. Dans la chaîne RAG, le LLM est en **bout de pipeline**. Il reçoit le contexte qu'on lui donne. Si ce contexte est bon, les LLMs récents (Claude, GPT, Mistral Large) répondent presque toujours correctement. S'il est mauvais, aucun LLM ne sauvera la mise.

Le réflexe "passons au modèle supérieur" est souvent une fausse piste coûteuse. Le passage à un modèle plus haut de gamme sur un RAG défaillant donne en général 1 à 3 points de gain. Corriger une cause de retrieval en donne 15 à 30. Le rapport effort / impact n'est pas le même.

**Le bon réflexe** : commencer le diagnostic par les étapes en amont du LLM (parsing, chunking, retrieval). Le LLM est rarement le maillon faible. Les [4 causes techniques d'échec d'un RAG](les-4-causes-techniques-echec-rag.md) détaillent comment cibler la bonne cause au lieu de blâmer la dernière étape visible.

## Réflexe 5 : Ignorer les sources renvoyées par le retrieval

Pour debugger un cas d'échec, on regarde la question et la réponse, on s'interroge sur "ce que le LLM aurait dû comprendre". Mais on n'ouvre pas le **contexte qui a été injecté dans le prompt**. C'est l'équivalent de chercher pourquoi une recette est ratée sans regarder les ingrédients.

Pourtant, c'est là que se trouve 90 % de l'information pour diagnostiquer. Sur la majorité des audits que je fais, le bon document existe dans la base, n'a tout simplement pas été récupéré par le retrieval, et personne ne s'en était aperçu parce que personne n'avait ouvert les chunks utilisés.

**Le bon réflexe** : tracer systématiquement le pipeline complet (Langfuse, LangSmith, ou équivalent). Pour chaque réponse problématique, on doit pouvoir lister : requête, chunks récupérés avec leurs scores, prompt final, réponse. Sans cette visibilité, le diagnostic est de la divination.

## Réflexe 6 : Optimiser sur les requêtes qu'on imagine, pas sur celles posées en prod

Pendant le développement, l'équipe teste sur ses propres questions ("est-ce que ça répond bien sur X et Y ?"). En production, les utilisateurs posent des questions complètement différentes. Sur un projet support B2B récent, 22 % des requêtes réelles portaient sur les conditions générales. Personne dans l'équipe ne testait ce cas. Personne ne savait que le système y performait à 3 %.

C'est un biais d'auteur classique : on développe un produit pour les questions qu'on se pose soi-même, pas pour celles que les utilisateurs posent. Le résultat est un système optimisé sur les mauvais cas, avec un faux sentiment de qualité côté équipe.

**Le bon réflexe** : logger les requêtes utilisateur **dès le jour 1**, même en bêta interne. Classer par volume et par taux de réussite. Optimiser par ordre d'impact business réel, pas par ordre d'intuition. La méthode de priorisation (matrice requêtes × succès) est détaillée dans [UX d'un produit IA : 5 patterns qui multiplient le feedback par 5](ux-produit-ia-5-patterns-feedback-utilisateur.md).

## Réflexe 7 : Récolter du feedback trop générique pour servir à quoi que ce soit

"Cette réponse vous a-t-elle plu ?" récolte 1 % de réponses. "Avez-vous obtenu l'information que vous cherchiez ?" en récolte 5 fois plus. Le bouton "Pas pertinent" sur les sources affichées, lui, remonte typiquement 18 % de clics exploitables, et chaque clic est un hard negative gratuit utilisable pour fine-tuner un reranker.

Le réflexe "on mettra un pouce levé / baissé" est un cache-misère. Les équipes le déploient pour cocher la case "feedback utilisateur" et finissent avec un signal trop bruité ou trop rare pour servir à quoi que ce soit. Résultat : pas de donnée d'amélioration, et donc pas d'amélioration.

**Le bon réflexe** : questions fermées, précises, posées au bon moment. Sources affichées avec option "pas pertinent" pour générer du signal exploitable. L'UX devient un capteur de données, pas une simple couche de présentation. Les 5 patterns concrets qui rendent ça opérationnel sont ici : [UX d'un produit IA et collecte de feedback](ux-produit-ia-5-patterns-feedback-utilisateur.md).

## Ce qui les relie tous : la confusion entre symptôme et cause

Les 7 réflexes ont un dénominateur commun. À chaque fois, on traite ce qui est **visible et facile à manipuler** (le prompt, les 4 questions qu'on teste à la main, le LLM, le feedback générique) plutôt que ce qui est **invisible mais déterminant** (les chunks récupérés, le dataset complet, le pipeline en amont, les vraies requêtes utilisateur).

C'est confortable, et c'est précisément pour ça que c'est piégeux. Un RAG fiable n'est pas un RAG sur lequel on a tout retravaillé. C'est un RAG sur lequel on a **identifié les bonnes causes**, et corrigé celles-là.

### Récap actionnable

1. **Toujours ouvrir les chunks récupérés** avant de modifier le prompt.
2. **Dataset d'éval fixe** dès le jour 1, pas de validation à la main.
3. **Diagnostiquer avant d'empiler** des techniques avancées.
4. **Le LLM est rarement le coupable**, regarder le pipeline en amont.
5. **Tracer le pipeline complet** (Langfuse ou équivalent) pour chaque cas d'échec.
6. **Logger les requêtes prod** et prioriser par volume × succès, pas par intuition.
7. **Questions de feedback fermées et précises**, sources cliquables comme capteurs.

Si vous reconnaissez 2 ou 3 de ces réflexes dans votre équipe, vous avez identifié votre plus gros levier d'amélioration. Ce n'est pas une nouvelle techno qu'il vous faut, c'est un changement de réflexe. Et la plupart de ces réflexes remontent à un cadrage bâclé en amont : [ce qui fait réussir un projet IA se décide avant le code](reussir-projet-ia-avant-le-code.md), bien avant qu'on touche au pipeline.

---------

Si mes articles vous intéressent et que vous avez des questions ou simplement envie de discuter de vos propres défis, n'hésitez pas à m'écrire à [anas@tensoria.fr](mailto:anas@tensoria.fr), j'aime échanger sur ces sujets !

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
