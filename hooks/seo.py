"""SEO hook: dynamic meta descriptions for category/archive pages + sitemap cleanup."""

import os
import re


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
    """Set unique meta descriptions for blog category and archive pages."""
    url = page.url or ""
    title = page.title or ""

    is_notebook = url.startswith("notebooks/")

    if "/category/" in url:
        if is_notebook:
            page.meta["description"] = (
                f"Notebooks et tutoriels {title} : guides pratiques "
                f"et implémentations en IA et Data Science. "
                f"Par Anas Rabhi, consultant Data Scientist freelance."
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
        else:
            page.meta["description"] = (
                f"Articles publiés en {title} sur l'IA en entreprise : "
                f"RAG, LLM, agents IA et NLP. "
                f"Par Anas Rabhi, consultant Data Scientist freelance."
            )

    return context
