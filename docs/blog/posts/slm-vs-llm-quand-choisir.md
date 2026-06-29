---
title: "SLM vs LLM : quand choisir un petit modèle ?"
slug: slm-vs-llm-quand-choisir
description: "SLM vs LLM : coûts comparés, précision sur tâches spécialisées et grille de décision concrète pour choisir entre un petit et un grand modèle de langage en 2026."
categories:
  - "Blog"
  - "IA"
tags:
  - "SLM"
  - "Small Language Model"
  - "LLM"
  - "Intelligence Artificielle"
date: 2026-06-23
comments: true
authors:
  - Anas
pin: false
math: false
mermaid: false
faqs:
  - question: "Quelle est la différence entre un SLM et un LLM ?"
    answer: "C'est une question de taille et de compromis. Un LLM (Large Language Model) compte des dizaines voire des centaines de milliards de paramètres et vise la polyvalence, au prix d'un coût et d'une latence élevés. Un SLM (Small Language Model) va de quelques dizaines de millions à environ 10 milliards de paramètres et vise l'efficacité sur des tâches ciblées. Le SLM sait moins de choses mais coûte beaucoup moins cher et répond plus vite."
  - question: "Un SLM est-il vraiment moins cher qu'un LLM ?"
    answer: "Oui, et l'écart est large. Sur une même famille, GPT-4o coûte environ 10 $ le million de tokens en sortie contre 0,60 $ pour GPT-4o-mini, soit près de 17 fois moins. Un petit modèle open source auto-hébergé descend encore plus bas dès qu'on traite du volume. Selon une étude de 2025, un modèle d'environ 30 milliards de paramètres sur un GPU grand public à 2 000 $ devient rentable face aux API en quelques mois à peine."
  - question: "Un petit modèle peut-il être plus précis qu'un gros ?"
    answer: "Sur une tâche précise, oui. Plusieurs études montrent qu'un petit modèle finetuné égale ou dépasse GPT-4 sur de la classification, de l'extraction ou de la détection d'intention. Sur une tâche de prise de position, un modèle DeBERTa finetuné atteint 0,94 de F1 contre 0,58 pour GPT-4 en zero-shot. La spécialisation bat la taille quand le périmètre est étroit."
  - question: "Quand faut-il choisir un LLM plutôt qu'un SLM ?"
    answer: "Quand la tâche demande du raisonnement ouvert, une large culture générale, de la généralisation zero-shot ou des enchaînements complexes à plusieurs étapes. Les petits modèles s'effondrent sur ces capacités qui n'apparaissent qu'à grande échelle. Le LLM est aussi le bon choix quand les tâches sont très variées ou changent vite, car finetuner un petit modèle par cas ne serait pas rentable."
  - question: "Peut-on combiner un SLM et un LLM ?"
    answer: "C'est souvent la meilleure réponse en production. On fait gérer le volume de tâches simples par un SLM et on n'escalade vers un LLM que les cas difficiles, via une cascade pilotée par un score de confiance. La recherche FrugalGPT montre qu'une telle cascade peut égaler GPT-4 avec jusqu'à 98 % d'économie. NVIDIA estime que 40 à 70 % des appels d'un système d'agents pourraient être confiés à des petits modèles."
  - question: "Combien d'exemples faut-il pour spécialiser un SLM ?"
    answer: "Beaucoup moins qu'on ne croit. Une étude de classification montre que les performances saturent souvent autour de 200 à 500 exemples annotés. C'est l'un des grands intérêts du petit modèle finetuné : il atteint un bon niveau sur une tâche précise avec un jeu de données modeste, là où entraîner ou finetuner un gros modèle demande bien plus."
---

## SLM vs LLM : quand choisir un petit modèle ?

Le choix entre un SLM et un LLM se résume à une question : votre tâche est-elle précise et répétitive, ou large et imprévisible ? Sur une tâche cadrée comme classer, extraire ou router, un petit modèle (SLM) spécialisé suffit souvent, coûte de 15 à 50 fois moins cher et répond plus vite. Sur du raisonnement ouvert, de la culture générale ou des tâches très variées, un gros modèle (LLM) reste devant.

Et en production, la vraie réponse est souvent : les deux. Le petit modèle absorbe le volume, le gros intervient sur les cas difficiles.

