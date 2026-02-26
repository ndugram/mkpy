"""Markdown rendering utilities."""

from __future__ import annotations

import re


def extract_title(md: str, filename: str) -> str:
    """
    Extract title from markdown content.

    Prefers the first # heading, falls back to filename.

    Args:
        md: Raw markdown content.
        filename: Name of the markdown file.

    Returns:
        Extracted title string.
    """
    for line in md.split("\n"):
        line = line.strip()
        if line.startswith("# "):
            return line[2:].strip()
    name = filename.rsplit(".", 1)[0]
    return name.capitalize() if name != "index" else "Home"


def extract_headings(md: str, max_level: int = 3) -> list[tuple[int, str, str]]:
    """
    Extract all headings from markdown for TOC.

    Args:
        md: Raw markdown content.
        max_level: Maximum heading level to include.

    Returns:
        List of tuples: (level, text, anchor_id).
    """
    headings = []
    for line in md.split("\n"):
        match = re.match(r"^(#{1,6})\s+(.+)$", line)
        if match:
            level = len(match.group(1))
            if level <= max_level:
                text = match.group(2).strip()
                anchor = text.lower()
                anchor = re.sub(r"[^\w\s-]", "", anchor)
                anchor = re.sub(r"\s+", "-", anchor)
                headings.append((level, text, anchor))
    return headings


def render(md: str) -> str:
    """
    Render markdown to HTML.

    Args:
        md: Raw markdown content.

    Returns:
        Rendered HTML string.
    """
    import markdown

    return markdown.markdown(
        md,
        extensions=["extra", "tables", "fenced_code", "toc"],
        output_format="html5",
    )
