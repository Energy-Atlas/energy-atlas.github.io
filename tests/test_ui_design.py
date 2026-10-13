"""Checks for the rules of design/ui-design-spec.md, section 0."""

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CSS_DIR = ROOT / "docs" / "assets" / "css"


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def front_matter(path: str) -> str:
    text = read(path)
    if not text.startswith("---\n"):
        return ""
    return text.split("---\n", 2)[1]


def test_spec_is_versioned_outside_the_published_docs():
    spec = read("design/ui-design-spec.md")

    assert "## 0. EnergyAtlas Wiki Implementation Decisions" in spec
    assert "section 0 wins" in spec
    assert "design/ui-design-spec.md" in read("AGENTS.md")


def test_fonts_are_self_hosted_with_their_licences():
    fonts_css = read("docs/assets/css/fonts.css")
    font_files = re.findall(r'url\("\.\./fonts/([^"]+)"\)', fonts_css)

    assert {"Geist", "Geist Mono", "Cormorant Garamond"} <= set(re.findall(r'font-family: "([^"]+)";', fonts_css))
    assert font_files
    for name in font_files:
        assert (ROOT / "docs" / "assets" / "fonts" / name).is_file(), name
    for licence in ("OFL-Geist.txt", "OFL-GeistMono.txt", "OFL-CormorantGaramond.txt"):
        assert (ROOT / "docs" / "assets" / "fonts" / licence).is_file(), licence

    base = read("theme/base.html")
    assert "'assets/fonts/geist-latin.woff2' | url" in base
    assert "'assets/fonts/geist-mono-latin.woff2' | url" in base


def test_no_page_asset_requests_a_font_host():
    paths = [*CSS_DIR.glob("*.css"), ROOT / "theme" / "base.html", ROOT / "theme" / "main.html", ROOT / "mkdocs.yml"]
    for path in paths:
        text = path.read_text(encoding="utf-8")
        assert "fonts.googleapis.com" not in text, path.name
        assert "fonts.gstatic.com" not in text, path.name


def test_stylesheets_are_loaded_fonts_first():
    config = read("mkdocs.yml")

    fonts = config.index("assets/css/fonts.css")
    main = config.index("assets/css/main.css")
    syntax = config.index("assets/css/syntax.css")
    assert fonts < main < syntax
    assert "statusBar.css" not in config
    assert "  - md_in_html" in config


def test_surfaces_are_square_and_flat():
    css = read("docs/assets/css/main.css")

    for value in re.findall(r"border-radius:\s*([^;]+);", css):
        assert value.strip() == "0", value
    # The only gradient is the hover wash of the Welcome icon cards (spec 0.13).
    assert css.count("linear-gradient") == 1
    gradient_rule = css.split("linear-gradient", 1)[0].rsplit("}", 1)[1]
    assert ".ui-cards" in gradient_rule
    assert "backdrop-filter" not in css


def test_red_is_reserved_for_errors():
    for path in CSS_DIR.glob("*.css"):
        text = path.read_text(encoding="utf-8").lower()
        assert "#f1392a" not in text, path.name
        assert "#c92d22" not in text, path.name
        assert "--secondary-color" not in text, path.name

    css = read("docs/assets/css/main.css")
    uses = re.findall(r"([^{}]+)\{[^}]*var\(--ui-error\)", css)
    assert uses
    assert all("error" in selector for selector in uses), uses


def test_contrast_adjusted_tokens_are_used():
    css = read("docs/assets/css/main.css")
    dark = css.split(":root {", 1)[1].split("}", 1)[0]
    light = css.split(':root[data-theme="light"] {', 1)[1].split("}", 1)[0]

    assert "--ui-text-muted: #999999;" in dark
    assert "--ui-border-interactive: #6b6b6b;" in dark
    assert "--ui-text-muted: #5f6b7a;" in light
    assert "--ui-border-interactive: #768599;" in light


def test_strips_are_opt_in_per_page():
    main = read("theme/main.html")
    assert "page.meta.overview %} wiki-overview" in main

    overview_pages = [
        "docs/quick-start/index.md",
        "docs/workflows/index.md",
        "docs/architecture/index.md",
        "docs/library/index.md",
        "docs/user-stories/index.md",
        "docs/workflows/shading/index.md",
        "docs/web-api/development/index.md",
        "docs/web-api/development/web/index.md",
    ]
    for path in overview_pages:
        assert "overview: true" in front_matter(path), path

    for path in ("docs/python/index.md", "docs/web-api/index.md", "docs/wiki-guide/index.md"):
        assert "overview: true" not in front_matter(path), path


