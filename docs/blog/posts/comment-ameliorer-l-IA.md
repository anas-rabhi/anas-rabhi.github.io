---
title: "Comment améliorer le RAG"
slug: comment-ameliorer-le-rag
description: "Améliorer un RAG : méthode par l'analyse des erreurs, métriques clés (Faithfulness, RAGAS) et outils de monitoring. Approche pragmatique après 10+ projets terrain."
categories:
  - "Blog"
  - "LLM"
  - "IA"
  - "RAG"
tags:
  - "RAG"
  - "LLM"
  - "Intelligence Artificielle"
  - "Évaluation"
  - "Conseils Pratiques"
date: 2025-03-26
comments: true
authors:
  - Anas
pin: true
math: true
mermaid: true
---

Souvent, pour améliorer une application d'IA comme un RAG ou un agent, il est plus judicieux de se concentrer sur l'analyse fine des erreurs plutôt que de céder à la tentation d'ajouter systématiquement de nouveaux outils. Voyons pourquoi cette approche pragmatique est souvent la plus efficace — et surtout, comment la mettre en place concrètement avec les bons outils de mesure.

<!-- more -->

## La course aux outils : une fausse bonne idée ?

Lorsqu'on cherche à améliorer un système [RAG](mais-que-es-le-rag.md) ou un agent conversationnel, l'écosystème technologique nous présente une multitude d'outils. Frameworks, bases de données vectorielles, modèles d'embedding, techniques de réécriture de prompt... chacun promettant d'améliorer significativement les performances.

Pourtant, céder à cette "course aux outils" sans une compréhension claire du problème à résoudre peut s'avérer contre-productif. L'approche la plus pragmatique repose moins sur l'accumulation de nouvelles briques technologiques que sur une **analyse rigoureuse des erreurs** et l'**amélioration continue** de l'architecture existante.

## Décortiquer les erreurs d'un RAG : où chercher ?

Prenons l'exemple concret d'un système RAG. Lorsqu'il fournit une réponse incorrecte, les causes potentielles sont nombreuses :

1. **Le LLM lui-même :** Le modèle peut "halluciner", c'est-à-dire inventer des informations qui ne sont pas présentes dans les documents récupérés.
2. **L'étape de récupération (Retrieve) :** Les documents pertinents ne sont pas correctement identifiés. Le problème peut venir du modèle d'embedding, de la requête de recherche, ou de l'indexation.
3. **Le découpage (Chunking) :** La manière dont les documents sont segmentés peut être inadaptée, coupant des informations importantes ou ne fournissant pas assez de contexte.
4. **Le pré-traitement des données :** La qualité initiale des documents (nettoyage, formatage) peut impacter l'ensemble du processus.

