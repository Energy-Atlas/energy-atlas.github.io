"""Hand-drawn editorial icon family for the EnergyAtlas Wiki subspaces.

Each icon is authored as a few centrelines on a 24x24 grid. Every centreline is rendered as an ink stroke:
a Catmull-Rom spline, displaced by a small seeded low-frequency wobble, outlined with a width that swells
gently along the stroke and tapers at loose ends, then written as a filled path. The result reads as a
pen line drawn by hand, not as a geometric stroke.

Usage: python design/icons/generate_subspace_icons.py [--out DIR] [icon ...]   (all icons when none given)
Writes <name>.svg and preview.html into DIR (default: tmp/custom-icons/subspace-icons/). Copy the validated SVGs to
theme/icons/subspaces/, which the theme includes inline (design/ui-design-spec.md, section 0.15).
"""

from __future__ import annotations

import math
import random
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parents[2] / "tmp" / "custom-icons" / "subspace-icons"

INK = "#3b3631"       # warm charcoal
ACCENT = "#c2704f"    # muted terracotta

BASE_WIDTH = 1.3      # stroke width in grid units (24-unit canvas)
WOBBLE = 0.09         # displacement amplitude of the hand wobble, grid units
STEP = 0.18           # centreline sampling step, grid units


# ---------------------------------------------------------------------------------------------------------------------
# Geometry helpers
# ---------------------------------------------------------------------------------------------------------------------

def catmull_rom(points, closed=False, step=STEP):
    """Sample a centripetal-ish Catmull-Rom spline through points at roughly `step` spacing."""
    pts = list(points)
    if closed:
        ext = [pts[-1]] + pts + [pts[0], pts[1]]
    else:
        ext = [pts[0]] + pts + [pts[-1]]
    out = []
    for i in range(1, len(ext) - 2):
        p0, p1, p2, p3 = ext[i - 1], ext[i], ext[i + 1], ext[i + 2]
        seg = math.dist(p1, p2)
        n = max(2, int(seg / step))
        for k in range(n):
            t = k / n
            t2, t3 = t * t, t * t * t
            x = 0.5 * ((2 * p1[0]) + (-p0[0] + p2[0]) * t + (2 * p0[0] - 5 * p1[0] + 4 * p2[0] - p3[0]) * t2
                       + (-p0[0] + 3 * p1[0] - 3 * p2[0] + p3[0]) * t3)
            y = 0.5 * ((2 * p1[1]) + (-p0[1] + p2[1]) * t + (2 * p0[1] - 5 * p1[1] + 4 * p2[1] - p3[1]) * t2
                       + (-p0[1] + 3 * p1[1] - 3 * p2[1] + p3[1]) * t3)
            out.append((x, y))
    out.append(pts[0] if closed else pts[-1])
    return out


def arc_points(cx, cy, r, start_deg, end_deg, n=None):
    """Points on a circular arc (degrees, y down), for authoring rings and curves."""
    span = end_deg - start_deg
    n = n or max(6, int(abs(span) / 18))
    return [(cx + r * math.cos(math.radians(start_deg + span * i / n)),
             cy + r * math.sin(math.radians(start_deg + span * i / n))) for i in range(n + 1)]


def cumulative(pts):
    s = [0.0]
    for a, b in zip(pts, pts[1:]):
        s.append(s[-1] + math.dist(a, b))
    return s


def normals(pts):
    out = []
    for i in range(len(pts)):
        a = pts[max(0, i - 1)]
        b = pts[min(len(pts) - 1, i + 1)]
        dx, dy = b[0] - a[0], b[1] - a[1]
        length = math.hypot(dx, dy) or 1.0
        out.append((-dy / length, dx / length))
    return out


class Noise:
    """Smooth 1-D noise along arc length: a sum of a few seeded sines."""

    def __init__(self, rng: random.Random, octaves=3, base_wavelength=7.0):
        self.terms = []
        for o in range(octaves):
            wavelength = base_wavelength / (1.9 ** o) * rng.uniform(0.8, 1.25)
            self.terms.append((2 * math.pi / wavelength, rng.uniform(0, 2 * math.pi), 1.0 / (1.6 ** o)))
        self.norm = sum(t[2] for t in self.terms)

    def __call__(self, s):
        return sum(a * math.sin(w * s + p) for w, p, a in self.terms) / self.norm


