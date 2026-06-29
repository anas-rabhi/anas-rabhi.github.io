---
title: "How to Train an SLM (Small Language Model)?"
slug: entrainer-un-slm-fine-tuning-distillation
description: "How to train an SLM: fine-tuning, LoRA/QLoRA, distillation, or from scratch. The methods, the real cost, and a pragmatic step-by-step approach."
categories:
  - "Blog"
  - "AI"
tags:
  - "SLM"
  - "Small Language Model"
  - "Fine-tuning"
  - "LoRA"
date: 2026-06-29
comments: true
authors:
  - Anas
pin: false
math: false
mermaid: false
faqs:
  - question: "Should you train an SLM or use an existing model?"
    answer: "In the vast majority of cases, start with an existing model. Before training anything, test what a good open-source small model already gives you with prompt engineering, few-shot examples, and structured output, then measure. You only move to training if the measured performance isn't enough. Training an SLM is useful for a very strict output format, niche domain vocabulary, or to bring down inference cost, not by default."
  - question: "What is the difference between fine-tuning and distillation?"
    answer: "Fine-tuning starts from an already-trained model and adjusts it on your data for a specific task. Distillation trains a small model (the student) to imitate a large model (the teacher), to obtain a smaller and faster model that keeps a good share of the performance. Fine-tuning is for specializing, distillation is for compressing."
  - question: "What are LoRA and QLoRA?"
    answer: "LoRA (Low-Rank Adaptation) is a fine-tuning method that freezes the base model and only trains small added adapters, which drastically reduces memory and cost. QLoRA combines LoRA with 4-bit quantization of the base model. The QLoRA paper shows you can fine-tune a 65-billion-parameter model on a single 48 GB GPU, where classic fine-tuning would require several."
  - question: "How many examples do you need to fine-tune an SLM?"
    answer: "Fewer than you'd think. On many classification tasks, performance saturates around 200 to 500 annotated examples. What matters most isn't volume but the quality and diversity of the examples, perfectly representative of your use case."
  - question: "How much does it cost to train an SLM?"
    answer: "The raw compute is surprisingly low: a LoRA/QLoRA fine-tuning of a 7-billion-parameter model is measured in a few GPU hours and a few tens to a few hundred euros. What costs the most is building the dataset, iterating, and evaluating. Training from scratch remains the realm of labs, even if recent projects have done it for small models with fewer than 1,000 GPU hours."
  - question: "What tools should you use to train an SLM?"
    answer: "For fine-tuning, the most used are Hugging Face's TRL and PEFT libraries, along with Unsloth and Axolotl, which simplify and speed up the process. For training a small model from scratch, frameworks like Nanotron are built for it. The choice mainly depends on your method: fine-tuning an existing model or full training."
---

## How to train an SLM, and should you really do it?

Training an SLM can mean several very different things: fine-tuning an existing small model on your data, distilling one from a large model, or training one from scratch. For 95% of companies, the right answer is fine-tuning, and only after checking that an existing model wasn't already enough.

That's the first reflex to have, and it saves a lot of time and money. Before launching any training, test what a good open-source small model already gives you with prompt engineering, a few examples, and structured output. Measure. You only allow yourself to train if the measurement shows it isn't enough.

<!-- more -->

In this article, I go through the ways to train an SLM, the realistic method (LoRA/QLoRA fine-tuning), distillation, training from scratch, and the evaluation discipline that separates a usable model from one that collapses in production. If the real question is still "should I train, or is a RAG enough?", I have a dedicated article on that [trade-off between RAG, fine-tuning, and training](entrainement-finetuning-rag-modele-ia.md).

## Should you really train an SLM?

No, not by default. Training is only justified in specific cases, and the wrong reflex is expensive.

Training an SLM becomes relevant when:

- you need a **very strict output format** that a good prompt doesn't hold reliably;
- you work with **niche domain vocabulary** that public models don't master;
- you want to **bring down cost and latency** by replacing a large model with a small specialized model that stays just as good on your task.

Outside these cases, an existing model used well is almost always enough. And even when training is justified, you have to keep a real risk in mind: base models improve fast. An SLM fine-tuned today can be overtaken in six months by a new public small model, with no effort on your part. That's the whole trade-off I detail in [SLM vs LLM: when to choose a small model](slm-vs-llm-quand-choisir.md).

## The ways to train an SLM

"Training" covers several methods that don't share the same cost or the same goal. Here are the five you'll come across, from the heaviest to the most accessible.

| Method | What it's for | Cost and effort |
|---|---|---|
| Training from scratch | building a model from A to Z | very high, reserved for labs |
| Continued pre-training | adding a broad domain to an existing model | high |
| Supervised fine-tuning (SFT) | learning a specific task or format | medium |
| Distillation | compressing a large model into a small one | medium |
| LoRA / QLoRA fine-tuning | specializing at low cost | low, a single GPU is enough |

