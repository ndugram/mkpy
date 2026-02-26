# mkpy

Minimalistic Python library for generating and serving documentation from Markdown files.

## Installation

```bash
pip install mkpy-client
```

## Quick Start

```python
from mkpy import Docs

docs = Docs(
    title="My Project",
    theme="dark",
    port=3000,
)
docs.run()
```

## CLI

```bash
# Run with defaults
mkpy serve

# With options
mkpy serve --folder docs --theme dark --port 3000

# From config file
mkpy serve main.py
```

## Features

- Automatic markdown to HTML conversion
- Built-in HTTP server
- Auto routes from file structure
- Light and dark themes
- Custom CSS and JavaScript
- Auto-discovery of css/ and js/ folders
- Navigation menu
- Sitemap generation

## Configuration File

```python
# main.py
from mkpy import Docs

docs = Docs(
    folder="docs",
    title="My Project",
    theme="dark",
    port=3000,
    custom_css="styles.css",
)
```

## Structure

```
docs/
├── index.md
├── about.md
└── guide/
    └── install.md
```

Routes:
- `/` -> index.md
- `/about` -> about.md
- `/guide/install` -> guide/install.md

## Requirements

- Python 3.9+
- markdown
- rich (optional, for colored output)
- typer (optional, for CLI)

## License

MIT
