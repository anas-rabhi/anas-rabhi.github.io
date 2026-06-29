---
title: "Local AI: Running an SLM On-Premise"
slug: ia-locale-on-premise-slm
description: "Local AI: running an SLM locally or on-premise for privacy and cost. Tools (Ollama, vLLM, llama.cpp), quantization, hardware, and limits."
categories:
  - "Blog"
  - "AI"
tags:
  - "SLM"
  - "Local AI"
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
  - question: "Why run an SLM locally?"
    answer: "For three concrete reasons: privacy (your data never leaves your infrastructure, which simplifies GDPR compliance), cost (at high volume, self-hosting becomes cheaper than APIs), and latency (a local model responds faster and works offline). It's especially relevant for sensitive data and regulated industries."
  - question: "Which tool should I use to run an LLM locally?"
    answer: "For the workstation and prototyping, Ollama and LM Studio are the simplest: a single command or a graphical interface is enough. llama.cpp is the underlying engine that runs models in the GGUF format, including on CPU or Mac. For production with throughput, you move to vLLM or Hugging Face's Text Generation Inference, built to serve many requests in parallel."
  - question: "What hardware do I need to run an SLM?"
    answer: "It depends on the size. A model of 1 to 3 billion parameters runs on just about any recent laptop, sometimes on CPU. A 7 to 8 billion model quantized to 4 bits needs about 6 to 8 GB of video memory, or an Apple Silicon Mac with unified memory. Beyond that, you need a real GPU. Quantization is the key to fitting a model on a modest machine."
  - question: "What is quantization (GGUF, 4-bit)?"
    answer: "Quantization reduces the precision of a model's parameters, for example from 16 bits to 4 bits, to shrink its size and speed up inference. GGUF is the most common file format for quantized models run with llama.cpp. A variant like Q4_K_M offers a good trade-off between size and quality. The precision loss is generally small relative to the gain in size and speed."
  - question: "Is local AI GDPR compliant?"
    answer: "Running a model on your own infrastructure avoids sending personal data to an external API, which removes a large part of the data transfer and localization questions. It's not automatic compliance, but it's a major asset for sensitive data. European open-source models like Mistral further strengthen the sovereignty angle."
  - question: "When does self-hosting become profitable?"
    answer: "According to a 2025 study, a model of around 30 billion parameters on a $2,000 consumer GPU becomes profitable against APIs within a few months once you process volume. Indicative thresholds: under 10 million tokens per month, the API stays more advantageous; between 10 and 50 million, self-hosting becomes interesting; beyond that, it wins clearly."
  - question: "Can you build a 100% local RAG?"
    answer: "Yes, and it's the most common use case for local AI in companies. You combine a local embedding model (BGE, E5) for retrieval, a self-hosted vector database (Qdrant or pgvector), and a local SLM for generation. No data leaves your infrastructure, which often makes it the only acceptable architecture for sensitive documents."
---

## Local AI: why and how to run an SLM yourself

Running an SLM locally means executing a language model on your own machine or your own server, without going through an external API. It has become realistic because small models are good enough and light enough for it, and it's often the right choice for three reasons: privacy, cost, and latency.

Concretely, your data never leaves your infrastructure, you no longer pay per token, and the model responds fast, even offline. For a company handling sensitive data or processing volume, those three arguments carry weight.

<!-- more -->

In this article, I cover the why (privacy, GDPR, cost), the tools for running a model locally, how to get started concretely, quantization, the hardware you need, the sovereign RAG case, and the situations where self-hosting makes no sense. If you want to lay the groundwork first, start with my article on [what an SLM is](c-est-quoi-un-slm.md).

## Why run an SLM locally?

Local AI addresses constraints the cloud doesn't remove. Here are the four arguments that keep coming up on engagements.

- **Privacy and GDPR.** Sending sensitive documents to an external API raises data transfer and localization questions. A local model keeps everything on your infrastructure: the data doesn't leave. For regulated industries (healthcare, legal, HR, defense), that single point often tips the balance.
- **Sovereignty.** Beyond GDPR, some organizations want to depend on no foreign provider at all. European open-source models like Mistral's let you build a fully controlled stack.
- **Cost at scale.** Per token, APIs stay unbeatable on small volumes. But as soon as you process volume, self-hosting a small model ends up costing less. I come back to this below with figures.
- **Latency and offline.** A local model has no network round-trip. It responds faster and works without a connection, which opens up embedded use and isolated environments.

These are exactly the kind of constraints that make a RAG on a local LLM unavoidable for sensitive data, a point I also touch on in [long context vs RAG](long-context-vs-rag-quand-utiliser.md).

