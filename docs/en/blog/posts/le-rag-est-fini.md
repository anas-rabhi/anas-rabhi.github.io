---
title: "RAG vs Long Context LLM: Is RAG Really Dead?"
slug: le-rag-est-il-vraiment-fini
description: "RAG or long context LLM? A comparison of costs (1M tokens = €2–10/question), the lost-in-the-middle effect, and the cases where RAG remains essential in enterprise."
categories:
  - "Blog"
  - "AI"
  - "RAG"
tags:
  - "RAG"
  - "Artificial Intelligence"
  - "Strategy"
  - "Costs"
date: 2026-02-05
comments: true
authors:
  - Anas
pin: true
math: true
mermaid: true
---

## Introduction: RAG, a magic method?

Every time a new model launches with a larger context window, people announce that RAG is obsolete. Yet RAG was born out of a very concrete need: you cannot hand a 400 or 500-page document to an LLM and ask it questions on the spot.

In enterprise settings, you often have dozens (or even hundreds) of files. RAG offers a simple answer: build a document base out of small pieces (chunks), then dynamically supply the relevant chunks to the AI with each question.

<!-- more -->

In short, it is a technique like any other: sometimes the right fit, sometimes not. If you have a short 10-page document, there is no need to set up a RAG pipeline: you can load it directly into an LLM and ask questions. With 100 articles of 100 pages each, even if loading everything is *technically* possible, it is not always relevant (or cost-effective).

Context windows are growing fast, some models now reach 1M tokens, roughly 700,000 words, but loading 1M tokens still comes at a price: sometimes between €2 and €10 per question. Techniques exist to reduce those costs (caching, etc.), but €0.20 × 100 questions still adds up to €20.

More importantly, injecting too much information often degrades answer quality. The more you overload the context window, the more the LLM loses the thread. RAG is not going anywhere.

RAG became the standard after ChatGPT's arrival because it addresses a fundamental problem: LLMs' knowledge is limited to what they saw during training. In most enterprise use cases, you want the AI to answer questions on internal data. The same principle is used by AI search engines like Perplexity to index and cite web content.

RAG has a "magical" quality: combine a vector database that stores company documents with an LLM, and you can let the AI answer almost any question on that data.

### How does it work?

A RAG pipeline has two main stages:

1) **Processing and ingestion**
Documents are processed, split into chunks, then ingested into a vector database (see [Cloudflare's explainer on vector databases](https://www.cloudflare.com/en-gb/learning/ai/what-is-vector-database/)). This step is invisible to end users; it happens at the start of the project and is updated whenever documents change.

2) **Retrieval and generation**
At each query, relevant chunks are retrieved from the vector database and injected into the LLM prompt to improve the answer and reduce hallucinations.

Setting up a "basic" RAG is fairly quick. And because humans generalize fast, the thought is: *it works, ship it, done*. Except it never plays out that way.

A fast RAG typically returns 50 to 70% correct answers. In enterprise, that may not be enough to expose to end users.

## RAG vs Long Context LLM: the real debate

This is where the debate has been concentrated since 2024. With context windows exploding (Gemini at 1M tokens, Claude at 200K), the logic becomes: *"If I can put everything in the context, why bother with RAG?"*

That is a fair question. Here is what it looks like in practice:

| | RAG | Long Context LLM |
|---|---|---|
| **Cost per query** | Low (3–5 chunks injected) | High (entire corpus every time) |
| **Quality on large corpora** | Good when retrieval is good | Degrades with size |
| **Latency** | Fast | Slower on long contexts |
| **Data updates** | Partial re-indexing | Full reload |
| **Best suited for** | 50+ document corpora | 5–20 short documents |

One effect that is consistently underestimated: the **"lost in the middle problem"**. The more context you inject, the more the LLM tends to neglect what sits in the middle. It retains the beginning and the end more reliably. On a 400-page corpus, this degradation is real and measurable.

## When Long Context is genuinely the better choice

There are cases where injecting the full context is the right call:

- **A single long document**: a 50-page contract, an annual report, a source code base, no RAG needed, load it all and ask questions.
- **Questions that cross an entire document**: "What are the contradictions in this text?", RAG may miss passages if the question is too broad.
- **Global summary of a document**: "Summarize the key points of this white paper", more reliable than partial retrieval over chunks.
- **Corpus of fewer than 20 short documents**: if everything fits without blowing the budget, the complexity of a RAG pipeline is not justified.

RAG remains the right choice as soon as the corpus is large, queries are targeted, cost is a constraint, or data changes frequently.

## What "RAG is dead" proponents forget

Two constraints that Long Context LLMs do not solve:

**Data confidentiality.** In enterprise, HR, legal, and technical documents cannot always be sent to a cloud LLM. An on-premise RAG with a local LLM (Llama, Mistral) remains the only option in those cases. Long Context changes nothing about that.

**Cost at scale.** 100 users × 10 questions/day = 1,000 queries. At €2 per query with Long Context (500-page corpus), that is €2,000/day. With RAG, you inject 3–5 relevant chunks per query; the cost drops by 90% or more. In enterprise, that matters enormously.

And for those wondering: *"What about fine-tuning?"*, that is a third option worth considering, but it introduces other problems (true total cost, the risk it simply does not work, obsolescence every time a new model is released). I covered all of this with real numbers and a decision framework in [Training, fine-tuning or RAG: which to choose for your AI?](entrainement-finetuning-rag-modele-ia.md)

## RAG is evolving: toward Agentic RAG

The real shift is that RAG is no longer "just" vector retrieval. It now integrates agent capabilities: query reformulation, multi-source search, result verification, iteration.

**Agentic RAG** is a RAG where the AI itself decides to relaunch a search if initial results are insufficient, to combine multiple sources, or to adapt its retrieval strategy. It is a direct response to classic RAG's limits on complex queries. I covered the 5 agentic patterns and their real cost in [Agentic RAG vs classic RAG: what is the difference?](agentic-rag-vs-rag-classique.md)

If you want to understand the fundamental difference between the two approaches, [What is an AI agent](c-est-quoi-un-agent-ia.md) is the right starting point. And if you want to go deeper on the building blocks that make agents genuinely useful in production, two articles cover that: [MCP (Model Context Protocol)](mcp-model-context-protocol-agents-ia.md), the open standard that is becoming the default in 2026 for connecting agents to their tools, and [AI agent memory](memoire-agents-ia-long-terme.md), consistently the most underestimated feature in any serious agent.

## Conclusion: is RAG really dead?

RAG is not dead. It remains a pragmatic approach for making LLMs useful on internal data, with a solid balance between relevance, cost, and quality.

Long Context LLM is a complementary tool, not a replacement. Each has its use cases, and I laid out the full decision framework, with real costs and benchmarks, in [long context vs RAG: when to use which](long-context-vs-rag-quand-utiliser.md). Agentic RAG represents the natural evolution for cases where classic RAG hits its limits.

Rather than asking whether RAG is finished, the real question is: **at what point is a RAG useful (or not) for your specific use case**, and how to optimize it when it is the right choice.

***

If my articles interest you and you have questions, or just want to discuss your own challenges, feel free to write to me at [anas@tensoria.fr](mailto:anas@tensoria.fr), I enjoy talking about these topics!

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
