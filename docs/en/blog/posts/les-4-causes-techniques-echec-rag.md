---
title: "4 Technical Causes of RAG Failure (and How to Fix Them)"
slug: les-4-causes-techniques-dechec-dun-rag-et-comment-les-corriger
description: "Why your RAG plateaus at 50-70%: parsing, chunking, retrieval, LLM. A fast cause-by-cause diagnosis with concrete fixes from real projects."
categories:
  - "Blog"
  - "AI"
  - "RAG"
tags:
  - "RAG"
  - "Optimisation"
  - "Retrieval"
  - "LLM"
  - "Artificial Intelligence"
  - "AI Architecture"
date: 2026-02-05
comments: true
authors:
  - Anas
pin: false
math: true
mermaid: true
---

## Introduction

A "basic" RAG is quick to set up, but it often plateaus between 50 and 70% correct answers. In a business context, that's not good enough for reliable use.

If you're looking for an **error analysis method** to prioritize improvement actions, the dedicated article is here:  
[My RAG isn't working: why error analysis changes everything](pourquoi-le-rag-ne-fonctionne-pas.md)

If you want to first understand **why RAG remains useful despite large context windows**, I have a dedicated article:  
[Is RAG really dead?](le-rag-est-fini.md)

Here, we focus on the other question: **why a RAG doesn't answer correctly, and how to improve it**.

<!-- more -->

> To understand the technical foundations of a RAG before diagnosing its failures, see the [complete RAG guide](/rag/).

## Technical cause 1: The LLM isn't good enough

This case is the simplest. In general, with the right context, the latest LLMs know how to respond.

When is the LLM the problem? Often when it's drowning in information: we retrieve too many chunks, sometimes not relevant enough, and the real information gets lost.

How to fix it? Either choose a better model, or optimize the number of chunks to retrieve. But that's a separate project.

## Technical cause 2: Document parsing is insufficient

Parsing means correctly extracting information from documents. Example: an invoice needs to be extracted in a structured way. Tables are a classic case: depending on their format, retrieving columns and rows can become very complex. Even images are a problem, unless you describe them via an LLM and insert the description into the text.

Parsing is one of the biggest problems in RAG. Getting clean parsing is hard, because every company structures its documents differently (tables, images, formulas, charts, etc.). Parsing is therefore specific to each document type, even if solutions exist that attempt to generalize (for example docling: https://www.docling.ai/). I've dedicated a full article to this topic with an honest comparison of 2026 tools (Docling, Unstructured, LlamaParse, Marker) and two concrete client cases (industrial and e-commerce): [PDF parsing for RAG, how to really extract data from your documents](parsing-pdf-rag-extraction-documents.md).

## Technical cause 3: The information isn't in the provided context

Sometimes we don't retrieve the right documents: the query is vague or doesn't match well with the vector database.

In this case, the problem may come from **chunking**. Example: a PDF where the last paragraph is split across two pages, with a chunking method that cuts by page. Result: the paragraph is split into two chunks, and the LLM can't find the right information.

If that's the cause (which you can determine by analyzing errors, see this [article](pourquoi-le-rag-ne-fonctionne-pas.md)), you need to work on chunking: chunk size, splitting method, overlap, etc.

## Technical cause 4: The information isn't in the documents (and chunking is fine)

Sometimes, even with good chunking, the problem comes from the **retriever**. The retriever fetches relevant chunks and injects them into the prompt. If it doesn't find the right chunks, the LLM won't be able to answer.

Often, the search is semantic. We use an embeddings model to vectorize documents, then the user's question, and compare the vectors (with the same model, otherwise it makes no sense).

You can optimize the embedding model, especially if you're using an open-source model like `BAAI/bge-m3` (https://huggingface.co/BAAI/bge-m3). If you're using a model like OpenAI's `text-embedding-3-large`, you're already on something very performant, unless your vocabulary is very specific (niche domain). In that case, fine-tuning is an option, but one to consider after the others.

A very effective method is to **combine semantic search and keyword search**, using BM25-type techniques (https://en.wikipedia.org/wiki/Okapi_BM25). I've detailed the practical implementation of [hybrid RAG BM25 + vector](rag-hybride-bm25-vectoriel.md) in a dedicated article. In some cases, you see quality gains of 10 to 20%. Example: on an e-commerce site, a query about a color can be handled poorly by semantic search; adding keyword search forces chunks that contain the color.

Finally, even with all that, the retriever may not reach the target performance (aiming for 100% correct answers isn't realistic). A frequent cause: the search is based on the **question**, whereas what we want to extract is the **answer**. The question can be too short or vague. Techniques exist for this (https://arxiv.org/pdf/2312.10997), like HyDE (Hypothetical Document Embeddings), very useful when the question is poorly formulated. For more on these retrieval levers (reranking, contextual retrieval, query rewriting, etc.), I've written a complete article on [techniques to optimize your RAG](optimiser-rag-techniques.md) with the measured gain for each one.

## Conclusion

A RAG that works well isn't a "magic" RAG: it's a RAG that has been **analyzed, measured, and optimized**. Quality depends on parsing, chunking, the retriever, and the model.

If you'd like, I can also detail a simple audit method to quickly identify the real cause of errors.

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
