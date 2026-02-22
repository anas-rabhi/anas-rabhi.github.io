---
title: "Les 5 erreurs que tout le monde fait avec le RAG"
description: "Retour d'expérience sur les erreurs les plus fréquentes quand on se lance dans un projet RAG en entreprise : mauvaise communication, sous-estimation, données ignorées, dépendance aux frameworks et absence de mesure."
categories:
  - "Blog"
  - "IA"
  - "RAG"
tags:
  - "RAG"
  - "Intelligence Artificielle"
  - "Retour d'expérience"
  - "Conseils Pratiques"
date: 2026-02-21
comments: true
authors:
  - Anas
pin: true
math: true
mermaid: true
---

## Introduction

Depuis 2023, j'ai réalisé une dizaine de projets RAG moi-même, et j'en ai dirigé une autre dizaine avec des équipes. Certains se sont très bien passés, d'autres un peu moins, mais on a toujours essayé d'apprendre et se corriger tout au long du projet. Avec le recul, je retrouve toujours les mêmes erreurs, que ce soit chez moi au début, chez des clients, ou chez des confrères. Ce ne sont pas des erreurs techniques (j'en parle dans [cet article](les-4-causes-techniques-echec-rag.md)), mais des erreurs de posture, d'approche et de méthode.

Ce sont des erreurs qu'on fait tous au moins une fois. L'idée ici, c'est de les poser clairement pour éviter de les répéter.

<!-- more -->

## Erreur n°1 — Croire que le RAG va répondre à tout

C'est probablement l'erreur la plus fréquente, et elle ne vient pas forcément de l'équipe technique. Elle vient d'un décalage entre ce que le client imagine et ce que le RAG fait réellement.

Un RAG, c'est de la **question-réponse ciblée** sur une base documentaire. On pose une question, le système va chercher les bons morceaux de documents, et le LLM formule une réponse à partir de ça. C'est puissant, mais c'est cadré.

Le problème, c'est que pour quelqu'un qui n'est pas dans le monde de l'IA, "une IA, ça répond à tout". C'est l'image que les gens ont. Donc quand on met en place un chatbot RAG, le client s'attend naturellement à ce que ça gère n'importe quelle demande.

Je me souviens d'un de nos premiers projets RAG, en 2023, quand GPT-3.5 commençait à être vraiment exploitable. On avait mis en place un chatbot pour [Odecia](https://odecia.fr) afin de répondre aux questions des clients sur leur site. Le système fonctionnait bien sur les questions qu'on avait anticipées. Sauf qu'en analysant les vraies questions des utilisateurs, on s'est vite rendu compte que **les questions réelles n'avaient rien à voir avec celles qu'on avait imaginées**.

Des utilisateurs demandaient "résume-moi ce fichier", ou posaient des questions qui n'avaient aucun rapport avec la documentation disponible. Pour un data scientist, c'est évident que ça ne peut pas marcher : le RAG n'a pas accès au fichier de l'utilisateur, et il ne peut répondre que sur ce qu'il connaît. Mais pour une personne extérieure au monde de l'IA, c'est incompréhensible. "C'est de l'IA, non ? Ça devrait comprendre."

C'était un de nos premiers RAG, et ça nous a appris une chose essentielle : **il faut dès le début bien communiquer sur ce que le RAG peut faire et ce qu'il ne peut pas faire**. Expliquer clairement le périmètre. Donner des exemples de questions qui fonctionnent et de questions qui ne fonctionneront pas. Gérer les attentes dès le départ, pas après la déception.

Depuis, on fait systématiquement cet exercice avec chaque nouveau client. Et ça change tout. Moins de frustration, moins de déception, et un projet qui part sur de bonnes bases. C'est vrai que ça fait moins rêver, mais on ne vend pas de rêve au client, on essaye de vendre un produit qui fonctionne, avec la réalité du terrain. Ce que je dis souvent à mes clients : on a pas besoin que l'IA fasse 100% de réponses justes pour que ça nous fasse gagner du temps. A 90% de bonnes réponses on est déjà gagnant dans l'histoire. Economiquement parlant, 90% bonnes réponses, veut dire qu'on peut renseigner 9 clients sur 10, ce qui évite déjà la perte de temps à répondre à des questions répétitives, et évite de perdre des clients. Le client est très statisfait quand il trouve des réponses de façon instantanée, et sans avoir à chercher manuellement dans des documents.

## Erreur n°2 — Penser que le prochain RAG sera simple parce qu'on en a déjà fait un

Celle-là, on l'a tous faite. On livre un premier RAG, ça se passe bien, et on se dit : "Bon, maintenant on a la méthode, le prochain sera rapide." Faux.

Un RAG, c'est **du cas par cas**. Chaque projet dépend des données du client, du type de questions posées, du volume de documents, de la complexité des formats. D'un business à un autre, ce sont des données différentes, des questions différentes, et donc des problèmes différents.

Pour donner un ordre d'idée concret : j'ai eu des projets RAG où on a passé **2 mois** pour industrialiser le système et atteindre environ 90 % de bonnes réponses. Des milliers de documents à ingérer, des mises à jour hebdomadaires, mais des documents relativement propres et des questions prévisibles. C'était du travail, mais on savait où on allait.

Et puis j'ai eu d'autres projets où on a passé **6 mois** pour atteindre à peine 80 % de bonnes réponses. La documentation était complexe : des tableaux dans des PDF, des schémas techniques, des documents semi-structurés, des formats hétérogènes. Chaque type de document posait un nouveau problème. Chaque amélioration sur un type de question en cassait une autre.

Le vrai défi, c'est que **plus il y a de données, plus le RAG devient compliqué**. Ce n'est pas linéaire. Passer de 100 à 1000 documents, ce n'est pas juste "10x plus de travail", c'est un changement de nature : le retriever doit être plus précis, le chunking doit être plus fin, et les cas limites se multiplient.

J'ai aussi eu des clients qui venaient nous voir parce que **leur RAG existant ne fonctionnait pas**. Quelqu'un leur avait promis un truc simple et rapide. Ça avait été fait en quelques jours avec LangChain en mode automatique, sans se poser de questions sur les données. Résultat : des performances sous les 70 %, un client frustré, et un projet à reprendre quasiment de zéro.

Chaque RAG est un projet en soi. Il n'y a pas de raccourci.

## Erreur n°3 — Foncer dans le code sans regarder les données

C'est une erreur classique de développeur (et je m'inclus dedans). On reçoit un brief, on a envie de coder, et on se lance directement dans le pipeline : parsing, chunking, embeddings, retriever, prompt. On a nos habitudes, on connaît l'architecture, on veut avancer vite.