Face à une erreur, ajouter un nouvel outil sans avoir identifié laquelle de ces étapes est défaillante revient souvent à ajouter de la complexité inutile. J'ai décrit cette méthode d'[analyse d'erreur en détail dans cet article](rag-trop-simple.md) avec des cas concrets chiffrés.

## Mais comment savoir si on s'améliore vraiment ?

C'est la question qu'on pose rarement. On fait un changement — nouveau modèle d'embedding, taille de chunk différente, re-ranking — et comment savoir si c'est vraiment mieux ?

Sans cadre d'évaluation, on navigue à vue. On change quelque chose, ça semble mieux sur 2-3 exemples, on valide. Mauvaise méthode.

**La bonne approche :**

1. **Constituer un jeu de test fixe** avec 30 à 50 paires question/réponse attendue. Ce jeu ne change pas — c'est votre baseline.
2. **Mesurer les métriques RAG** sur ce jeu avant et après chaque modification.
3. **Décider avec des chiffres**, pas avec des impressions.

Sans baseline fixe, chaque changement est une supposition.

## Les métriques RAG clés à suivre

Trois métriques suffisent pour commencer :

**Faithfulness (fidélité)**
La réponse générée est-elle fidèle aux documents récupérés ? Une réponse "fidèle" ne va pas au-delà de ce que les chunks contiennent. C'est la métrique principale pour détecter les hallucinations.

**Answer Relevancy (pertinence de la réponse)**
La réponse répond-elle vraiment à la question posée ? Un LLM peut être fidèle aux sources mais répondre à côté. Cette métrique capte ça.

**Context Precision (précision du contexte)**
Les chunks récupérés par le retrieval sont-ils tous utiles ? Si vous récupérez 5 chunks et que 3 ne servent à rien, votre retrieval a un problème de précision.

Il existe des outils qui calculent ces métriques automatiquement, notamment **[RAGAS](https://docs.ragas.io/)**, qui utilise lui-même un LLM comme juge. Ce n'est pas parfait, mais c'est bien plus scalable qu'une évaluation 100% humaine une fois passé le démarrage.

## L'évaluation : humaine d'abord, automatisée ensuite

Dans les premières phases de développement, **rien ne remplace une évaluation humaine**. Un humain comprend les nuances, le contexte, et identifie des types d'erreurs subtiles qu'une métrique automatique peut manquer.

Investir du temps pour décortiquer manuellement un échantillon représentatif de cas problématiques est souvent **plus rentable à long terme** : ça fournit des insights qualitatifs précieux pour orienter les améliorations.

L'automatisation (RAGAS, DeepEval) prend ensuite le relais pour vérifier l'impact des corrections à plus grande échelle.

## L'outil de monitoring : voir pour comprendre

Améliorer sans voir, c'est improviser. Pour chaque erreur analysée, il faut pouvoir inspecter :

- La requête utilisateur originale
- Les chunks récupérés (avec leur score de similarité)
- Le prompt complet envoyé au LLM
- La réponse générée

**[Langfuse](https://langfuse.com/)** fait ça très bien, en open-source. On voit exactement à quelle étape ça a déraillé. C'est souvent là qu'on réalise que le problème qu'on pensait être de la génération est en réalité un problème de retrieval — et ça change tout.

Un conseil : configurez le monitoring dès le début, même en phase de test. Les premières semaines de production sont une mine d'or en termes d'erreurs à analyser. Pour une vue complète des outils disponibles, j'en parle aussi dans [cet article sur les outils de monitoring RAG](rag-trop-simple.md).

## Corriger les problèmes à la source

Une fois l'erreur comprise grâce à l'évaluation, l'amélioration devient ciblée. Chaque erreur identifiée peut alors être corrigée en ajustant le composant défaillant :

* Améliorer le prompt envoyé au LLM.
* Affiner la stratégie de découpage (chunking).
* Tester et choisir un meilleur modèle d'embedding.
* Nettoyer ou enrichir les données sources.
* Ajuster les paramètres de l'algorithme de recherche.
* Parfois, oui, intégrer un nouvel outil — mais seulement après analyse.

## L'amélioration continue en production

L'évaluation ne s'arrête pas une fois l'application déployée. En production, il est essentiel de **continuer à monitorer les performances** en continu. Les données évoluent, de nouveaux cas d'usage apparaissent, les attentes des utilisateurs changent.

Idéalement, mettez en place des mécanismes pour **intégrer les retours utilisateurs** (pouce levé/baissé sur les réponses) dans le cycle d'amélioration. C'est un cycle continu : observer, analyser, améliorer.

Si vous cherchez à voir cette méthode appliquée sur un cas réel, lisez [comment un RAG multi-sources a été optimisé pour la rédaction d'appels d'offres BTP](cas-usage-rag-redaction-appels-offres-btp.md) — le retour d'expérience illustre exactement cette approche itérative.

## Conclusion : une approche méthodique et itérative

Plutôt que de céder à l'attrait du dernier outil à la mode, une démarche plus payante consiste à :

1. **Évaluer** rigoureusement les sorties (jeu de test fixe + métriques).
2. **Analyser** les erreurs pour en comprendre la cause racine.
3. **Améliorer** de manière ciblée le composant défaillant.
4. **Monitorer** en continu et intégrer les retours.

C'est souvent la voie la plus directe vers des applications IA réellement performantes et utiles au quotidien.

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