def test_welcome_page_has_hero_then_cover_then_subspace_grid():
    welcome = read("docs/quick-start/index.md")

    hero = welcome.index('<div class="ui-hero">')
    cover = welcome.index("software-interface-cover.png")
    grid = welcome.index('<div class="ui-grid ui-cards" markdown>')
    assert hero < cover < grid
    assert "<span>EnergyAtlas</span>" in welcome
    assert "<em>agentic digital twins for city-scale energy insights.</em>" in welcome

    cards = re.findall(r'^-   <span class="ui-icon" data-icon="([a-z-]+)"></span>\[([^\]]+)\]\(',
                       welcome.split('<div class="ui-grid ui-cards" markdown>', 1)[1], re.MULTILINE)
    cells = [title for _, title in cards]
    for slug, _ in cards:
        assert (ROOT / "theme" / "icons" / "subspaces" / f"{slug}.svg").is_file(), slug
    assert cells == [
        "Quick Start",
        "Workflows",
        "Architecture",
        "Python",
        "WebAPI",
        "Library",
        "User Stories",
        "Wiki Guide",
    ]


def test_breadcrumbs_follow_the_full_navigation_ancestry():
    main = read("theme/main.html")

    assert "page.ancestors | reverse" in main
    assert 'class="wiki-breadcrumbs-sep"' in main


def test_page_changes_do_not_fade_the_content():
    base = read("theme/base.html")

    assert "fadeOutContent" not in base
    assert "fadeInContent" not in base
    assert "<style>" not in base


def test_the_root_asset_mirror_is_gone():
    assert not (ROOT / "assets").exists()
    assert not (ROOT / "wiki-template.html").exists()


def test_frame_is_centred_beside_a_sidebar_with_its_own_rule():
    css = read("docs/assets/css/main.css")

    frame = css.split(".wiki-page-shell .menu-content {", 1)[1].split("}", 1)[0]
    assert "margin: 0 auto;" in frame
    sidebar = css.split(".wiki-sidebar {", 1)[1].split("}", 1)[0]
    assert "box-shadow: 1px 0 0 var(--ui-border-subtle);" in sidebar


def test_development_notice_floats_and_repeats_in_the_sidebar():
    css = read("docs/assets/css/main.css")
    base = read("theme/base.html")

    banner = css.split(".wiki-dev-notice-banner {", 1)[1].split("}", 1)[0]
    assert "position: fixed;" in banner
    assert "right: 1.5rem;" in banner
    assert "left:" not in banner
    assert "body.wiki-has-dev-banner" not in css

    # The sidebar copy sits at the bottom of the sidebar body, after the page tree and before the tool row.
    assert base.index('class="wiki-space-navigation"') < base.index('class="wiki-sidebar-notice"')
    assert base.index('class="wiki-sidebar-notice"') < base.index('class="wiki-sidebar-tools"')
    assert base.count("EnergyAtlas Wiki is still under active development.") == 2


def test_icon_hook_inlines_icon_and_backdrop():
    import hooks.icons as icons

    html = icons.on_page_content('<p><span class="ui-icon" data-icon="workflows"></span><a href="x">W</a></p>', None, {}, [])
    assert '<span class="ui-icon ui-icon-workflows" aria-hidden="true"><svg' in html
    assert '<span class="ui-card-backdrop" aria-hidden="true"><svg' in html
    assert "hooks/icons.py" in read("mkdocs.yml")


def test_icon_cards_hover_with_gradient_and_cropped_backdrop():
    css = read("docs/assets/css/main.css")

    card = css.split(".md-content .ui-cards > :is(ul, ol) > li {", 1)[1].split("}", 1)[0]
    assert "overflow: hidden;" in card
    backdrop = css.split(".md-content .ui-cards .ui-card-backdrop {", 1)[1].split("}", 1)[0]
    assert "left: 70%;" in backdrop
    assert "top: 72%;" in backdrop
    assert "width: 105%;" in backdrop
    assert "linear-gradient" in css.split(".md-content .ui-cards > :is(ul, ol) > li::before {", 1)[1].split("}", 1)[0]
