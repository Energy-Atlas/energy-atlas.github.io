"""Inline the subspace icons into page content.

A page writes `<span class="ui-icon" data-icon="workflows"></span>`; the build replaces it with the icon's SVG from
theme/icons/subspaces/, so its ink and accent follow the theme through CSS (design/ui-design-spec.md, 0.13 and 0.15).
Inside a `ui-cards` grid the same icon is also inlined a second time as the card's hover backdrop.
"""

from __future__ import annotations

import re
from functools import lru_cache
from pathlib import Path
from typing import Any

ICON_DIR = Path(__file__).resolve().parents[1] / "theme" / "icons" / "subspaces"
PLACEHOLDER = re.compile(r'<span class="ui-icon" data-icon="([a-z0-9-]+)"></span>')


@lru_cache(maxsize=None)
def icon_svg(name: str) -> str:
    path = ICON_DIR / f"{name}.svg"
    if not path.is_file():
        raise ValueError(f"Unknown icon '{name}': no {path.relative_to(ICON_DIR.parents[2])}")
    return path.read_text(encoding="utf-8").strip()


def render_icon(name: str) -> str:
    svg = icon_svg(name)
    return (
        f'<span class="ui-icon ui-icon-{name}" aria-hidden="true">{svg}</span>'
        f'<span class="ui-card-backdrop" aria-hidden="true">{svg}</span>'
    )


def on_page_content(html: str, page: Any, config: Any, files: Any) -> str:
    return PLACEHOLDER.sub(lambda match: render_icon(match.group(1)), html)
