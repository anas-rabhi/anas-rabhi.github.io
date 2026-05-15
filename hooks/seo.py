"""SEO hook: meta descriptions, language detection, hreflang pairing, sitemap cleanup."""

import os
import re


FR_EN_PAIRS = {
    "": "en/",
    "a-propos/": "en/a-propos/",
    "blog/": "en/blog/",
    "blog/2026/04/15/chunking-optimal-rag/": "en/blog/2026/04/15/chunking-optimal-rag/",
    "blog/2026/04/22/optimiser-rag-techniques/": "en/blog/2026/04/22/optimiser-rag-techniques/",
    "blog/2026/05/02/entrainement-finetuning-rag-modele-ia/": "en/blog/2026/05/02/entrainement-finetuning-rag-modele-ia/",
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