Sauf que la première chose à faire, avant même d'écrire une seule ligne de code, c'est **d'ouvrir les données du client et de les regarder**.

Combien de fois j'ai vu des estimations de projet complètement à côté de la réalité parce que personne n'avait pris le temps de regarder les documents ? On estime "3 semaines" sur la base d'un brief qui dit "on a des PDF", et quand on ouvre les PDF, on découvre des scans de mauvaise qualité, des tableaux imbriqués, des en-têtes incohérents, des documents de 200 pages sans structure, ou pire, des fichiers qui mélangent texte, images et annotations manuscrites.

Les données, c'est **80 % du travail d'un RAG**. Si les documents sont propres, bien structurés, avec du texte exploitable, le RAG sera relativement simple à mettre en place. Si les documents sont un chaos de formats hétérogènes, aucun framework ni aucune techno miracle ne va résoudre le problème à votre place.

Concrètement, avant de coder quoi que ce soit, je prends maintenant systématiquement une demi-journée (parfois plus) pour :

- Ouvrir un échantillon représentatif des documents du client
- Regarder les formats (PDF, Word, Excel, HTML, images...)
- Vérifier la qualité du texte extractible
- Identifier les cas problématiques (tableaux, schémas, scans)
- Estimer la volumétrie et la fréquence de mise à jour
- Comprendre quelles questions les utilisateurs vont poser sur ces données

C'est cette étape qui me permet d'estimer correctement un projet. Et c'est cette étape que la plupart des gens sautent. On veut aller vite, on veut montrer un premier résultat. Mais un premier résultat sur des données qu'on n'a pas comprises, ça ne vaut rien.

## Erreur n°4 — Tout faire avec un framework sans comprendre ce qui se passe derrière

J'ai utilisé LangChain dans mes premiers RAG. J'ai aussi beaucoup utilisé LlamaIndex. Et je ne dis pas que ces frameworks sont mauvais. Mais je dis qu'il y a un vrai piège à les utiliser sans comprendre ce qu'ils font derrière leurs fonctions.

Le problème est simple, **quand le RAG ne répond pas bien à une question, la première chose à faire, c'est de comprendre pourquoi**. Et pour comprendre pourquoi, il faut remonter chaque étape du pipeline (j'en parle en détail dans [cet article sur l'analyse d'erreur](pourquoi-le-rag-ne-fonctionne-pas.md)). Est-ce que le parsing a bien extrait l'information ? Est-ce que le chunking n'a pas coupé au mauvais endroit ? Est-ce que le retriever a trouvé les bons chunks ? Est-ce que le prompt était bien formulé ?

Quand chaque étape est encapsulée dans une abstraction de framework, **debugger devient un cauchemar**. On passe un temps fou à comprendre ce que fait la fonction `X` dans la classe `Y`, à naviguer dans la documentation, à chercher comment customiser un comportement qui ne nous convient pas.

