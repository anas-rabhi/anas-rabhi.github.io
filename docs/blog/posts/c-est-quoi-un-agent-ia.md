---
title: "Mais c'est quoi un agent IA ?"
slug: mais-cest-quoi-un-agent-ia
description: "Découvrez ce qu'est un agent IA et son fonctionnement."
categories:
  - "Blog"
  - "IA"
tags:
  - "Agents"
  - "Intelligence Artificielle"
  - "Agents IA"
date: 2025-12-16
comments: true
authors:
  - Anas
pin: true
math: true
mermaid: true
---


## La tendance 2025 en IA : les agents IA

Vous vous êtes peut-être dit : *« Encore un nouveau terme »*.
Et franchement, je vous comprends.

Il y a quelques mois, on parlait de RAG, cette IA qui révolutionne tout et qui allait soi-disant remplacer tous les employés du monde grâce aux bases de connaissance. Aujourd'hui, on vous parle d'**agents IA**, comme si c'était l'étape suivante et indispensable.

En réalité, voici encore une nouvelle technologie IA, et on essaie de vous faire croire que vous en avez absolument besoin. Rassurez-vous, je vis très bien sans agent IA qui me fait le café, me prépare à manger et nettoie mon appartement. Mais, car il y a toujours un "mais", ces agents IA ont vraiment une vraie utilité et sont là pour répondre un réel besoin.

