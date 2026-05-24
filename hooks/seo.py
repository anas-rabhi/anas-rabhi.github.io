"""SEO hook: meta descriptions, language detection, hreflang pairing, sitemap cleanup."""

import os
import re


FR_EN_PAIRS = {
    "": "en/",
    "a-propos/": "en/a-propos/",
    "blog/": "en/blog/",
    "blog/2025/06/21/mais-que-es-le-rag/": "en/blog/2025/06/21/mais-que-es-le-rag/",
    "blog/2025/12/16/c-est-quoi-un-agent-ia/": "en/blog/2025/12/16/c-est-quoi-un-agent-ia/",
    "blog/2026/03/20/agentic-rag-vs-rag-classique/": "en/blog/2026/03/20/agentic-rag-vs-rag-classique/",
    "blog/2026/04/01/rag-hybride-bm25-vectoriel/": "en/blog/2026/04/01/rag-hybride-bm25-vectoriel/",
    "blog/2026/04/15/chunking-optimal-rag/": "en/blog/2026/04/15/chunking-optimal-rag/",
    "blog/2026/04/22/optimiser-rag-techniques/": "en/blog/2026/04/22/optimiser-rag-techniques/",
    "blog/2026/05/02/entrainement-finetuning-rag-modele-ia/": "en/blog/2026/05/02/entrainement-finetuning-rag-modele-ia/",
    "blog/2026/05/15/evaluer-rag-production-metriques-ragas/": "en/blog/2026/05/15/evaluer-rag-production-metriques-ragas/",
    "blog/2026/05/15/mcp-model-context-protocol-agents-ia/": "en/blog/2026/05/15/mcp-model-context-protocol-agents-ia/",
    "blog/2026/05/16/parsing-pdf-rag-extraction-documents/": "en/blog/2026/05/16/parsing-pdf-rag-extraction-documents/",
    "blog/2026/05/19/memoire-agents-ia-long-terme/": "en/blog/2026/05/19/memoire-agents-ia-long-terme/",
    "blog/2026/05/23/mauvais-reflexes-equipes-rag/": "en/blog/2026/05/23/mauvais-reflexes-equipes-rag/",
    "blog/2026/05/29/embeddings-rag-comprendre-importance/": "en/blog/2026/05/29/embeddings-rag-comprendre-importance/",
    "blog/2026/06/02/crewai-langchain-langgraph-comparatif-pragmatique/": "en/blog/2026/06/02/crewai-langchain-langgraph-comparatif-pragmatique/",
}
EN_FR_PAIRS = {v: k for k, v in FR_EN_PAIRS.items()}


def on_post_build(config):
    """Remove pagination pages from sitemap to fix noindex/sitemap conflict."""
    sitemap_path = os.path.join(config["site_dir"], "sitemap.xml")
    if not os.path.exists(sitemap_path):
        return
    with open(sitemap_path, "r", encoding="utf-8") as f:
        content = f.read()
    cleaned = re.sub(
        r"\s*<url>\s*<loc>[^<]*/page/\d+/[^<]*</loc>.*?</url>",
        "",
        content,
        flags=re.DOTALL,
    )
    with open(sitemap_path, "w", encoding="utf-8") as f:
        f.write(cleaned)


def on_page_context(context, page, config, nav):
    """Set meta descriptions, language, and hreflang alternates."""
    url = page.url or ""
    title = page.title or ""

    is_en = url.startswith("en/")
    page.meta["lang"] = "en" if is_en else "fr"

    site_url = config.get("site_url", "").rstrip("/") + "/"
    if is_en and url in EN_FR_PAIRS:
        page.meta["alternate_url_fr"] = site_url + EN_FR_PAIRS[url]
        page.meta["alternate_url_en"] = site_url + url
    elif not is_en and url in FR_EN_PAIRS:
        page.meta["alternate_url_fr"] = site_url + url
        page.meta["alternate_url_en"] = site_url + FR_EN_PAIRS[url]

    is_notebook = url.startswith("notebooks/") or url.startswith("en/notebooks/")
    is_en_blog = url.startswith("en/blog/")

    if "/category/" in url:
        if is_notebook:
            page.meta["description"] = (
                f"Notebooks et tutoriels {title} : guides pratiques "
                f"et implémentations en IA et Data Science. "
                f"Par Anas Rabhi, consultant Data Scientist freelance."
            )
        elif is_en_blog:
            page.meta["description"] = (
                f"{title} articles: field notes, best practices and use cases "
                f"in enterprise AI. By Anas Rabhi, freelance AI Engineer & Data Scientist."
            )
        else:
            page.meta["description"] = (
                f"Articles {title} : retours d'expérience, bonnes pratiques "
                f"et cas d'usage en IA. "
                f"Par Anas Rabhi, consultant Data Scientist freelance."
            )
    elif "/archive/" in url:
        if is_notebook:
            page.meta["description"] = (
                f"Notebooks publiés en {title} : tutoriels et implémentations "
                f"en IA et Data Science. "
                f"Par Anas Rabhi, consultant Data Scientist freelance."
            )
        elif is_en_blog:
            page.meta["description"] = (
                f"Articles published in {title} on enterprise AI: "
                f"RAG, LLMs, AI agents and NLP. "
                f"By Anas Rabhi, freelance AI Engineer & Data Scientist."
            )
        else:
            page.meta["description"] = (
                f"Articles publiés en {title} sur l'IA en entreprise : "
                f"RAG, LLM, agents IA et NLP. "
                f"Par Anas Rabhi, consultant Data Scientist freelance."
            )

    return context
