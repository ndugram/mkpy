from __future__ import annotations

import importlib.util
import os
import sys
from typing import Annotated

import typer
from typing_extensions import Annotated as TyperAnnotated

from .docs import Docs

app = typer.Typer(help="Minimalistic documentation generator and server")


def load_docs_from_file(file_path: str) -> Docs:
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"File '{file_path}' not found")

    spec = importlib.util.spec_from_file_location("docs_config", file_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load '{file_path}'")

    module = importlib.util.module_from_spec(spec)
    sys.modules["docs_config"] = module
    spec.loader.exec_module(module)

    docs = None
    for name in dir(module):
        obj = getattr(module, name)
        if isinstance(obj, Docs):
            docs = obj
            break

    if docs is None:
        raise ValueError(f"No Docs instance found in '{file_path}'")

    return docs


@app.command()
def serve(
    file: Annotated[
        str | None,
        typer.Argument(help="Python file with Docs configuration"),
    ] = None,
    folder: Annotated[
        str,
        typer.Option("--folder", "-f", help="Path to folder containing markdown files"),
    ] = "docs",
    title: Annotated[
        str,
        typer.Option("--title", "-t", help="Documentation title"),
    ] = "MKPY",
    theme: Annotated[
        str,
        typer.Option("--theme", help="Theme: light or dark"),
    ] = "light",
    host: Annotated[
        str,
        typer.Option("--host", help="Host address"),
    ] = "127.0.0.1",
    port: Annotated[
        int,
        typer.Option("--port", "-p", help="Port number"),
    ] = 8000,
    no_nav: Annotated[
        bool,
        typer.Option("--no-nav", help="Disable navigation menu"),
    ] = False,
) -> None:
    """Serve documentation."""
    if file:
        docs = load_docs_from_file(file)
    else:
        docs = Docs(
            folder=folder,
            title=title,
            theme=theme,
            host=host,
            port=port,
            show_nav=not no_nav,
        )
    docs.run()


@app.command()
def version() -> None:
    from . import __version__

    typer.echo(f"mkpy {__version__}")


def main() -> None:
    app()


if __name__ == "__main__":
    main()
