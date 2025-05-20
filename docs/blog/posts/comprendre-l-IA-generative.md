---
title: "Comprendre l'intelligence artificielle : L'IA générative (Partie 2)"
description: "Découvrez les concepts fondamentaux de l'intelligence artificielle expliqués simplement, avec des exemples concrets et des conseils pratiques pour mieux comprendre cette technologie transformative."
categories:
  - "Blog"
  - "IA"
tags:
  - "Intelligence Artificielle"
  - "Conseils Pratiques"
date: 2025-04-10
comments: true
authors:
  - Anas
pin: true
math: true
mermaid: true
---

## Introduction

Dans la première partie de cette exploration de l'intelligence artificielle, j'ai voulu vulgariser des concepts souvent très flous en abordant des concepts tels que le machine learning et le deep learning. Aujourd'hui, je vous invite à plonger avec moi dans un domaine dont on entend parler partout depuis deux ans : l'IA générative.

Avec l'essor impressionnant d'outils comme ChatGPT, Perplexity ou Midjourney, l'IA générative s'est imposée sur le devant de la scène. Contrairement aux autres formes d'IA qui se contentent d'analyser ou de classer des données, cette technologie est capable de créer de nouvelles données. Que ce soit pour générer du texte, des images, ou même de l'audio. En gros, tout réside dans le mot "Générative" : pour faire simple c'est une forme ou domaine d'IA qui va permettre de générer un nouveau contenu.

Mon objectif dans cette partie est de vous expliquer ce qu'est l'IA générative, de vous éclairer sur son fonctionnement de manière accessible, d'illustrer avec des exemples concrets ses applications, et de discuter des implications profondes qu'elle peut avoir. Je vous propose donc de découvrir comment les machines peuvent non seulement "comprendre" le monde, mais aussi participer activement à sa création.

<!-- more -->

## Les premiers pas

Une des choses qui m'a le plus impressionné dans le domaine de l'IA générative a été l'émergence de modèles performants tels que GPT-3 (ChatGPT en 2022). Qu'on a appelé les LLM, large language modèles ou gros modèles en français si on peut dire ça comme ça. La première chose remarquable, c'est l'impression de dialoguer avec une intelligence artificielle qui non seulement comprend nos propos, mais parvient également à maintenir une conversation cohérente.

