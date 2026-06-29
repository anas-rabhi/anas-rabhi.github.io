---
title: "IA locale : faire tourner un SLM en local (on-premise)"
slug: ia-locale-on-premise-slm
description: "IA locale : faire tourner un SLM en local ou on-premise pour la confidentialité et le coût. Outils (Ollama, vLLM, llama.cpp), quantification, matériel et limites."
categories:
  - "Blog"
  - "IA"
tags:
  - "SLM"
  - "IA locale"
  - "On-premise"
  - "LLMOps"
date: 2026-06-29
comments: true
authors:
  - Anas
pin: false
math: false
mermaid: false
faqs:
  - question: "Pourquoi faire tourner un SLM en local ?"
    answer: "Pour trois raisons concrètes : la confidentialité (les données ne quittent pas votre infrastructure, ce qui simplifie la conformité RGPD), le coût (à fort volume, l'auto-hébergement devient moins cher que les API), et la latence (un modèle local répond plus vite et fonctionne hors ligne). C'est particulièrement pertinent pour les données sensibles et les secteurs régulés."
  - question: "Quel outil pour exécuter un LLM en local ?"
    answer: "Pour le poste de travail et le prototypage, Ollama et LM Studio sont les plus simples : une commande ou une interface graphique suffit. llama.cpp est le moteur sous-jacent qui fait tourner les modèles au format GGUF, y compris sur CPU ou Mac. Pour la production avec du débit, on passe à vLLM ou à Text Generation Inference de Hugging Face, conçus pour servir beaucoup de requêtes en parallèle."
  - question: "Quelle config faut-il pour faire tourner un SLM ?"
    answer: "Ça dépend de la taille. Un modèle de 1 à 3 milliards de paramètres tourne sur à peu près n'importe quel ordinateur portable récent, parfois sur CPU. Un modèle de 7 à 8 milliards quantifié en 4 bits demande environ 6 à 8 Go de mémoire vidéo, ou un Mac Apple Silicon à mémoire unifiée. Au-delà, il faut un vrai GPU. La quantification est la clé pour faire tenir un modèle sur une machine modeste."
  - question: "C'est quoi la quantification (GGUF, 4 bits) ?"
    answer: "La quantification réduit la précision des paramètres d'un modèle, par exemple de 16 bits à 4 bits, pour diviser sa taille et accélérer l'inférence. GGUF est le format de fichier le plus répandu pour les modèles quantifiés exécutés avec llama.cpp. Une variante comme Q4_K_M offre un bon compromis entre taille et qualité. La perte de précision est en général faible au regard du gain de taille et de vitesse."
  - question: "L'IA locale est-elle conforme au RGPD ?"
    answer: "Faire tourner un modèle sur votre propre infrastructure évite d'envoyer des données personnelles à une API externe, ce qui lève une grande partie des questions de transfert et de localisation des données. Ce n'est pas une conformité automatique, mais c'est un atout majeur pour les données sensibles. Des modèles open source européens comme Mistral renforcent encore l'angle souveraineté."
  - question: "À partir de quand l'auto-hébergement est-il rentable ?"
    answer: "Selon une étude de 2025, un modèle d'environ 30 milliards de paramètres sur un GPU grand public à 2 000 $ devient rentable face aux API en quelques mois dès qu'on traite du volume. Les seuils indicatifs : moins de 10 millions de tokens par mois, l'API reste plus avantageuse ; entre 10 et 50 millions, l'auto-hébergement devient intéressant ; au-delà, il s'impose."
  - question: "Peut-on faire un RAG 100 % local ?"
    answer: "Oui, et c'est le cas d'usage le plus courant de l'IA locale en entreprise. On combine un modèle d'embeddings local (BGE, E5) pour la recherche, une base vectorielle auto-hébergée (Qdrant ou pgvector) et un SLM local pour la génération. Aucune donnée ne quitte votre infrastructure, ce qui en fait souvent la seule architecture acceptable pour des documents sensibles."
---

## IA locale : pourquoi et comment faire tourner un SLM chez soi

Faire tourner un SLM en local, c'est exécuter un modèle de langage sur votre propre machine ou votre propre serveur, sans passer par une API externe. C'est devenu réaliste parce que les petits modèles sont assez bons et assez légers pour ça, et c'est souvent le bon choix pour trois raisons : la confidentialité, le coût, et la latence.

Concrètement, vos données ne quittent jamais votre infrastructure, vous ne payez plus au token, et le modèle répond vite, même hors ligne. Pour une entreprise qui manipule des données sensibles ou qui traite du volume, ces trois arguments pèsent lourd.

<!-- more -->

