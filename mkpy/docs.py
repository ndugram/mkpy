from __future__ import annotations

import os
from typing import Annotated, Literal

from annotated_doc import Doc

from .markdown import extract_title, render as render_markdown
from .themes import THEMES, ThemeName
from .server import run_server


class Docs:
    """
    A minimalistic documentation generator and server.

    Automatically reads markdown files from a folder, converts them to HTML,
    and serves them via built-in HTTP server with automatic routing.

    Example:
        >>> from mkpy import Docs
        >>> docs = Docs(
        ...     title="My Project",
        ...     theme="dark",
        ...     port=3000,
        ... )
        >>> docs.run()
    """

    def __init__(
        self,
        folder: Annotated[
            str,
            Doc(
                """
                Path to folder containing markdown files.
                Defaults to "docs" in current directory.
                """
            ),
        ] = "docs",
        title: Annotated[
            str,
            Doc(
                """
                Title displayed in browser tab and page header.
                """
            ),
        ] = "MKPY",
        theme: Annotated[
            str | Literal["light", "dark"],
            Doc(
                """
                Color theme. Available: "light", "dark".
                """
            ),
        ] = "light",
        host: Annotated[
            str,
            Doc(
                """
                Host address to bind server to.
                """
            ),
        ] = "127.0.0.1",
        port: Annotated[
            int,
            Doc(
                """
                Port number for HTTP server.
                """
            ),
        ] = 8000,
        show_nav: Annotated[
            bool,
            Doc(
                """
                Whether to show automatic navigation menu.
                """
            ),
        ] = True,
        custom_css: Annotated[
            str | None,
            Doc(
                """
                Custom CSS to inject into every page.
                Can be inline CSS or path to .css file (e.g., "styles/custom.css").
                """
            ),
        ] = None,
        custom_js: Annotated[
            str | None,
            Doc(
                """
                Custom JavaScript to inject into every page.
                Can be inline JS or path to .js file (e.g., "scripts/main.js").
                """
            ),
        ] = None,
    ) -> None:
        """
        Initialize Docs instance.

        Args:
            folder: Path to markdown files folder.
            title: Documentation title.
            theme: Theme name ("light" or "dark").
            host: Server host address.
            port: Server port number.
            show_nav: Show navigation menu.
            custom_css: Custom CSS content or path to CSS file.
            custom_js: Custom JavaScript content or path to JS file.
        """
        self.folder = folder
        self.title = title
        self.theme = theme
        self.host = host
        self.port = port
        self.show_nav = show_nav
        self.custom_css = custom_css
        self.custom_js = custom_js

        if theme not in THEMES:
            raise ValueError(f"Theme '{theme}' not found. Available: {list(THEMES.keys())}")

        self.routes: dict[str, str] = {}
        self._auto_discover_assets()
        self._build_routes()

    def _auto_discover_assets(self) -> None:
        css_folder = os.path.join(self.folder, "css")
        if os.path.isdir(css_folder):
            css_files = []
            for f in sorted(os.listdir(css_folder)):
                if f.endswith(".css"):
                    with open(os.path.join(css_folder, f), "r", encoding="utf-8") as file:
                        css_files.append(file.read())
            if css_files:
                auto_css = "\n".join(css_files)
                if self.custom_css:
                    self.custom_css = auto_css + "\n" + self.custom_css
                else:
                    self.custom_css = auto_css

        js_folder = os.path.join(self.folder, "js")
        if os.path.isdir(js_folder):
            js_files = []
            for f in sorted(os.listdir(js_folder)):
                if f.endswith(".js"):
                    with open(os.path.join(js_folder, f), "r", encoding="utf-8") as file:
                        js_files.append(file.read())
            if js_files:
                auto_js = "\n".join(js_files)
                if self.custom_js:
                    self.custom_js = auto_js + "\n" + self.custom_js
                else:
                    self.custom_js = auto_js

    def _build_routes(self) -> None:
        if not os.path.exists(self.folder):
            raise FileNotFoundError(f"Folder '{self.folder}' not found")

        for root, _, files in os.walk(self.folder):
            for file in files:
                if file.endswith(".md"):
                    full_path = os.path.join(root, file)

                    route = os.path.relpath(full_path, self.folder)
                    route = route.replace("\\", "/")
                    route = route.replace(".md", "")

                    if route.endswith("index"):
                        route = route[:-6] if route.endswith("/index") else route[:-5]

                    route = "/" + route.strip("/") if route != "/" else "/"

                    self.routes[route] = full_path

    @property
    def navigation(self) -> list[tuple[str, str]]:
        """
        Build navigation from routes with smart title extraction.

        Extracts title from first # heading in each markdown file,
        or uses filename as fallback.
        """
        nav = []
        for route in sorted(self.routes.keys()):
            file_path = self.routes[route]
            with open(file_path, "r", encoding="utf-8") as f:
                md = f.read()
            filename = os.path.basename(file_path)
            title = extract_title(md, filename)
            nav.append((route, title))
        return nav

    def _load_custom_asset(self, value: str | None, asset_type: str) -> str:
        if value is None:
            return ""
        
        if asset_type == "css" and value.endswith(".css"):
            if os.path.isfile(value):
                with open(value, "r", encoding="utf-8") as f:
                    return f.read()
            relative_path = os.path.join(self.folder, "..", value)
            if os.path.isfile(relative_path):
                with open(relative_path, "r", encoding="utf-8") as f:
                    return f.read()

        elif asset_type == "js" and value.endswith(".js"):
            if os.path.isfile(value):
                with open(value, "r", encoding="utf-8") as f:
                    return f.read()
            relative_path = os.path.join(self.folder, "..", value)
            if os.path.isfile(relative_path):
                with open(relative_path, "r", encoding="utf-8") as f:
                    return f.read()

        return value

    def render(self, file_path: str) -> str:
        """
        Render a markdown file to full HTML page.

        Args:
            file_path: Path to markdown file.

        Returns:
            Complete HTML page string.
        """
        with open(file_path, "r", encoding="utf-8") as f:
            md = f.read()

        content = render_markdown(md)
        base_css = THEMES[self.theme]
        custom_css = self._load_custom_asset(self.custom_css, "css")

        nav_html = ""
        if self.show_nav:
            nav_items = []
            for route, title in self.navigation:
                nav_items.append(f'<a href="{route}">{title}</a>')
            nav_html = f"""
            <nav class="mkpy-nav">
                {" | ".join(nav_items)}
            </nav>
            """

        custom_css_block = f"<style>\n{custom_css}\n</style>" if custom_css else ""

        return f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{self.title}</title>
    <style>
    {base_css}
    .mkpy-nav {{
        margin-bottom: 2em;
        padding-bottom: 1em;
        border-bottom: 1px solid {'#30363d' if self.theme == 'dark' else '#eee'};
    }}
    .mkpy-nav a {{
        margin-right: 1em;
        color: {'#58a6ff' if self.theme == 'dark' else '#0066cc'};
    }}
    </style>
    {custom_css_block}
