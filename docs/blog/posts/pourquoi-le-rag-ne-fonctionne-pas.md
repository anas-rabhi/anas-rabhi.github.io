---
title: "Mon RAG ne marche pas : pourquoi l'analyse d'erreur change tout"
slug: mon-rag-ne-marche-pas-analyse-erreur
description: "RAG qui ne fonctionne pas ? Diagnostic en 3 questions, quick wins à tester en 2h et méthode d'analyse d'erreur issue du terrain. Guide pratique."
categories:
  - "Blog"
  - "IA"
tags:
  - "RAG"
  - "Intelligence Artificielle"
  - "Conseils Pratiques"
  - "Optimisation"
date: 2025-06-04
comments: true
authors:
  - Anas
pin: true
math: true
mermaid: true
---

## Introduction

J'ai déjà écrit un article sur [comment améliorer le RAG avec des métriques et des outils d'évaluation](comment-ameliorer-l-IA.md), mais le sujet est tellement vaste qu'il y a toujours de nouvelles choses à partager. D'autant plus que j'entends souvent des remarques comme :
*"Je ne comprends pas, pourtant j'ai ajouté [la techno à la mode], mais le résultat n'est pas bon."*

<!-- more -->

## Le RAG n'est pas magique (et c'est normal)

Le RAG, c'est un peu LE projet à la mode depuis le début de l'IA générative. Tout le monde veut son assistant boosté à l'IA, capable de répondre à n'importe quelle question sur ses données. On trouve des tutos "RAG en deux lignes", des outils "no-code", et ça donne l'impression que c'est simple.

Mais la réalité, c'est qu'une fois le projet en place, les tests sont rarement aussi magiques qu'espéré. L'IA ne répond pas à tout, hallucine parfois, ou passe complètement à côté d'une question basique. Et là, grosse frustration.

Première chose à retenir : aucun système IA ne peut avoir 100% de bonnes réponses.
La vraie valeur, on l'obtient en comprenant bien le problème qu'on veut résoudre, pas en cherchant la perfection.

## Diagnostic rapide : 3 questions pour isoler le problème

Avant de partir dans tous les sens, voici les 3 questions à se poser dans l'ordre. Elles permettent d'orienter vers le bon composant en moins de 10 minutes.

**1. Est-ce que le retrieval trouve quelque chose ?**
Regardez les chunks récupérés pour la requête qui échoue. Il y en a ? Ils sont pertinents ? Si le retrieval ne remonte rien, le problème n'est pas le LLM — c'est l'indexation ou la formulation de la requête.

**2. Si les chunks sont là, est-ce que la réponse hallucine ?**
Comparez la réponse générée avec les chunks fournis. L'IA a-t-elle inventé des informations qui n'étaient pas dans les sources ? Si oui, c'est un problème de génération (prompt, modèle, température).

**3. Si les chunks sont pertinents et la réponse est logique — est-ce que l'information existe vraiment dans la base ?**
Parfois, la base ne contient tout simplement pas la réponse. C'est un problème de données, pas de RAG.

Ces 3 questions guident vers le bon composant. Ensuite, les solutions diffèrent selon le diagnostic.

## Les quick wins à tester avant de tout refaire

Avant de changer d'architecture, d'embeddings ou de modèle, voici ce qui règle souvent 80% des problèmes. Ce sont des changements qui se testent en 1-2 heures.

**Si le retrieval ne trouve pas les bons chunks :**
- Réduire la taille des chunks (essayez 512 tokens au lieu de 1024)
- Augmenter le top-k (récupérer 7 chunks au lieu de 3)
- Tester la [recherche hybride](rag-trop-simple.md) (vectoriel + BM25) pour les requêtes avec des mots-clés précis

**Si le LLM hallucine :**
- Ajouter dans le prompt : *"Réponds uniquement à partir du contexte fourni. Si l'information n'est pas dans le contexte, dis-le explicitement."*
- Baisser la temperature à 0 ou 0.1 pour réduire la créativité du modèle

**Si la qualité est aléatoire d'une requête à l'autre :**
- Vérifier la qualité des données sources (PDFs mal extraits, tableaux corrompus, textes dupliqués)
- Vérifier l'overlap des chunks (un overlap de 10-15% évite de couper une information importante)