# ---------------------------------------------------------------------------------------------------------------------
# Ink strokes
# ---------------------------------------------------------------------------------------------------------------------

def ink_stroke(points, rng, closed=False, width=BASE_WIDTH, taper=(0.7, 0.62), wobble=WOBBLE, overshoot=0.0,
               spline=True):
    """Return a closed outline (list of points) of a hand-inked stroke along the given points.

    taper: end widths as fractions of `width` at (start, end) for open strokes.
    overshoot: for closed shapes, draw past the start by this many units, as a hand closing a loop does.
    """
    centre = catmull_rom(points, closed=closed) if spline else list(points)
    if closed:
        # Draw a closed shape as one open stroke that overlaps its start slightly.
        s = cumulative(centre)
        extra = []
        for p, d in zip(centre[1:], s[1:]):
            if d > overshoot:
                break
            extra.append(p)
        centre = centre + extra[1:]
    s = cumulative(centre)
    total = s[-1] or 1.0
    nrm = normals(centre)
    displace = Noise(rng)
    swell = Noise(rng, octaves=2, base_wavelength=9.0)

    left, right = [], []
    for p, n, d in zip(centre, nrm, s):
        u = d / total
        off = wobble * displace(d)
        cx, cy = p[0] + n[0] * off, p[1] + n[1] * off
        w = width * (1.0 + 0.10 * swell(d))
        # Loose ends taper over up to 1.4 units, never more than a fifth of a short stroke, so short marks stay
        # lines instead of turning into commas.
        ramp = min(1.4, total * 0.2)
        if d < ramp:
            w *= taper[0] + (1 - taper[0]) * _ease(d / ramp)
        if total - d < ramp:
            w *= taper[1] + (1 - taper[1]) * _ease((total - d) / ramp)
        half = w / 2
        left.append((cx + n[0] * half, cy + n[1] * half))
        right.append((cx - n[0] * half, cy - n[1] * half))

    def unit(dx, dy):
        length = math.hypot(dx, dy) or 1.0
        return dx / length, dy / length

    end_out = unit(centre[-1][0] - centre[-2][0], centre[-1][1] - centre[-2][1])
    start_out = unit(centre[0][0] - centre[1][0], centre[0][1] - centre[1][1])
    end_cap = _cap(centre[-1], left[-1], end_out)
    start_cap = _cap(centre[0], right[0], start_out)
    return left + end_cap + right[::-1] + start_cap


def _ease(t):
    t = max(0.0, min(1.0, t))
    return t * t * (3 - 2 * t)


def _cap(c, a, outward):
    """A round cap from outline point a, around stroke end c, bulging in the outward direction."""
    ax, ay = a[0] - c[0], a[1] - c[1]
    r = math.hypot(ax, ay)
    if r == 0:
        return []
    start = math.atan2(ay, ax)
    # Sweep the side whose midpoint points outward.
    sign = 1 if math.cos(start + math.pi / 2) * outward[0] + math.sin(start + math.pi / 2) * outward[1] > 0 else -1
    return [(c[0] + r * math.cos(start + sign * math.pi * k / 6), c[1] + r * math.sin(start + sign * math.pi * k / 6))
            for k in range(1, 6)]


def ink_dot(cx, cy, r, rng):
    """A small, slightly irregular filled dot."""
    k = 18
    phase = rng.uniform(0, 2 * math.pi)
    return [(cx + r * (1 + 0.07 * math.sin(2 * a + phase)) * math.cos(a),
             cy + r * (1 + 0.07 * math.sin(3 * a + phase)) * math.sin(a))
            for a in (2 * math.pi * i / k for i in range(k))]


def outline_to_d(pts):
    """Closed smooth path through outline points (Catmull-Rom to cubic Bezier), rounded to 2 decimals."""
    n = len(pts)
    f = lambda v: f"{v:.2f}".rstrip("0").rstrip(".") if "." in f"{v:.2f}" else f"{v:.2f}"
    d = [f"M{f(pts[0][0])} {f(pts[0][1])}"]
    for i in range(n):
        p0, p1, p2, p3 = pts[i - 1], pts[i], pts[(i + 1) % n], pts[(i + 2) % n]
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        d.append(f"C{f(c1[0])} {f(c1[1])} {f(c2[0])} {f(c2[1])} {f(p2[0])} {f(p2[1])}")
    d.append("Z")
    return "".join(d)