Dans cet article, je couvre le pourquoi (confidentialité, RGPD, coût), les outils pour exécuter un modèle en local, comment démarrer concrètement, la quantification, le matériel nécessaire, le cas du RAG souverain, et les situations où l'auto-hébergement n'a pas de sens. Si vous voulez d'abord poser les bases, commencez par mon article sur [ce qu'est un SLM](c-est-quoi-un-slm.md).

## Pourquoi faire tourner un SLM en local ?

L'IA locale répond à des contraintes que le cloud ne lève pas. Voici les quatre arguments qui reviennent en mission.

- **La confidentialité et le RGPD.** Envoyer des documents sensibles à une API externe pose des questions de transfert et de localisation des données. Un modèle local garde tout sur votre infrastructure : les données ne sortent pas. Pour les secteurs régulés (santé, juridique, RH, défense), ce seul point fait souvent pencher la balance.
- **La souveraineté.** Au-delà du RGPD, certaines organisations veulent ne dépendre d'aucun fournisseur étranger. Des modèles open source européens comme ceux de Mistral permettent de monter une stack entièrement maîtrisée.
- **Le coût à l'échelle.** Au token, les API restent imbattables sur de petits volumes. Mais dès qu'on traite du volume, l'auto-hébergement d'un petit modèle finit par coûter moins cher. J'y reviens plus bas avec des chiffres.
- **La latence et le hors-ligne.** Un modèle local n'a pas d'aller-retour réseau. Il répond plus vite et fonctionne sans connexion, ce qui ouvre l'embarqué et les environnements isolés.

C'est exactement le genre de contraintes qui rendent un RAG sur LLM local incontournable pour les données sensibles, un point que j'aborde aussi dans [long context vs RAG](long-context-vs-rag-quand-utiliser.md).

## Les outils pour faire tourner un modèle en local

L'écosystème a énormément mûri. Il faut surtout distinguer les outils de poste de travail des outils de production.

Pour **prototyper et développer** :

- **Ollama** : l'outil le plus simple pour lancer un modèle en local. Une commande, et le modèle tourne. Parfait pour tester et pour les petits usages.
- **LM Studio** : une interface graphique de bureau pour télécharger et discuter avec des modèles locaux, sans toucher au terminal.
- **llama.cpp** : le moteur d'inférence en C/C++ qui fait tourner les modèles au format GGUF, y compris sur CPU ou sur Mac. C'est la brique sous-jacente de beaucoup d'outils grand public.

Pour la **production** :

- **vLLM** : un moteur de service à haut débit. Grâce à sa gestion mémoire (PagedAttention), il sert beaucoup de requêtes en parallèle avec un bon rendement. C'est le choix quand il faut tenir la charge.
- **Text Generation Inference (TGI)** : la solution de service de Hugging Face, pensée pour déployer des modèles en production.

La règle simple : Ollama ou LM Studio pour commencer et tester, vLLM ou TGI quand vous passez à l'échelle et que le débit compte.

## Du modèle local à votre code : l'API compatible OpenAI

Avec Ollama, on récupère et on lance un modèle en deux commandes : l'installation de l'outil, puis `ollama run qwen3`, qui télécharge la version quantifiée et démarre le modèle. On peut alors lui parler dans le terminal.

L'intérêt pour une équipe technique tient à un détail d'implémentation : Ollama, vLLM et TGI exposent tous une API compatible avec celle d'OpenAI. Les routes, le format des requêtes et celui des réponses sont identiques. Un code qui appelle déjà GPT ou Claude continue donc de fonctionner en changeant deux choses, l'URL du serveur et le nom du modèle. Le même appel `chat.completions.create(...)` interroge alors votre modèle local. Brancher un prototype sur un modèle local relève de la configuration, pas de la réécriture.

C'est aussi ce qui simplifie le passage en production : on prototype avec Ollama sur son poste, puis on remplace le serveur par vLLM ou TGI, qui exposent la même interface mais encaissent la charge. Le code applicatif ne change pas, seule la brique qui sert le modèle change.

## La quantification : faire tenir un modèle sur une machine modeste

La quantification est ce qui rend l'IA locale accessible : sans elle, la plupart des petits modèles resteraient trop lourds pour une machine ordinaire.

La quantification réduit la précision des paramètres, par exemple de 16 bits à 4 bits. On divise ainsi la taille du modèle et on accélère l'inférence, avec une perte de qualité en général faible. Le format le plus répandu côté local est **GGUF**, utilisé par llama.cpp, avec des variantes comme **Q4_K_M** qui offrent un bon compromis taille/qualité. Côté GPU, on croise aussi les méthodes **AWQ** et **GPTQ**.

