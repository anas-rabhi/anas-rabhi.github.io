---
title: "The 5 Most Common RAG Mistakes"
description: "Field notes from 20+ RAG projects: the 5 recurring mistakes in enterprise deployments and how to avoid them. Expectations, data, frameworks, and measurement."
categories:
  - "Blog"
  - "AI"
  - "RAG"
tags:
  - "RAG"
  - "Artificial Intelligence"
  - "Field Experience"
  - "Practical Tips"
date: 2026-02-21
comments: true
authors:
  - Anas
pin: false
math: true
mermaid: true
---

## Introduction

Since 2023, I've run about ten RAG projects myself and led another ten with teams. Some went very well, others less so, but we always tried to learn and correct course along the way. Looking back, I keep seeing the same mistakes, whether from myself early on, from clients, or from peers. These aren't technical mistakes (I cover those in [this article](les-4-causes-techniques-echec-rag.md)), they're mistakes of posture, approach, and method.

Everyone makes them at least once. The point here is to name them clearly so they don't get repeated.

<!-- more -->

> Article connected to the [complete RAG guide](/rag/), where I detail the foundations, optimization, and production deployment.

## Mistake #1: Believing RAG will answer everything

This is probably the most frequent mistake, and it doesn't necessarily come from the technical team. It comes from a gap between what the client imagines and what RAG actually does.

RAG is **targeted question-answering** over a document base. You ask a question, the system retrieves the right document chunks, and the LLM formulates an answer from that. It's powerful, but it's scoped.

The problem is that for someone outside the AI world, "an AI answers everything." That's the mental model people have. So when you deploy a RAG chatbot, the client naturally expects it to handle any request.

