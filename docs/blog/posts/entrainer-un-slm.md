---
title: "Comment entraîner un SLM (Small Language Model) ?"
slug: entrainer-un-slm-fine-tuning-distillation
description: "Comment entraîner un SLM : fine-tuning, LoRA/QLoRA, distillation ou from scratch. Les méthodes, le coût réel et la démarche pragmatique étape par étape."
categories:
  - "Blog"
  - "IA"
tags:
  - "SLM"
  - "Small Language Model"
  - "Finetuning"
  - "LoRA"
date: 2026-06-29
comments: true
authors:
  - Anas
pin: false
math: false
mermaid: false
faqs:
  - question: "Faut-il entraîner un SLM ou utiliser un modèle existant ?"
    answer: "Dans la grande majorité des cas, commencez par un modèle existant. Avant d'entraîner quoi que ce soit, testez ce qu'un bon petit modèle open source donne déjà avec du prompt engineering, des exemples (few-shot) et une sortie structurée, puis mesurez. On ne passe à l'entraînement que si les performances mesurées ne suffisent pas. Entraîner un SLM est utile pour un format de sortie très strict, un vocabulaire métier pointu ou pour faire baisser le coût d'inférence, pas par défaut."
  - question: "Quelle est la différence entre fine-tuning et distillation ?"
    answer: "Le fine-tuning part d'un modèle déjà entraîné et l'ajuste sur vos données pour une tâche précise. La distillation entraîne un petit modèle (l'élève) à imiter un gros modèle (le professeur), pour obtenir un modèle plus petit et plus rapide qui conserve une bonne partie des performances. Le fine-tuning sert à spécialiser, la distillation sert à compresser."
  - question: "C'est quoi LoRA et QLoRA ?"
    answer: "LoRA (Low-Rank Adaptation) est une méthode de fine-tuning qui gèle le modèle de base et n'entraîne que de petits adaptateurs ajoutés, ce qui réduit énormément la mémoire et le coût. QLoRA combine LoRA avec une quantification en 4 bits du modèle de base. Le papier QLoRA montre qu'on peut ainsi finetuner un modèle de 65 milliards de paramètres sur un seul GPU de 48 Go, là où un fine-tuning classique en demanderait plusieurs."
  - question: "Combien d'exemples faut-il pour fine-tuner un SLM ?"
    answer: "Moins qu'on ne croit. Sur beaucoup de tâches de classification, les performances saturent autour de 200 à 500 exemples annotés. Ce qui compte le plus, ce n'est pas le volume mais la qualité et la diversité des exemples, parfaitement représentatifs de votre cas d'usage."
  - question: "Combien coûte l'entraînement d'un SLM ?"
    answer: "Le calcul pur est étonnamment bas : un fine-tuning LoRA/QLoRA d'un modèle de 7 milliards de paramètres se compte en quelques heures de GPU et quelques dizaines à quelques centaines d'euros. Ce qui coûte le plus cher, c'est de construire le jeu de données, d'itérer et d'évaluer. Un entraînement depuis zéro reste réservé aux laboratoires, même si des projets récents l'ont fait pour de petits modèles avec moins de 1 000 heures de GPU."
  - question: "Quels outils pour entraîner un SLM ?"
    answer: "Pour le fine-tuning, les plus utilisés sont les bibliothèques TRL et PEFT de Hugging Face, ainsi que Unsloth et Axolotl qui simplifient et accélèrent le processus. Pour un entraînement depuis zéro de petit modèle, des frameworks comme Nanotron sont conçus pour ça. Le choix dépend surtout de votre méthode : fine-tuning d'un modèle existant ou entraînement complet."
---

## Comment entraîner un SLM, et faut-il vraiment le faire ?

Entraîner un SLM peut vouloir dire plusieurs choses très différentes : finetuner un petit modèle existant sur vos données, en distiller un à partir d'un gros, ou en entraîner un depuis zéro. Pour 95 % des entreprises, la bonne réponse est le fine-tuning, et seulement après avoir vérifié qu'un modèle existant ne suffisait pas déjà.

C'est le premier réflexe à avoir, et il fait gagner beaucoup de temps et d'argent. Avant de lancer le moindre entraînement, testez ce qu'un bon petit modèle open source donne déjà avec du prompt engineering, quelques exemples et une sortie structurée. Mesurez. On ne s'autorise à entraîner que si la mesure montre que ça ne suffit pas.

<!-- more -->