Le rapport technique de Microsoft sur [Phi-3](https://arxiv.org/abs/2404.14219) en donne une mesure parlante : un modèle de 3,8 milliards de paramètres, une fois quantifié en 4 bits, tient dans environ 1,8 Go et tourne sur un iPhone. Un modèle qui demandait un serveur se retrouve à tourner sur un téléphone ou un ordinateur portable.

## Quel matériel pour quel modèle ?

La question revient toujours : « il me faut quoi comme machine ? ». Voici les ordres de grandeur, en gardant en tête que la quantification en 4 bits est supposée.

| Taille du modèle | Ce qu'il faut | Exemples de modèles |
|---|---|---|
| 1 à 4 milliards | un ordinateur portable récent, parfois le CPU suffit | Llama 3.2 1B/3B, Qwen3 1,7B et 4B, SmolLM3 3B, Phi-4-mini (3,8B), Gemma 4 E2B/E4B |
| 7 à 9 milliards | environ 6 à 8 Go de mémoire vidéo, ou un Mac Apple Silicon | Qwen3 8B, Ministral 3 8B |
| 10 milliards et plus | un vrai GPU (type RTX 4090/5090) | au-delà du périmètre SLM |

Pour estimer rapidement la mémoire : en 4 bits, comptez environ un demi-gigaoctet par milliard de paramètres, plus une marge pour le contexte de la conversation. Un modèle de 7 milliards tient donc autour de 4 à 5 Go de mémoire vidéo, ce qui passe sur la plupart des GPU grand public récents.

Les Mac à mémoire unifiée sont aussi un bon support pour l'inférence locale : le modèle y partage la mémoire entre le CPU et le GPU, ce qui permet de charger des modèles plus gros qu'avec une carte graphique d'entrée de gamme. Et un GPU grand public récent suffit pour la plupart des SLM, sans matériel de datacenter. Pour le détail des familles de modèles et de leurs tailles, voir mon article sur [ce qu'est un SLM](c-est-quoi-un-slm.md).

## Le RAG 100 % local, sur données confidentielles

S'il fallait donner une seule raison de faire tourner un SLM en local en entreprise, ce serait le RAG sur données confidentielles. C'est le cas qui revient le plus souvent en mission.

Un [RAG](mais-que-es-le-rag.md) classique envoie vos documents internes à une API externe au moment de générer la réponse. Pour des contrats, des dossiers RH ou des données médicales, c'est souvent rédhibitoire. La version locale garde tout sur votre infrastructure : un modèle d'embeddings local pour indexer et chercher (un modèle BGE ou E5, par exemple), une base vectorielle auto-hébergée (Qdrant, ou pgvector directement dans votre PostgreSQL), et un SLM local pour la génération. À aucun moment une donnée ne sort.

C'est un peu plus de travail qu'un RAG branché sur une API, mais pour beaucoup de secteurs régulés, c'est la seule architecture acceptable. Et un SLM y suffit souvent, parce que la tâche est cadrée : répondre à partir de passages qu'on lui fournit. Quand le raisonnement multi-documents devient lourd, on garde la possibilité d'escalader vers un gros modèle, comme je l'explique dans [SLM vs LLM](slm-vs-llm-quand-choisir.md).

## À partir de quand l'auto-hébergement est-il rentable ?

C'est la question qui décide vraiment. Et la réponse dépend du volume.

