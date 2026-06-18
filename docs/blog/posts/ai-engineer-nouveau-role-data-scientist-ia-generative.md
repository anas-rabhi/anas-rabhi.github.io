---
title: "AI Engineer : le nouveau rôle du data scientist en IA générative"
slug: ai-engineer-nouveau-role-data-scientist-ia-generative
description: "AI engineer : le rôle de celui qui intègre les modèles d'IA générative en production sans les entraîner. Définition, différence avec le data scientist et le ML engineer."
categories:
  - "Blog"
  - "IA"
  - "Métier"
tags:
  - "AI Engineer"
  - "Data Scientist"
  - "IA générative"
  - "Métier"
  - "LLMOps"
date: 2026-06-18
comments: true
authors:
  - Anas
pin: false
math: false
mermaid: false
---

## AI Engineer : qui c'est, et pourquoi le terme existe

Un AI engineer, c'est celui qui intègre des modèles d'IA générative en production sans les entraîner lui-même. Il part de modèles existants, des LLM accessibles par API ou en open source, et son travail consiste à les transformer en quelque chose d'utile et de fiable : un RAG, un agent, une chaîne de traitement qui tient en production. C'est un rôle qui n'existait pas vraiment il y a trois ans.

Je suis Anas Rabhi, data scientist freelance, et c'est de plus en plus comme ça que je décris ce que je fais. C'est surtout une nouvelle appellation. En data science, le rôle a toujours bougé selon les capacités de chacun et selon ce dont l'entreprise avait besoin : la même personne a pu être appelée data scientist, ingénieur IA, machine learning engineer, parfois les trois. « AI engineer » est la dernière de ces étiquettes, celle qui colle au travail qu'on fait depuis l'arrivée de l'IA générative. Cet article explique ce qu'elle recouvre, pourquoi elle est apparue, et en quoi elle diffère du data scientist et du ML engineer.

<!-- more -->

## C'est quoi un AI engineer, concrètement

Le terme s'est popularisé en 2023, notamment avec l'essai *The Rise of the AI Engineer*. L'idée de départ est simple : depuis que des modèles très capables sont disponibles par simple appel d'API, on peut construire des produits d'IA sérieux sans jamais entraîner de modèle. Le centre de gravité du travail s'est déplacé.

Un AI engineer passe le plus clair de son temps sur ce qu'il y a autour du modèle. Récupérer les bons documents, structurer le contexte, écrire les prompts, brancher des outils, gérer les cas d'erreur, mesurer la qualité des réponses, et faire tenir tout ça en production avec des coûts et une latence acceptables.

Ce n'est ni un data scientist classique ni un développeur classique. C'est quelqu'un qui se situe entre les deux : assez de logiciel pour mettre en production, assez de compréhension des modèles pour savoir ce qu'on peut leur demander et où ils vont échouer.

## Pourquoi ce rôle est apparu avec l'IA générative

Avant, faire de l'IA voulait souvent dire entraîner un modèle. On collectait des données labellisées, on choisissait une architecture, on entraînait, on évaluait, on recommençait. C'était le coeur du métier de data scientist, et ça reste indispensable pour beaucoup de problèmes.

L'IA générative a changé l'équation. Les modèles de fondation arrivent déjà entraînés, et ils sont assez bons pour résoudre des tâches qu'on aurait mis des mois à adresser avant. Du coup, le goulot d'étranglement n'est plus l'entraînement. Il est dans l'intégration : comment brancher ce modèle sur les données de l'entreprise, comment l'évaluer, comment le rendre fiable, comment le mettre entre les mains des utilisateurs.

C'est exactement le sujet que je creuse dans [réussir un projet IA se décide avant la première ligne de code](reussir-projet-ia-avant-le-code.md). Le métier d'AI engineer, c'est en grande partie ce travail d'intégration et de cadrage, plus que le choix du modèle. D'ailleurs, dans la plupart des cas, on n'entraîne rien du tout : [entraînement, finetuning ou RAG, que choisir](entrainement-finetuning-rag-modele-ia.md) montre pourquoi le finetuning est rarement la première réponse.

