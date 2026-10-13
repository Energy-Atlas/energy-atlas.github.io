# EnergyAtlas Wiki

A documentation wiki built with MkDocs, styled to match the EnergyAtlas design system.

## Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Serve locally:**
   ```bash
   mkdocs serve
   ```
   The wiki will be available at `http://127.0.0.1:8000`
   
   **Note:** If CSS is not loading:
   - Stop the server (Ctrl+C) and restart it
   - Hard refresh your browser (Ctrl+F5)
   - Check browser console for 404 errors on CSS files

3. **Build static site:**
   ```bash
   mkdocs build
   ```
   The static site will be generated in the `site/` directory.

## Project Structure

```
.
├── docs/                         # Published wiki source
│   ├── assets/                   # CSS, JavaScript, images, icons, and self-hosted fonts
│   ├── quick-start/              # Welcome and onboarding
│   ├── workflows/                # Input/output, GUI, and shading workflows
│   ├── python/                   # Python reference
│   ├── web-api/                  # Web API and development reference
│   ├── library/                  # Objects, enums, and resource libraries
│   ├── user-stories/             # User stories
│   └── wiki-guide/               # Contribution guides and site map
├── design/
│   └── ui-design-spec.md   # UI design specification (not published)
├── theme/                  # Custom MkDocs theme
│   ├── base.html          # Base template
│   └── main.html          # Main content template
├── mkdocs.yml             # MkDocs configuration
└── requirements.txt        # Python dependencies
```

## Design

The wiki uses a custom theme that follows `design/ui-design-spec.md` (its section 0 records this site's decisions):

- **Light and dark themes** that follow the system preference, with a toggle
- **Sidebar shell**: subspace switcher and page tree at the left, a framed article, and the table of contents
- **Grid framing**: square, flat surfaces bounded by thin rules; numbered section strips on overview pages
- **Geist, Geist Mono, and Cormorant Garamond**, self-hosted in `docs/assets/fonts/`
- **Responsive design** for mobile and desktop

## Customization

### Adding Pages

1. Create a new Markdown file in the appropriate `docs/` subdirectory
2. Add the page to `mkdocs.yml` in the `nav` section
3. The page will automatically appear in the navigation

### Styling

- Main styles: `docs/assets/css/main.css` (tokens at the top); fonts in `fonts.css`; code colours in `syntax.css`
- Theme templates: `theme/base.html` and `theme/main.html`
- UI changes follow `design/ui-design-spec.md`
- Overview pages turn on numbered section strips with `overview: true` in their front matter

### Content Structure

Pages can be structured with markdown headers. The theme will automatically style:
- Headings (h1-h6)
- Links
- Code blocks
- Tables
- Lists
- Blockquotes

## Development

### Live Reload

When running `mkdocs serve`, the site will automatically reload when you make changes to:
- Markdown files in `docs/`
- Theme templates in `theme/`
- CSS files in `docs/assets/css/`
- Configuration in `mkdocs.yml`

### Building for Production

```bash
mkdocs build
```

The static site will be in the `site/` directory, ready to deploy to any static hosting service.

## License

[Add your license here]
