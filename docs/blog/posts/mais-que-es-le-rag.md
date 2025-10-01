---
title: "Mais c'est quoi le RAG vraiment ? Définition, fonctionnement, limites et conseils"
description: "Découvrez ce qu'est le RAG (Retrieval-Augmented Generation), son fonctionnement, ses avantages, ses limites et comment l'optimiser pour vos projets d'IA en entreprise."
categories:
  - "Blog"
  - "IA"
tags:
  - "RAG"
  - "Intelligence Artificielle"
  - "Retrieval-Augmented Generation"
  - "RAG fonctionnement"
  - "RAG limites"
  - "RAG optimisation"
date: 2025-06-21
comments: true
authors:
  - Anas
pin: true
math: true
mermaid: true
---

## Introduction au RAG (Retrieval-Augmented Generation)

Tout le monde a plus ou moins entendu parler du RAG (Retrieval-Augmented Generation). Mais **c'est quoi le RAG** exactement ? Beaucoup l'ont même déjà implémenté, parfois avec des outils "no-code" ou des librairies Python comme LangChain ou LlamaIndex. C'est simple à mettre en place, mais je vois aussi pas mal de gens déçus du résultat. En réalité, il faut surtout comprendre à quoi ça sert et comment ça fonctionne pour savoir si c'est adapté à votre besoin.

Au début, je ne comptais pas réexpliquer le RAG ici, il existe déjà plein de ressources sur le sujet. Mais en discutant avec des personnes qui veulent l'utiliser en entreprise, je me rends compte qu'on passe souvent à côté de l'essentiel : à quoi ça sert vraiment un RAG, et comment ça marche concrètement.

Je vais donc essayer de revenir sur les points que j'ai l'habitude d'éclaircir quand on me pose la question.

<!-- more --> 

### La facilité d'implémentation du RAG

Mettre en place un RAG, c'est facile. C'est même trop facile : on suit un tuto, on branche deux librairies, et hop, ça tourne. Mais attention, le résultat n'est pas toujours à la hauteur des attentes (spoiler : souvent, on est déçu).

Justement, cette simplicité cache un piège. Pour une question très basique, le RAG peut donner l'impression que tout fonctionne parfaitement. Mais dès qu'on sort un peu du cadre, on se rend vite compte que les réponses ne suivent plus.

C'est là qu'on peut passer beaucoup de temps à bricoler, à optimiser les mauvaises briques, sans forcément comprendre où est le vrai problème. Et c'est normal : comme tout projet d'IA, le RAG est plus complexe qu'il n'y paraît. Il faut vraiment comprendre comment chaque brique fonctionne pour éviter de tourner en rond. J'ai déjà écrit des articles sur comment améliorer le RAG [ici](https://ianas.fr/blog/2025/03/26/comment-am%C3%A9liorer-le-rag/) ou sur l'analyse d'erreur pour comprendre ce qui coince [ici](https://ianas.fr/blog/2025/06/04/mon-rag-ne-marche-pas-pourquoi-l-analyse-derreur-change-tout/).

Mais revenons aux bases du RAG dans cet article.

### C'est quoi le RAG et pourquoi l'utiliser en entreprise ?

Avant de parler du RAG, il faut déjà comprendre **c'est quoi le RAG** et pourquoi on en a besoin. Depuis l'arrivée de ChatGPT, on a tous vu à quel point les modèles de langage (appelés LLM) sont puissants. Mais il y a une limite : ils ne connaissent pas nos données à nous, ni les infos internes d'une entreprise.

Prenons un exemple tout simple : j'ai une documentation sur une page Word. Si je veux poser des questions à l'IA sur ce document, je peux copier le texte dans ChatGPT : l'IA va le lire et répondre, parce que j'ai mis le texte directement dans ce qu'on appelle le contexte du modèle (ou le prompt). 

Sauf que la fenêtre de contexte est limitée à un certain nombre de mots (ou plus précisément de tokens). On peut charger une page, mais pas 10 000 d'un coup. En entreprise, on a souvent des documents très volumineux, et on aimerait qu'une IA puisse répondre à des questions sur l'ensemble de ces documents.