def thin(pts, keep_every=2):
    """Drop outline points to keep files small; the Bezier fit restores smoothness."""
    return pts[::keep_every] if len(pts) > 40 else pts


# ---------------------------------------------------------------------------------------------------------------------
# Icons. Each returns (ink_outlines, accent_outlines).
# ---------------------------------------------------------------------------------------------------------------------

def icon_workflows(rng):
    ink, accent = [], []
    # Start: an open ring at the lower left, drawn as one loop that just overlaps itself.
    ink.append(ink_stroke(arc_points(5.2, 17.0, 2.2, 200, 548), rng, width=BASE_WIDTH * 0.95))
    # The route: one loose S from the start, dipping and rising to the destination.
    ink.append(ink_stroke([(8.3, 16.3), (11.0, 16.9), (13.4, 15.2), (13.6, 11.6), (14.9, 8.9), (16.9, 7.7)], rng))
    # Destination: a terracotta point.
    accent.append(ink_dot(19.1, 6.9, 1.6, rng))
    return ink, accent


def rounded_rect(x0, y0, x1, y1, r, rng, jitter=0.12):
    """Points around a rounded rectangle, starting at the middle of the top edge, with slightly unsteady corners."""
    j = lambda: rng.uniform(-jitter, jitter)
    corners = [(x1 - r + j(), y0 + r + j(), -90, 0), (x1 - r + j(), y1 - r + j(), 0, 90),
               (x0 + r + j(), y1 - r + j(), 90, 180), (x0 + r + j(), y0 + r + j(), 180, 270)]
    pts = [((x0 + x1) / 2 + j(), y0 + j() * 0.5)]
    for cx, cy, a0, a1 in corners:
        pts += arc_points(cx, cy, r, a0, a1, n=3)
    return pts


def rotate(points, origin, degrees):
    a = math.radians(degrees)
    ox, oy = origin
    return [(ox + (x - ox) * math.cos(a) - (y - oy) * math.sin(a),
             oy + (x - ox) * math.sin(a) + (y - oy) * math.cos(a)) for x, y in points]


def ink_blob(points, rng, wobble=0.06):
    """A filled organic shape through the given points (closed spline with a light wobble)."""
    centre = catmull_rom(points, closed=True, step=0.25)
    s = cumulative(centre)
    nrm = normals(centre)
    noise = Noise(rng, octaves=2, base_wavelength=5.0)
    return [(p[0] + n[0] * wobble * noise(d), p[1] + n[1] * wobble * noise(d)) for p, n, d in zip(centre, nrm, s)]


def icon_quick_start(rng):
    ink, accent = [], []
    # The compass ring.
    ink.append(ink_stroke(arc_points(12.0, 12.0, 8.2, -100, 268, n=24), rng))
    # The needle on a north-east bearing: the terracotta north half filled, the south half drawn.
    c, u, v = (12.0, 12.0), (0.707, -0.707), (0.707, 0.707)
    at = lambda a, b: (c[0] + u[0] * a + v[0] * b, c[1] + u[1] * a + v[1] * b)
    accent.append(ink_blob([at(4.9, 0.0), at(0.2, 1.25), at(-0.2, 0.0), at(0.2, -1.25)], rng))
    ink.append(ink_stroke([at(0.0, 1.2), at(-4.6, 0.05), at(0.0, -1.2)], rng, width=BASE_WIDTH * 0.8,
                          taper=(0.8, 0.8), spline=False))
    return ink, accent


def icon_architecture(rng):
    ink, accent = [], []
    # Three blocks: one above, two below, joined by soft branching lines.
    ink.append(ink_stroke(rounded_rect(9.0, 3.4, 15.0, 8.6, 1.3, rng), rng, closed=True, overshoot=0.9))
    ink.append(ink_stroke(rounded_rect(3.4, 15.2, 9.4, 20.4, 1.3, rng), rng, closed=True, overshoot=0.9))
    accent.append(ink_blob(rounded_rect(15.1, 15.5, 20.3, 20.1, 1.4, rng, jitter=0.08), rng))
    ink.append(ink_stroke([(12.0, 10.0), (11.4, 12.2), (8.6, 12.9), (6.5, 13.8)], rng))
    ink.append(ink_stroke([(12.0, 10.0), (12.6, 12.2), (15.4, 12.9), (17.6, 13.9)], rng))
    return ink, accent


