---
title: "The 7 Wrong Reflexes of RAG Teams (and How to Fix Them)"
slug: mauvais-reflexes-equipes-rag
description: "The 7 counter-productive reflexes observed across 20+ RAG projects: tweaking the prompt first, judging on 3 examples, blaming the LLM... The biases that waste weeks, and their fixes."
categories:
  - "Blog"
  - "AI"
  - "RAG"
tags:
  - "RAG"
  - "Method"
  - "Field experience"
  - "Practical Advice"
  - "Anti-patterns"
date: 2026-05-23
comments: true
authors:
  - Anas
pin: false
math: true
mermaid: true
---

## Introduction

When a RAG project stalls, it's almost never because of a missing technology. It's because of a chain of **counter-productive reflexes** that teams adopt without realizing it. You tweak the prompt when the problem is in the retrieval. You call it "working" after four manual tests. You stack advanced techniques before you've understood where things are actually breaking.

After roughly twenty RAG projects in consulting and audit engagements, I keep running into the same 7 reflexes. These aren't technical mistakes. They're cognitive biases. But they sabotage performance just as reliably as bad chunking. Here's the list, with the replacement reflex for each one.

<!-- more -->

> This article complements [the 5 recurring mistakes in RAG projects](/blog/2026/02/21/les-5-erreurs-les-plus-fr%C3%A9quentes-avec-le-rag/) on the methodology and posture side. For the full RAG overview, see the [RAG guide](/rag/).

## Reflex 1: Modifying the prompt before looking at retrieval

This is the most common reflex. When an answer is bad, you reread the prompt, tweak it, add an instruction. It's what you can control visually, what changes the output instantly. It feels reassuring. And in **80% of cases, it's not the cause of the problem**.

A RAG is a pipeline. The final answer depends on everything that happens upstream: parsing, chunking, retrieval. If the information you need wasn't retrieved by the retriever, the LLM cannot invent it. You can rework the prompt every which way and still go in circles.

**The right reflex**: before touching the prompt, open the **chunks actually injected** for the failing query. If the information isn't there, the prompt isn't the problem. That's the whole point of [RAG error analysis](/blog/2025/06/04/mon-rag-ne-marche-pas-analyse-erreur/), a method I detail in a dedicated article.

## Reflex 2: Testing on 3-4 examples and concluding "it works"

You change the chunking, rerun 4 questions, it seems better, you validate. This is availability bias at work: what you've seen replaces what you haven't. An "improvement" on 4 cases can easily be a regression on 50.

I saw a concrete case where going from chunk size 1024 to 512 visibly improved short questions (the only ones the team was testing). On the full dataset, it was a 12-point degradation: long questions, underrepresented in manual tests, were losing their context.

**The right reflex**: a **fixed evaluation dataset** of 30 to 50 representative question-answer pairs, run before and after every change. This is non-negotiable. Without it, you're not improving a system, you're groping in the dark. The full method for building the dataset and measuring results is here: [evaluating a RAG in production](evaluer-rag-production-metriques-ragas.md). Part of that check can be automated with [unit tests on the LLM](tester-llm-tests-unitaires.md) (format, length, entities), which replace by-hand verification.

## Reflex 3: Stacking advanced techniques before diagnosing

HyDE, reranker, contextual retrieval, query expansion: added in sequence "because we read an article that said it's good". Except each technique has a cost (latency, complexity, technical debt) and a **conditional** gain. If your problem is parsing, HyDE won't change a thing. If your problem is query formulation, adding a reranker masks the symptom without treating the cause.

I audited a system that stacked 4 advanced techniques and performed at 58%. After disabling everything except the base retrieval, we were at 61%. The techniques had been added without any prior diagnosis, some were compensating for each other, others were working against each other.

**The right reflex**: diagnose first, add second. Every technique must address an identified cause. The order is always the same: error analysis, hypothesis, isolated test on a fixed dataset, decision. For the full picture of techniques and the typical gain from each: [techniques to optimize your RAG](optimiser-rag-techniques.md).

## Reflex 4: Blaming the LLM by default

"The LLM doesn't understand my question." Almost never true. In the RAG chain, the LLM is at the **end of the pipeline**. It receives the context you give it. If that context is good, recent LLMs (Claude, GPT, Mistral Large) almost always respond correctly. If it's bad, no LLM will save you.

The "let's switch to a better model" reflex is often a costly dead end. Upgrading to a higher-tier model on a broken RAG typically yields 1 to 3 points of gain. Fixing a retrieval root cause yields 15 to 30. The effort-to-impact ratio is not the same.

**The right reflex**: start the diagnosis at the stages upstream of the LLM (parsing, chunking, retrieval). The LLM is rarely the weak link. The [4 technical root causes of RAG failure](/blog/2026/02/05/les-4-causes-techniques-dechec-dun-rag-et-comment-les-corriger/) details how to target the right cause instead of blaming the last visible step.

## Reflex 5: Ignoring the sources returned by retrieval

To debug a failure, you look at the question and the answer, you wonder "what the LLM should have understood". But you don't open the **context that was actually injected into the prompt**. It's the equivalent of wondering why a recipe went wrong without looking at the ingredients.

