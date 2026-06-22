---
title: "My RAG Doesn't Work: Error Analysis Changes Everything"
slug: mon-rag-ne-marche-pas-analyse-erreur
description: "RAG not working? A 3-question diagnostic, quick wins testable in 2 hours, and a field-tested error analysis method. Practical, concrete guide."
categories:
  - "Blog"
  - "AI"
tags:
  - "RAG"
  - "Artificial Intelligence"
  - "Practical Tips"
  - "Optimization"
date: 2025-06-04
comments: true
authors:
  - Anas
pin: false
math: true
mermaid: true
---

## Introduction

I've written before about [how to evaluate a RAG in production](evaluer-rag-production-metriques-ragas.md), but the topic is broad enough that there's always more to share. Especially since I keep hearing comments like:
*"I don't understand, I added [the trendy tech], but the results aren't good."*

<!-- more -->

> For the full picture (foundations, optimization, failures and fixes), see the [RAG guide](/rag/).

## RAG isn't magic (and that's normal)

RAG is THE project everyone wants since generative AI took off. Everyone wants their AI-powered assistant, capable of answering any question about their data. You find "RAG in two lines" tutorials, no-code tools, and it gives the impression it's simple.

But the reality is that once the project is up and running, tests are rarely as magical as hoped. The AI doesn't answer everything, hallucinates sometimes, or completely misses a basic question. And that's deeply frustrating.

First thing to keep in mind: no AI system can have 100% correct answers.
The real value comes from understanding the problem you're trying to solve, not from chasing perfection.

## Quick diagnostic: 3 questions to isolate the problem

Before going in every direction at once, here are the 3 questions to ask yourself, in order. They point you toward the right component in under 10 minutes.

**1. Does the retrieval find anything?**
Look at the chunks retrieved for the failing query. Are there any? Are they relevant? If retrieval returns nothing, the problem isn't the LLM: it's the indexing or the query formulation.

**2. If the chunks are there, is the answer hallucinating?**
Compare the generated answer with the provided chunks. Did the AI invent information that wasn't in the sources? If so, that's a generation problem (prompt, model, temperature).

**3. If the chunks are relevant and the answer is logical: does the information actually exist in the knowledge base?**
Sometimes the base simply doesn't contain the answer. That's a data problem, not a RAG problem.

These 3 questions point you to the right component. From there, the solutions differ based on the diagnosis.

## Quick wins to try before rebuilding everything

Before changing your architecture, embeddings, or model, here's what fixes 80% of problems. These are changes you can test in 1 to 2 hours.

**If retrieval isn't finding the right chunks:**
- Reduce chunk size (try 512 tokens instead of 1024)
- Increase top-k (retrieve 7 chunks instead of 3)
- Test [hybrid search](rag-hybride-bm25-vectoriel.md) (vector + BM25) for queries with specific keywords

**If the LLM is hallucinating:**
- Add to the prompt: *"Answer only from the provided context. If the information is not in the context, say so explicitly."*
- Lower the temperature to 0 or 0.1 to reduce model creativity

**If quality is inconsistent from one query to another:**
- Check the quality of source data (poorly extracted PDFs, corrupted tables, duplicated text)
- Check chunk overlap (10-15% overlap avoids cutting important information)

If none of these quick wins improves things, then yes, it warrants a deeper analysis. That's when you can consider [more advanced RAG optimization techniques like HyDE, reranking, or contextual retrieval](optimiser-rag-techniques.md).

## Concrete examples of error analysis

Because it's clearer with examples, here are two real cases:

**1. When vector search falls short**
On one project, everything seemed to work... except that certain queries with specific keywords returned nothing, even though the answer was clearly in the base.
After analysis, we saw that the vector search wasn't capturing certain synonyms or phrasings.
So we added BM25 search (keyword-based) alongside the vector search (the pattern I detail in [Hybrid RAG BM25 + vector](rag-hybride-bm25-vectoriel.md)). Result: the "hard" questions finally got answers.

**2. Forgotten business attributes**
In an e-commerce context, it was impossible to surface products of a specific color ("I want a red t-shirt"), even though the data was there.
Analysis showed that the color semantics weren't being captured well in the embedding vectors. We simply added metadata filtering before passing to the AI: problem solved.

## How to run the error analysis

Here's how I approach it, and honestly, it works in 90% of cases:

1. Take a sample of examples where the RAG fails.
2. For each case, ask:
   - Does the retrieval find anything or not?
   - Is the generation hallucinating?
   - Does the information actually exist in the base?
   - Is it a format, metadata, or phrasing problem?
3. Categorize the errors (retrieval, ranking, hallucination, data...).
4. Test simple fixes... before changing everything.

And above all: note what comes up most often, to prioritize the real improvements.

To start, all error analysis must be done by hand. It's essential to truly understand where the problems come from. But let's be honest: at some point, when query volume increases, it becomes quickly unmanageable. That's where good tooling becomes indispensable.

## Which tools to use?

LangFuse is probably one of the most practical (and open-source) for tracing the entire RAG pipeline: you visualize every step, from the original query to the retrieved chunks, the final prompt sent to the LLM, and the generated answer. Ideal for pinpointing exactly where things go wrong.

LangSmith does the same as LangFuse, with a different interface. The advantage: if you're already using LangChain, the integration is natural.

For deeper monitoring, Weights & Biases lets you track performance metrics over time and compare different versions of the system. Useful for checking whether an "improvement" didn't break something else elsewhere.

The idea is not to drown in dashboard overload: you just need enough visibility to quickly understand where to look when something's off. If you want to go further on [specific metrics to track (Faithfulness, RAGAS...)](evaluer-rag-production-metriques-ragas.md), I cover them in detail in a dedicated article on how to evaluate a RAG in production (the 3 evaluation levels, dataset construction, RAGAS / DeepEval / TruLens comparison, and my audit process on client engagements).

## Key takeaways

RAG is neither magic nor perfect.
What makes the difference isn't the latest technology you added, but the ability to understand why it fails and to iterate intelligently.

The method in summary:
1. Diagnose with the 3 questions
2. Test the quick wins first
3. If that's not enough, analyze methodically
4. Fix at the source before adding complexity

And if your RAG has [specific technical causes](les-4-causes-techniques-echec-rag.md), I cover those in detail too.

One last thing: before even starting the formal error analysis, there are daily habits that are often enough to explain why a RAG plateaus. Changing the prompt first, judging on three examples, blaming the LLM by default. I've listed seven of them, observed across most of the projects I audit, with the concrete fix for each: [the 7 bad habits of RAG teams](mauvais-reflexes-equipes-rag.md).

---

If my articles interest you and you have questions or just want to discuss your own challenges, feel free to write to me at [anas@tensoria.fr](mailto:anas@tensoria.fr), I enjoy talking about these topics!

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