Le temps que j'ai investi à customiser les briques de LlamaIndex et à comprendre les différentes étapes internes, j'ai passé **plus de temps à le faire qu'à coder mon propre système** de RAG. Et mon propre système, je le comprends de bout en bout, je peux le modifier en 5 minutes, et je sais exactement ce qui se passe à chaque étape.

Il y a un autre avantage à coder ses propres briques : **une fois que vous les avez, elles sont à vous**. D'un projet à l'autre, vous reprenez votre code, sur lequel vous avez la connaissance et la maîtrise totale. Vous pouvez changer ce dont vous avez besoin sans être dépendant des choix d'un framework.

Les frameworks sont précieux quand ils encapsulent des calculs complexes qu'on ne veut pas recoder (comme TensorFlow ou PyTorch pour le deep learning). Mais pour un RAG, les étapes sont conceptuellement simples : parser un document, le découper, le vectoriser, chercher les plus proches voisins, construire un prompt. Ce n'est pas de la rocket science. Le coder soi-même une première fois, c'est un excellent exercice qui permet d'apprendre chaque étape en profondeur et de garder la main.

Et sur le long terme, c'est encore plus vrai. Des nouvelles techniques sortent toutes les semaines dans le monde du RAG. Quand on veut les explorer ou les intégrer, on est toujours dépendant du framework et de sa capacité à s'adapter. Et soyons honnêtes : la capacité d'adaptation des frameworks d'IA générative est souvent mauvaise. Le temps qu'une technique soit intégrée proprement dans un framework, il y en a déjà trois nouvelles qui sont sorties.

Ce que je dis là s'applique aussi aux Agents IA, mais ça, on en reparlera une prochaine fois.

## Erreur n°5 — Ne pas mesurer dès le début

Celle-là, c'est l'erreur silencieuse. Le RAG est en place, il tourne, les utilisateurs posent des questions, et on a l'impression que "ça marche". Mais est-ce que ça marche vraiment ? À quel point ? On ne sait pas, parce qu'on n'a rien mis en place pour mesurer.

J'ai vu trop de projets où on ne commence à mesurer que quand les retours négatifs arrivent. À ce moment-là, on n'a aucune baseline, aucun historique, aucun moyen de savoir si les choses se sont dégradées ou si elles n'ont jamais été bonnes.

La mesure, ça doit commencer **dès le premier jour**. Pas besoin d'un outil sophistiqué au départ : un simple jeu de 30 à 50 questions-réponses de référence, qu'on passe régulièrement sur le système, suffit à avoir une idée claire de la performance. C'est ce qu'on appelle un **dataset d'évaluation**, et c'est la chose la plus importante que personne ne fait.

Sans ça, chaque modification devient un pari. On change le chunking, on ajuste le prompt, on change de modèle d'embeddings, et on n'a **aucun moyen objectif de savoir si c'est mieux ou pire**. On se fie au ressenti, aux retours informels, aux deux ou trois questions qu'on teste à la main. Ce n'est pas suffisant.

Concrètement, ce que je recommande :

- **Constituer un dataset d'éval** dès le début du projet, avec des questions représentatives et leurs réponses attendues
- **Le passer à chaque modification** du système pour vérifier qu'on progresse (et qu'on ne casse rien)
- **Logger les interactions** en production pour identifier les vrais cas d'usage et les vrais problèmes
- **Suivre un score simple** (% de bonnes réponses) dans le temps

C'est basique, mais c'est ce qui fait la différence entre un projet RAG qui s'améliore dans le temps et un projet qui stagne sans qu'on comprenne pourquoi.

## Conclusion

Ces 5 erreurs, je les ai toutes faites. L'IA générative donne une impression de magie, et avec cette impression vient la conviction que tout est réalisable rapidement. Même avec des années de projets data science derrière moi, l'habitude de faire du monitoring, de mesurer les performances, de structurer les choses, je n'ai pas été immunisé. On a mal estimé certains projets, on a voulu aller trop vite, et on s'est confronté à chacune de ces erreurs.

Et je continue à voir des équipes les refaire, souvent dans le même ordre : on se lance trop vite, on ne communique pas assez sur les limites, on sous-estime la complexité, on s'enferme dans un framework, et on oublie de mesurer.

Le RAG n'est pas un produit qu'on installe et qu'on oublie. C'est un **système vivant** qui demande de la rigueur, de la patience, et surtout une bonne compréhension des données et du besoin métier. La technique vient après.

Si vous voulez aller plus loin sur les aspects techniques, j'ai écrit sur [les 4 causes techniques d'échec d'un RAG](les-4-causes-techniques-echec-rag.md) et sur [l'analyse d'erreur comme méthode d'amélioration](pourquoi-le-rag-ne-fonctionne-pas.md).

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