La solution qui a émergé est la suivante : à chaque question, on sélectionne seulement quelques extraits de la documentation qui sont pertinents, et on les insère dans le contexte (ou prompt) du modèle.

C'est exactement ce que fait le RAG : il permet, pour chaque question, de choisir les extraits pertinents et de les ajouter au contexte pour que l'IA puisse répondre, même sur de très gros volumes de documents, si vous aimez lire, AWS en parle très bien ici aussi : ([aws.amazon.com](https://aws.amazon.com/fr/what-is/retrieval-augmented-generation/))

### Comment fonctionne un système RAG ?

Pour faire simple, la première étape du RAG, c'est de stocker les documents dont on a besoin dans une base de données vectorielle. Mais comme un modèle de langage ne peut pas tout lire d'un coup (à cause de la fameuse limite de contexte), on découpe chaque document en petits morceaux, qu'on appelle des chunks. Ensuite, on transforme chaque chunk en un vecteur qui capture sa signification (sa sémantique). C'est ce qu'on appelle la vectorisation : ça permet de comparer rapidement la question de l'utilisateur avec tous les morceaux de documents, pour trouver ceux qui sont les plus proches.

 > Vectoriser un texte consiste à le transformer en un vecteur qui capture sa signification (sa sémantique). Cela permet de comparer facilement la similarité entre la question de l'utilisateur et les différents fragments de documents. Par exemple, si "un chat blanc" est représenté par [1, 1], "un chat noir" par [1, 0], et "un chien noir" par [7, 1], on voit que "un chat noir" est plus proche de "un chat blanc" que de "un chien noir". Ce principe permet d'identifier rapidement les passages les plus pertinents à insérer dans le contexte du modèle.

L'étape de vectorisation est cruciale : c'est elle qui permet de retrouver les bons documents quand on pose une question. Pour ça, on utilise ce qu'on appelle des modèles d'embeddings. Leur rôle est de transformer le texte en un vecteur qui capture sa signification, sa "sémantique". Ces modèles sont eux-mêmes des IA, entraînées spécialement pour cette tâche, pour en savoir plus.

Comme on peut le voir, il y a déjà un vrai travail en amont : il faut bien préparer les documents. La performance du RAG dépend beaucoup de deux choses : comment on découpe les documents (la taille et la méthode de découpage, ce qu'on appelle le chunking), et la qualité du modèle d'embeddings qu'on utilise pour transformer ces morceaux en vecteurs. Rien que sur ces deux points, on a déjà de quoi améliorer les futurs résultats.

Une fois la base de données prête, on passe à l'étape suivante : quand un utilisateur pose une question, on transforme cette question en vecteur, puis on cherche dans la base les morceaux (chunks) les plus proches, c'est-à-dire ceux qui ressemblent le plus à la question. Cette recherche se fait en comparant la distance entre le vecteur de la question et ceux des chunks déjà stockés. On récupère alors quelques chunks (le nombre est défini à l'avance), et on les envoie au modèle de langage pour qu'il puisse répondre.
Au final, le prompt envoyé à l'IA ressemble à ça :

```
Voici les chunks pertinents pour la question : 
Chunk 1 : <TEXT DU CHUNK 1>
Chunk 2 : <TEXT DU CHUNK 2>
...

Voici la question de l'utilisateur : Dans quel document je peux trouver des informations concernant le planning du moteur avec la référence X2D2E?
```

Dans cette deuxième phase, plusieurs paramètres peuvent être optimisés pour améliorer le RAG :
- La recherche en utilisant la question peut ne pas être suffisante. 
- Le nombre de chunks récupérés peut être trop faible ou trop grand.
- La qualité du modèle LLM qui génère la réponse peut être améliorée.

À partir de cette base, on peut commencer à expérimenter et évaluer le RAG. Pour ensuite l'améliorer en analysant les erreurs et en changeant les paramètres. Si vous êtes à l'étape de l'évaluation, je vous invite à lire mon article sur l'analyse d'erreur pour comprendre ce qui coince [ici](https://ianas.fr/blog/2025/06/04/mon-rag-ne-marche-pas--pourquoi-lanalyse-derreur-change-tout/).

### À quoi ça sert vraiment le RAG ? Quelles sont ses limites ?

Je pense que c'est la question la plus importante. Le RAG ne permet pas de répondre à toutes les questions que vous pouvez lui poser, en raison de certaines limites. Dans sa version la plus basique et la plus simple, celle que je détaille ici, il ne permet de répondre qu'à des questions directes qui ciblent un contenu limité.

Je m'explique. Si on lui demande de répondre à une question très large, il est possible que le nombre de chunks récupérés ne soit pas suffisant pour répondre à la question.

**Où le RAG fonctionne bien :**
- **Accès à des informations spécialisées** : documents internes ou connaissances métier non disponibles dans les modèles de base
- **Fournir une information précise** : le RAG est particulièrement efficace pour répondre à des questions ciblées en allant chercher directement l'information demandée dans les documents fournis

**Où le RAG montre ses limites :**
- **Raisonnement itératif limité** : Le RAG ne sait pas raisonner en plusieurs étapes pour affiner sa recherche. Il ne vérifie pas si les documents récupérés sont vraiment les plus pertinents ou si l'information est complète. Par exemple, pour une question complexe, il va juste ramener les passages les plus proches sémantiquement, sans "comprendre" le contexte global comme le ferait un humain.
- **Dépendance à l'organisation des données** : Si les documents sont mal structurés ou mal indexés, la recherche sera inefficace. Une bonne organisation, des métadonnées et une structuration claire sont essentiels.
- **Qualité et biais des sources** : Le RAG ne fait que transmettre ce qu'il trouve. Si les documents sont incomplets, obsolètes ou biaisés, la réponse le sera aussi, pour en savoir plus : [elastic.co](https://www.elastic.co/fr/what-is/retrieval-augmented-generation/)

**À retenir :**
- Le RAG ne garantit pas la complétude ni la véracité des réponses. Il y a toujours un risque d'hallucination ou d'erreur.
- Pour fiabiliser un RAG, il faut : bien organiser les données, surveiller la qualité des sources, calibrer les paramètres (chunking, embeddings, etc.), et permettre la citation des sources pour pouvoir vérifier les informations si besoin.
- L'évaluation et l'amélioration d'un RAG se font surtout en conditions réelles, car les problèmes apparaissent à l'usage.

### Conclusion : Le RAG est-il utile pour vos projets d'IA ?

Le RAG est vraiment utile, à condition de prendre le temps de bien le mettre en place et de l'améliorer au fil du temps. Ce n'est pas un outil qu'on implémente en vitesse pour le laisser tourner tout seul : il faut l'évaluer, l'ajuster, et corriger ce qui ne va pas pour qu'il soit vraiment efficace.

Les limites que j'ai évoquées ne sont pas simples à éliminer, mais il existe des solutions pour les atténuer. On parle souvent d'Agentic RAG par exemple pour améliorer certains aspects du RAG. Si vous cherchez un système qui donne 100 % de bonnes réponses, le RAG (et l'IA en général) n'est pas faite pour vous. Mais si vous êtes prêt à viser 90-95 % de réponses correctes, et à investir un peu de temps pour bien l'implémenter, alors le RAG peut vraiment devenir votre meilleur allié.

Si vous voulez en savoir plus sur le RAG, même le gouvernement a publié un guide pour faire du RAG : [Guide de la génération augmentée par récupération (RAG)](https://www.entreprises.gouv.fr/la-dge/publications/guide-de-la-generation-augmentee-par-recuperation-rag).

---------

Si mes articles vous intéressent et que vous avez des questions ou simplement envie de discuter de vos propres défis, n'hésitez pas à m'écrire à anas0rabhi@gmail.com, j'aime échanger sur ces sujets !

Vous pouvez aussi vous abonner à ma newsletter :)

<div style="text-align: center; margin: 40px 0;">
  <a href="https://anas-ai.kit.com/d8b1a255cc" target="_blank" style="display: inline-block; background-color: #222222; color: #ffffff; font-weight: bold; padding: 16px 32px; text-decoration: none; border-radius: 8px; font-size: 18px; letter-spacing: 0.8px; box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2); transition: all 0.3s ease; border: none;">
    <span style="margin-right: 10px;">✉️</span> S'abonner à ma newsletter
  </a>
</div>

---