def icon_python(rng):
    ink, accent = [], []
    # A snake in two S-bends: the tail curls at the lower right, the head is a solid oval at the upper left.
    body = [(18.2, 17.6), (18.9, 19.6), (15.6, 20.3), (11.0, 19.2), (9.6, 15.9), (12.0, 13.1), (15.5, 11.6),
            (16.4, 8.3), (13.9, 5.6), (10.6, 5.3)]
    ink.append(ink_stroke(body, rng, taper=(0.4, 1.0)))
    ink.append(ink_blob(rotate(arc_points(8.3, 6.2, 1.0, 0, 340, n=12), (8.3, 6.2), 0), rng))
    head = [(x, y) for x, y in arc_points(0, 0, 1.0, 0, 345, n=14)]
    head = [(8.0 + 2.3 * x, 6.3 + 1.55 * y) for x, y in head]
    ink[-1] = ink_blob(rotate(head, (8.0, 6.3), 12), rng)
    # A forked terracotta tongue flicking out of the head.
    accent.append(ink_stroke([(5.6, 6.9), (4.0, 7.3), (2.9, 6.6)], rng, width=BASE_WIDTH * 0.62, taper=(0.9, 0.7)))
    accent.append(ink_stroke([(4.1, 7.3), (3.0, 8.4)], rng, width=BASE_WIDTH * 0.62, taper=(0.9, 0.7)))
    return ink, accent


def icon_web_api(rng):
    ink, accent = [], []
    ink.append(ink_stroke([(8.4, 6.4), (5.6, 9.4), (3.4, 12.0), (5.6, 14.6), (8.4, 17.6)], rng))
    ink.append(ink_stroke([(15.6, 6.4), (18.4, 9.4), (20.6, 12.0), (18.4, 14.6), (15.6, 17.6)], rng))
    accent.append(ink_stroke([(13.7, 4.6), (12.3, 11.6), (10.5, 19.4)], rng))
    return ink, accent


def icon_library(rng):
    ink, accent = [], []
    # Two books upright, the second one terracotta, and a third leaning against them.
    ink.append(ink_stroke(rounded_rect(3.4, 4.6, 8.0, 19.8, 1.0, rng), rng, closed=True, overshoot=0.9))
    accent.append(ink_blob(rounded_rect(9.4, 7.4, 13.0, 19.6, 0.9, rng, jitter=0.08), rng))
    lean = rotate(rounded_rect(14.2, 6.4, 18.4, 21.2, 1.0, rng), (14.2, 19.8), 16)
    ink.append(ink_stroke(lean, rng, closed=True, overshoot=0.9))
    return ink, accent


def icon_user_stories(rng):
    ink, accent = [], []
    # A figure, head and shoulders, at the lower left.
    ink.append(ink_stroke(arc_points(8.2, 11.4, 2.7, -80, 290, n=16), rng, width=BASE_WIDTH * 0.95))
    ink.append(ink_stroke([(2.9, 20.4), (3.6, 17.0), (8.2, 15.4), (12.8, 17.0), (13.5, 20.4)], rng))
    # Its story: a terracotta speech bubble at the upper right, its tail pointing to the figure.
    bubble = [(17.6, 3.2), (20.7, 4.3), (21.0, 7.2), (18.6, 9.0), (15.7, 9.0), (14.7, 10.9), (14.8, 8.4),
              (13.8, 6.6), (14.6, 4.2)]
    accent.append(ink_stroke(bubble, rng, closed=True, overshoot=0.8, width=BASE_WIDTH * 0.95))
    return ink, accent


