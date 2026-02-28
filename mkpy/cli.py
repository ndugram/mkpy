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
def build(
    folder: Annotated[
        str,
        typer.Option("--folder", "-f", help="Path to folder containing markdown files"),
    ] = "docs",
    output: Annotated[
        str,
        typer.Option("--output", "-o", help="Output directory for static files"),
    ] = "project",
    title: Annotated[
        str,
        typer.Option("--title", "-t", help="Documentation title"),
    ] = "MKPY",
    theme: Annotated[
        str,
        typer.Option("--theme", help="Theme: light or dark"),
    ] = "light",
    no_nav: Annotated[
        bool,
        typer.Option("--no-nav", help="Disable navigation menu"),
    ] = False,
) -> None:
    from rich.console import Console
    from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
    from rich.table import Table
    from rich.panel import Panel
    from rich import box

    console = Console()

    os.makedirs(output, exist_ok=True)
    docs = Docs(
        folder=folder,
        title=title,
        theme=theme,
        show_nav=not no_nav,
    )

    routes = list(docs.routes.items())
    total = len(routes)

    console.print(Panel.fit(
        f"[bold cyan]MKPY Build[/bold cyan]\n"
        f"Converting [yellow]{total}[/yellow] markdown files to HTML",
        border_style="cyan",
    ))

    table = Table(box=box.ROUNDED, show_header=True, header_style="bold magenta")
    table.add_column("Status", style="green", width=8)
    table.add_column("Source", style="cyan")
    table.add_column("Output", style="yellow")

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
        console=console,
    ) as progress:
        task = progress.add_task("[cyan]Building...", total=total)

        for route, md_path in routes:
            html_content = docs.render(md_path)

            if route == "/":
                html_filename = "index.html"
            else:
                html_filename = f"{route.lstrip('/')}.html"

            output_path = os.path.join(output, html_filename)

            os.makedirs(os.path.dirname(output_path), exist_ok=True)

            with open(output_path, "w", encoding="utf-8") as f:
                f.write(html_content)
            relative_md = os.path.relpath(md_path, folder)
            table.add_row("✓", relative_md, html_filename)

            progress.advance(task)

    console.print()
    console.print(table)

    console.print()
    console.print(Panel.fit(
        f"[bold green]✓ Build complete![/bold green]\n"
        f"Output directory: [yellow]{os.path.abspath(output)}[/yellow]\n"
        f"Files created: [cyan]{total}[/cyan]",
        border_style="green",
    ))


@app.command()
def version() -> None:
    from . import __version__

    typer.echo(f"mkpy {__version__}")


def main() -> None:
    app()


if __name__ == "__main__":
    main()