Yet that's where 90% of the diagnostic information lives. In most audits I run, the right document exists in the knowledge base, it simply wasn't retrieved, and nobody had noticed because nobody had opened the chunks that were used.

**The right reflex**: trace the full pipeline systematically (Langfuse, LangSmith, or equivalent). For every problematic answer, you need to be able to list: query, retrieved chunks with their scores, final prompt, response. Without this visibility, diagnosis is guesswork. The structured approach to that diagnosis is exactly what [error analysis when your RAG doesn't work](pourquoi-le-rag-ne-fonctionne-pas.md) covers, step by step.

## Reflex 6: Optimizing for the queries you imagine, not the ones asked in production

During development, the team tests on its own questions ("does it answer well on X and Y?"). In production, users ask completely different questions. On a recent B2B support project, 22% of real queries were about the terms and conditions. Nobody on the team was testing that case. Nobody knew the system performed at 3% on it.

This is a classic author bias: you build a product for the questions you ask yourself, not for the ones users actually ask. The result is a system optimized on the wrong cases, with a false sense of quality on the team's side.

**The right reflex**: log user queries **from day 1**, even in internal beta. Classify by volume and success rate. Optimize in order of real business impact, not in order of intuition. The prioritization method (query x success matrix) is detailed in [UX for AI products: 5 patterns that multiply feedback by 5](/blog/2026/05/21/ux-produit-ia-5-patterns-feedback-utilisateur/).

## Reflex 7: Collecting feedback too generic to be useful

"Did you find this answer helpful?" collects 1% of responses. "Did you get the information you were looking for?" collects 5 times more. The "Not relevant" button on displayed sources typically generates 18% exploitable clicks, and each click is a free hard negative usable to fine-tune a reranker.

The "we'll add a thumbs up / thumbs down" reflex is a cosmetic fix. Teams deploy it to check the "user feedback" box and end up with a signal too noisy or too rare to be useful. Result: no improvement data, and therefore no improvement.

**The right reflex**: closed, specific questions, asked at the right moment. Sources displayed with a "not relevant" option to generate exploitable signal. UX becomes a data sensor, not just a presentation layer. The 5 concrete patterns that make this operational are here: [UX for AI products and feedback collection](/blog/2026/05/21/ux-produit-ia-5-patterns-feedback-utilisateur/).

## What ties them all together: confusing symptom with cause

All 7 reflexes share the same root. Each time, you're treating what is **visible and easy to manipulate** (the prompt, the 4 questions tested by hand, the LLM, the generic feedback) rather than what is **invisible but determinant** (the retrieved chunks, the full dataset, the upstream pipeline, the real user queries).

It's comfortable, and that's precisely why it's a trap. A reliable RAG isn't one where you've reworked everything. It's one where you've **identified the right causes**, and fixed those specifically. If the reflexes above feel familiar, [the 5 most common RAG mistakes](les-5-erreurs-rag.md) covers the project-level and strategic patterns that compound them.

### Actionable recap

1. **Always open the retrieved chunks** before modifying the prompt.
2. **Fixed evaluation dataset** from day 1, no manual validation.
3. **Diagnose before stacking** advanced techniques.
4. **The LLM is rarely the culprit**, look at the upstream pipeline.
5. **Trace the full pipeline** (Langfuse or equivalent) for every failure case.
6. **Log production queries** and prioritize by volume x success, not intuition.
7. **Closed, specific feedback questions**, clickable sources as sensors.

If you recognize 2 or 3 of these reflexes in your team, you've identified your biggest lever for improvement. It's not a new technology you need. It's a change of reflex.

---------

If my articles interest you and you have questions, or just want to discuss your own challenges, feel free to write to me at [anas@tensoria.fr](mailto:anas@tensoria.fr). I enjoy talking about these topics!

You can also [book a call](https://cal.eu/anas-rabhi/rendez-vous-ianas) or subscribe to my newsletter :)


---

### About me

I'm **Anas Rabhi**, freelance AI Engineer & Data Scientist. I help companies design and deploy AI solutions (RAG, AI agents, NLP). [Read more about my work and approach](/en/a-propos/), or browse the [full blog](/en/blog/).

Discover my services at [tensoria.fr](https://tensoria.fr) or try our AI agents solution at [heeya.fr](https://heeya.fr).

<div style="text-align: center; margin: 40px 0; gap: 16px; display: flex; flex-wrap: wrap; justify-content: center;">
  <a href="https://cal.eu/anas-rabhi/rendez-vous-ianas" target="_blank" style="display: inline-block; background-color: #4F46E5; color: #ffffff; font-weight: bold; padding: 16px 32px; text-decoration: none; border-radius: 8px; font-size: 18px; letter-spacing: 0.8px; box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2); transition: all 0.3s ease; border: none;">
    Book a call
  </a>
  <a href="https://anas-ai.kit.com/d8b1a255cc" target="_blank" style="display: inline-block; background-color: #222222; color: #ffffff; font-weight: bold; padding: 16px 32px; text-decoration: none; border-radius: 8px; font-size: 18px; letter-spacing: 0.8px; box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2); transition: all 0.3s ease; border: none;">
    <span style="margin-right: 10px;">✉️</span> Subscribe to my newsletter
  </a>
</div>