## AI engineer, data scientist, ML engineer : les différences

Les trois rôles se recouvrent, et beaucoup de gens portent les trois casquettes selon les projets. Mais il y a une vraie différence d'axe.

**Le data scientist** part de la donnée. Son réflexe est de l'analyser, de la modéliser, de répondre à une question avec une méthode statistique ou un modèle entraîné. C'est mon métier d'origine, et c'est la base de tout le reste.

**Le ML engineer** part du modèle entraîné et de son cycle de vie : industrialiser l'entraînement, servir le modèle, le monitorer, gérer le réentraînement. C'est de l'ingénierie autour d'un modèle qu'on possède.

**L'AI engineer** part d'un modèle qu'il n'a pas entraîné et qu'il considère comme une brique. Son travail est de construire un système autour : retrieval, prompts, outils, garde-fous, évaluation, interface. Le modèle est un composant parmi d'autres, pas le produit final.

En pratique, sur une mission d'IA générative, je fais surtout de l'AI engineering, avec un fond de data science pour comprendre les données et un peu de ML engineering pour la mise en production.

## Ce que fait un AI engineer au quotidien

Le quotidien ressemble assez peu à l'image qu'on se fait de l'IA. Il y a peu d'entraînement de modèle, et beaucoup d'ingénierie de système. Voici les briques qui reviennent sur la plupart de mes missions :

- **Le RAG** : connecter un LLM aux documents de l'entreprise pour qu'il réponde sur leur base. C'est le cas d'usage le plus fréquent, et j'en explique le principe dans [c'est quoi le RAG](mais-que-es-le-rag.md).
- **Les agents** : faire enchaîner au modèle des actions et des appels d'outils pour mener une tâche, un sujet que je détaille dans le guide [agents IA](/agents-ia/).
- **L'évaluation** : sans mesure, on ne sait pas si le système marche. C'est la partie la moins visible et la plus déterminante, comme je l'explique dans [comment améliorer un RAG par l'analyse d'erreur](comment-ameliorer-l-IA.md).
- **Le LLMOps et la production** : coûts, latence, monitoring, sécurité, et toute la plomberie qui sépare une démo d'un produit qui tient.
- **L'ingénierie logicielle** : c'est ce qui distingue un AI engineer d'un simple utilisateur de ChatGPT. Il faut savoir construire et maintenir un système, pas juste écrire un bon prompt.

La compétence centrale, au fond, c'est le pragmatisme : savoir quand l'IA est la bonne réponse, et quand une solution plus simple suffit.

## Pourquoi je me définis désormais comme AI engineer

Pendant des années, je me suis présenté comme data scientist, et c'est toujours vrai sur le fond. Mais quand je regarde ce que je fais réellement sur mes missions d'IA générative, je n'entraîne presque jamais de modèle. Je passe mon temps à intégrer des modèles existants dans des produits qui doivent fonctionner pour de vrais utilisateurs.

C'est ça, le travail d'AI engineer. Le titre n'a pas d'importance en soi, mais il décrit mieux la réalité du métier aujourd'hui : moins de modélisation pure, plus d'intégration, d'évaluation et de mise en production. Et c'est précisément là que se joue la valeur pour une entreprise.

Si vous avez un projet d'IA générative à mettre en production, c'est le genre de mission sur lequel j'interviens en tant que [consultant IA](/consultant-ia-toulouse/), du cadrage jusqu'au déploiement.

## Questions fréquentes sur le métier d'AI engineer

**C'est quoi un AI engineer ?**
C'est un profil qui construit des produits d'IA en intégrant des modèles existants, principalement des LLM, sans les entraîner lui-même. Son travail porte sur tout ce qui entoure le modèle : retrieval, prompts, outils, évaluation, mise en production.

**Quelle est la différence entre un data scientist et un AI engineer ?**
Le data scientist part de la donnée et entraîne souvent ses propres modèles. L'AI engineer part de modèles de fondation déjà entraînés et se concentre sur l'intégration et la mise en production. Beaucoup de gens font les deux selon les projets.

