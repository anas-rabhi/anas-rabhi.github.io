---
title: Over one year of learning and building with LLMs
date: 2024-08-04 11:30:00 +0800
categories: [Blog, LLM]
tags: [LLM]
pin: true
math: true
mermaid: true
---

## Introduction

This is an evolving draft and there is no real order. I’m just trying to write down whatever comes to mind... 😀

I was telling myself that I need to start writing down what I have been learning since the beginning of LLMs. This field is growing very fast, but there are still many questions remaining unanswered. I have been implementing LLM-based apps since the appearance of these new big models, and I don't know if I will have the chance to be on the front lines of another big step in AI like this one. We are all here discovering new things together and trying to navigate pragmatically, which is not always easy.

## Some personal learnings

>Most of the blog articles about GenAI products said something that I also agree with: "Building 80-90% of the product could take only a few weeks, but the remaining 10-20% could take a few months and a few neurons"— okay, the neurons part I just made it up. More seriously, the LLMs output is not deterministic, so trying to make it reliable for a given task is not easy and takes time.

>It's not just about the LLM; it's about the whole package. The model is very important, but even if we have the best model, a bad UI and a poorly designed product will discourage users. For example, in a RAG application, if we use the best model on the market but have a poor retrieval strategy, the whole product will perform poorly.

>Start simple. Take a few hours to validate if the best LLM (and a VectorDB, if needed) is capable of solving the task.

>An API and a prompt are all we need: no frameworks, no RAG implementation, no agentic workflow... or anything else. When I start a new project, I try to keep it very simple and then grow it step by step, iterating through the whole process.

>Frameworks are nice only if you understand what they really do. Building GenAI apps is pretty simple and straightforward. However, frameworks add a lot of abstractions, and using them without knowing what they really do could significantly impact the performance of the app.

>Iterate quickly. The most important thing when building LLM-based apps is to get user feedback. Making the app available as soon as possible helps significantly in the following steps.

>Evaluations are very important: without evaluations, we can't measure if one prompt performs better than another, or if a reranking method is really working or is useless...

>Each change to the app (prompt, number of chunks, anything...) needs to be evaluated.

>Monitoring LLMs is not easy, and it's very tempting to use generic tools to make myself feel like I am monitoring something lol 

>Prompting is very important, and it takes time (and maybe some of your hair) to find the most efficient one.