For the underlying mechanics of pre-training and post-training (SFT, RLHF), I refer you to my article on [training and fine-tuning a model](entrainement-finetuning-rag-modele-ia.md). Here, I focus on what really concerns a small model: economical fine-tuning, distillation, and training from scratch when it's justified.

## LoRA / QLoRA fine-tuning in practice

This is the realistic path for nearly all projects, and by far the most useful to master. The starting idea is simple: instead of retraining the billions of parameters of a model, you touch almost none of them.

**Why you don't retrain the whole model.** Fine-tuning a model the old way means adjusting all of its parameters. On a 7-billion model, that means loading the model, its gradients, and the optimizer states into memory, easily more than 100 GB of VRAM. Out of reach for a normal machine. LoRA sidesteps this entirely.

**What LoRA does, concretely.** LoRA (Low-Rank Adaptation) freezes the base model, you no longer touch it, and inserts small trainable matrices alongside it, the adapters. During training, only these matrices learn. They are tiny: you often train less than 1% of the model's parameters. So you need far less memory and time, while still getting a model specialized on your task. At the end, you can either keep the adapter separate (a few megabytes loaded on top of the base model) or merge it into the model.

**What QLoRA adds.** QLoRA pushes the logic further by loading the base model in 4 bits during training, instead of 16. You divide the required memory again, without retraining that base model, which stays frozen. The [QLoRA](https://arxiv.org/abs/2305.14314) paper shows you can fine-tune a 65-billion-parameter model on a single 48 GB GPU, with no notable loss of quality. For an SLM of a few billion parameters, a consumer GPU is more than enough.

**The hyperparameters, and the ones that really matter.** Three settings carry most of the weight:

- the **rank `r`**: the size of the adapters. The larger it is, the more the model can learn, but the more it risks overfitting. 8 to 32 covers most cases, 16 is a good starting point.
- the **`alpha`**: a scaling factor applied to the adapters. The common convention is to set it to double the rank, so 32 for a rank of 16.
- the **target modules**: which layers you plug the adapters into. Often the attention layers, sometimes all the linear layers for a stronger effect.

To this you add a small learning rate and 3 to 5 epochs. No need to over-optimize on the first try: the goal is first to learn the task and the output format, then to adjust by looking at where the model gets it wrong.

**The data format.** You present the examples as instructions: an instruction (often a system prompt), an input, and the expected output. For classification, the output is for example a JSON with the label. What matters most is consistency: the same format everywhere, clean outputs. A well-built dataset weighs more than any hyperparameter setting.

**How much data.** Fewer than you'd think. On many classification tasks, performance saturates around 200 to 500 annotated examples ([study on text classification](https://arxiv.org/html/2406.08660v2)). Quality and diversity matter more than volume. It's also the lesson of Microsoft's Phi models, whose performance comes above all from carefully chosen data, the idea defended in their paper [*Textbooks Are All You Need*](https://arxiv.org/abs/2306.11644). When data is missing, you generate it, a topic I'll cover in a dedicated article on synthetic data generation.

**What it costs.** On the compute side, it's negligible: a LoRA/QLoRA fine-tuning of a 7-billion-parameter model is measured in a few GPU hours and a few tens to a few hundred euros. What costs the most is everything else: building the dataset, iterating on it, and evaluating it seriously.

**The tools.** The most used are Hugging Face's TRL and PEFT libraries, which handle LoRA and QLoRA natively, along with Unsloth and Axolotl, which simplify the configuration and speed up training. For a specific task, it's set up in a few dozen lines.

**The trap to avoid.** On a small dataset, the number one risk is overfitting: the model learns your examples by heart instead of understanding the task. You spot it by watching the gap between performance on training and on validation. The other trap is forgetting: by specializing too hard, a model can lose general capabilities. Hence the importance of measuring at every step.

## Distillation: a small model from a large one

Distillation answers a different need: you have a large model that works well, and you want the same thing smaller and faster.

The principle: you train a small model, the student, to reproduce the outputs of a large model, the teacher. The founding result is DistilBERT, which keeps [97% of BERT's performance while being 40% smaller and 60% faster](https://arxiv.org/abs/1910.01108). This is the approach Meta used for its small Llama 3.2 1B and 3B models, trained in part from larger models.

Distillation requires access to the teacher model and a bit more infrastructure than plain fine-tuning, but it often produces the strongest small models. That's also why a large share of today's high-performing SLMs are, in one way or another, distilled.

## Training from scratch: possible, but rarely useful

Training an SLM completely from scratch remains the exception. It's long, costly, and only makes sense for very particular data that public models have never seen, or for research.

And yet, it's no longer reserved for the giants. The French lab Pleias trained two small reasoning models, [Baguettotron (321 million parameters) and Monad (56 million)](https://huggingface.co/blog/Pclanglais/synth-data-frontier), solely on synthetic data, with fewer than 1,000 H100 hours for the final run. Monad was trained in under six hours on 16 H100 GPUs, using the Nanotron framework. It's the illustration that a well-designed small model, on good data, can come out with a modest compute budget.

But let's be clear: for 99% of companies, training from scratch has no value. The value is in fine-tuning and distilling existing models, not in rebuilding a language model.

## From training to production: measure, then quantize

A training run is only worth as much as its evaluation. It's the most neglected and the most important step.

Before touching the model, you build three separate sets: training, validation, and a **held-out test set** (holdout) that you never touch during training. You never train on the test set. For a classification task, you measure the per-class F1 and look at the confusion matrix to see where the model really goes wrong. Without this measurement, you can ship a model that looks good on a few examples and that collapses the moment a real user uses it.

Once the model is validated, you optimize it for deployment. You merge the LoRA adapters into the model, then quantize it, for example to the 4-bit GGUF format, so it fits on a modest machine and responds fast. This is what then lets you [run an SLM locally, without the cloud](ia-locale-slm-on-premise.md), a subject in its own right.

And here again, it's the same approach as everywhere: start simple, measure, and only add complexity if it's necessary. You earn the right to fine-tune, you don't grant it to yourself by default.

## FAQ: common questions about training an SLM

**Should you train an SLM or use an existing model?**
In the vast majority of cases, start with an existing model. First test what a good small model already gives you with prompt engineering, examples, and structured output, then measure. You only train if it isn't enough: very strict output format, niche domain vocabulary, or reducing inference cost.

**What is the difference between fine-tuning and distillation?**
Fine-tuning starts from an already-trained model and adjusts it on your data for a specific task. Distillation trains a small model to imitate a large one, to obtain a smaller and faster model. Fine-tuning specializes, distillation compresses.

**What are LoRA and QLoRA?**
LoRA freezes the base model and only trains small adapters, which sharply reduces memory and cost. QLoRA combines LoRA with 4-bit quantization of the base model, to the point of fine-tuning a 65-billion-parameter model on a single 48 GB GPU.

**How many examples do you need to fine-tune an SLM?**
Often 200 to 500 annotated examples are enough on classification tasks. Quality and diversity matter more than volume.

**How much does it cost to train an SLM?**
The raw compute of a LoRA/QLoRA fine-tuning of a 7-billion-parameter model is measured in a few GPU hours and a few tens to a few hundred euros. What costs the most is data preparation and iterations.

**What tools should you use to train an SLM?**
For fine-tuning: Hugging Face's TRL and PEFT, Unsloth, Axolotl. For training a small model from scratch: frameworks like Nanotron.

## Further reading

- **[What is an SLM (Small Language Model)?](c-est-quoi-un-slm.md)**: the definition, recent models, and why the topic matters in 2026
- **[SLM vs LLM: when to choose a small model?](slm-vs-llm-quand-choisir.md)**: the decision grid before you even think about training
- **[RAG, fine-tuning, or training: which to choose?](entrainement-finetuning-rag-modele-ia.md)**: the underlying trade-off between the three approaches
- **[Local AI: running an SLM locally](ia-locale-slm-on-premise.md)**: deploying the trained model on your own infrastructure

If my articles interest you and you have questions or just want to discuss your own AI challenges, feel free to write to me at [anas@tensoria.fr](mailto:anas@tensoria.fr), I love talking about these topics!

Wondering whether training a small model is worth it for your case? Discover my consulting work at [tensoria.fr](https://tensoria.fr).

You can also [book a call](https://cal.eu/anas-rabhi/rendez-vous-ianas) or subscribe to my newsletter :)


---

### About me

I'm **Anas Rabhi**, freelance AI Engineer & Data Scientist. I help companies design and deploy AI solutions (RAG, AI agents, NLP).

Discover my services at [tensoria.fr](https://tensoria.fr) or try our AI agents solution at [heeya.fr](https://heeya.fr).

<div style="text-align: center; margin: 40px 0; gap: 16px; display: flex; flex-wrap: wrap; justify-content: center;">
  <a href="https://cal.eu/anas-rabhi/rendez-vous-ianas" target="_blank" style="display: inline-block; background-color: #4F46E5; color: #ffffff; font-weight: bold; padding: 16px 32px; text-decoration: none; border-radius: 8px; font-size: 18px; letter-spacing: 0.8px; box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2); transition: all 0.3s ease; border: none;">
    Book a call
  </a>
  <a href="https://anas-ai.kit.com/d8b1a255cc" target="_blank" style="display: inline-block; background-color: #222222; color: #ffffff; font-weight: bold; padding: 16px 32px; text-decoration: none; border-radius: 8px; font-size: 18px; letter-spacing: 0.8px; box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2); transition: all 0.3s ease; border: none;">
    <span style="margin-right: 10px;">✉️</span> Subscribe to my newsletter
  </a>
</div>
