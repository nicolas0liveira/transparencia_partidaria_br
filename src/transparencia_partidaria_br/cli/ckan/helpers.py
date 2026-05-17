import os
import requests
from requests.compat import urlparse
import typer
from rich.console import Console

from transparencia_partidaria_br.utils.ckan_client import CKANClient
from transparencia_partidaria_br.config.env import CKAN_BASE_URLS

# --------------------------------------
# HELPERS
# --------------------------------------

def _resolve_base_url(ctx: typer.Context, source: str | None, base_url: str | None, console: Console) -> str:
    if base_url:
        return base_url

    config = ctx.obj
    source = source or config.ckan.source

    if source not in CKAN_BASE_URLS:
        console.print(f"Fonte inválida: {source}")
        raise typer.Exit(1)

    return CKAN_BASE_URLS[source]


def _get_client(ctx: typer.Context, source: str | None, base_url: str | None, console: Console) -> CKANClient:
    url = _resolve_base_url(ctx, source, base_url, console)
    return CKANClient(url)

def get_size_from_url(url: str) -> str:
    try:
        resp = requests.head(url, allow_redirects=True, timeout=5)
        size = resp.headers.get("content-length")

        if size:
            size = int(size)
            return f"{size/1024/1024:.2f} MB"

    except Exception:
        pass

    return "-"

def detect_real_format(resource):
    url = resource.get("url", "")
    parsed = urlparse(url)
    filename = os.path.basename(parsed.path)

    if "." in filename:
        return filename.split(".")[-1].upper()

    return resource.get("format", "-")

def detect_content_type(url):
    try:
        r = requests.head(url, timeout=5)
        return r.headers.get("content-type")
    except Exception:
        return None