## The tools for running a model locally

The ecosystem has matured a lot. The main thing is to distinguish workstation tools from production tools.

To **prototype and develop**:

- **Ollama**: the simplest tool to launch a model locally. One command, and the model runs. Perfect for testing and for small use cases.
- **LM Studio**: a desktop graphical interface to download and chat with local models, without touching the terminal.
- **llama.cpp**: the C/C++ inference engine that runs models in the GGUF format, including on CPU or Mac. It's the underlying building block of many consumer tools.

For **production**:

- **vLLM**: a high-throughput serving engine. Thanks to its memory management (PagedAttention), it serves many requests in parallel with good efficiency. It's the choice when you need to handle load.
- **Text Generation Inference (TGI)**: Hugging Face's serving solution, designed to deploy models in production.

The simple rule: Ollama or LM Studio to start and test, vLLM or TGI when you scale up and throughput matters.

## From the local model to your code: the OpenAI-compatible API

With Ollama, you pull and launch a model in two commands: installing the tool, then `ollama run qwen3`, which downloads the quantized version and starts the model. You can then talk to it in the terminal.

The value for a technical team comes down to an implementation detail: Ollama, vLLM, and TGI all expose an API compatible with OpenAI's. The routes, the request format, and the response format are identical. So code that already calls GPT or Claude keeps working by changing just two things: the server URL and the model name. The same `chat.completions.create(...)` call then queries your local model. Plugging a prototype onto a local model is a matter of configuration, not rewriting.

This is also what simplifies the move to production: you prototype with Ollama on your machine, then replace the server with vLLM or TGI, which expose the same interface but absorb the load. The application code doesn't change, only the component that serves the model does.

## Quantization: fitting a model on a modest machine

Quantization is what makes local AI accessible: without it, most small models would remain too heavy for an ordinary machine.

Quantization reduces the precision of the parameters, for example from 16 bits to 4 bits. This divides the model's size and speeds up inference, with a generally small loss of quality. The most common format on the local side is **GGUF**, used by llama.cpp, with variants like **Q4_K_M** that offer a good size/quality trade-off. On the GPU side, you also come across the **AWQ** and **GPTQ** methods.

Microsoft's technical report on [Phi-3](https://arxiv.org/abs/2404.14219) gives a telling measurement: a model of 3.8 billion parameters, once quantized to 4 bits, fits in about 1.8 GB and runs on an iPhone. A model that used to require a server ends up running on a phone or a laptop.

## What hardware for which model?

The question always comes back: "what kind of machine do I need?". Here are the orders of magnitude, keeping in mind that 4-bit quantization is assumed.

| Model size | What you need | Example models |
|---|---|---|
| 1 to 4 billion | a recent laptop, sometimes the CPU is enough | Llama 3.2 1B/3B, Qwen3 1.7B and 4B, SmolLM3 3B, Phi-4-mini (3.8B), Gemma 4 E2B/E4B |
| 7 to 9 billion | about 6 to 8 GB of video memory, or an Apple Silicon Mac | Qwen3 8B, Ministral 3 8B |
| 10 billion and up | a real GPU (RTX 4090/5090 type) | beyond the SLM scope |

To quickly estimate memory: at 4 bits, count about half a gigabyte per billion parameters, plus some margin for the conversation context. A model of 7 billion therefore fits around 4 to 5 GB of video memory, which works on most recent consumer GPUs.

Macs with unified memory are also a good platform for local inference: the model shares memory between the CPU and the GPU, which lets you load bigger models than with an entry-level graphics card. And a recent consumer GPU is enough for most SLMs, no datacenter hardware needed. For the detail of model families and their sizes, see my article on [what an SLM is](c-est-quoi-un-slm.md).

## The 100% local RAG, on confidential data

If I had to give a single reason to run an SLM locally in a company, it would be RAG on confidential data. It's the case that comes up most often on engagements.

A classic [RAG](mais-que-es-le-rag.md) sends your internal documents to an external API at the moment of generating the answer. For contracts, HR files, or medical data, that's often a dealbreaker. The local version keeps everything on your infrastructure: a local embedding model to index and search (a BGE or E5 model, for example), a self-hosted vector database (Qdrant, or pgvector directly in your PostgreSQL), and a local SLM for generation. At no point does any data leave.

It's a bit more work than a RAG plugged into an API, but for many regulated industries, it's the only acceptable architecture. And an SLM is often enough here, because the task is well-scoped: answer from the passages you feed it. When multi-document reasoning gets heavy, you keep the option of escalating to a large model, as I explain in [SLM vs LLM](slm-vs-llm-quand-choisir.md).

