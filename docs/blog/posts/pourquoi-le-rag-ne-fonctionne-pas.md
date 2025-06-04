---
title: "Mon RAG ne marche pas : pourquoi l’analyse d’erreur change tout"
description: "Vous avez intégré un RAG, mais les résultats ne sont pas à la hauteur ? Découvrez pourquoi l’analyse d’erreur est la clé pour comprendre et améliorer votre projet, avec des exemples concrets et des conseils issus du terrain."
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

J’ai déjà écrit un article sur comment améliorer le RAG [ici](https://ianas.fr/blog/2025/03/26/comment-am%C3%A9liorer-le-rag/), mais le sujet est tellement vaste qu’il y a toujours de nouvelles choses à partager. D’autant plus que je reçois souvent des remarques comme :  
*"Je ne comprends pas, pourtant j’ai ajouté [la techno à la mode], mais le résultat n’est pas bon."*

### Le RAG n’est pas magique (et c’est normal)

Le RAG, c’est un peu LE projet à la mode depuis le début de l’IA générative. Tout le monde veut son assistant boosté à l’IA, capable de répondre à n’importe quelle question sur ses données. On trouve des tutos "RAG en deux lignes", des outils "no-code", et ça donne l’impression que c’est simple.  
Mais la réalité, c’est qu’une fois le projet en place, les tests sont rarement aussi magiques qu’espéré. L’IA ne répond pas à tout, hallucine parfois, ou passe complètement à côté d’une question basique. Et là, grosse frustration.

Première chose à retenir : aucun système IA ne peut avoir 100 % de bonnes réponses.  
Il faut surtout se poser la question: quel niveau d’erreur je suis prêt à accepter.
La vraie valeur, on l’obtient en comprenant bien le problème qu’on veut résoudre, pas en cherchant la perfection.

### Quand on veut vraiment améliorer le RAG

Si vous êtes convaincu que le RAG est le bon choix, alors il faut investir du temps... mais pas n’importe comment.  
La première version est souvent bluffante, mais très vite, on voit les limites. Les retours utilisateurs sont clairs :  
- certaines questions restent sans réponse,
- il y a des erreurs "bêtes",
- et l’utilisation devient frustrante.

À chaque fois, la question c’est : "Qu’est-ce qu’on fait maintenant ? On ajoute une nouvelle techno ? On change de modèle ?"

Ma réponse : **on analyse**.  
Analyser, ce n’est pas juste regarder les logs ou changer des paramètres au hasard. C’est décortiquer chaque échec pour comprendre d’où il vient. Avant d’ajouter quoi que ce soit, il faut comprendre : c’est la base du métier, que ce soit en data science, en ML, ou en stats.

### Exemples concrets d’analyse d’erreur

Parce que c’est plus parlant, voici deux exemples vécus :

**1. Quand la recherche vectorielle fait défaut**  
Sur un projet, tout semblait marcher... sauf que certaines requêtes avec des mots-clés précis ne donnaient rien, alors que la réponse était bien dans la base.  
Après analyse, on a vu que la recherche vectorielle ne captait pas certains synonymes ou formulations.  
On a donc ajouté une recherche BM25 (basée sur les mots-clés) en plus du vectoriel. Résultat : les questions "difficiles" trouvaient enfin des réponses.

**2. Les attributs métiers oubliés**  
Dans un e-commerce, impossible de sortir les produits d’une couleur précise ("je veux un t-shirt rouge"), alors que les données étaient là.  
L’analyse a montré que la sémantique de la couleur n’était pas bien capturée dans les vecteurs d'embeddings. On a simplement ajouté un filtrage par métadonnée avant de passer à l’IA : problème réglé.

### Comment mener l’analyse d’erreur ?

Voilà comment je m’y prends, et franchement, ça marche dans 90 % des cas :

1 : Prendre un échantillon d’exemples où le RAG se plante.  
2 : Pour chaque cas, se demander :  
   - Est-ce que le retrieval trouve quelque chose ou non ?  
   - Est-ce que la génération hallucine ?  
   - Est-ce que l’info existe vraiment dans la base ?  
   - Est-ce un problème de format, de métadonnée, de formulation ?  
3 : Catégoriser les erreurs (retrieval, ranking, hallucination, data...).  
4 : Tester des corrections simples... avant de tout changer.

Et surtout : noter ce qui revient le plus souvent, pour prioriser les vraies améliorations.

Pour commencer, toutes les analyses d’erreur doivent se faire à la main. C’est indispensable pour vraiment comprendre d’où viennent les problèmes et comment fonctionnent les différents frameworks RAG. Mais soyons honnêtes : à un moment, quand le volume de requêtes augmente, ça devient vite ingérable. C’est là que de bons outils deviennent indispensables pour garder une vision claire de ce qui se passe à chaque étape.

### Quels outils choisir ? 

LangFuse est probablement l’un des plus pratiques (et open-source) pour tracer tout le pipeline RAG : on visualise chaque étape, de la requête originale aux chunks récupérés, le prompt final envoyé au LLM, et la réponse générée. Idéal pour repérer précisément où ça déraille.

LangSmith fait la même chose que Langfuse, avec une interface différente. L’avantage : si vous utilisez déjà LangChain, l’intégration est naturelle.

Pour aller plus loin dans le suivi, Weights & Biases permet de tracker les métriques de performance dans le temps et de comparer différentes versions du système. Pratique pour vérifier si une "amélioration" n’a pas cassé autre chose ailleurs.

Et puis il y a les solutions maison, qui permettent de garder le contrôle sur tout : un logging JSON bien structuré, qui enregistre les prompts, les chunks récupérés et les réponses du LLM.

L’idée, c’est de ne pas se perdre dans la surenchère de dashboards : il faut juste assez de visibilité pour comprendre rapidement où chercher quand quelque chose cloche.

### Ce qu’il faut retenir

Le RAG, ce n’est ni magique, ni parfait.  
Ce qui fait la différence, ce n’est pas la dernière techno ajoutée, mais la capacité à comprendre pourquoi ça rate et à itérer intelligemment.  
L’analyse d’erreur, c’est la base : avant d’empiler les couches de complexité, prenez le temps de regarder, d’écouter les utilisateurs, et de corriger à la source.

---------

Si mes articles vous intéressent et que vous avez des questions ou simplement envie de discuter de vos propres défis, n'hésitez pas à m'écrire à anas0rabhi@gmail.com, j'aime échanger sur ces sujets !

Vous pouvez aussi vous abonner à ma newsletter :)

<div style="text-align: center; margin: 40px 0;">
  <a href="https://anas-ai.kit.com/d8b1a255cc" target="_blank" style="display: inline-block; background-color: #222222; color: #ffffff; font-weight: bold; padding: 16px 32px; text-decoration: none; border-radius: 8px; font-size: 18px; letter-spacing: 0.8px; box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2); transition: all 0.3s ease; border: none;">
    <span style="margin-right: 10px;">✉️</span> S'abonner à ma newsletter
  </a>
</div>
