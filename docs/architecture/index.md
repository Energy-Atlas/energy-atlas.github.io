---
full_width: true
likec4: true
overview: true
---

# Architecture Overview

This subspace documents how EnergyAtlas turns geospatial input into simulated, aggregated,
and published energy results. Every diagram here is live: it is rendered in your browser from
the same architecture model the pages describe, not from a picture of one.

## Reading the diagrams

Each diagram supports three things a static image cannot:

- **Inspect.** Click any card to read its description and see the relationships that enter and
  leave it. Cards are deliberately title-only so the diagram stays legible; the detail lives
  one click away.
- **Expand.** Systems drawn as a single card, such as Simulation, contain further structure.
  Opening one reveals the stages inside it.
- **Drill down.** Cards that have a dedicated detail view navigate to it. Use the browser's
  own back control, or the navigation panel in the diagram, to return.

Diagrams follow the site's light and dark theme, and pan and zoom independently of the page.

<figure class="likec4-figure">
  <div class="likec4-figure-canvas">
    <likec4-view view-id="index" browser="true"></likec4-view>
  </div>
  <noscript><p class="likec4-figure-fallback">The architecture map requires JavaScript. The
  sections below describe the same structure in text.</p></noscript>
  <figcaption>Coarse map of ingestion, the UBEM pipeline, persistence, and downstream
  consumers. Click any card to inspect it, or drill into Feature2Building, Simulation, or any
  table group.</figcaption>
  <p class="likec4-figure-hint">Tap the diagram to open it full screen.</p>
</figure>

## The pipeline in brief

Input GeoJSON and weather data enter **Preprocessing**, which performs schema matching,
geometric preprocessing, and archetype assignment.

**Feature2Building (F2B)** turns each preprocessed feature into simulation-domain objects: a
Building, the Zones it owns, and the Faces those Zones own — each characterised by
construction, systems, and energy-load archetypes.

**Simulation** precomputes boundary conditions, runs the Zone5R1C thermal model per zone, and
aggregates zone results into building and site results.

Results land in three persistent table groups. **Definition Tables** hold Building and Zone
definitions, **Result Tables** hold zone, building, and site energy results, and **GIS
Tables** hold processed feature properties alongside a selective projection of site energy
results. GIS Tables export **Results GeoJSON**.

The **Scenario Mixer** reads persisted annual results and serves interactive scenario
mixtures back to the WebUI without re-running a simulation.

## Detailed views

- [Simulation Stages and Data Flow](simulation-data-flow.md) — the full path from GeoJSON
  ingestion through simulation, aggregation, persistence, and GIS export.
- [Scenario Simulation](scenario-simulation.md) — how scenario mappings produce building
  upgrade copies and parallel simulation instances alongside a baseline.
- [Post-hoc Scenario Mixer](post-hoc-scenario-mixer.md) — how persisted results and modeling
  parameters drive a real-time scenario mixture and a WebUI style update.

## How these diagrams are maintained

The diagrams are generated from a LikeC4 model kept in this repository under
`architecture/`. Connector geometry is produced by a router that re-routes every relationship
as a strictly orthogonal path with rounded corners, and the deployment fails if any route
cannot be routed cleanly. Contributors adding or changing a view should start from
`architecture/README.md`.
