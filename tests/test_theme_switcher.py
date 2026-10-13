import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_base_template_bootstraps_dark_first_theme_and_renders_toggle():
    base = read("theme/base.html")

    assert "energyatlas-wiki-theme" in base
    assert "document.documentElement.dataset.theme = theme" in base
    assert "prefers-color-scheme: light" in base
    assert 'id="wiki-theme-toggle"' in base
    assert 'aria-pressed="false"' in base
    assert '<span class="wiki-theme-toggle-track" aria-hidden="true">' in base
    assert "Edit on GitHub" not in base
    assert not re.search(r">\s*Edit\s*<", base)
    assert not re.search(r">\s*View on GitHub\s*<", base)
    assert 'aria-label="Edit this page"' in base
    assert 'aria-label="View GitHub repository"' in base
    assert 'class="wiki-sidebar-tool"' in base
    assert 'class="wiki-sidebar-tool-edit-icon"' in base
    assert 'class="wiki-sidebar-tool-github-icon"' in base
    assert 'href="{{ page.edit_url }}"' in base
    assert 'href="{{ config.repo_url }}"' in base
    assert base.index('class="wiki-sidebar-brand"') < base.index('id="wiki-space-switcher"')
    assert base.index('id="wiki-space-switcher"') < base.index('id="wiki-theme-toggle"')
    assert base.index('id="wiki-theme-toggle"') < base.index('href="{{ page.edit_url }}"')


def test_theme_script_is_loaded_before_plotly_renderer():
    config = read("mkdocs.yml")

    theme_script = "assets/js/theme-toggle.js"
    plotly_renderer = "assets/js/plotly-render.js"

    assert theme_script in config
    assert config.index(theme_script) < config.index(plotly_renderer)


def test_theme_tokens_exist_for_both_themes():
    css = read("docs/assets/css/main.css")

    assert ':root[data-theme="light"]' in css
    assert "--plotly-font-color" in css
    assert ".wiki-theme-toggle" in css
    assert "--wiki-theme-toggle-width: 4rem;" in css
    assert ".wiki-theme-toggle-thumb" in css
    assert ':root[data-theme="dark"] .wiki-theme-toggle-thumb' in css
    assert '.wiki-theme-toggle[data-theme="dark"] .wiki-theme-toggle-thumb' not in css
    assert "z-index: 1;" in css
    assert "z-index: 2;" in css
    assert "--wiki-sidebar-width: 17rem;" in css
    assert "--wiki-article-max-width: 60rem;" in css
    assert ".wiki-space-switcher" in css
    assert "scrollbar-gutter: stable;" in css
    assert ".wiki-sidebar-tools" in css
    assert ".wiki-sidebar-tool .wiki-sidebar-tool-github-icon" in css
    assert "fill: currentColor;" in css
    assert "stroke: none;" in css

    # The active page is marked by an accent edge, not a filled block (spec 0.7).
    active_link_block = css.split(".wiki-space-tree-link.active {", 1)[1].split("}", 1)[0]
    assert "box-shadow: inset 2px 0 0 var(--ui-accent);" in active_link_block
    assert "background" not in active_link_block

    syntax = read("docs/assets/css/syntax.css")
    assert '[data-theme="light"] .code-block-body .n' in syntax


def test_theme_toggle_controller_persists_choice_and_announces_changes():
    script = read("docs/assets/js/theme-toggle.js")

    assert "energyatlas-wiki-theme" in script
    assert "localStorage.setItem" in script
    assert "prefers-color-scheme: dark" in script
    assert "aria-pressed" in script
    assert "energyatlas-theme-change" in script


def test_wiki_shell_controller_manages_accessible_drawer():
    script = read("docs/assets/js/wiki-shell.js")

    assert "wiki-sidebar-open" in script
    assert "aria-expanded" in script
    assert "setSidebarAvailable" in script
    assert "sidebar.setAttribute('inert', '')" in script
    assert "Escape" in script
    assert "focusableSelector" in script
    assert "matchMedia('(min-width: 1081px)')" in script


def test_plotly_renderer_reads_css_theme_tokens_and_reacts_to_theme_change():
    script = read("docs/assets/js/plotly-render.js")

    assert "getThemePlotlyDefaults" in script
    assert "getComputedStyle(document.documentElement)" in script
    assert "energyatlas-theme-change" in script
    assert "Plotly.react" in script
