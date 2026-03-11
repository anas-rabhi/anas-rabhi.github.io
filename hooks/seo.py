"""SEO hook: dynamic meta descriptions for category and archive pages."""


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
