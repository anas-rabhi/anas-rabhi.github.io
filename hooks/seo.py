"""SEO hook: meta descriptions, language detection, hreflang pairing, sitemap cleanup."""

import os
import re


FR_EN_PAIRS = {
    "": "en/",
    "a-propos/": "en/a-propos/",
    "blog/": "en/blog/",
    "blog/archive/2025/": "en/blog/archive/2025/",
    "blog/archive/2026/": "en/blog/archive/2026/",
    "blog/category/agent-ia/": "en/blog/category/ai-agent/",
    "blog/category/blog/": "en/blog/category/blog/",
    "blog/category/ia/": "en/blog/category/ai/",
    "blog/category/llm/": "en/blog/category/llm/",
    "blog/category/rag/": "en/blog/category/rag/",
}
EN_FR_PAIRS = {v: k for k, v in FR_EN_PAIRS.items()}
_DISCOVERED_BLOG_PAIRS = False


def _absolute_url(site_url, url):
    """Build a normalized absolute URL from a MkDocs page URL."""
    return site_url + (url or "")


def _read_front_matter_value(path, key):
    pattern = re.compile(rf"^{re.escape(key)}:\s*[\"']?([^\"'\n]+)[\"']?\s*$")
    in_front_matter = False
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip() == "---":
                if in_front_matter:
                    return None
                in_front_matter = True
                continue
            if not in_front_matter:
                continue
            if line.strip() == "...":
                return None
            match = pattern.match(line)
            if match:
                return match.group(1).strip()
    return None


def _discover_blog_pairs(config):
    """Pair FR blog plugin URLs with their EN blog plugin translation URLs."""
    global _DISCOVERED_BLOG_PAIRS
    if _DISCOVERED_BLOG_PAIRS:
        return

    docs_dir = config.get("docs_dir", "docs")
    fr_posts_dir = os.path.join(docs_dir, "blog", "posts")
    en_posts_dir = os.path.join(docs_dir, "en", "blog", "posts")
    if not os.path.isdir(fr_posts_dir) or not os.path.isdir(en_posts_dir):
        _DISCOVERED_BLOG_PAIRS = True
        return

    for filename in os.listdir(fr_posts_dir):
        if not filename.endswith(".md"):
            continue
        fr_path = os.path.join(fr_posts_dir, filename)
        en_path = os.path.join(en_posts_dir, filename)
        if not os.path.exists(en_path):
            continue

        fr_date = _read_front_matter_value(fr_path, "date")
        fr_slug = _read_front_matter_value(fr_path, "slug")
        en_date = _read_front_matter_value(en_path, "date")
        en_slug = _read_front_matter_value(en_path, "slug")
        if not fr_date or not fr_slug or not en_date or not en_slug:
            continue

        fr_year, fr_month, fr_day = fr_date.split("-")
        en_year, en_month, en_day = en_date.split("-")
        fr_url = f"blog/{fr_year}/{fr_month}/{fr_day}/{fr_slug}/"
        en_url = f"en/blog/{en_year}/{en_month}/{en_day}/{en_slug}/"
        FR_EN_PAIRS[fr_url] = en_url
        EN_FR_PAIRS[en_url] = fr_url

    _DISCOVERED_BLOG_PAIRS = True


def _set_hreflang_meta(page, config, url, is_en):
    """Populate per-page hreflang data for templates and the language menu."""
    if "/page/" in url:
        return

    _discover_blog_pairs(config)

    site_url = config.get("site_url", "").rstrip("/") + "/"
    if is_en and url in EN_FR_PAIRS:
        fr_url = _absolute_url(site_url, EN_FR_PAIRS[url])
        en_url = _absolute_url(site_url, url)
        x_default_url = fr_url
    elif not is_en and url in FR_EN_PAIRS:
        fr_url = _absolute_url(site_url, url)
        en_url = _absolute_url(site_url, FR_EN_PAIRS[url])
        x_default_url = fr_url
    else:
        self_url = _absolute_url(site_url, url)
        fr_url = None if is_en else self_url
        en_url = self_url if is_en else None
        x_default_url = self_url

    hreflang_urls = []
    if fr_url:
        hreflang_urls.append({"lang": "fr", "url": fr_url})
        page.meta["alternate_url_fr"] = fr_url
    if en_url:
        hreflang_urls.append({"lang": "en", "url": en_url})
        page.meta["alternate_url_en"] = en_url

    page.meta["hreflang_urls"] = hreflang_urls
    page.meta["alternate_url_x_default"] = x_default_url


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
    _set_hreflang_meta(page, config, url, is_en)

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
