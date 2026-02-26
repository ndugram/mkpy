"""HTTP server for mkpy."""

from __future__ import annotations

import mimetypes
import os
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .docs import Docs


class DocsHandler(BaseHTTPRequestHandler):
    """HTTP request handler for mkpy documentation server."""

    docs: Docs = None  # type: ignore[assignment]

    def do_GET(self) -> None:
        """Handle GET requests."""
        path = self.path.split("?")[0].rstrip("/") or "/"

        if path == "/sitemap.xml":
            sitemap = self.docs.generate_sitemap(
                f"http://{self.docs.host}:{self.docs.port}"
            )
            self.send_response(200)
            self.send_header("Content-Type", "application/xml")
            self.end_headers()
            self.wfile.write(sitemap.encode("utf-8"))
            return
        if self._serve_static(path):
            return

        if path in self.docs.routes:
            html = self.docs.render(self.docs.routes[path])

            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Cache-Control", "no-cache")
            self.end_headers()
            self.wfile.write(html.encode("utf-8"))

        elif path + "/" in self.docs.routes:
            self.send_response(302)
            self.send_header("Location", path + "/")
            self.end_headers()

        else:
            html = self.docs.render_error(404, "Page Not Found")
            self.send_response(404)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(html.encode("utf-8"))

    def _serve_static(self, path: str) -> bool:
        """Serve static files from static/ folder."""
        static_folder = os.path.join(self.docs.folder, "..", "static")

        for static_base in [static_folder, "static", "assets"]:
            if os.path.isdir(static_base):
                file_path = os.path.join(static_base, path.lstrip("/"))
                if os.path.isfile(file_path):
                    self._serve_file(file_path)
                    return True

        return False

    def _serve_file(self, file_path: str) -> None:
        """Serve a static file."""
        mime_type, _ = mimetypes.guess_type(file_path)
        content_type = mime_type or "application/octet-stream"

        with open(file_path, "rb") as f:
            content = f.read()

        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)

    def log_message(self, format: str, *args) -> None:
        """Log HTTP requests."""
        path = self.path.split("?")[0]
        code = str(self.response_code) if hasattr(self, "response_code") else "200"

        try:
            from rich.console import Console

            console = Console()
            if code.startswith("2"):
                console.print(f"[green]{code}[/green] [dim]{path}[/dim]")
            elif code.startswith("4") or code.startswith("5"):
                console.print(f"[red]{code}[/red] [dim]{path}[/dim]")
            else:
                console.print(f"[yellow]{code}[/yellow] [dim]{path}[/dim]")
        except Exception:
            print(f"{code} {path}")


def run_server(docs: Docs) -> None:
    """Start the documentation server."""
    try:
        from rich.console import Console

        console = Console()
        use_rich = True
    except ImportError:
        use_rich = False

    DocsHandler.docs = docs

    static_folder = os.path.join(docs.folder, "..", "static")
    if not os.path.exists(static_folder):
        os.makedirs(static_folder, exist_ok=True)

    url = f"http://{docs.host}:{docs.port}"

    if use_rich:
        console.print("[bold green]⚡[/bold green] [bold]mkpy[/bold] started")
        console.print(f"📂 Docs: [cyan]{docs.folder}[/cyan]")
        console.print(f"🎨 Theme: [cyan]{docs.theme}[/cyan]")
        console.print(f"[success]➜[/success] [bold]{url}[/bold]")
        console.print("[dim]Press Ctrl+C to stop[/dim]")
    else:
        print("⚡ mkpy started")
        print(f"📂 Docs: {docs.folder}")
        print(f"🎨 Theme: {docs.theme}")
        print(f"➜ {url}")
        print("Press Ctrl+C to stop")

    server = HTTPServer((docs.host, docs.port), DocsHandler)

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        if use_rich:
            console.print("[warning]👋[/warning] Shutting down...")
        else:
            print("👋 Shutting down...")
