 ---                                                                                                                      
  Audit SEO complet — ianas.fr                                                                                             
                                                                                                                           
  Score SEO global : 52/100                                                                                                
                                                                                                                           
  ┌──────────────────────────────┬────────┬───────┐
  │          Catégorie           │ Score  │ Poids │
  ├──────────────────────────────┼────────┼───────┤
  │ SEO Technique                │ 55/100 │ 25%   │
  ├──────────────────────────────┼────────┼───────┤
  │ Qualité du contenu           │ 72/100 │ 25%   │
  ├──────────────────────────────┼────────┼───────┤
  │ SEO On-Page                  │ 40/100 │ 20%   │
  ├──────────────────────────────┼────────┼───────┤
  │ Schema / Données structurées │ 50/100 │ 10%   │
  ├──────────────────────────────┼────────┼───────┤
  │ Performance                  │ 65/100 │ 10%   │
  ├──────────────────────────────┼────────┼───────┤
  │ Images                       │ 35/100 │ 5%    │
  ├──────────────────────────────┼────────┼───────┤
  │ AI Search Readiness          │ 55/100 │ 5%    │
  └──────────────────────────────┴────────┴───────┘

  ---
  Top 5 problemes critiques

  1. Pas de balises Open Graph / Twitter Cards — aucun partage social ne rend bien
  2. lang="fr" manquant sur toutes les pages (config language: fr absente de mkdocs.yml)
  3. Title de la homepage generique — juste "Intelligence artificielle", pas de branding
  4. Meta description homepage trop courte — 55 caracteres au lieu de 120-160
  5. Pas de og:image / image dans le JSON-LD Article — ineligible aux rich results Google

  Top 5 Quick Wins

  1. Ajouter language: fr dans mkdocs.yml (+impact accessibilite et SEO)
  2. Ajouter les balises Open Graph et Twitter Card dans main.html
  3. Personnaliser le title et la meta description de la homepage
  4. Ajouter dateModified dans le schema Article
  5. Mettre a jour le copyright de 2025 a 2026

  ---
  1. SEO Technique (55/100)

  robots.txt — OK

  User-agent: *
  Allow: /
  Disallow: /*?q=
  Sitemap: https://ianas.fr/sitemap.xml
  - Les pages de recherche interne sont bien bloquees
  - Le sitemap est reference
  - Minor : les 2 regles Disallow sont redondantes (/*?q=* couvre deja /*?q=)

  Sitemap — Problemes detectes

  - 31 URLs listees, ce qui est correct pour la taille du site
  - Toutes les lastmod sont identiques (2026-02-23) = date de build, pas de vraie date de modification. Les crawlers ne
  peuvent pas prioriser le contenu frais
  - Les pages d'archive, categorie et pagination sont incluses (bruit pour le crawl budget)
  - Pas de changefreq ni priority (impact faible)

  Canonical URLs — Inconsistant

  - Le template main.html genere une canonical, mais la homepage ne semble pas en avoir
  - MkDocs Material genere aussi sa propre canonical → risque de doublon
  - Risque : duplication de contenu (avec/sans slash, parametres de requete)

  lang attribute — MANQUANT

  - Aucun lang="fr" sur la balise <html>
  - Cause : la config language: fr manque dans mkdocs.yml sous theme:
  - Impact : nuit a l'accessibilite et au classement dans les resultats francophones

  Navigation — Features desactivees

  Plusieurs features de Material sont commentees dans mkdocs.yml :
  - navigation.instant — desactive le prefetch (perd en performance percue)
  - navigation.instant.prefetch — meme chose
  - navigation.tabs.sticky — les tabs disparaissent au scroll

  HTTPS et securite

  - Le site est bien en HTTPS
  - Widget Heeya charge en async (bon)

  ---
  2. Qualite du contenu (72/100)

  Points forts

  - 15 articles bien structures avec un maillage interne solide entre les articles RAG
  - Descriptions meta presentes dans le frontmatter de 14/15 articles (manquante sur new_genai_frameworks.md)
  - Contenu entre 500 et 2600 mots par article, longueur correcte
  - Tags et categories coherents et bien organises
  - Bonne expertise E-E-A-T : retours d'experience terrain, cas clients concrets

  Problemes

  │                       Probleme                       │                Articles concernes                │ Severite │
  ├──────────────────────────────────────────────────────┼──────────────────────────────────────────────────┼──────────┤
  │ Pas de H1 dans le contenu (le titre frontmatter sert │ La plupart commencent par H2                     │ Medium   │
  │  de H1 via Material)                                 │                                                  │          │
  ├──────────────────────────────────────────────────────┼──────────────────────────────────────────────────┼──────────┤
  │ new_genai_frameworks.md n'a pas de description       │ 1 article                                        │ High     │
  ├──────────────────────────────────────────────────────┼──────────────────────────────────────────────────┼──────────┤
  │ Articles courts (<700 mots)                          │ les-4-causes-techniques-echec-rag.md,            │ Medium   │
  │                                                      │ le-rag-est-fini.md                               │          │
  ├──────────────────────────────────────────────────────┼──────────────────────────────────────────────────┼──────────┤
  ├──────────────────────────────────────────────────────┼──────────────────────────────────────────────────┼──────────┤
  │ Aucun article n'a de meta title explicite            │ Tous                                             │ Medium   │
  └──────────────────────────────────────────────────────┴──────────────────────────────────────────────────┴──────────┘

  Maillage interne

  - Bon maillage entre les articles RAG (les articles se referencent mutuellement)
  - Les liens vers heeya.fr et tensoria.fr sont presents
  - Manque : pas de liens depuis les articles vers la page d'accueil / page contact

  ---
  3. SEO On-Page (40/100)

  Title tags

  ┌──────────┬─────────────────────────────────────────────┬────────────────────────────────────┐
  │   Page   │                Title actuel                 │              Probleme              │
  ├──────────┼─────────────────────────────────────────────┼────────────────────────────────────┤
  │ Homepage │ Intelligence artificielle                   │ Trop generique, pas de branding    │
  ├──────────┼─────────────────────────────────────────────┼────────────────────────────────────┤
  │ Blog     │ Blog - Intelligence artificielle            │ Generique                          │
  ├──────────┼─────────────────────────────────────────────┼────────────────────────────────────┤
  │ Articles │ [Titre article] - Intelligence artificielle │ Format OK mais site_name generique │
  └──────────┴─────────────────────────────────────────────┴────────────────────────────────────┘

  Recommandation : Changer site_name en Anas Rabhi - IA ou utiliser des meta titles explicites.

  Meta descriptions

  ┌────────────┬─────────────────────────────────────────────────────────────┬─────────────┬─────────────────┐
  │    Page    │                         Description                         │  Longueur   │     Verdict     │
  ├────────────┼─────────────────────────────────────────────────────────────┼─────────────┼─────────────────┤
  │ Homepage   │ "Articles techniques autour de l'intelligence artificielle" │ 55 car.     │ Trop court      │
  ├────────────┼─────────────────────────────────────────────────────────────┼─────────────┼─────────────────┤
  │ Blog index │ Herite de la homepage                                       │ 55 car.     │ Trop court      │
  ├────────────┼─────────────────────────────────────────────────────────────┼─────────────┼─────────────────┤
  │ Articles   │ Frontmatter description                                     │ 80-200 car. │ Generalement OK │
  └────────────┴─────────────────────────────────────────────────────────────┴─────────────┴─────────────────┘

  Open Graph — ABSENT

  - Aucune balise og:* sur la homepage
  - Les articles de blog ont og:type, og:title, og:description, og:url via Material
  - og:image absent partout — les partages LinkedIn/Twitter n'ont aucune image

  Twitter Cards — ABSENT

  - Aucune balise twitter:card, twitter:title, etc.
  - Impact direct sur la visibilite des partages sur X/Twitter

  ---
  4. Schema / Donnees structurees (50/100)

  Ce qui est en place

  - WebSite schema sur la homepage (via main.html)
  - Article schema sur les articles de blog avec headline, description, author, publisher, datePublished

  Ce qui manque

  ┌───────────────────────────────────────────┬──────────────────────────────────────────────────────┐
  │             Element manquant              │                        Impact                        │
  ├───────────────────────────────────────────┼──────────────────────────────────────────────────────┤
  │ image dans Article schema                 │ Ineligible aux rich results Google                   │
  ├───────────────────────────────────────────┼──────────────────────────────────────────────────────┤
  │ dateModified                              │ Google recommande fortement                          │
  ├───────────────────────────────────────────┼──────────────────────────────────────────────────────┤
  │ articleSection, keywords                  │ Aide a la classification                             │
  ├───────────────────────────────────────────┼──────────────────────────────────────────────────────┤
  │ SearchAction dans WebSite schema          │ Pas de sitelinks searchbox                           │
  ├───────────────────────────────────────────┼──────────────────────────────────────────────────────┤
  │ sameAs dans l'auteur                      │ Pas de liens vers les profils sociaux dans le schema │
  ├───────────────────────────────────────────┼──────────────────────────────────────────────────────┤
  │ inLanguage                                │ Manque le signal de langue                           │
  ├───────────────────────────────────────────┼──────────────────────────────────────────────────────┤
  │ publisher devrait etre Organization       │ Google prefere Organization avec logo                │
  ├───────────────────────────────────────────┼──────────────────────────────────────────────────────┤
  │ Schema Blog ou CollectionPage pour /blog/ │ Le blog utilise le schema WebSite                    │
  └───────────────────────────────────────────┴──────────────────────────────────────────────────────┘

  ---
  5. Performance (65/100)

  - Plugin minify active (bon, reduit le HTML)
  - navigation.instant desactive — chaque navigation est un full page reload
  - Widget Heeya charge en async (bon, non bloquant)
  - Font Google (Roboto) chargee en externe — potentiel impact LCP
  - Pas de lazy loading d'images configure

  ---
  6. Images (35/100)

  - Tres peu d'images dans les articles — c'est un manque pour le SEO images et l'engagement
  - Pas de og:image configure nulle part
  - Quand des images sont presentes, elles ont generalement un alt text (ex: comprendre-l-IA-guide.md)
  - Pas de favicon configure correctement — favicon: assets/favicon.png est defini mais le fichier docs/assets/ ne semble
  pas contenir de fichiers

  ---
  7. AI Search Readiness (55/100)

  Points forts

  - Structure en questions/reponses dans certains articles (FAQ dans utiliser-chatgpt-efficacement.md)
  - Expertise demontree avec des cas clients concrets
  - Bon maillage thematique autour du RAG

  Points faibles

  - Pas de schema FAQPage sur les articles avec des FAQ
  - Pas de speakable schema
  - Les descriptions pourraient etre plus "citables" (phrases declaratives claires)

  ---
  Plan d'action prioritise

  CRITIQUE (a faire immediatement)

  1. Ajouter language: fr dans mkdocs.yml :
  theme:
    name: material
    language: fr
  2. Ameliorer le title et la description du site dans mkdocs.yml :
  site_name: Anas Rabhi - Consultant IA
  site_description: >-
    Blog et retours d'expérience sur l'IA en entreprise : RAG, agents IA,
    NLP et LLMOps. Par Anas Rabhi, consultant Data Scientist freelance.
  3. Ajouter les balises Open Graph et Twitter Cards dans main.html
  4. Ajouter image au schema Article dans main.html

  HIGH (dans la semaine)

  5. Ajouter une meta description dediee pour la page /blog/
  6. Ajouter une description a new_genai_frameworks.md
  7. Creer une image OG par defaut et la configurer
  8. Ajouter dateModified dans le schema Article
  9. Mettre a jour le copyright a 2026

  MEDIUM (dans le mois)

  10. Activer navigation.instant et navigation.instant.prefetch pour ameliorer la performance percue
  11. Ajouter des images/schemas dans les articles (au moins une par article)
  12. Enrichir le schema WebSite avec SearchAction et sameAs
  13. Ajouter un schema FAQPage pour les articles contenant des FAQ
  14. Differencier les lastmod dans le sitemap (plugin ou hook custom)

  LOW (backlog)

  15. Nettoyer les regles redondantes du robots.txt
  16. Considerer noindex sur les pages d'archive/categorie/pagination
  17. Ajouter des hreflang pour les 2 articles en anglais
  18. Configurer le publisher comme Organization avec logo dans le schema