Mais alors, c'est quoi un agent IA ? C'est quoi une IA *agentic* ?
Pour comprendre ça, il faut d'abord comprendre ce qu'est ChatGPT... et surtout **quelles sont ses limites**.
Car les agents IA sont là pour répondre (ou contourner) les limites des modèles de langage comme [ChatGPT](https://chatgpt.com/), [Gemini](https://gemini.google.com/) ou encore [Claude](https://www.anthropic.com/claude).

<!-- more -->

***

## ChatGPT : un modèle de langage et ses limites

Je vais essayer de faire simple.

Derrière ChatGPT, il y a un **modèle de langage**, c'est-à-dire une IA qu'on a entraînée avec des milliards de données pour répondre à des questions. Quand l'IA répond, elle ne fait qu'une seule chose : **générer du texte**.

Dit autrement :
un modèle de langage, par définition, **ne fait que prédire le prochain mot**.

Si vous utilisez ChatGPT au quotidien, vous allez sûrement me dire :
*« De quoi il parle ? ChatGPT crée aussi des images, fait des recherches sur le web, analyse des documents… »*

Et vous avez raison.
Mais il faut comprendre une chose importante : **ChatGPT aujourd'hui n'est plus juste un modèle de langage**. C'est une application complète, avec plein de briques autour.

Revenons un instant en arrière.

Partons du principe que ChatGPT ne peut :

* ni chercher sur Internet
* ni créer d'images
* ni accéder à vos fichiers

Et qu'il ne peut **que générer du texte**.

Voilà, on est revenus au [ChatGPT de fin 2022](https://www.lebigdata.fr/evolution-chatgpt-openai#:~:text=Les%20d%C3%A9veloppeurs%20d'OpenAI%20ont%20lanc%C3%A9%20ChatGPT%20le%2030%20novembre%202022.).

À cette époque-là, on rêvait déjà d'une IA capable de :

* faire des recherches sur le web
* chercher dans des documents
* répondre à des mails
* enchaîner plusieurs actions toute seule

Et très vite, une question est apparue :
**comment créer une IA capable de faire tout ça en même temps ?**

Entraîner une seule IA pour faire tout cela n'est pas vraiment envisageable.
Et surtout, ce n'est **pas comme ça que fonctionne l'IA**.

(Si vous voulez aller plus loin sur ces sujets, j'en parle plus en détail ici :

* [Comprendre l'IA](https://ianas.fr/blog/2025/04/05/comprendre-lintelligence-artificielle--guide-simple-partie-1/)
* [Comprendre l'IA générative](https://ianas.fr/blog/2025/05/15/comprendre-lintelligence-artificielle--lia-g%C3%A9n%C3%A9rative-partie-2/)
  )

***

## Les modèles de langage peuvent planifier et exécuter des tâches étape par étape

Petit à petit, on s'est rendu compte d'une chose très intéressante :
les modèles de langage sont capables de **raisonner**, de **planifier** et de **décomposer une tâche** en plusieurs étapes.

Par exemple, si je demande :

> *« Achète les ingrédients pour un gâteau au chocolat. »*

Le modèle peut très bien se dire :

* Chercher une recette de gâteau au chocolat
* Extraire la liste des ingrédients
* Préparer une liste de courses
* Trouver un magasin
* Commander en ligne ou préparer un itinéraire

Le modèle de langage sait faire ça… **dans sa tête**.

Le problème, c'est qu'il ne peut rien faire dans le monde réel.

Mais imaginons maintenant qu'à chaque étape, on lui donne accès à **un outil spécifique** :

* Un outil pour chercher sur Internet
* Un outil pour passer une commande
* Un outil pour envoyer un email
* Un outil pour interagir avec une base de données

Ces outils, ce sont **nous, les développeurs**, qui les mettons à sa disposition.

Avant d'aller plus loin, cette partie est vraiment importante.

Pour permettre au modèle de rechercher sur Internet, par exemple, on lui apprend simplement à **exprimer son intention**.
Il va dire quelque chose comme :

```
cherche_sur_le_web("recette gâteau au chocolat")
```

Dès que cette commande apparaît :

1. Le programme lance la recherche
2. Récupère les résultats
3. Les renvoie au modèle de langage

Tout ça est automatisé avec du code.

Et à partir de ce moment-là, on ne parle plus d'un simple modèle de langage.

👉 **On vient de créer un agent IA.**

***

## Concrètement, c'est quoi un agent IA ?

Un agent IA, c'est un **modèle de langage** auquel on a donné :

* une liste d'outils
* la capacité de les utiliser
* et le droit de recommencer autant de fois que nécessaire

L'objectif est simple :
👉 **il ne s'arrête pas tant que la tâche n'est pas vraiment terminée**.

Dans la réalité, le modèle de langage ne “tourne” pas en continu.
Encore une fois, c'est le développeur qui orchestre tout ça :
il relance le modèle, lui fournit les réponses des outils, et continue la boucle.

Tant que le modèle ne dit pas quelque chose comme *« Terminé »*, on continue.

Il y a souvent une confusion autour de ce terme.

Un **vrai agent IA** est autonome :

* il choisit lui-même quels outils utiliser
* il décide quand recommencer
* il change de stratégie si ça ne marche pas
* il décide seul quand s'arrêter

Ce n'est pas juste une suite d'étapes écrites à l'avance.
C'est le modèle de langage qui pilote tout.

***

## Exemple : réserver un restaurant pour un groupe d'amis

Imaginons que vous demandiez à un agent IA dédié à la réservation :

> *« Réserve une table dans un restaurant italien pour 5 personnes ce samedi soir, pas trop loin d'ici. »*

### Voici ce qu'il se passe, étape par étape :

**1. Première étape**
L'agent décide de chercher des restaurants italiens ouverts le samedi soir à proximité :

```
cherche_restaurants("italien", "proche", "samedi soir")
```

**2. On exécute et on répond**
Le programme va chercher les résultats et les renvoie à l'agent IA.

**3. Nouvelle décision**
L'agent analyse la liste et vérifie la disponibilité :

```
verifie_disponibilite("Restaurant Bella Roma", "samedi 20h", 5)
```

**4. La boucle continue**
Si ce n'est pas disponible, il recommence avec un autre restaurant.

**5. Dernière étape**
Dès qu'une table est trouvée :

```
reserve_table("Restaurant choisi", "samedi 20h", 5)
```

**6. Fin de la boucle**
L'agent n'appelle plus aucun outil et vous répond :

> *« Réservation confirmée au Restaurant Bella Roma, samedi à 20h pour 5 personnes. »*

***

## Agent IA : de votre point de vue d'utilisateur

De votre côté, tout ce mécanisme est invisible.

Vous posez une question.
Quelques secondes plus tard, vous avez une réponse finale.

Vous ne voyez pas :

* le nombre d'étapes
* les essais ratés
* les recherches intermédiaires

Et c'est justement le but.

Les agents IA ne sont pas faits pour impressionner techniquement l'utilisateur.
Ils sont faits pour **prendre une mission** et **la mener jusqu'au bout**.

Pour vous, ça ressemble juste à un assistant très malin qui comprend ce que vous voulez et revient seulement quand c'est vraiment fini.

***

## Pourquoi on parle autant des agents IA maintenant ?

Les agents IA ne sont pas une idée totalement nouvelle.
Ce qui est nouveau, c'est que **les modèles de langage sont enfin assez bons pour que ça marche**.

Ils savent aujourd'hui :

* raisonner sur plusieurs étapes
* corriger leurs erreurs
* s'adapter si une stratégie ne fonctionne pas

Ajoutez à ça :

* des APIs partout
* des outils faciles à brancher
* des coûts de plus en plus maîtrisés

Et surtout, des **besoins très concrets côté entreprises**.

C'est pour ça qu'on en parle autant aujourd'hui.

***

## Les limites (parce que oui, il y en a)

Un agent IA reste une IA.

Il peut :

* se tromper
* mal interpréter une situation
* utiliser un mauvais outil

C'est pour ça qu'en pratique, on met toujours des garde-fous :

* limitations d'accès
* validation humaine
* budgets maximum
* logs et contrôles

Les agents IA sont puissants, mais ils ne remplacent pas le jugement humain.
Pas encore, en tout cas.

***

## Pour conclure

Les agents IA ne sont ni magiques, ni indispensables à tout le monde.

Ce sont avant tout des **modèles de langage bien orchestrés**, capables de réfléchir, d'agir et de recommencer jusqu'à atteindre un objectif.

Pour l'utilisateur, c'est simple.
Pour le développeur, c'est beaucoup plus complexe.

Et c'est probablement ça, la vraie évolution de l'IA aujourd'hui :
non pas une IA qui parle mieux, mais une IA qui **fait réellement des choses**.

***

Si mes articles vous intéressent, que vous avez des questions ou simplement envie de discuter de vos propres défis liés à l'IA, n'hésitez pas à m'écrire à [anas0rabhi@gmail.com](mailto:anas0rabhi@gmail.com), j'adore échanger sur ces sujets !

Vous souhaitez mettre en place des agents IA dans votre entreprise ? Découvrez mon activité de conseil sur [tensoria.fr](https://tensoria.fr).

Vous pouvez aussi [réserver un créneau d'échange](https://cal.com/anas-rabhi/ianas) ou vous abonner à ma newsletter :)


---

### À propos de moi

Je suis **Anas Rabhi**, consultant Data Scientist freelance. J'accompagne les entreprises dans leur stratégie et mise en œuvre de solutions d'IA (RAG, Agents, NLP). 

Découvrez mes services sur [tensoria.fr](https://tensoria.fr) ou testez notre solution d'agents IA [heeya.fr](https://heeya.fr).

<div style="text-align: center; margin: 40px 0; gap: 16px; display: flex; flex-wrap: wrap; justify-content: center;">
  <a href="https://cal.com/anas-rabhi/ianas" target="_blank" style="display: inline-block; background-color: #4F46E5; color: #ffffff; font-weight: bold; padding: 16px 32px; text-decoration: none; border-radius: 8px; font-size: 18px; letter-spacing: 0.8px; box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2); transition: all 0.3s ease; border: none;">
    Réserver un créneau
  </a>
  <a href="https://anas-ai.kit.com/d8b1a255cc" target="_blank" style="display: inline-block; background-color: #222222; color: #ffffff; font-weight: bold; padding: 16px 32px; text-decoration: none; border-radius: 8px; font-size: 18px; letter-spacing: 0.8px; box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2); transition: all 0.3s ease; border: none;">
    <span style="margin-right: 10px;">✉️</span> S'abonner à ma newsletter
  </a>
</div>

***