## When does self-hosting become profitable?

This is the question that really decides. And the answer depends on volume.

A 2025 study on the cost of on-premise deployment ([arXiv 2509.18101](https://arxiv.org/abs/2509.18101)) puts a number on the break-even point against APIs. A model of around 30 billion parameters, on a $2,000 consumer GPU, becomes profitable in under 3 months once there's volume. The smaller the model, the faster that return on investment.

The volume thresholds are a good reference point:

- **under 10 million tokens per month**: the API stays more advantageous, the hardware would sit idle;
- **between 10 and 50 million**: self-hosting becomes interesting;
- **beyond 50 million**: it clearly wins.

In other words, local AI isn't just a matter of principle about privacy, it's also an economic calculation that flips with volume. It's the same reasoning I apply to other cost levers like [prompt caching](prompt-caching-reduire-cout-llm.md).

## When you shouldn't self-host

Let's be honest: local AI isn't always the right choice, and selling it as a given would be dishonest.

Stay on an API when:

- **the volume is low.** Below a few million tokens per month, paying for a GPU that runs idle costs more than the API.
- **you need cutting-edge reasoning or very long context.** There, large cloud models stay ahead, and no local SLM replaces them.
- **you don't have the ops skills.** Hosting, monitoring, updating, and securing a model in production takes know-how. Without a team to carry it, the simplicity of an API has value.

There's also a useful middle ground between the public API and full on-premise: the sovereign cloud. Hosting an open-source model with a European provider like OVHcloud or Scaleway keeps your data in the Union without having to manage the hardware yourself. It's often the right compromise when the real constraint is data localization, not physical control of the machine.

The right instinct stays the same as everywhere else: start from the real need, measure, and choose the simplest tool that solves it. Local AI is a solid option when privacy or volume justifies it, not an end in itself.

## FAQ: common questions about local AI

**Why run an SLM locally?**
For privacy (your data doesn't leave your infrastructure), cost (cheaper than APIs at high volume), and latency (fast responses, offline operation). It's mainly relevant for sensitive data and regulated industries.

**Which tool should I use to run an LLM locally?**
Ollama and LM Studio for the workstation and prototyping, llama.cpp as the underlying engine (GGUF format, even on CPU or Mac), and vLLM or TGI for high-throughput production.

**What hardware do I need to run an SLM?**
A model of 1 to 3 billion parameters runs on a recent laptop. A 7 to 8 billion in 4 bits needs about 6 to 8 GB of video memory or an Apple Silicon Mac. Beyond that, you need a real GPU.

**What is quantization (GGUF, 4-bit)?**
It reduces the precision of the parameters to shrink the model's size and speed up inference. GGUF is the most common format for quantized models run with llama.cpp, with variants like Q4_K_M. The quality loss is generally small.

**Is local AI GDPR compliant?**
Running a model on your infrastructure avoids sending personal data to an external API, which removes a large part of the transfer and localization questions. It's not automatic compliance, but a major asset, reinforced by European models like Mistral.

**When does self-hosting become profitable?**
According to a 2025 study, a model of around 30 billion parameters on a $2,000 GPU becomes profitable within a few months once there's volume. Below 10 million tokens per month, the API stays preferable; beyond 50 million, self-hosting wins.

**Can you build a 100% local RAG?**
Yes, it's even the most common use case for local AI in companies. You combine a local embedding model (BGE, E5), a self-hosted vector database (Qdrant or pgvector), and a local SLM for generation. No data leaves your infrastructure, which often makes it the only acceptable architecture for sensitive data.

## Further reading

- **[What is an SLM (Small Language Model)?](c-est-quoi-un-slm.md)**: the definition, the recent models, and why the topic matters in 2026
- **[SLM vs LLM: when to choose a small model?](slm-vs-llm-quand-choisir.md)**: the decision grid between small and large model
- **[How to train an SLM?](entrainer-un-slm.md)**: fine-tuning or distilling a model before deploying it locally
- **[Prompt caching: cut your LLM cost](prompt-caching-reduire-cout-llm.md)**: another cost lever, complementary to self-hosting

If my articles interest you, you have questions, or you just want to discuss your own AI challenges, feel free to write to me at [anas@tensoria.fr](mailto:anas@tensoria.fr), I love talking about these topics!

Want to deploy AI on your own infrastructure to keep your data in-house? Discover my consulting work at [tensoria.fr](https://tensoria.fr).

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
