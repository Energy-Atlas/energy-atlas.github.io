(() => {
    const FONT_FAMILY = '"Geist", "Inter", "Helvetica Neue", Arial, sans-serif';

    const getCssValue = (name, fallback) => {
        const value = getComputedStyle(document.documentElement).getPropertyValue(name).trim();
        return value || fallback;
    };

    const getThemePlotlyDefaults = () => {
        const subtitleColor = getCssValue('--plotly-subtitle-color', '#9aa0a6');

        return {
            fontColor: getCssValue('--plotly-font-color', '#e5e5e5'),
            gridColor: getCssValue('--plotly-grid-color', 'rgba(255,255,255,0.12)'),
            zeroLineColor: getCssValue('--plotly-zeroline-color', 'rgba(255,255,255,0.2)'),
            paperBg: getCssValue('--plotly-paper-bg', 'rgba(0,0,0,0)'),
            plotBg: getCssValue('--plotly-plot-bg', 'rgba(0,0,0,0)'),
            subtitleStyle: `font-size: 0.85em; color: ${subtitleColor};`
        };
    };

    const parseSpec = (raw) => {
        if (!raw) {
            return null;
        }

        const trimmed = raw.trim();
        if (!trimmed) {
            return null;
        }

        if (window.jsyaml) {
            try {
                return window.jsyaml.load(trimmed);
            } catch (error) {
                // Fall back to JSON parsing below.
            }
        }

        try {
            return JSON.parse(trimmed);
        } catch (error) {
            return null;
        }
    };

    const applyTitleAndSubtitle = (spec, layout, themeDefaults) => {
        const titleValue = spec.title ?? layout.title ?? '';
        const subtitleValue = spec.subtitle ?? layout.subtitle ?? '';
        const subtitleStyle = spec.subtitle_style ?? themeDefaults.subtitleStyle;

        if (!titleValue && !subtitleValue) {
            return;
        }

        let titleText = '';
        if (typeof titleValue === 'string') {
            titleText = titleValue;
        } else if (titleValue && typeof titleValue === 'object') {
            titleText = titleValue.text ?? '';
        }

        if (subtitleValue) {
            layout.title = {
                ...((typeof titleValue === 'object' && titleValue) ? titleValue : {}),
                text: `${titleText}<br><span style="${subtitleStyle}">${subtitleValue}</span>`
            };
        } else if (titleValue) {
            layout.title = titleValue;
        }
    };

    const applyDefaults = (layout) => {
        const themeDefaults = getThemePlotlyDefaults();

        if (!layout.paper_bgcolor) {
            layout.paper_bgcolor = themeDefaults.paperBg;
        }

        if (!layout.plot_bgcolor) {
            layout.plot_bgcolor = themeDefaults.plotBg;
        }

        const defaultFont = {
            color: themeDefaults.fontColor,
            family: FONT_FAMILY
        };

        if (!layout.font) {
            layout.font = { ...defaultFont };
        } else {
            layout.font = { ...defaultFont, ...layout.font };
        }

        const axisDefaults = {
            color: themeDefaults.fontColor,
            gridcolor: themeDefaults.gridColor,
            zerolinecolor: themeDefaults.zeroLineColor
        };

        if (!layout.xaxis) {
            layout.xaxis = { ...axisDefaults };
        } else {
            layout.xaxis = { ...axisDefaults, ...layout.xaxis };
        }

        if (!layout.yaxis) {
            layout.yaxis = { ...axisDefaults };
        } else {
            layout.yaxis = { ...axisDefaults, ...layout.yaxis };
        }

        if (!layout.legend) {
            layout.legend = { orientation: 'h', y: -0.2, x: 0, yanchor: 'top' };
        }

        if (!layout.margin) {
            layout.margin = { t: 60, r: 24, b: 72, l: 60 };
        }

        return themeDefaults;
    };

    const normalizeLayout = (spec) => {
        const layout = { ...(spec.layout || {}) };

        if (spec.background) {
            layout.paper_bgcolor = spec.background;
            layout.plot_bgcolor = spec.background;
        }

        const themeDefaults = applyDefaults(layout);
        applyTitleAndSubtitle(spec, layout, themeDefaults);

        return layout;
    };

    const normalizeConfig = (spec) => {
        return {
            responsive: true,
            ...(spec.config || {})
        };
    };

    const normalizeData = (spec) => {
        return spec.data || spec.traces || [];
    };

    const drawPlot = (container, spec, useReact = false) => {
        const data = normalizeData(spec);
        const layout = normalizeLayout(spec);
        const config = normalizeConfig(spec);
        const renderer = useReact && window.Plotly.react ? window.Plotly.react : window.Plotly.newPlot;

        container.__energyAtlasPlotlySpec = spec;
        return renderer(container, data, layout, config);
    };

    const findBlocks = () => {
        return document.querySelectorAll(
            'code.language-plotly, code.plotly, code[class*="language-plotly"], code[class*="plotly"], pre.plotly code, div.plotly code'
        );
    };

    const renderPlotlyBlocks = () => {
        if (!window.Plotly) {
            return false;
        }

        const blocks = findBlocks();
        blocks.forEach((codeBlock, index) => {
            const spec = parseSpec(codeBlock.textContent);
            if (!spec) {
                return;
            }

            const pre = codeBlock.closest('pre');

            const container = document.createElement('div');
            container.className = 'plotly-chart';
            container.dataset.plotlyIndex = String(index);

            if (spec.id) {
                container.id = spec.id;
            }

            if (spec.height) {
                const heightValue = typeof spec.height === 'number' ? `${spec.height}px` : spec.height;
                container.style.height = heightValue;
            }

            if (spec.width) {
                const widthValue = typeof spec.width === 'number' ? `${spec.width}px` : spec.width;
                container.style.width = widthValue;
            }

            if (pre) {
                pre.replaceWith(container);
            } else {
                codeBlock.replaceWith(container);
            }

            drawPlot(container, spec);
        });

        return true;
    };

    const renderPlaygrounds = () => {
        if (!window.Plotly) {
            return false;
        }

        const playgrounds = document.querySelectorAll('[data-plotly-playground]');
        if (!playgrounds.length) {
            return true;
        }

        playgrounds.forEach((container) => {
            if (container.dataset.plotlyInitialized === 'true') {
                return;
            }

            const initial = container.querySelector('textarea');
            const output = container.querySelector('.plotly-playground-chart');
            const error = container.querySelector('.plotly-playground-error');

            if (!initial || !output) {
                return;
            }

            const renderSpec = (raw) => {
                const spec = parseSpec(raw);
                if (!spec) {
                    if (error) {
                        error.textContent = 'Invalid JSON. Fix the syntax to render.';
                    }
                    return;
                }

                if (error) {
                    error.textContent = '';
                }

                drawPlot(output, spec, output.dataset.plotlyRendered === 'true');
                output.dataset.plotlyRendered = 'true';
            };

            renderSpec(initial.value);

            initial.addEventListener('input', () => renderSpec(initial.value));
            container.dataset.plotlyInitialized = 'true';
        });

        return true;
    };

    const rerenderExistingCharts = () => {
        if (!window.Plotly) {
            return;
        }

        document.querySelectorAll('.plotly-chart').forEach((container) => {
            if (container.__energyAtlasPlotlySpec) {
                drawPlot(container, container.__energyAtlasPlotlySpec, true);
            }
        });
    };

    const attemptRender = (tries = 0) => {
        const success = renderPlotlyBlocks() && renderPlaygrounds();
        if (success || tries >= 5) {
            return;
        }
        setTimeout(() => attemptRender(tries + 1), 200);
    };

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', () => attemptRender());
    } else {
        attemptRender();
    }

    window.addEventListener('load', () => attemptRender());
    window.addEventListener('energyatlas-theme-change', () => rerenderExistingCharts());
})();