</head>
<body>
    {nav_html}
    <main>
    {content}
    </main>
    <footer style="margin-top: 3em; padding-top: 1em; border-top: 1px solid {'#30363d' if self.theme == 'dark' else '#eee'}; font-size: 0.85em; opacity: 0.7;">
        Generated by <a href="https://github.com/ndugram/mkpy">mkpy</a>
    </footer>
    <script>
    // Add smooth scroll for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {{
        anchor.addEventListener('click', function (e) {{
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) target.scrollIntoView({{ behavior: 'smooth' }});
        }});
    }});
    </script>
    <script>
    // Highlight current nav item
    const path = window.location.pathname.replace(/\\/$/, '') || '/';
    document.querySelectorAll('.mkpy-nav a').forEach(link => {{
        const linkPath = new URL(link.href).pathname.replace(/\\/$/, '') || '/';
        if (linkPath === path) {{
            link.style.fontWeight = '600';
            link.style.textDecoration = 'underline';
        }}
    }});
    </script>
    {self._load_custom_asset(self.custom_js, 'js')}
</body>
</html>
"""

    def render_error(self, code: int, message: str) -> str:
        """
        Render error page.

        Args:
            code: HTTP status code.
            message: Error message.

        Returns:
            HTML error page string.
        """
        css = THEMES[self.theme]
        return f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{code} - {message}</title>
    <style>
    {css}
    .error-container {{
        text-align: center;
        padding: 4em 0;
    }}
    .error-code {{
        font-size: 6em;
        font-weight: bold;
        opacity: 0.3;
    }}
    .error-message {{
        font-size: 1.5em;
        margin-top: 1em;
    }}
    a {{
        color: {'#58a6ff' if self.theme == 'dark' else '#0066cc'};
    }}
    </style>
</head>
<body>
    <div class="error-container">
        <div class="error-code">{code}</div>
        <div class="error-message">{message}</div>
        <p><a href="/">← Back to home</a></p>
    </div>
</body>
</html>
"""

    def generate_sitemap(self, host: Annotated[
        str,
        Doc(
            """
            Base URL for sitemap generation.
            """
        ),
    ] = "http://localhost") -> str:
        """
        Generate sitemap.xml for SEO.

        Args:
            host: Base URL of the documentation site.

        Returns:
            XML sitemap string.
        """
        urls = []
        for route in sorted(self.routes.keys()):
            url = f"{host}{route}"
            urls.append(f"  <url>\n    <loc>{url}</loc>\n  </url>")
        return '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "\n".join(urls) + "\n</urlset>"

    def run(self) -> None:
        run_server(self)
