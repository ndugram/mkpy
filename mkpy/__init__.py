"""mkpy - Minimalistic Python documentation generator and server."""

from .docs import Docs
from .markdown import render as render_markdown

__version__ = "1.4.1"

__all__ = ["Docs", "render_markdown", "__version__"]
