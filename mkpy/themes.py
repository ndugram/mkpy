"""Built-in themes for mkpy."""

from __future__ import annotations

from typing import Literal

ThemeName = Literal["light", "dark"]

THEMES: dict[ThemeName, str] = {
    "light": """
    * { box-sizing: border-box; }
    body {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        background: #ffffff;
        color: #1a1a1a;
        max-width: 900px;
        margin: 0 auto;
        padding: 40px 20px;
        line-height: 1.7;
    }
    h1, h2, h3, h4 { margin-top: 1.5em; margin-bottom: 0.5em; font-weight: 600; }
    h1 { font-size: 2.2em; border-bottom: 2px solid #eee; padding-bottom: 0.3em; }
    h2 { font-size: 1.6em; }
    h3 { font-size: 1.3em; }
    a { color: #0066cc; text-decoration: none; }
    a:hover { text-decoration: underline; }
    code {
        background: #f5f5f5;
        padding: 0.2em 0.4em;
        border-radius: 4px;
        font-family: "SF Mono", Monaco, Consolas, monospace;
        font-size: 0.9em;
    }
    pre {
        background: #f5f5f5;
        padding: 1em;
        border-radius: 8px;
        overflow-x: auto;
    }
    pre code { background: none; padding: 0; }
    blockquote {
        border-left: 4px solid #0066cc;
        margin: 1em 0;
        padding: 0.5em 1em;
        background: #f9f9f9;
    }
    table { border-collapse: collapse; width: 100%; margin: 1em 0; }
    th, td { border: 1px solid #ddd; padding: 10px; text-align: left; }
    th { background: #f5f5f5; }
    img { max-width: 100%; border-radius: 8px; }
    ul, ol { padding-left: 1.5em; }
    li { margin: 0.3em 0; }
    hr { border: none; border-top: 1px solid #eee; margin: 2em 0; }
    """,
    "dark": """
    * { box-sizing: border-box; }
    body {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        background: #0d1117;
        color: #c9d1d9;
        max-width: 900px;
        margin: 0 auto;
        padding: 40px 20px;
        line-height: 1.7;
    }
    h1, h2, h3, h4 { margin-top: 1.5em; margin-bottom: 0.5em; font-weight: 600; color: #ffffff; }
    h1 { font-size: 2.2em; border-bottom: 1px solid #30363d; padding-bottom: 0.3em; }
    h2 { font-size: 1.6em; }
    h3 { font-size: 1.3em; }
    a { color: #58a6ff; text-decoration: none; }
    a:hover { text-decoration: underline; }
    code {
        background: #21262d;
        padding: 0.2em 0.4em;
        border-radius: 4px;
        font-family: "SF Mono", Monaco, Consolas, monospace;
        font-size: 0.9em;
    }
    pre {
        background: #161b22;
        padding: 1em;
        border-radius: 8px;
        overflow-x: auto;
    }
    pre code { background: none; padding: 0; }
    blockquote {
        border-left: 4px solid #58a6ff;
        margin: 1em 0;
        padding: 0.5em 1em;
        background: #161b22;
    }
    table { border-collapse: collapse; width: 100%; margin: 1em 0; }
    th, td { border: 1px solid #30363d; padding: 10px; text-align: left; }
    th { background: #21262d; }
    img { max-width: 100%; border-radius: 8px; }
    ul, ol { padding-left: 1.5em; }
    li { margin: 0.3em 0; }
    hr { border: none; border-top: 1px solid #30363d; margin: 2em 0; }
    """
}
