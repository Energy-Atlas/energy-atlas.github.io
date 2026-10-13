from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_main_template_renders_central_page_footer():
    main = read("theme/main.html")

    assert "wiki-page-footer" in main
    assert "wiki-article-nav" in main
    assert "page.meta.previous_article" in main
    assert "page.meta.next_article" in main
    assert "wiki-article-nav-icon" in main
    assert "\u2190" not in main
    assert "\u2192" not in main
    next_button_start = main.index("wiki-article-nav-button wiki-article-nav-button-next")
    next_button_end = main.index("wiki-article-nav-label\">Next", next_button_start)
    next_button = main[next_button_start:next_button_end]
    assert next_button.index("{{ page.meta.next_article.title }}") < next_button.index("wiki-article-nav-icon")
    assert main.index("wiki-article-nav") < main.index("wiki-page-footer-separator")
    assert main.index("wiki-page-footer-separator") < main.index("Last page update")
    assert "Last page update {{ page.meta.page_updated_at or \"Unknown\" }}" in main
    assert "Last website update {{ config.extra.website_updated_at or \"Unknown\" }}" in main
    assert "Found an issue on this page?" in main


def test_article_navigation_styles_exist():
    css = read("docs/assets/css/main.css")

    assert ".md-content .wiki-article-nav-button" in css
    assert ".wiki-article-nav-icon" in css
