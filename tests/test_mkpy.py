"""Tests for mkpy."""
from __future__ import annotations

import os
import tempfile
from pathlib import Path

import pytest

from mkpy import Docs
from mkpy.markdown import extract_title, render as render_markdown


class TestDocs:
    """Test Docs class."""

    def test_default_values(self):
        """Test default initialization."""
        with tempfile.TemporaryDirectory() as tmpdir:
            docs_path = Path(tmpdir) / "docs"
            docs_path.mkdir()
            (docs_path / "index.md").write_text("# Hello")

            docs = Docs(folder=str(docs_path))

            assert docs.folder == str(docs_path)
            assert docs.title == "MKPY"
            assert docs.theme == "light"
            assert docs.port == 8000
            assert docs.show_nav is True

    def test_custom_values(self):
        """Test custom initialization."""
        with tempfile.TemporaryDirectory() as tmpdir:
            docs_path = Path(tmpdir) / "docs"
            docs_path.mkdir()
            (docs_path / "index.md").write_text("# Hello")

            docs = Docs(
                folder=str(docs_path),
                title="Custom",
                theme="dark",
                port=3000,
                show_nav=False,
            )

            assert docs.title == "Custom"
            assert docs.theme == "dark"
            assert docs.port == 3000
            assert docs.show_nav is False

    def test_routes_creation(self):
        """Test route creation from files."""
        with tempfile.TemporaryDirectory() as tmpdir:
            docs_path = Path(tmpdir) / "docs"
            docs_path.mkdir()
            (docs_path / "index.md").write_text("# Home")
            (docs_path / "about.md").write_text("# About")
            (docs_path / "guide").mkdir()
            (docs_path / "guide" / "install.md").write_text("# Install")

            docs = Docs(folder=str(docs_path))

            assert "/" in docs.routes
            assert "/about" in docs.routes
            assert "/guide/install" in docs.routes

    def test_theme_validation(self):
        """Test theme validation."""
        with tempfile.TemporaryDirectory() as tmpdir:
            docs_path = Path(tmpdir) / "docs"
            docs_path.mkdir()
            (docs_path / "index.md").write_text("# Hello")

            with pytest.raises(ValueError):
                Docs(folder=str(docs_path), theme="invalid")

    def test_render_html(self):
        """Test HTML rendering."""
        with tempfile.TemporaryDirectory() as tmpdir:
            docs_path = Path(tmpdir) / "docs"
            docs_path.mkdir()
            (docs_path / "index.md").write_text("# Hello\n\n**Bold**")

            docs = Docs(folder=str(docs_path))

            html = docs.render(docs.routes["/"])

            # h1 with id from toc extension
            assert "<h1" in html
            assert "Hello" in html
            assert "<strong>Bold</strong>" in html
            assert "mkpy-nav" in html

    def test_render_without_nav(self):
        """Test HTML rendering without navigation."""
        with tempfile.TemporaryDirectory() as tmpdir:
            docs_path = Path(tmpdir) / "docs"
            docs_path.mkdir()
            (docs_path / "index.md").write_text("# Hello")

            docs = Docs(folder=str(docs_path), show_nav=False)

            html = docs.render(docs.routes["/"])

            # nav element should not be present
            assert "<nav class=\"mkpy-nav\">" not in html


class TestMarkdown:
    """Test markdown utilities."""

    def test_extract_title_from_heading(self):
        """Test title extraction from heading."""
        md = "# My Title\n\nContent"
        assert extract_title(md, "test.md") == "My Title"

    def test_extract_title_from_filename(self):
        """Test title extraction from filename."""
        md = "No heading here"
        assert extract_title(md, "about.md") == "About"

    def test_extract_title_index(self):
        """Test title extraction for index file."""
        md = "No heading"
        assert extract_title(md, "index.md") == "Home"

    def test_render_markdown(self):
        """Test markdown rendering."""
        md = "# Heading\n\n**bold** and *italic*"
        html = render_markdown(md)

        # h1 with id from toc extension
        assert "<h1" in html
        assert "Heading" in html
        assert "<strong>bold</strong>" in html
        assert "<em>italic</em>" in html

    def test_render_code_blocks(self):
        """Test code block rendering."""
        md = "```python\nprint('hello')\n```"
        html = render_markdown(md)

        assert "<code" in html
        assert "print('hello')" in html

    def test_render_tables(self):
        """Test table rendering."""
        md = "| a | b |\n|---|---|\n| 1 | 2 |"
        html = render_markdown(md)

        assert "<table>" in html
        assert "<td>1</td>" in html