Dans cet article, je détaille les façons d'entraîner un SLM, la méthode réaliste (le fine-tuning LoRA/QLoRA), la distillation, l'entraînement depuis zéro, et la discipline d'évaluation qui sépare un modèle utilisable d'un modèle qui s'effondre en production. Si la vraie question est encore « dois-je entraîner, ou un RAG suffit-il ? », j'ai un article dédié à cet [arbitrage entre RAG, finetuning et entraînement](entrainement-finetuning-rag-modele-ia.md).

## Faut-il vraiment entraîner un SLM ?

Non, pas par défaut. L'entraînement n'est justifié que dans des cas précis, et le mauvais réflexe coûte cher.

Entraîner un SLM devient pertinent quand :

- vous avez besoin d'un **format de sortie très strict** qu'un bon prompt ne tient pas de façon fiable ;
- vous travaillez avec un **vocabulaire métier pointu** que les modèles publics ne maîtrisent pas ;
- vous voulez **faire baisser le coût et la latence** en remplaçant un gros modèle par un petit modèle spécialisé qui reste aussi bon sur votre tâche.

Hors de ces cas, un modèle existant bien utilisé suffit presque toujours. Et même quand l'entraînement se justifie, il faut garder en tête un risque réel : les modèles de base progressent vite. Un SLM finetuné aujourd'hui peut se faire rattraper dans six mois par un nouveau petit modèle public, sans aucun effort de votre part. C'est tout l'arbitrage que je détaille dans [SLM vs LLM : quand choisir un petit modèle](slm-vs-llm-quand-choisir.md).

## Les façons d'entraîner un SLM

« Entraîner » recouvre plusieurs méthodes qui n'ont ni le même coût, ni le même but. Voici les cinq que vous croiserez, de la plus lourde à la plus accessible.

| Méthode | À quoi ça sert | Coût et effort |
|---|---|---|
| Entraînement depuis zéro | créer un modèle de A à Z | très élevé, réservé aux labos |
| Pré-entraînement continu | ajouter un domaine large à un modèle existant | élevé |
| Fine-tuning supervisé (SFT) | apprendre une tâche ou un format précis | moyen |
| Distillation | compresser un gros modèle en un petit | moyen |
| Fine-tuning LoRA / QLoRA | spécialiser à moindre coût | faible, un seul GPU suffit |

Pour la mécanique de fond du pré-entraînement et du post-entraînement (SFT, RLHF), je renvoie à mon article sur [l'entraînement et le finetuning d'un modèle](entrainement-finetuning-rag-modele-ia.md). Ici, je me concentre sur ce qui concerne vraiment un petit modèle : le fine-tuning économique, la distillation, et l'entraînement depuis zéro quand il se justifie.

## Le fine-tuning LoRA / QLoRA en pratique

C'est la voie réaliste pour la quasi-totalité des projets, et de loin la plus utile à maîtriser. L'idée de départ est simple : au lieu de réentraîner les milliards de paramètres d'un modèle, on n'en touche presque aucun.

**Pourquoi on ne réentraîne pas tout le modèle.** Finetuner un modèle à l'ancienne, c'est ajuster l'intégralité de ses paramètres. Sur un modèle de 7 milliards, ça veut dire charger en mémoire le modèle, ses gradients et les états de l'optimiseur, soit facilement plus de 100 Go de VRAM. Hors de portée d'une machine normale. LoRA contourne ça entièrement.

**Ce que fait LoRA, concrètement.** LoRA (Low-Rank Adaptation) gèle le modèle de base, on n'y touche plus, et insère à côté de petites matrices entraînables, les adaptateurs. Pendant l'entraînement, seules ces matrices apprennent. Elles sont minuscules : on entraîne souvent moins de 1 % des paramètres du modèle. On a donc besoin de beaucoup moins de mémoire et de temps, tout en obtenant un modèle spécialisé sur votre tâche. À la fin, on peut soit garder l'adaptateur à part (quelques mégaoctets qu'on charge par-dessus le modèle de base), soit le fusionner dans le modèle.