**Un AI engineer entraîne-t-il des modèles ?**
Rarement. La plupart du temps, il utilise des modèles existants par API ou en open source. Le finetuning n'arrive qu'en dernier recours, quand le RAG et un bon prompt ne suffisent pas.

**Faut-il être data scientist pour devenir AI engineer ?**
Non, plusieurs chemins mènent au rôle, notamment le développement logiciel. Un fond de data science aide à comprendre les données et les limites des modèles, mais la compétence d'ingénierie système est tout aussi importante.

**Quelles compétences pour un AI engineer ?**
Le RAG, les agents, l'ingénierie de prompt, l'évaluation, le LLMOps, et surtout de solides bases en ingénierie logicielle pour construire un système qui tient en production.

**Data scientist ou AI engineer : comment je me définis ?**
Les deux, et ça dépend du projet. Sur une mission d'IA générative, je n'entraîne presque jamais de modèle, je l'intègre en production : c'est du travail d'AI engineer. Sur un projet de data science plus classique, je reste data scientist. Le titre m'importe peu, c'est juste celui qui décrit le mieux ce que je fais sur le moment.

**AI engineer, est-ce juste un nouveau nom à la mode ?**
Le titre est récent, mais il décrit un travail réel qui a émergé avec les modèles de fondation : intégrer de l'IA générative en production plutôt qu'entraîner des modèles. En data science, les intitulés ont toujours été flous et changeants, sans vrai standard. L'important n'est pas l'étiquette mais ce qu'on fait réellement, et ce que l'entreprise en retire.

## Un titre récent pour un travail réel

L'AI engineer n'est pas une révolution, c'est un déplacement. Les modèles de fondation ont rendu l'entraînement moins central et l'intégration plus déterminante. Le rôle décrit simplement ceux qui font ce travail d'intégration en production : data scientists qui ont évolué, développeurs qui sont montés vers l'IA, ou profils hybrides comme le mien.

Au fond, peu importe le titre. Ce qui compte, c'est de résoudre un problème métier avec la solution la plus simple qui tienne en production. Que vous appeliez ça data science ou AI engineering, c'est le même métier vu sous un autre angle.

---------

Si mes articles vous intéressent et que vous avez des questions ou simplement envie de discuter de vos propres défis, n'hésitez pas à m'écrire à [anas@tensoria.fr](mailto:anas@tensoria.fr), j'aime échanger sur ces sujets !

Vous pouvez aussi [réserver un créneau d'échange](https://cal.eu/anas-rabhi/rendez-vous-ianas) ou vous abonner à ma newsletter :)


---

### À propos de moi

Je suis **Anas Rabhi**, AI engineer et data scientist freelance. J'accompagne les entreprises dans leur stratégie et mise en œuvre de solutions d'IA générative (RAG, Agents, NLP).

Découvrez mes services sur [tensoria.fr](https://tensoria.fr) ou testez notre solution d'agents IA [heeya.fr](https://heeya.fr).

<div style="text-align: center; margin: 40px 0; gap: 16px; display: flex; flex-wrap: wrap; justify-content: center;">
  <a href="https://cal.eu/anas-rabhi/rendez-vous-ianas" target="_blank" style="display: inline-block; background-color: #4F46E5; color: #ffffff; font-weight: bold; padding: 16px 32px; text-decoration: none; border-radius: 8px; font-size: 18px; letter-spacing: 0.8px; box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2); transition: all 0.3s ease; border: none;">
    Réserver un créneau
  </a>
  <a href="https://anas-ai.kit.com/d8b1a255cc" target="_blank" style="display: inline-block; background-color: #222222; color: #ffffff; font-weight: bold; padding: 16px 32px; text-decoration: none; border-radius: 8px; font-size: 18px; letter-spacing: 0.8px; box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2); transition: all 0.3s ease; border: none;">
    <span style="margin-right: 10px;">✉️</span> S'abonner à ma newsletter
  </a>
</div>
