# Embedding Plotly.js Charts in Wiki Page

This guide shows how to embed Plotly charts in Markdown using a **simple fenced block**. No heavy JavaScript is required in Markdown; all rendering happens via the shared Plotly asset.

Use the [Interactive Plotting Playground](plotting-playground.md) to build and preview your own plots.


## Defaults (applied automatically)

These defaults are set by the renderer to make charts look good on a dark page:

- Background is transparent (`paper_bgcolor` and `plot_bgcolor`).
- Font uses the site family (`"Geist", ...`) and the theme's text color (`#e5e5e5` in dark, `#18202c` in light).
- Axis grid lines are subtle (`rgba(255,255,255,0.12)`).
- Legend is moved below the chart (horizontal) to reduce label overlap.
- Chart margins include extra bottom space for the legend.

You can override any of these by supplying `background` or a full `layout` block.

## Full Plotly control

Everything under `data`, `layout`, and `config` maps directly to Plotly. For advanced use (legends, templates, fonts, axis formatting, hover, etc.), you can paste Plotly’s native JSON here without additional JavaScript in Markdown. Check out [Ploly.js](https://plotly.com/javascript/reference/index/).


## Quick start

Rendered chart:

```plotly
{
  "data": [
    {"type": "scatter", "mode": "lines+markers", "x": [1, 2, 3, 4], "y": [10, 15, 13, 17]}
  ],
  "layout": {"title": "Example chart"}
}
```

Plain script (copy/paste):

```python
{
  "data": [
    {"type": "scatter", "mode": "lines+markers", "x": [1, 2, 3, 4], "y": [10, 15, 13, 17]}
  ],
  "layout": {"title": "Example chart"}
}
```

### Optional top-level keys

- `title`: chart title (string)
- `subtitle`: chart subtitle (string)
- `subtitle_style`: inline CSS for subtitle
- `background`: sets `paper_bgcolor` and `plot_bgcolor`
- `height` / `width`: dimensions
- `data`: Plotly trace list
- `layout`: Plotly layout object
- `config`: Plotly config object

## Multi-series line chart (markers + fills) with custom background

Rendered chart:

```plotly
{
  "title": "Multi-series line chart",
  "subtitle": "Markers + fill to axis + fill between series",
  "background": "#1a1a1a",
  "data": [
    {
      "type": "scatter",
      "mode": "lines+markers",
      "name": "Baseline",
      "x": [2019, 2020, 2021, 2022, 2023],
      "y": [120, 128, 115, 140, 135],
      "line": {"color": "#4da3ff", "width": 2},
      "marker": {"size": 7, "color": "#4da3ff"}
    },
    {
      "type": "scatter",
      "mode": "lines+markers",
      "name": "Retrofit",
      "x": [2019, 2020, 2021, 2022, 2023],
      "y": [105, 110, 102, 120, 118],
      "line": {"color": "#f1392a", "width": 2, "dash": "dash"},
      "marker": {"size": 7, "color": "#f1392a", "symbol": "diamond"}
    },
    {
      "type": "scatter",
      "mode": "lines",
      "name": "Lower bound",
      "x": [2019, 2020, 2021, 2022, 2023],
      "y": [95, 100, 92, 108, 105],
      "line": {"color": "rgba(0,0,0,0)"},
      "showlegend": false
    },
    {
      "type": "scatter",
      "mode": "lines",
      "name": "Upper bound",
      "x": [2019, 2020, 2021, 2022, 2023],
      "y": [130, 138, 125, 150, 145],
      "fill": "tonexty",
      "fillcolor": "rgba(77,163,255,0.2)",
      "line": {"color": "rgba(0,0,0,0)"},
      "showlegend": false
    }
  ],
  "layout": {
    "xaxis": {"title": "Year"},
    "yaxis": {"title": "Energy (GWh)"},
    "legend": {"orientation": "h", "y": -0.2, "x": 0}
  }
}
```

Plain script (copy/paste):

```json
{
  "title": "Multi-series line chart",
  "subtitle": "Markers + fill to axis + fill between series",
  "background": "#1a1a1a",
  "data": [
    {
      "type": "scatter",
      "mode": "lines+markers",
      "name": "Baseline",
      "x": [2019, 2020, 2021, 2022, 2023],
      "y": [120, 128, 115, 140, 135],
      "line": {"color": "#4da3ff", "width": 2},
      "marker": {"size": 7, "color": "#4da3ff"}
    },
    {
      "type": "scatter",
      "mode": "lines+markers",
      "name": "Retrofit",
      "x": [2019, 2020, 2021, 2022, 2023],
      "y": [105, 110, 102, 120, 118],
      "line": {"color": "#f1392a", "width": 2, "dash": "dash"},
      "marker": {"size": 7, "color": "#f1392a", "symbol": "diamond"}
    },
    {
      "type": "scatter",
      "mode": "lines",
      "name": "Lower bound",
      "x": [2019, 2020, 2021, 2022, 2023],
      "y": [95, 100, 92, 108, 105],
      "line": {"color": "rgba(0,0,0,0)"},
      "showlegend": false
    },
    {
      "type": "scatter",
      "mode": "lines",
      "name": "Upper bound",
      "x": [2019, 2020, 2021, 2022, 2023],
      "y": [130, 138, 125, 150, 145],
      "fill": "tonexty",
      "fillcolor": "rgba(77,163,255,0.2)",
      "line": {"color": "rgba(0,0,0,0)"},
      "showlegend": false
    }
  ],
  "layout": {
    "xaxis": {"title": "Year"},
    "yaxis": {"title": "Energy (GWh)"},
    "legend": {"orientation": "h", "y": -0.2, "x": 0}
  }
}
```

## Vertically stacked bar

Rendered chart:

```plotly
{
  "title": "Stacked energy end uses",
  "subtitle": "Vertical stacked bars",
  "data": [
    {"type": "bar", "name": "HVAC", "x": ["Office", "Residential", "Retail", "Lab"], "y": [42, 30, 22, 35]},
    {"type": "bar", "name": "Lighting", "x": ["Office", "Residential", "Retail", "Lab"], "y": [18, 16, 14, 12]},
    {"type": "bar", "name": "Plug Loads", "x": ["Office", "Residential", "Retail", "Lab"], "y": [12, 20, 10, 15]}
  ],
  "layout": {
    "barmode": "stack",
    "xaxis": {"title": "Building type"},
    "yaxis": {"title": "Annual energy (MWh)"},
    "legend": {"orientation": "h", "y": -0.2}
  }
}
```

Plain script (copy/paste):

```json
{
  "title": "Stacked energy end uses",
  "subtitle": "Vertical stacked bars",
  "data": [
    {"type": "bar", "name": "HVAC", "x": ["Office", "Residential", "Retail", "Lab"], "y": [42, 30, 22, 35]},
    {"type": "bar", "name": "Lighting", "x": ["Office", "Residential", "Retail", "Lab"], "y": [18, 16, 14, 12]},
    {"type": "bar", "name": "Plug Loads", "x": ["Office", "Residential", "Retail", "Lab"], "y": [12, 20, 10, 15]}
  ],
  "layout": {
    "barmode": "stack",
    "xaxis": {"title": "Building type"},
    "yaxis": {"title": "Annual energy (MWh)"},
    "legend": {"orientation": "h", "y": -0.2}
  }
}
```

## Grouped bars (shared bins)

Rendered chart:

```plotly
{
  "title": "Load distribution by bin",
  "subtitle": "Grouped bars per bin (shared bins)",
  "data": [
    {"type": "bar", "name": "Scenario A", "x": ["0-5", "5-10", "10-15", "15-20", "20-25"], "y": [12, 18, 9, 6, 3]},
    {"type": "bar", "name": "Scenario B", "x": ["0-5", "5-10", "10-15", "15-20", "20-25"], "y": [10, 14, 12, 8, 4]}
  ],
  "layout": {
    "barmode": "group",
    "xaxis": {"title": "Bin (kW)"},
    "yaxis": {"title": "Count"}
  }
}
```

Plain script (copy/paste):

```json
{
  "title": "Load distribution by bin",
  "subtitle": "Grouped bars per bin (shared bins)",
  "data": [
    {"type": "bar", "name": "Scenario A", "x": ["0-5", "5-10", "10-15", "15-20", "20-25"], "y": [12, 18, 9, 6, 3]},
    {"type": "bar", "name": "Scenario B", "x": ["0-5", "5-10", "10-15", "15-20", "20-25"], "y": [10, 14, 12, 8, 4]}
  ],
  "layout": {
    "barmode": "group",
    "xaxis": {"title": "Bin (kW)"},
    "yaxis": {"title": "Count"}
  }
}
```

## Pie and donut

Rendered chart:

```plotly
{
  "title": "Energy share by sector",
  "data": [
    {"type": "pie", "labels": ["Residential", "Commercial", "Industrial", "Other"], "values": [45, 30, 20, 5], "textinfo": "label+percent"}
  ],
  "layout": {"legend": {"orientation": "h", "y": -0.1}}
}
```

Plain script (copy/paste):

```json
{
  "title": "Energy share by sector",
  "data": [
    {"type": "pie", "labels": ["Residential", "Commercial", "Industrial", "Other"], "values": [45, 30, 20, 5], "textinfo": "label+percent"}
  ],
  "layout": {"legend": {"orientation": "h", "y": -0.1}}
}
```

Rendered chart (donut):

```plotly
{
  "title": "Donut chart example",
  "data": [
    {"type": "pie", "hole": 0.45, "labels": ["Heating", "Cooling", "Lighting", "Plug Loads"], "values": [40, 25, 20, 15], "textinfo": "label+percent"}
  ]
}
```

Plain script (copy/paste):

```json
{
  "title": "Donut chart example",
  "data": [
    {"type": "pie", "hole": 0.45, "labels": ["Heating", "Cooling", "Lighting", "Plug Loads"], "values": [40, 25, 20, 15], "textinfo": "label+percent"}
  ]
}
```

## Scatter plot

Rendered chart:

```plotly
{
  "title": "Scatter plot with markers",
  "subtitle": "Color + size encodes another metric",
  "data": [
    {
      "type": "scatter",
      "mode": "markers",
      "x": [1.1, 2.5, 3.2, 4.8, 5.0, 6.3],
      "y": [10, 12, 9, 15, 14, 16],
      "text": ["A", "B", "C", "D", "E", "F"],
      "marker": {"size": [8, 12, 10, 16, 14, 18], "color": [2, 3, 1, 4, 3, 5], "colorscale": "Viridis", "showscale": true}
    }
  ],
  "layout": {
    "xaxis": {"title": "Input variable"},
    "yaxis": {"title": "Outcome"}
  }
}
```

Plain script (copy/paste):

```json
{
  "title": "Scatter plot with markers",
  "subtitle": "Color + size encodes another metric",
  "data": [
    {
      "type": "scatter",
      "mode": "markers",
      "x": [1.1, 2.5, 3.2, 4.8, 5.0, 6.3],
      "y": [10, 12, 9, 15, 14, 16],
      "text": ["A", "B", "C", "D", "E", "F"],
      "marker": {"size": [8, 12, 10, 16, 14, 18], "color": [2, 3, 1, 4, 3, 5], "colorscale": "Viridis", "showscale": true}
    }
  ],
  "layout": {
    "xaxis": {"title": "Input variable"},
    "yaxis": {"title": "Outcome"}
  }
}
```

## Axis bins (histogram-style)

Plotly supports bins via `xbins` / `ybins` on histogram traces. Example:

Rendered chart:

```plotly
{
  "title": "Histogram with explicit bins",
  "data": [
    {"type": "histogram", "x": [1, 2, 2, 3, 3, 3, 4, 4, 5, 5, 6], "xbins": {"start": 0, "end": 7, "size": 1}}
  ],
  "layout": {"bargap": 0.05}
}
```

Plain script (copy/paste):

```json
{
  "title": "Histogram with explicit bins",
  "data": [
    {"type": "histogram", "x": [1, 2, 2, 3, 3, 3, 4, 4, 5, 5, 6], "xbins": {"start": 0, "end": 7, "size": 1}}
  ],
  "layout": {"bargap": 0.05}
}
```