Si aucun de ces quick wins n'améliore les choses, alors oui, ça mérite une analyse plus poussée.

## Exemples concrets d'analyse d'erreur

Parce que c'est plus parlant, voici deux exemples vécus :

**1. Quand la recherche vectorielle fait défaut**
Sur un projet, tout semblait marcher... sauf que certaines requêtes avec des mots-clés précis ne donnaient rien, alors que la réponse était bien dans la base.
Après analyse, on a vu que la recherche vectorielle ne captait pas certains synonymes ou formulations.
On a donc ajouté une recherche BM25 (basée sur les mots-clés) en plus du vectoriel. Résultat : les questions "difficiles" trouvaient enfin des réponses.

**2. Les attributs métiers oubliés**
Dans un e-commerce, impossible de sortir les produits d'une couleur précise ("je veux un t-shirt rouge"), alors que les données étaient là.
L'analyse a montré que la sémantique de la couleur n'était pas bien capturée dans les vecteurs d'embeddings. On a simplement ajouté un filtrage par métadonnée avant de passer à l'IA : problème réglé.

## Comment mener l'analyse d'erreur ?

Voilà comment je m'y prends, et franchement, ça marche dans 90% des cas :

1. Prendre un échantillon d'exemples où le RAG se plante.
2. Pour chaque cas, se demander :
   - Est-ce que le retrieval trouve quelque chose ou non ?
   - Est-ce que la génération hallucine ?
   - Est-ce que l'info existe vraiment dans la base ?
   - Est-ce un problème de format, de métadonnée, de formulation ?
3. Catégoriser les erreurs (retrieval, ranking, hallucination, data...).
4. Tester des corrections simples... avant de tout changer.

Et surtout : noter ce qui revient le plus souvent, pour prioriser les vraies améliorations.

Pour commencer, toutes les analyses d'erreur doivent se faire à la main. C'est indispensable pour vraiment comprendre d'où viennent les problèmes. Mais soyons honnêtes : à un moment, quand le volume de requêtes augmente, ça devient vite ingérable. C'est là que de bons outils deviennent indispensables.

## Quels outils choisir ?

LangFuse est probablement l'un des plus pratiques (et open-source) pour tracer tout le pipeline RAG : on visualise chaque étape, de la requête originale aux chunks récupérés, le prompt final envoyé au LLM, et la réponse générée. Idéal pour repérer précisément où ça déraille.

LangSmith fait la même chose que Langfuse, avec une interface différente. L'avantage : si vous utilisez déjà LangChain, l'intégration est naturelle.

Pour aller plus loin dans le suivi, Weights & Biases permet de tracker les métriques de performance dans le temps et de comparer différentes versions du système. Pratique pour vérifier si une "amélioration" n'a pas cassé autre chose ailleurs.

L'idée, c'est de ne pas se perdre dans la surenchère de dashboards : il faut juste assez de visibilité pour comprendre rapidement où chercher quand quelque chose cloche. Si vous voulez aller plus loin sur les [métriques spécifiques à suivre (Faithfulness, RAGAS...)](comment-ameliorer-l-IA.md), j'en parle en détail dans un article dédié.

## Ce qu'il faut retenir

Le RAG, ce n'est ni magique, ni parfait.
Ce qui fait la différence, ce n'est pas la dernière techno ajoutée, mais la capacité à comprendre pourquoi ça rate et à itérer intelligemment.

La méthode en résumé :
1. Diagnostiquer avec les 3 questions
2. Tester les quick wins d'abord
3. Si ça ne suffit pas, analyser méthodiquement
4. Corriger à la source avant d'ajouter de la complexité

Pour voir cette approche appliquée sur un vrai projet, lisez [le cas client assurance](integration-ia-rapports-sinistre-assurance.md) ou [le cas client BTP](cas-usage-rag-redaction-appels-offres-btp.md). Et si votre RAG a des [causes techniques spécifiques](les-4-causes-techniques-echec-rag.md), j'en parle aussi en détail.

---------

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