def icon_wiki_guide(rng):
    ink, accent = [], []
    # An open book: two pages drawn from the spine outwards, and the spine itself.
    ink.append(ink_stroke([(12.0, 7.6), (8.4, 5.5), (3.5, 6.2), (3.5, 12.0), (3.6, 17.6), (8.3, 17.2),
                           (12.0, 19.2)], rng))
    ink.append(ink_stroke([(12.0, 7.6), (15.6, 5.5), (20.5, 6.2), (20.5, 12.0), (20.4, 17.6), (15.7, 17.2),
                           (12.0, 19.2)], rng))
    ink.append(ink_stroke([(12.0, 8.6), (12.05, 13.4), (12.0, 18.2)], rng, width=BASE_WIDTH * 0.85))
    # A terracotta ribbon marking the page.
    accent.append(ink_blob([(15.0, 5.9), (16.8, 5.6), (16.9, 12.4), (15.95, 11.2), (15.0, 12.6)], rng))
    return ink, accent


ICONS = {
    "quick-start": (icon_quick_start, 3),
    "workflows": (icon_workflows, 11),
    "architecture": (icon_architecture, 5),
    "python": (icon_python, 7),
    "web-api": (icon_web_api, 13),
    "library": (icon_library, 17),
    "user-stories": (icon_user_stories, 19),
    "wiki-guide": (icon_wiki_guide, 23),
}


# ---------------------------------------------------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------------------------------------------------

def build_svg(name):
    fn, seed = ICONS[name]
    rng = random.Random(seed)
    ink, accent = fn(rng)
    lines = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24">']
    if ink:
        lines.append(f'  <g class="ink" fill="{INK}">')
        lines += [f'    <path d="{outline_to_d(thin(o))}"/>' for o in ink]
        lines.append("  </g>")
    if accent:
        lines.append(f'  <g class="accent" fill="{ACCENT}">')
        lines += [f'    <path d="{outline_to_d(o)}"/>' for o in accent]
        lines.append("  </g>")
    lines.append("</svg>")
    return "\n".join(lines) + "\n"


PREVIEW = """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>Subspace icons</title>
<style>
  body {{ margin: 0; font: 13px/1.4 system-ui, sans-serif; color: #3b3631; background: #fff; }}
  section {{ padding: 24px 32px; }}
  .dark {{ background: #000; color: #b0b0b0; }}
  .dark .ink {{ fill: #e5e5e5; }}
  .paper {{ background: #f4f7fb; }}
  .row {{ display: flex; align-items: flex-end; gap: 28px; flex-wrap: wrap; }}
  figure {{ margin: 0; text-align: center; }}
  figcaption {{ margin-top: 6px; font-size: 11px; opacity: 0.7; }}
  svg {{ display: block; margin: 0 auto; }}
  .s18 svg {{ width: 18px; height: 18px; }} .s24 svg {{ width: 24px; height: 24px; }}
  .s48 svg {{ width: 48px; height: 48px; }} .s120 svg {{ width: 120px; height: 120px; }}
  .grid svg {{ background-image: linear-gradient(#0001 1px, transparent 1px), linear-gradient(90deg, #0001 1px, transparent 1px);
              background-size: 5px 5px; outline: 1px solid #0002; }}
</style></head><body>
{sections}
</body></html>
"""


def write_preview(names):
    def row(cls, size):
        cells = "".join(f'<figure class="s{size}">{(HERE / f"{n}.svg").read_text()}<figcaption>{n}</figcaption></figure>'
                        for n in names)
        return f'<div class="row {cls}">{cells}</div>'
    big = "".join(f'<figure style="width:240px">{(HERE / f"{n}.svg").read_text().replace('width="24" height="24"', 'width="240" height="240"')}<figcaption>{n}</figcaption></figure>' for n in names)
    sections = [f'<section class="paper"><div class="row">{big}</div></section>']
    for theme in ("", "paper", "dark"):
        sections.append(f'<section class="{theme}">{row("", 120)}<br>{row("", 48)}<br>{row("", 24)}<br>{row("", 18)}</section>')
    sections.append(f'<section>{row("grid", 120)}</section>')
    (HERE / "preview.html").write_text(PREVIEW.format(sections="\n".join(sections)), encoding="utf-8")


def main(argv):
    global HERE
    if argv[:1] == ["--out"]:
        HERE = Path(argv[1]).resolve()
        argv = argv[2:]
    HERE.mkdir(parents=True, exist_ok=True)
    names = argv or list(ICONS)
    for name in names:
        (HERE / f"{name}.svg").write_text(build_svg(name), encoding="utf-8")
        print("wrote", name)
    write_preview(list(ICONS))


if __name__ == "__main__":
    main(sys.argv[1:])