I remember one of our first RAG projects, in 2023, when GPT-3.5 was becoming genuinely usable. We had built a chatbot for [Odecia](https://odecia.fr) to answer customer questions on their website. The system worked well on the questions we had anticipated. Except that when we analyzed the real user questions, we quickly realized **the actual questions had nothing to do with what we had imagined**.

Users were asking "summarize this file for me," or asking questions completely unrelated to the available documentation. For a data scientist, it's obvious that can't work: RAG doesn't have access to the user's file, and it can only answer based on what it knows. But for someone outside the AI world, it's incomprehensible. "It's AI, right? It should understand."

That was one of our first RAG projects, and it taught us one essential thing: **you need to communicate clearly from the start about what RAG can and cannot do**. Explain the scope plainly. Give examples of questions that work and questions that won't. Manage expectations upfront, not after the disappointment.

Since then, we do this exercise systematically with every new client. And it changes everything. Less frustration, less disappointment, and a project that starts on solid ground. Yes, it's less glamorous, but we're not selling dreams, we're trying to sell a product that works, with the reality of the field. What I often tell clients: we don't need the AI to get 100% of answers right for it to save us time. At 90% correct answers, we're already winning. Economically speaking, 90% correct means we can answer 9 out of 10 clients, which already eliminates the time wasted on repetitive questions and avoids losing clients. Customers are very satisfied when they find answers instantly, without having to dig through documents manually.

## Mistake #2: Thinking the next RAG will be easy because you've done one before

Everyone makes this one. You ship a first RAG, it goes well, and you tell yourself: "Now we have the method, the next one will be fast." Wrong.

RAG is **case by case**. Every project depends on the client's data, the type of questions being asked, the document volume, the format complexity. From one business to another, it's different data, different questions, and therefore different problems.

To give a concrete sense of scale: I've had RAG projects where we spent **2 months** industrializing the system to reach around 90% correct answers. Thousands of documents to ingest, weekly updates, but relatively clean documents and predictable questions. It was work, but we knew where we were going.

And then I've had other projects where we spent **6 months** to barely reach 80% correct answers. The documentation was complex: tables inside PDFs, technical diagrams, semi-structured documents, heterogeneous formats. Each document type brought a new problem. Each improvement on one question type broke something in another.

The real challenge is that **the more data there is, the more complex the RAG becomes**. It's not linear. Going from 100 to 1,000 documents isn't just "10x more work", it's a change in nature: the retriever needs to be more precise, chunking needs to be finer, and edge cases multiply.

I've also had clients come to us because **their existing RAG wasn't working**. Someone had promised them something simple and fast. It had been built in a few days with LangChain on autopilot, with no real look at the data. Result: performance under 70%, a frustrated client, and a project to rebuild almost from scratch.

Every RAG is a project in its own right. There are no shortcuts.

## Mistake #3: Diving into code without looking at the data

This is a classic developer mistake (I include myself in this). You get a brief, you want to code, and you launch straight into the pipeline: parsing, chunking, embeddings, retriever, prompt. You have your habits, you know the architecture, you want to move fast.

Except the first thing to do, before writing a single line of code, is **to open the client's data and look at it**.

How many times have I seen project estimates completely disconnected from reality because nobody had taken the time to look at the documents? You estimate "3 weeks" based on a brief that says "we have PDFs," and when you open the PDFs, you find poor-quality scans, nested tables, inconsistent headers, 200-page documents with no structure, or worse, files mixing text, images, and handwritten annotations.

The data is **80% of the work in a RAG**. If the documents are clean and well-structured with extractable text, the RAG will be relatively straightforward to build. If the documents are a chaos of heterogeneous formats, no framework or miracle technology will solve the problem for you.

Concretely, before writing anything, I now systematically spend half a day (sometimes more) to:

- Open a representative sample of the client's documents
- Look at the formats (PDF, Word, Excel, HTML, images...)
- Check the quality of extractable text
- Identify the problematic cases (tables, diagrams, scans)
- Estimate volume and update frequency
- Understand what questions users will ask on this data

This step is what lets me estimate a project accurately. And it's the step most people skip. People want to move fast, they want to show a first result. But a first result on data you haven't understood is worth nothing.

## Mistake #4: Doing everything with a framework without understanding what's happening underneath

I used LangChain in my first RAG projects. I also used LlamaIndex extensively. And I'm not saying these frameworks are bad. But I am saying there's a real trap in using them without understanding what they're doing behind their functions.

The problem is simple: **when the RAG doesn't answer a question well, the first thing to do is understand why**. And to understand why, you need to trace back each step of the pipeline (I go into this in detail in [this article on error analysis](pourquoi-le-rag-ne-fonctionne-pas.md)). Did parsing correctly extract the information? Did chunking cut at the wrong point? Did the retriever find the right chunks? Was the prompt properly formed?

When each step is wrapped in a framework abstraction, **debugging becomes a nightmare**. You spend an enormous amount of time understanding what function `X` does inside class `Y`, navigating documentation, figuring out how to customize behavior that doesn't suit you.

The time I invested customizing LlamaIndex components and understanding the various internal steps, I actually spent **more time doing that than coding my own RAG system**. And my own system, I understand it end to end, I can modify it in 5 minutes, and I know exactly what's happening at each step.

There's another advantage to building your own components: **once you have them, they're yours**. From project to project, you reuse your code, which you fully know and control. You can change what you need without depending on a framework's choices.

Frameworks are valuable when they encapsulate complex computations you don't want to recode (like TensorFlow or PyTorch for deep learning). But for RAG, the steps are conceptually simple: parse a document, split it, vectorize it, find the nearest neighbors, build a prompt. It's not rocket science. Coding it yourself once is an excellent exercise that lets you learn each step in depth and keep full control.

And in the long run, this is even more true. New techniques come out every week in the RAG world (I detailed the main ones, including HyDE, reranking, and contextual retrieval, in [my article on 8 techniques to optimize your RAG](optimiser-rag-techniques.md)). When you want to explore or integrate them, you're always dependent on the framework and its ability to adapt. And honestly, the adaptability of generative AI frameworks is often poor. By the time a technique is cleanly integrated into a framework, three new ones have already come out.

What I'm saying here applies to AI Agents as well. For agent frameworks (CrewAI, LangGraph, Pydantic AI, Smolagents), another article cuts through the noise with a pragmatic take: [pragmatic comparison of AI agent frameworks in 2026](crewai-langchain-langgraph-comparatif-pragmatique.md).

## Mistake #5: Not measuring from day one

This is the silent mistake. The RAG is in place, it's running, users are asking questions, and you have the impression that "it works." But does it really? How well? You don't know, because nothing was set up to measure.

I've seen too many projects where measurement only starts when negative feedback arrives. At that point, there's no baseline, no history, no way to know whether things degraded or were never good to begin with.

Measurement has to start **on day one**. You don't need a sophisticated tool at the beginning: a simple set of 30 to 50 reference question-answer pairs, run regularly against the system, is enough to get a clear picture of performance. This is what's called an **evaluation dataset**, and it's the most important thing nobody does. I wrote a guide to [build one in 30 minutes](dataset-evaluation-rag-questions-synthetiques.md), synthetic question generation included.

Without this, every change becomes a gamble. You change the chunking, adjust the prompt, switch embedding models, and you have **no objective way to know if it's better or worse**. You rely on gut feeling, informal feedback, the two or three questions you test by hand. That's not enough.

Concretely, what I recommend:

- **Build an eval dataset** at the start of the project, with representative questions and their expected answers
- **Run it after every change** to the system to verify you're progressing (and not breaking anything)
- **Log production interactions** to identify real use cases and real problems
- **Track a simple score** (% correct answers) over time

It's basic, but it's what makes the difference between a RAG project that improves over time and one that stagnates without anyone understanding why. For the full method (dataset construction, retrieval and generation metrics, choosing between RAGAS, DeepEval, or TruLens, and my audit process on client projects), I wrote a dedicated article on [how to evaluate a RAG in production](evaluer-rag-production-metriques-ragas.md).

## Conclusion

I've made all 5 of these mistakes. Generative AI creates an impression of magic, and with that impression comes the conviction that everything is achievable quickly. Even with years of data science projects behind me, the habit of monitoring, measuring performance, and structuring things properly, I wasn't immune. We underestimated certain projects, we pushed too fast, and we ran into each of these mistakes firsthand.

And I keep seeing teams repeat them, often in the same order: they move too fast, they don't communicate enough about the limits, they underestimate the complexity, they lock themselves into a framework, and they forget to measure.

RAG isn't a product you install and forget. It's a **living system** that demands rigor, patience, and above all a solid understanding of the data and the business need. The technical part comes after. That's the through-line of everything I've learned in the field.

If you want to go deeper on the technical side, I've written about [the 4 technical causes of RAG failure](les-4-causes-techniques-echec-rag.md) and [error analysis as an improvement method](pourquoi-le-rag-ne-fonctionne-pas.md). And at the level of day-to-day behaviors, these 5 methodological mistakes play out as more specific reflexes that sabotage projects daily: I've listed seven of them in [the 7 bad habits of RAG teams](mauvais-reflexes-equipes-rag.md), with the fix to apply for each one.

***

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