Ayant travaillé sur des projets de traitement du langage naturel (NLP) (voir la partie 1 : [Comprendre l'intelligence artificielle - Guide pratique simple](https://ianas.fr/blog/2025/04/05/comprendre-lintelligence-artificielle--guide-pratique-simple-partie-1/)), je savais que la tâche n'était pas aussi simple d'obtenir des résultat aussi bons. Et si cette tâche était simple, des géants de la technologie comme Google auraient déjà mis au point des IA aussi performantes. Cependant, à l'époque (avant 2022), personne ne savait vraiment comment s'y prendre.

L'arrivée de ChatGPT a marqué un tournant en introduisant une nouvelle approche dans l'IA, qui, en réalité, n'est pas si complexe mais repose surtout sur la puissance brute. Elle consiste à utiliser d'énormes quantités de données et de puissance de calcul pour entraîner de grands modèles (avec beaucoup de paramètres) de type "Transformer" pendant de longues périodes. Les modèles Transformer ne sont pas nouveaux, ils existent depuis [2017](https://arxiv.org/abs/1706.03762). Ce qui était vraiment novateur, c'était l'échelle et la manière dont ils ont été utilisés. 

C’est un peu comme si, pour gagner une course de voiture, au lieu d’optimiser la forme de la voiture ou d’améliorer la technique du pilote, on décidait simplement d’installer le plus de **moteurs** puissants possible tout en **agrandissant** la voiture, en espérant que la voiture ira forcément plus vite grâce à toute cette puissance, même si ce n’est pas la solution la plus élégante. Dans notre cas, la **taille du modèle** correspond à la **taille de la voiture**, et le **moteur de la voiture** fait référence à la **donnée** ingérée par le modèle.

    Pour vous donner une idée du coût, environ 4 millions de dollars ont été nécessaires pour entraîner l'un des premiers modèles d'IA à atteindre une performance satisfaisante : GPT-3 (voir : [Coût d'entraînement de GPT-4](https://team-gpt.com/blog/how-much-did-it-cost-to-train-gpt-4/)), sans compter le salaire des chercheurs et les années de recherche nécessaires pour y parvenir.

## Un changement en IA

Vous l’avez compris, l’intelligence artificielle a connu un véritable tournant avec l’arrivée de cette approche « bourrin » 😅 : après cette découverte, plus rien n’a été comme avant dans le domaine de l’IA.

Mais revenons à l'essentiel. Je me suis peut-être emporté en parlant déjà des modèles transformers, mais rappelez-vous, dans la [partie 1](https://ianas.fr/blog/2025/04/05/comprendre-lintelligence-artificielle--guide-pratique-simple-partie-1/) quand je définissais les modèles comme des algorithmes qui apprennent grâce aux données qu'on leur fournit. Eh bien, les transformers, c'est un type d'algorithme qui a été construit différemment des autres. Pour garder les choses simples, imaginons cela comme un bâtiment : selon l'usage que l'on veut faire d'un bâtiment, on va choisir une forme particulière. Un immeuble résidentiel n'aura pas forcément la même forme qu'un immeuble d'entreprises. C'est un peu le même principe : en IA, les modèles peuvent avoir différentes architectures. 

Le point commun de tous les modèles d'IA, c'est qu'à l'intérieur de chacun d'eux, il y a des chiffres qu'on appelle « paramètres ». Un paramètre peut prendre n’importe quelle valeur numérique. Pris isolément, un paramètre n’a pas de signification pour nous, mais c’est l’ensemble de ces millions (voire milliards) de paramètres qui permet au modèle « d’apprendre » et de fonctionner.

Les paramètres sont ajustés grâce aux données qu'on fournit au modèle lors de son apprentissage. Les données permettent de trouver la combinaison de paramètres optimale pour que l'IA soit la plus performante possible. Le dernier élément à comprendre dans un modèle d'IA, c'est que tous ces paramètres sont connectés entre eux par des opérations mathématiques. C'est ce qui permet de calculer le résultat final de l'IA.
C'est tout ? C'est juste des chiffres et des opérations qui permettent à ChatGPT d'être aussi fort ? Eh bien, aussi simple que cela puisse paraître => OUI. Bien évidemment, l'idée globale est simple, mais lorsqu'on s'y met, ça peut vite devenir complexe.

S'il y a une chose à retenir en IA générative, c'est qu'on utilise massivement des données pour entraîner de très gros modèles pour qu'ils continuent de s'améliorer en termes de performance comme on peut le voir sur le graphique suivant : le modèle de 70 milliards de paramètres (Llama 3 70b) a une des meilleures performances, alors que ceux ayant 7 ou 8 milliards sont en dessous. Évidemment, on arrive de plus en plus à améliorer l'efficacité de plus petits modèles mais nous y viendrons plus tard.

![Illustration de la montée en performance des modèles d'IA générative](./img/performance.png)




---------

Si mes articles vous intéressent et que vous avez des questions ou simplement envie de discuter de vos propres défis, n'hésitez pas à m'écrire à anas0rabhi@gmail.com, j'aime échanger sur ces sujets !

Vous pouvez aussi vous abonner à ma newsletter :)

<div style="text-align: center; margin: 40px 0;">
  <a href="https://anas-ai.kit.com/d8b1a255cc" target="_blank" style="display: inline-block; background-color: #222222; color: #ffffff; font-weight: bold; padding: 16px 32px; text-decoration: none; border-radius: 8px; font-size: 18px; letter-spacing: 0.8px; box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2); transition: all 0.3s ease; border: none;">
    <span style="margin-right: 10px;">✉️</span> S'abonner à ma newsletter
  </a>
</div>
