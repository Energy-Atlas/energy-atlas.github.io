from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


CSS = "docs/assets/css/main.css"


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def block(css: str, selector: str) -> str:
    return css.split(selector, 1)[1].split("}", 1)[0]


def test_base_template_uses_sidebar_icon_as_svg_favicon():
    base = read("theme/base.html")

    favicon = '<link rel="icon" type="image/svg+xml" href="{{ \'assets/images/icon.svg\' | url }}" />'
    sidebar_icon = '<img class="wiki-sidebar-logo" src="{{ \'assets/images/icon.svg\' | url }}"'

    assert favicon in base
    assert sidebar_icon in base
    assert base.index(favicon) < base.index("{% for path in config.extra_css %}")


def test_base_template_renders_subspace_sidebar_and_attached_toc():
    base = read("theme/base.html")

    assert 'id="wiki-sidebar"' in base
    assert 'id="wiki-sidebar-toggle"' in base
    assert 'id="wiki-space-switcher"' in base
    assert "current_space.item.children" in base
    assert 'class="menu-column menu-column-toc"' in base
    assert 'class="toc-heading">On this page' in base
    assert 'class="wiki-topbar"' not in base


def test_mkdocs_navigation_defines_confirmed_subspaces_in_order():
    config = read("mkdocs.yml")
    headings = [
        "  - Quick Start:",
        "  - Workflows:",
        "  - Architecture:",
        "  - Python:",
        "  - WebAPI:",
        "  - Library:",
        "  - User Stories:",
        "  - Wiki Guide:",
    ]

    positions = [config.index(heading) for heading in headings]
    assert positions == sorted(positions)
    assert "EnergyAtlas References" not in config


def test_subspace_switcher_uses_distinct_icons_without_an_eyebrow_label():
    base = read("theme/base.html")

    assert '<span class="wiki-space-switcher-label">Subspace</span>' not in base
    assert "render_space_icon(current_space.item.title)" in base
    assert "render_space_icon(nav_item.title)" in base
    assert 'class="wiki-space-switcher-option-main"' in base
    assert 'class="wiki-space-switcher-check"' in base
    # Every subspace has its own icon from the hand-drawn family, included from theme/icons/subspaces/.
    # The sidebar uses the bold weight; the regular weight is for the Welcome cards.
    assert "{% include 'icons/subspaces/' ~ slug ~ '-bold.svg' %}" in base
    assert 'data-icon-source="energyatlas-hand-drawn"' in base
    assert "lucide" not in base
    for title, slug in (
        ("Quick Start", "quick-start"),
        ("Workflows", "workflows"),
        ("Architecture", "architecture"),
        ("Python", "python"),
        ("WebAPI", "web-api"),
        ("Library", "library"),
        ("User Stories", "user-stories"),
        ("Wiki Guide", "wiki-guide"),
    ):
        assert f"'{title}': '{slug}'" in base
        for variant in (f"{slug}.svg", f"{slug}-bold.svg", f"{slug}-light.svg"):
            icon = read(f"theme/icons/subspaces/{variant}")
            assert 'viewBox="0 0 24 24"' in icon
            assert '<g class="ink"' in icon
            assert '<g class="accent"' in icon

    # The ink follows the row's text colour; the accent takes the theme's accent blue.
    css = read(CSS)
    assert "fill: currentColor;" in block(css, ".wiki-space-icon .ink {")
    assert "fill: var(--ui-accent);" in block(css, ".wiki-space-icon .accent {")
    assert "--ui-icon-accent" not in css
    dropdown = block(css, ".wiki-space-switcher-summary .wiki-space-icon,\n.wiki-space-switcher-option .wiki-space-icon {")
    assert "width: 26px;" in dropdown
    assert ".wiki-space-switcher-option-main {" in css
    assert ".wiki-space-switcher-check {" in css
    assert "--wiki-bar-height: 3.5rem;" in css

    # The switcher row lines up with the brand row and the article's breadcrumb bar (spec 0.7).
    summary_block = block(css, ".wiki-space-switcher-summary {")
    assert "height: var(--wiki-bar-height);" in summary_block
    for selector in (".wiki-sidebar-header {", ".menu-column-header {", ".toc-heading {"):
        assert "height: var(--wiki-bar-height);" in block(css, selector)

    # Subspace names are set in the primary sans, bold, in normal case.
    label_block = block(css, ".wiki-space-switcher-value,\n.wiki-space-switcher-option {")
    assert "font-family: var(--font-sans);" in label_block
    assert "font-weight: 700;" in label_block
    assert "text-transform" not in label_block


def test_wide_tables_use_table_local_horizontal_scrollers():
    base = read("theme/base.html")

    assert "table-scroll-wrapper-wide" in base
    assert "columnCount >= 5" in base
    assert "wrapper.scrollWidth > wrapper.clientWidth" in base
    assert "wrapper.setAttribute('aria-label', 'Scrollable table')" in base

    css = read(CSS)
    assert ".table-scroll-wrapper-wide > table" in css
    assert "width: max-content;" in css
    assert "overscroll-behavior-inline: contain;" in css


def test_desktop_sidebar_has_persistent_animated_collapse_control():
    base = read("theme/base.html")
    shell = read("docs/assets/js/wiki-shell.js")

    assert 'id="wiki-sidebar-collapse"' in base
    assert 'aria-controls="wiki-sidebar"' in base
    assert "energyatlas-wiki-sidebar-collapsed" in base
    assert "setDesktopCollapsed" in shell
    assert "syncCollapsedAccessibility" in shell
    assert "energyatlas-wiki-sidebar-collapsed" in shell

    css = read(CSS)
    assert ':root[data-sidebar-collapsed="true"] .wiki-sidebar' in css
    assert ':root[data-sidebar-collapsed="true"] .wiki-sidebar-tools' in css
    # The tool row keeps its width when the sidebar collapses, so its controls never move.
    assert "width: var(--wiki-sidebar-width);" in block(css, ".wiki-sidebar-tools {")
    assert "width" not in block(css, ':root[data-sidebar-collapsed="true"] .wiki-sidebar-tools {')


def test_scroll_progress_owns_a_separate_full_width_bottom_row():
    base = read("theme/base.html")

    assert 'id="scroll-progress-track"' in base
    assert 'role="progressbar"' in base
    assert 'aria-label="Page scroll progress"' in base
    assert "scrollableHeight > 0" in base
    assert "scrollProgressTrack.setAttribute('aria-valuenow'" in base

    css = read(CSS)
    assert "--wiki-scroll-progress-height: 2px;" in css
    assert "bottom: var(--wiki-scroll-progress-height);" in css
    progress_block = block(css, ".scroll-progress-bar {")
    assert "height: var(--wiki-scroll-progress-height);" in progress_block
    assert "bottom: 0;" in progress_block
    assert "z-index: 3800;" in progress_block