C'est tout le sujet de cet article. Plutôt que de répéter ce qu'est un petit modèle, sujet que je traite dans mon article sur [ce qu'est un SLM et pourquoi en 2026](c-est-quoi-un-slm.md), je vais ici poser une grille de décision chiffrée pour trancher entre les deux sur un projet réel.

<!-- more -->

## SLM ou LLM : la différence en deux mots

La différence entre un SLM et un LLM n'est pas une question de nature, mais de compromis. Les deux sont des modèles de langage qui prédisent le mot suivant. Ce qui change, c'est l'échelle et ce qu'on accepte de sacrifier.

Un LLM mise sur la polyvalence et la culture générale, au prix d'un coût et d'une latence élevés. Un SLM mise sur l'efficacité et la spécialisation, au prix d'une culture plus limitée. Là où NVIDIA, dans son papier [*Small Language Models are the Future of Agentic AI*](https://arxiv.org/abs/2506.02153), place la frontière autour de 10 milliards de paramètres, je tire en pratique la définition plus bas, vers le sous-milliard, parce que c'est là qu'un modèle tourne vraiment n'importe où.

Le reste de l'article compare les deux sur les seuls critères qui comptent quand on décide : le coût, la précision, les limites, et la façon de les combiner.

## Coût, latence, confidentialité : les arguments du petit modèle

C'est sur le coût que l'écart est le plus brutal, et c'est souvent ce qui déclenche la réflexion.

À périmètre égal, un petit modèle coûte un ordre de grandeur de moins. Chez OpenAI, GPT-4o est facturé autour de 10 $ le million de tokens en sortie, contre 0,60 $ pour GPT-4o-mini : près de 17 fois moins cher, même famille, même fournisseur. Un petit modèle open source servi par un acteur comme Together tourne autour de 0,18 $ le million de tokens, soit plusieurs dizaines de fois moins qu'un gros modèle propriétaire. NVIDIA avance de son côté que servir un modèle de 7 milliards de paramètres revient de 10 à 30 fois moins cher qu'un modèle de 70 à 175 milliards. C'est l'estimation d'un papier de position, à prendre comme un ordre de grandeur, mais il va dans le même sens.

Et si on auto-héberge, l'écart bascule encore plus vite dès qu'il y a du volume. Une étude de 2025 sur le coût du déploiement on-premise ([arXiv 2509.18101](https://arxiv.org/abs/2509.18101)) chiffre le seuil de rentabilité face aux API : un modèle d'environ 30 milliards de paramètres, sur un GPU grand public à 2 000 $, devient rentable en moins de 3 mois. Un modèle de 70 à 120 milliards, qui demande deux cartes A100 à 30 000 $, met lui de 4 à 34 mois. La règle est simple : plus le modèle est petit, plus le retour sur investissement de l'auto-hébergement est rapide.

Les deux autres arguments du petit modèle suivent la même logique :

- **La latence.** Un petit modèle répond plus vite. Un Llama 8B servi sur du matériel spécialisé atteint près de 877 tokens par seconde (mesure Artificial Analysis), et un Phi-3 mini tourne sur un iPhone à plus de 12 tokens par seconde, hors ligne. Pour une fonction appelée des milliers de fois par jour, l'écart est décisif.
- **La confidentialité.** Un SLM tient sur votre infrastructure. Les données ne partent pas vers une API externe, ce qui lève d'un coup une bonne partie des questions de RGPD et de souveraineté sur les documents sensibles. Quand ces données sont critiques, on déploie le modèle en [local, sur sa propre infrastructure](ia-locale-slm-on-premise.md).

## Sur une tâche précise, le petit modèle peut gagner

C'est le point contre-intuitif, et le plus important : sur une tâche étroite et bien définie, un petit modèle spécialisé n'égale pas seulement un gros modèle, il le dépasse souvent.

Le projet LoRA Land de Predibase a finetuné 310 petits modèles (base Mistral 7B pour la plupart) sur des tâches précises. Résultat : en moyenne, ces modèles [dépassent leur modèle de base de 34 points et GPT-4 de 10 points](https://arxiv.org/abs/2405.00732) sur leurs tâches respectives. À condition de bien lire ce chiffre : c'est vrai sur des tâches étroites et finetunées, pas en généraliste.

Sur de la classification de texte, l'écart est parfois spectaculaire. Une étude comparant des petits modèles finetunés à GPT-4 en zero-shot ([arXiv 2406.08660](https://arxiv.org/html/2406.08660v2)) mesure, sur une tâche de prise de position, 0,94 de F1 pour un DeBERTa finetuné contre 0,58 pour GPT-4. Sur de la détection d'émotion dans du texte politique, 0,89 d'accuracy contre 0,20. Et surtout, ces performances saturent souvent autour de 200 à 500 exemples annotés : on atteint un très bon niveau avec un jeu de données modeste.

La distillation va dans le même sens depuis longtemps. DistilBERT conserve [97 % des performances de BERT en étant 40 % plus petit et 60 % plus rapide](https://arxiv.org/abs/1910.01108). Pour aller plus loin sur le sujet de la spécialisation, j'ai écrit un guide complet sur [quand finetuner plutôt qu'utiliser un RAG](entrainement-finetuning-rag-modele-ia.md).

## Là où le LLM reste clairement devant

Soyons clairs, parce que l'argument précédent est souvent mal compris : un petit modèle gagne sur une tâche précise, pas en général. Dès qu'on sort du cadre, le gros modèle reprend l'avantage, et l'écart est net.

Les travaux sur les capacités émergentes des modèles le montrent bien. En dessous d'environ 10 milliards de paramètres, les modèles obtiennent des résultats proches du hasard sur un benchmark de culture générale comme MMLU. Sur des problèmes de maths en plusieurs étapes (GSM8K), les petits modèles plafonnent près de zéro là où un très gros modèle, avec du raisonnement pas à pas, dépasse les 50 %. Certaines capacités, comme le raisonnement en chaîne, la généralisation zero-shot ou les enchaînements complexes, n'apparaissent qu'à grande échelle.

Il faut nuancer, parce que les petits modèles récents comblent une partie de l'écart : Phi-3 mini atteint tout de même 69 % sur MMLU. Mais le principe tient : pour du raisonnement ouvert, une large culture générale, ou des tâches diverses et changeantes, le LLM reste le bon outil. Finetuner un petit modèle par cas n'aurait alors aucun sens.

Un LLM est aussi le choix pragmatique quand le volume est faible (l'API coûte moins cher qu'un GPU qui tourne à vide) ou quand on veut aller vite sans monter une chaîne d'entraînement et d'évaluation.

## En production, la vraie réponse est souvent : les deux

Dans la pratique, opposer SLM et LLM est un faux débat. Les systèmes les plus efficaces font travailler les deux ensemble, en envoyant chaque requête au modèle dont elle a besoin.

Le motif de référence est la cascade : un petit modèle traite la requête en premier, et on n'escalade vers un gros modèle que lorsque la confiance est trop basse. La recherche FrugalGPT de Stanford ([arXiv 2305.05176](https://arxiv.org/abs/2305.05176)) montre qu'une telle cascade peut égaler la performance de GPT-4 avec jusqu'à 98 % d'économie, ou améliorer la précision à coût égal.

Sur les systèmes d'agents, le même raisonnement s'applique. NVIDIA estime, sur plusieurs systèmes analysés, qu'entre 40 et 70 % des appels au gros modèle pourraient être confiés à des petits modèles spécialisés. Ce sont leurs estimations, sur leurs cas, mais l'idée est juste : on envoie par défaut tout sur le gros modèle, alors qu'une bonne partie du trafic ne le justifie pas. C'est la même logique de routage que je décris pour le coût dans mon article sur le [prompt caching](prompt-caching-reduire-cout-llm.md).

## Quel modèle pour quel cas d'usage

Au-delà des critères, voici ce que ça donne sur des tâches réelles. La logique ne change pas : plus la tâche est fermée et répétitive, plus le SLM est pertinent ; plus elle demande de comprendre, croiser et rédiger, plus le LLM devient indispensable.

| Cas d'usage | Bon choix | Pourquoi |
|---|---|---|
| Classer ou router des demandes (support, tickets) | SLM | tâche fermée, fort volume, latence faible |
| Extraire des infos structurées (dates, montants, entités) | SLM finetuné | périmètre étroit, peu d'exemples suffisent |
| Détecter des données personnelles, modérer, taguer | SLM | déterministe, tourne en local |
| Traduire ou reformuler des textes courts | SLM | tâche bien définie |
| Répondre sur une base documentaire interne (RAG) | LLM (+ RAG) | synthèse et raisonnement multi-documents |
| Assistant conversationnel généraliste | LLM | terrain ouvert, large culture générale |
| Générer ou relire du code | LLM | raisonnement et contexte large |
| Analyse complexe, croisement de sources | LLM | enchaînements à plusieurs étapes |
| IA embarquée, hors ligne, données sensibles | SLM | confidentialité, pas de cloud |

### Le cas du RAG

Le [RAG](mais-que-es-le-rag.md) mérite qu'on s'y arrête, parce que c'est là qu'on se trompe le plus souvent de modèle. On va chercher les passages pertinents dans vos documents, puis on demande au modèle de rédiger une réponse à partir de ces passages. Cette étape de synthèse, surtout quand elle croise plusieurs documents et doit citer ses sources sans inventer, demande un modèle capable. Un petit modèle décroche vite sur le raisonnement multi-documents et invente plus facilement dès qu'il sort de son périmètre.

Ça ne veut pas dire qu'un SLM n'a aucune place dans un RAG. Il peut router la question, la reformuler, classer son intention ou filtrer les résultats, autant d'étapes où il est rapide et bon marché. Mais la génération finale sur vos données, je la confie à un bon LLM. C'est encore un système hybride : petits modèles pour la mécanique, gros modèle pour la réponse.

### La modération, un cas d'école

À l'inverse du RAG, la modération de contenu est le cas type où un petit modèle suffit, et plusieurs grandes plateformes le prouvent en production :

- **Roblox** fait tourner un classifieur de sécurité vocale d'environ 100 millions de paramètres (basé sur WavLM, distillé d'un modèle plus gros) pour repérer les propos toxiques dans le chat audio, en 8 langues, entraîné sur plus de 100 000 heures d'audio. Le modèle est même publié en open source ([model card Roblox](https://huggingface.co/Roblox/voice-safety-classifier-v2)).
- **Meta** publie Llama Guard 3 en version 1 milliard de paramètres, distillée et élaguée à partir du modèle 8B, pour filtrer les entrées et sorties d'un LLM, pensée pour tenir sur mobile ([model card Meta](https://huggingface.co/meta-llama/Llama-Guard-3-1B)).
- **Google** propose ShieldGemma en version 2 milliards de paramètres, bâtie sur Gemma, pour classer un texte selon des catégories à risque ([model card Google](https://huggingface.co/google/shieldgemma-2b)).
- **Bumble** a ouvert le code de Private Detector, un petit classifieur d'images (basé sur EfficientNet) qui détecte l'envoi de photos intimes non sollicitées ([GitHub Bumble](https://github.com/bumble-tech/private-detector)).
- **Unitary** maintient Detoxify (toxic-bert), un classifieur de toxicité d'environ 110 millions de paramètres, auto-hébergeable, devenu un standard ([GitHub Unitary](https://github.com/unitaryai/detoxify)).

Soyons honnête sur la nuance : certaines API de modération reposent encore sur de gros modèles (celle d'OpenAI tourne sur GPT-4o, celle de Mistral sur un modèle de 8 milliards de paramètres). Mais les systèmes qui encaissent les plus gros volumes misent sur des modèles spécialisés et petits, parce que la modération est une tâche fermée, massive et sensible à la latence. Autrement dit, le terrain de jeu du SLM.

### Par secteur

La même logique se décline secteur par secteur :

- **Support client** : un SLM classe et route les demandes vers les bons services
- **Assurance** : un SLM trie et catégorise les déclarations ; la [rédaction de rapports de sinistre sur dossier](integration-ia-rapports-sinistre-assurance.md) repose sur un LLM qui synthétise les pièces.
- **BTP** : la [rédaction d'appels d'offres](cas-usage-rag-redaction-appels-offres-btp.md) croise normes et historique projets, un vrai travail de raisonnement pour un LLM.
- **Juridique** : extraire des clauses, un SLM le fait, parcontre croiser des contrats pour repérer des contradictions, c'est un LLM qui peut faire mieux.
- **Santé** : coder des actes ou extraire des données reste possible en local avec un SLM, pour la confidentialité, mais le raisonnement clinique demande un LLM.

## Ma grille de décision SLM vs LLM

Voici comment je tranche concrètement sur un projet. La grille tient sur quelques critères :

| Critère | Penche vers un SLM | Penche vers un LLM |
|---|---|---|
| Nature de la tâche | précise, répétitive | large, variée, imprévisible |
| Coût par token | 15 à 50 fois moins cher | élevé |
| Latence / temps réel | faible, possible en local | dépend de l'API |
| Confidentialité des données | tourne sur votre infra | données envoyées à une API |
| Raisonnement ouvert, culture générale | limité | fort |
| Données pour spécialiser | 200 à 500 exemples suffisent | aucune (zero-shot) |

La règle que j'applique : commencer par le plus petit modèle qui fait le travail, mesurer, et ne monter en taille que si c'est nécessaire.

Un exemple concret. Sur un problème de classification d'intentions (ranger des messages dans un petit nombre de catégories), le réflexe à la mode est de sortir un gros LLM par API. Mon premier réflexe est l'inverse : tester un petit modèle open source qui tient en production, avec du prompt engineering, quelques exemples et une sortie structurée, puis mesurer sur un jeu de test gardé de côté. Dans bien des cas, ça suffit.

Une nuance technique qui compte sur ce genre de tâche : la sortie structurée (structured output) garantit un format valide, mais le constrained decoding force toujours le modèle à choisir un label, ce qui masque l'incertitude. Or une étude ([arXiv 2408.02442](https://arxiv.org/pdf/2408.02442)) montre que trop contraindre la génération peut dégrader la qualité du raisonnement. Je préfère donc contraindre le format sans forcer la décision : récupérer la vraisemblance de chaque label, et utiliser le score top-1 et l'écart entre le top-1 et le top-2 comme signal de confiance. Si la marge est faible, je ne comptabilise pas l'événement plutôt que de polluer les métriques métier avec un faux label. Mieux vaut une réponse "incertain" qu'une fausse certitude.

C'est tout le bon réflexe SLM vs LLM : la question n'est jamais "quel est le modèle le plus impressionnant", mais "quel est le plus petit modèle qui résout mon problème de façon fiable".

## FAQ : questions fréquentes sur le choix SLM vs LLM

**Quelle est la différence entre un SLM et un LLM ?**
C'est une question de taille et de compromis. Un LLM compte des dizaines voire des centaines de milliards de paramètres et vise la polyvalence, au prix d'un coût élevé. Un SLM va de quelques dizaines de millions à environ 10 milliards de paramètres et vise l'efficacité sur des tâches ciblées, moins cher et plus rapide.

**Un SLM est-il vraiment moins cher qu'un LLM ?**
Oui, l'écart va de 15 à 50 fois selon les cas. GPT-4o coûte environ 10 $ le million de tokens en sortie contre 0,60 $ pour GPT-4o-mini. Et en auto-hébergeant, un modèle d'environ 30 milliards de paramètres sur un GPU à 2 000 $ devient rentable face aux API en quelques mois dès qu'il y a du volume.

**Un petit modèle peut-il être plus précis qu'un gros ?**
Sur une tâche précise, oui. Des études montrent qu'un petit modèle finetuné égale ou dépasse GPT-4 sur de la classification ou de l'extraction. Sur une tâche de prise de position, un DeBERTa finetuné atteint 0,94 de F1 contre 0,58 pour GPT-4 en zero-shot. La spécialisation bat la taille quand le périmètre est étroit.

**Quand faut-il choisir un LLM plutôt qu'un SLM ?**
Quand la tâche demande du raisonnement ouvert, une large culture générale, de la généralisation zero-shot ou des enchaînements complexes. Le LLM est aussi le bon choix quand les tâches sont diverses ou changent vite, ou quand le volume est trop faible pour rentabiliser une infrastructure dédiée.

**Peut-on combiner un SLM et un LLM ?**
Oui, et c'est souvent la meilleure réponse. On fait gérer le volume par un SLM et on escalade les cas difficiles vers un LLM via une cascade pilotée par la confiance. FrugalGPT montre qu'une telle cascade peut égaler GPT-4 avec jusqu'à 98 % d'économie.

**Combien d'exemples faut-il pour spécialiser un SLM ?**
Souvent 200 à 500 exemples annotés suffisent : c'est là que les performances saturent sur beaucoup de tâches de classification. C'est l'un des grands intérêts du petit modèle finetuné face à un gros modèle.

## Pour aller plus loin

- **[C'est quoi un SLM (Small Language Model) ?](c-est-quoi-un-slm.md)** : la définition, les exemples de modèles récents et pourquoi le sujet compte en 2026
- **[Comment entraîner un SLM ?](entrainer-un-slm.md)** : fine-tuning, LoRA/QLoRA et distillation une fois la décision prise
- **[IA locale : faire tourner un SLM en local](ia-locale-slm-on-premise.md)** : déployer un petit modèle on-premise pour la confidentialité et le coût
- **[RAG, finetuning ou entraînement : que choisir ?](entrainement-finetuning-rag-modele-ia.md)** : l'arbre de décision pour spécialiser un modèle sans gaspiller son budget
- **[Prompt caching : réduire le coût d'un LLM](prompt-caching-reduire-cout-llm.md)** : l'autre grand levier de coût, complémentaire du choix de la taille du modèle
- **[C'est quoi un agent IA ?](c-est-quoi-un-agent-ia.md)** : les systèmes où le routage entre petit et gros modèle prend tout son sens

Si mes articles vous intéressent, que vous avez des questions ou simplement envie de discuter de vos propres défis liés à l'IA, n'hésitez pas à m'écrire à [anas@tensoria.fr](mailto:anas@tensoria.fr), j'adore échanger sur ces sujets !

Vous hésitez entre un petit et un gros modèle pour votre cas d'usage ? Découvrez mon activité de conseil sur [tensoria.fr](https://tensoria.fr).

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