**Ce qu'ajoute QLoRA.** QLoRA pousse la logique plus loin en chargeant le modèle de base en 4 bits pendant l'entraînement, au lieu de 16. On divise encore la mémoire nécessaire, sans réentraîner ce modèle de base qui reste gelé. Le papier [QLoRA](https://arxiv.org/abs/2305.14314) montre qu'on peut ainsi finetuner un modèle de 65 milliards de paramètres sur un seul GPU de 48 Go, sans perte notable de qualité. Pour un SLM de quelques milliards de paramètres, un GPU grand public suffit largement.

**Les hyperparamètres, et ceux qui comptent vraiment.** Trois réglages portent l'essentiel :

- le **rang `r`** : la taille des adaptateurs. Plus il est grand, plus le modèle peut apprendre, mais plus il risque de surapprendre. 8 à 32 couvre la plupart des cas, 16 est un bon point de départ.
- l'**`alpha`** : un facteur d'échelle appliqué aux adaptateurs. La convention courante est de le mettre au double du rang, donc 32 pour un rang de 16.
- les **modules ciblés** : sur quelles couches on branche les adaptateurs. Souvent les couches d'attention, parfois toutes les couches linéaires pour un effet plus marqué.

On y ajoute un petit learning rate et 3 à 5 epochs. Pas besoin de sur-optimiser au premier essai : l'objectif est d'abord d'apprendre la tâche et le format de sortie, puis d'ajuster en regardant où le modèle se trompe.

**Le format des données.** On présente les exemples sous forme d'instructions : une consigne (souvent un prompt système), une entrée, et la sortie attendue. Pour de la classification, la sortie est par exemple un JSON avec le label. Ce qui compte le plus, c'est la cohérence : le même format partout, des sorties propres. Un jeu de données bien fait pèse plus lourd que n'importe quel réglage d'hyperparamètre.

**Combien de données.** Moins qu'on ne croit. Sur beaucoup de tâches de classification, les performances saturent autour de 200 à 500 exemples annotés ([étude sur la classification de texte](https://arxiv.org/html/2406.08660v2)). La qualité et la diversité comptent plus que le volume. C'est aussi la leçon des modèles Phi de Microsoft, dont la performance vient avant tout de données soigneusement choisies, l'idée défendue dans leur papier [*Textbooks Are All You Need*](https://arxiv.org/abs/2306.11644). Quand les données manquent, on en génère, un sujet que je traiterai dans un article dédié à la génération de données synthétiques.

**Ce que ça coûte.** Côté calcul, c'est dérisoire : un fine-tuning LoRA/QLoRA d'un modèle de 7 milliards de paramètres se compte en quelques heures de GPU et quelques dizaines à quelques centaines d'euros. Ce qui coûte le plus cher, c'est tout le reste : construire le jeu de données, itérer dessus, et évaluer sérieusement.

**Les outils.** Les plus utilisés sont les bibliothèques TRL et PEFT de Hugging Face, qui gèrent LoRA et QLoRA nativement, ainsi qu'Unsloth et Axolotl qui simplifient la configuration et accélèrent l'entraînement. Pour une tâche précise, ça se met en place en quelques dizaines de lignes.

**Le piège à éviter.** Sur un petit jeu de données, le risque numéro un est le surapprentissage : le modèle apprend vos exemples par cœur au lieu de comprendre la tâche. On le repère en surveillant l'écart entre les performances sur l'entraînement et sur la validation. L'autre piège, c'est l'oubli : en se spécialisant trop fort, un modèle peut perdre des capacités générales. D'où l'importance de mesurer à chaque étape.

## La distillation : un petit modèle à partir d'un gros

La distillation répond à un autre besoin : vous avez un gros modèle qui marche bien, et vous voulez la même chose en plus petit et plus rapide.

Le principe : on entraîne un petit modèle, l'élève, à reproduire les sorties d'un gros modèle, le professeur. Le résultat fondateur est DistilBERT, qui conserve [97 % des performances de BERT en étant 40 % plus petit et 60 % plus rapide](https://arxiv.org/abs/1910.01108). C'est cette approche que Meta a utilisée pour ses petits modèles Llama 3.2 1B et 3B, entraînés en partie à partir de modèles plus gros.

La distillation demande un accès au modèle professeur et un peu plus d'infrastructure que du simple fine-tuning, mais elle donne souvent les petits modèles les plus solides. C'est d'ailleurs pour ça qu'une grande partie des SLM performants d'aujourd'hui sont, d'une manière ou d'une autre, distillés.

## Entraîner depuis zéro : possible, mais rarement utile

Entraîner un SLM complètement de zéro reste l'exception. C'est long, coûteux, et ça n'a de sens que pour des données très particulières que les modèles publics n'ont jamais vues, ou pour de la recherche.

Et pourtant, ce n'est plus réservé aux géants. Le laboratoire français Pleias a entraîné deux petits modèles de raisonnement, [Baguettotron (321 millions de paramètres) et Monad (56 millions)](https://huggingface.co/blog/Pclanglais/synth-data-frontier), uniquement sur des données synthétiques, avec moins de 1 000 heures de H100 pour le run final. Monad a été entraîné en moins de six heures sur 16 GPU H100, à l'aide du framework Nanotron. C'est l'illustration qu'un petit modèle bien pensé, sur de bonnes données, peut sortir avec un budget de calcul modeste.

Mais soyons clairs : pour 99 % des entreprises, entraîner depuis zéro n'a aucun intérêt. La valeur est dans le fine-tuning et la distillation de modèles existants, pas dans la reconstruction d'un modèle de langage.

## De l'entraînement à la production : mesurer, puis quantifier

Un entraînement ne vaut que ce que vaut son évaluation. C'est l'étape la plus négligée et la plus importante.

Avant de toucher au modèle, on construit trois jeux séparés : entraînement, validation, et un **jeu de test gardé de côté** (holdout) qu'on ne touche jamais pendant l'entraînement. On ne s'entraîne jamais sur le test. Pour une tâche de classification, on mesure le F1 par classe et on regarde la matrice de confusion pour voir où le modèle se trompe vraiment. Sans cette mesure, vous pouvez sortir un modèle qui a l'air bon sur quelques exemples et qui s'écroule dès qu'un vrai utilisateur s'en sert.

Une fois le modèle validé, on l'optimise pour le déploiement. On fusionne les adaptateurs LoRA dans le modèle, puis on le quantifie, par exemple au format GGUF en 4 bits, pour qu'il tienne sur une machine modeste et réponde vite. C'est ce qui permet ensuite de [faire tourner un SLM en local, sans cloud](ia-locale-slm-on-premise.md), un sujet à part entière.

Et là encore, c'est la même démarche que partout : commencer simple, mesurer, et ne complexifier que si c'est nécessaire. On gagne le droit de fine-tuner, on ne se l'accorde pas par défaut.

## FAQ : questions fréquentes sur l'entraînement d'un SLM

**Faut-il entraîner un SLM ou utiliser un modèle existant ?**
Dans la grande majorité des cas, commencez par un modèle existant. Testez d'abord ce qu'un bon petit modèle donne déjà avec du prompt engineering, des exemples et une sortie structurée, puis mesurez. On entraîne seulement si ça ne suffit pas : format de sortie très strict, vocabulaire métier pointu, ou réduction du coût d'inférence.

**Quelle est la différence entre fine-tuning et distillation ?**
Le fine-tuning part d'un modèle déjà entraîné et l'ajuste sur vos données pour une tâche précise. La distillation entraîne un petit modèle à imiter un gros, pour obtenir un modèle plus petit et plus rapide. Le fine-tuning spécialise, la distillation compresse.

**C'est quoi LoRA et QLoRA ?**
LoRA gèle le modèle de base et n'entraîne que de petits adaptateurs, ce qui réduit fortement la mémoire et le coût. QLoRA combine LoRA avec une quantification en 4 bits du modèle de base, au point de finetuner un modèle de 65 milliards de paramètres sur un seul GPU de 48 Go.

**Combien d'exemples faut-il pour fine-tuner un SLM ?**
Souvent 200 à 500 exemples annotés suffisent sur des tâches de classification. La qualité et la diversité comptent plus que le volume.

**Combien coûte l'entraînement d'un SLM ?**
Le calcul pur d'un fine-tuning LoRA/QLoRA d'un modèle de 7 milliards de paramètres se compte en quelques heures de GPU et quelques dizaines à quelques centaines d'euros. Ce qui coûte le plus cher, c'est la préparation des données et les itérations.

**Quels outils pour entraîner un SLM ?**
Pour le fine-tuning : TRL et PEFT de Hugging Face, Unsloth, Axolotl. Pour un entraînement depuis zéro de petit modèle : des frameworks comme Nanotron.

## Pour aller plus loin

- **[C'est quoi un SLM (Small Language Model) ?](c-est-quoi-un-slm.md)** : la définition, les modèles récents et pourquoi le sujet compte en 2026
- **[SLM vs LLM : quand choisir un petit modèle ?](slm-vs-llm-quand-choisir.md)** : la grille de décision avant même de penser à entraîner
- **[RAG, finetuning ou entraînement : que choisir ?](entrainement-finetuning-rag-modele-ia.md)** : l'arbitrage de fond entre les trois approches
- **[IA locale : faire tourner un SLM en local](ia-locale-slm-on-premise.md)** : déployer le modèle entraîné sur votre propre infrastructure

Si mes articles vous intéressent, que vous avez des questions ou simplement envie de discuter de vos propres défis liés à l'IA, n'hésitez pas à m'écrire à [anas@tensoria.fr](mailto:anas@tensoria.fr), j'adore échanger sur ces sujets !

Vous vous demandez si entraîner un petit modèle vaut le coup pour votre cas ? Découvrez mon activité de conseil sur [tensoria.fr](https://tensoria.fr).

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