Une étude de 2025 sur le coût du déploiement on-premise ([arXiv 2509.18101](https://arxiv.org/abs/2509.18101)) chiffre le seuil de rentabilité face aux API. Un modèle d'environ 30 milliards de paramètres, sur un GPU grand public à 2 000 $, devient rentable en moins de 3 mois dès qu'il y a du volume. Plus le modèle est petit, plus ce retour sur investissement est rapide.

Les seuils de volume sont un bon repère :

- **moins de 10 millions de tokens par mois** : l'API reste plus avantageuse, le matériel tournerait à vide ;
- **entre 10 et 50 millions** : l'auto-hébergement devient intéressant ;
- **au-delà de 50 millions** : il s'impose nettement.

Autrement dit, l'IA locale n'est pas qu'une question de principe sur la confidentialité, c'est aussi un calcul économique qui bascule avec le volume. C'est le même raisonnement que celui que je tiens sur les autres leviers de coût comme le [prompt caching](prompt-caching-reduire-cout-llm.md).

## Quand il ne faut pas auto-héberger

Soyons honnête : l'IA locale n'est pas toujours le bon choix, et la vendre comme une évidence serait malhonnête.

Restez sur une API quand :

- **le volume est faible.** Sous quelques millions de tokens par mois, payer un GPU qui tourne à vide coûte plus cher que l'API.
- **vous avez besoin de raisonnement de pointe ou de très long contexte.** Là, les gros modèles cloud restent devant, et aucun SLM local ne les remplace.
- **vous n'avez pas les compétences ops.** Héberger, monitorer, mettre à jour et sécuriser un modèle en production demande du savoir-faire. Sans équipe pour le porter, la simplicité d'une API a de la valeur.

Il existe aussi un entre-deux utile entre l'API publique et l'on-premise complet : le cloud souverain. Héberger un modèle open source chez un fournisseur européen comme OVHcloud ou Scaleway garde vos données dans l'Union sans avoir à gérer le matériel vous-même. C'est souvent le bon compromis quand la vraie contrainte est la localisation des données, pas le contrôle physique de la machine.

Le bon réflexe reste le même que partout ailleurs : partir du besoin réel, mesurer, et choisir l'outil le plus simple qui le résout. L'IA locale est une option solide quand la confidentialité ou le volume la justifient, pas une fin en soi.

## FAQ : questions fréquentes sur l'IA locale

**Pourquoi faire tourner un SLM en local ?**
Pour la confidentialité (les données ne quittent pas votre infrastructure), le coût (moins cher que les API à fort volume) et la latence (réponse rapide, fonctionnement hors ligne). C'est surtout pertinent pour les données sensibles et les secteurs régulés.

**Quel outil pour exécuter un LLM en local ?**
Ollama et LM Studio pour le poste de travail et le prototypage, llama.cpp comme moteur sous-jacent (format GGUF, même sur CPU ou Mac), et vLLM ou TGI pour la production à fort débit.

**Quelle config faut-il pour faire tourner un SLM ?**
Un modèle de 1 à 3 milliards de paramètres tourne sur un portable récent. Un 7 à 8 milliards en 4 bits demande environ 6 à 8 Go de mémoire vidéo ou un Mac Apple Silicon. Au-delà, il faut un vrai GPU.

**C'est quoi la quantification (GGUF, 4 bits) ?**
Elle réduit la précision des paramètres pour diviser la taille du modèle et accélérer l'inférence. GGUF est le format le plus répandu pour les modèles quantifiés exécutés avec llama.cpp, avec des variantes comme Q4_K_M. La perte de qualité est en général faible.

**L'IA locale est-elle conforme au RGPD ?**
Faire tourner un modèle sur votre infrastructure évite d'envoyer des données personnelles à une API externe, ce qui lève une grande partie des questions de transfert et de localisation. Ce n'est pas une conformité automatique, mais un atout majeur, renforcé par des modèles européens comme Mistral.

**À partir de quand l'auto-hébergement est-il rentable ?**
Selon une étude de 2025, un modèle d'environ 30 milliards de paramètres sur un GPU à 2 000 $ devient rentable en quelques mois dès qu'il y a du volume. En dessous de 10 millions de tokens par mois, l'API reste préférable ; au-delà de 50 millions, l'auto-hébergement s'impose.

**Peut-on faire un RAG 100 % local ?**
Oui, c'est même le cas d'usage le plus courant de l'IA locale en entreprise. On combine un modèle d'embeddings local (BGE, E5), une base vectorielle auto-hébergée (Qdrant ou pgvector) et un SLM local pour la génération. Aucune donnée ne quitte votre infrastructure, ce qui en fait souvent la seule architecture acceptable pour des données sensibles.

## Pour aller plus loin

- **[C'est quoi un SLM (Small Language Model) ?](c-est-quoi-un-slm.md)** : la définition, les modèles récents et pourquoi le sujet compte en 2026
- **[SLM vs LLM : quand choisir un petit modèle ?](slm-vs-llm-quand-choisir.md)** : la grille de décision entre petit et gros modèle
- **[Comment entraîner un SLM ?](entrainer-un-slm.md)** : finetuner ou distiller un modèle avant de le déployer en local
- **[Prompt caching : réduire le coût d'un LLM](prompt-caching-reduire-cout-llm.md)** : un autre levier de coût, complémentaire de l'auto-hébergement

Si mes articles vous intéressent, que vous avez des questions ou simplement envie de discuter de vos propres défis liés à l'IA, n'hésitez pas à m'écrire à [anas@tensoria.fr](mailto:anas@tensoria.fr), j'adore échanger sur ces sujets !

Vous voulez déployer une IA sur votre propre infrastructure pour garder vos données ? Découvrez mon activité de conseil sur [tensoria.fr](https://tensoria.fr).

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
