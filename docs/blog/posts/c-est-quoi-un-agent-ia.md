---
title: "Mais c'est quoi un agent IA ?"
description: "Découvrez ce qu'est un agent IA et son fonctionnement."
categories:
  - "Blog"
  - "IA"
tags:
  - "Agents"
  - "Intelligence Artificielle"
  - "Agents IA"
date: 2025-07-02
comments: true
authors:
  - Anas
pin: true
math: true
mermaid: true
---

## La dernière tendance en IA : les agents IA

Vous vous êtes peut-être dit : "Encore un nouveau terme". Vous êtes sûrement un peu perdus : il y a quelques mois à peine, on vous parlait de RAG ou de ChatGPT, cette IA qui révolutionne tout et qui allait soi-disant remplacer tous les employés du monde. En réalité, voici encore une nouvelle technologie IA, et on essaie de vous faire croire que vous en avez absolument besoin. Rassurez-vous, je vis très bien sans agent IA qui me fait le café, me prépare à manger et nettoie mon appartement.

C'est quoi un agent IA ? C'est quoi une IA Agentic ? Pour ça il faut d'abord comprendre ce qu'est ChatGPT et les limites. Car les agents IA sont la pour répondre ou résoudre les limites des modèles de langage comme [ChatGPT](https://chatgpt.com/), [Gemini](https://gemini.google.com/) ou encore [Claude](https://www.anthropic.com/claude).

<!-- more --> 

### ChatGPT : un modèle de langage et ses limites

Je vais essayer de faire simple : derrière ChatGPT il y a un modèle de langage, c'est à dire une IA qu'on a entraînée avec des milliards de données pour répondre à des questions. Lorsque l'IA répond à une question, elle ne fait que générer du texte. Donc pour dire ça autrement, les modèles de langage ont pour seule tâche de générer du texte. 

Si vous utilisez ChatGPT au quotidien, vous pourriez vous demander : "De quoi il parle ? ChatGPT ne se contente pas de générer du texte, il crée aussi des images, effectue des recherches sur le web, et bien plus encore." Vous avez tout à fait raison. Mais il faut savoir que ChatGPT, dans sa version actuelle, ne se limite plus à un simple modèle de langage. 

Partons du principe que ChatGPT ne peut pas fournir d'image ni de recherche sur le web. Et qu'il ne peut que générer du texte. Voilà on est retombé au [début de ChatGPT en 2022](https://www.lebigdata.fr/evolution-chatgpt-openai#:~:text=Les%20d%C3%A9veloppeurs%20d'OpenAI%20ont%20lanc%C3%A9%20ChatGPT%20le%2030%20novembre%202022.). A ce moment la on rêvait d'une IA qui pouvait faire des recherches sur le web, générer des images, pouvoir répondre à mes mails, chercher dans des documents et tout ça à la fois. C'est la qu'on commençait à réflechir mais comment créer cette IA qui pouvait faire tout ça ? Patience les agents IA arrivent..

Entraîner une IA pour faire tout cela n'est pas envisageable, et ce n'est pas vraiment ainsi que fonctionne l'IA. Si vous souhaitez en savoir un peu plus sur l'IA en général, je vous invite à lire mes articles : 
- [Comprendre l'IA](https://ianas.fr/blog/2025/04/05/comprendre-lintelligence-artificielle--guide-simple-partie-1/)
- [Comprendre l'IA générative](https://ianas.fr/blog/2025/05/15/comprendre-lintelligence-artificielle--lia-g%C3%A9n%C3%A9rative-partie-2/).


### Les modèles de langage peuvent planifier et éxecuter des tâches étape par étape

On s'est rendu compte que ces modèles de langage sont capables de planifier et d'exécuter des tâches étape par étape. Par exemple, si je demande :

> "Achète les ingrédients pour un gâteau au chocolat."

Le modèle va pouvoir décomposer la tâche en plusieurs étapes : 
- Chercher une recette de gâteau au chocolat
- Extraire la liste des ingrédients
- Préparer la liste de courses
- Trouver un magasin
- Commander en ligne ou préparer l'itinéraire

Imaginons maintenant qu'à chaque étape, il soit possible de faire appel à un outil dédié pour exécuter une tâche précise. Par exemple :
- Si le modèle de langage a besoin de chercher une information sur le web, il peut s'appuyer sur un outil qui interroge Google : cet outil, c'est nous, les développeurs, qui le mettons à sa disposition.  
- Si le modèle de langage a besoin de passer une commande en ligne pour réaliser une tâche, il utilise également un outil conçu pour ça.

Avant d'aller plus loin, il est très important de bien comprendre cette étape. Pour cela, je vais décomposer le processus de recherche sur le web d'un point de vue développeur, mais de manière très simple :

Pour permettre au modèle de rechercher sur Internet, il faut lui apprendre à signaler clairement son intention. Par exemple, chaque fois qu'il souhaite effectuer une recherche, il dira : « cherche_sur_le_web(recette_gâteau_au_chocolat) ». Dès que je vois apparaître cette commande, je lance automatiquement la recherche, récupère la réponse, et la transmets ensuite au modèle de langage. Toutes ces opérations sont automatisées grâce à la programmation informatique.

Avec ça on a transformé un modèle de langage en agent IA.

### Concrêtement c'est quoi un agent IA ?

Un agent IA, est un modèle de langage auquel on a donné une liste d'outils et qui peut les executer en continue sans s'arrêter jusqu'à accomplir sa tâche. Dans la réalité le modèle de langage ne tourne pas en continu. Encore une fois, c'est au développeur de continuer à faire tourner le modèle de langage en lui donnant tous les outils nécessaires. Et tant que le modèle de langage, n'a pas dit "Terminé" on continue à le faire tourner.

Il y a souvent une confusion dans ce qu'est un agent IA. Un agent IA est vraiment autonome, on lui permet de faire appel aux outils qu'il souhaite sans réstrictions et c'est le seul décideur de quand il s'arrête.

#### Exemple : Réserver un restaurant pour un groupe d'amis

Imaginons que vous demandiez à un agent IA dédié à la réservation :  
> "Réserve une table dans un restaurant italien pour 5 personnes ce samedi soir, pas trop loin d'ici."

##### Voici comment ça se passe, étape par étape :

1. **Première étape : Premier outil**  
L'agent IA décide de chercher les restaurants italiens ouverts le samedi soir près de votre localisation.  
Il demande donc :  
`cherche_restaurants("italien", "proche", "samedi soir")`

2. **On exécute et on répond**  
Le programme qu'on a developpé va chercher la liste sur Internet et transmet les résultats à l'agent IA (le modèle de langage).

3. **Nouvelle étape : Nouveau choix d'outil**  
L'agent IA analyse la liste, sélectionne un restaurant et passe à l'étape suivante :  
`vérifie_disponibilité("Restaurant Bella Roma", "samedi 20h", 5 personnes)`

4. **On exécute à nouveau**  
Le programme qu'on a développé en amont vérifie sur le site du réstaurant les disponibilités, puis donne la réponse à l'agent IA.

5. **Et ça continue, étape après étape**  
Si le restaurant n'est pas disponible, le modèle recommence la boucle avec un autre restaurant.  
Dès qu'il trouve une table disponible, il enchaîne :  
`réserve_table("Restaurant choisi", "samedi 20h", 5 personnes)`

6. **La boucle s'arrête quand la tâche est vraiment finie**  
On fait tout ça, étape par étape, outil par outil, jusqu'à ce que l'agent IA vous dise :  
> « Réservation confirmée au Restaurant Bella Roma, samedi à 20h pour 5 personnes ! »
Autrement dit, jusqu'à que l'agent n'appel plus aucun outil.


### Agent IA : Et de votre point de vue d’utilisateur ?

De votre côté, en tant qu’utilisateur, toute cette boucle et cette organisation entre l’agent IA et les outils se passent dans les coulisses. Ce que vous voyez, c’est juste un échange tout simple : vous posez une question (« Réserve-moi un restaurant italien samedi soir »), et quelques instants plus tard, l’agent vous donne la réponse finale (« C’est réservé ! Voici l’adresse et l’heure »).

Vous n’avez pas besoin de savoir combien d’étapes il a fallu, quels outils ont été utilisés, ni combien de fois il a dû chercher, vérifier ou recommencer. Toute cette mécanique complexe est totalement invisible. Le but des agents IA, c’est justement de vous simplifier la vie : vous donnez une mission, et l’IA s’occupe de tout, du début à la fin.

Finalement, pour vous, l’expérience ressemble à un simple échange avec un assistant très malin qui comprend ce que vous voulez, gère toutes les étapes à votre place, et revient seulement quand la tâche est vraiment accomplie.

---------

Si mes articles vous intéressent et que vous avez des questions ou simplement envie de discuter de vos propres défis, n'hésitez pas à m'écrire à anas0rabhi@gmail.com, j'aime échanger sur ces sujets !

Vous pouvez aussi vous abonner à ma newsletter :)

<div style="text-align: center; margin: 40px 0;">
  <a href="https://anas-ai.kit.com/d8b1a255cc" target="_blank" style="display: inline-block; background-color: #222222; color: #ffffff; font-weight: bold; padding: 16px 32px; text-decoration: none; border-radius: 8px; font-size: 18px; letter-spacing: 0.8px; box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2); transition: all 0.3s ease; border: none;">
    <span style="margin-right: 10px;">✉️</span> S'abonner à ma newsletter
  </a>
</div>

---
