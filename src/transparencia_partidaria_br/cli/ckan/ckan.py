"""
CLI utilitário para interação com APIs CKAN.
"""
import re

import typer

from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from transparencia_partidaria_br.cli.ckan.helpers import _get_client, get_size_from_url
from transparencia_partidaria_br.config.env import CKAN_BASE_URLS
from transparencia_partidaria_br.cli.ckan.explore import explore as explore_cmd


console = Console()

app = typer.Typer(help="Operações com CKAN", no_args_is_help=True)

# --------------------------------------
# SUB-APPS (GRUPOS)
# --------------------------------------
config_app = typer.Typer(help="Configuração do CKAN", no_args_is_help=True)
dataset_app = typer.Typer(help="Operações com datasets", no_args_is_help=True)
query_app = typer.Typer(help="Consultas", no_args_is_help=True)
export_app = typer.Typer(help="Exportação", no_args_is_help=True)

dataset_app.command(name="explore",help="Exploração interativa de datasets",)(explore_cmd)

app.add_typer(config_app, name="config")
app.add_typer(dataset_app, name="dataset")
app.add_typer(query_app, name="query")
app.add_typer(export_app, name="export")


# ======================================
# CONFIG
# ======================================

@config_app.command()
def sources(ctx: typer.Context):
    config = ctx.obj
    default = config.ckan.source

    table = Table(title="Fontes CKAN")
    table.add_column("Nome", style="cyan")
    table.add_column("URL")

    for name, url in CKAN_BASE_URLS.items():
        label = f"{name} (default)" if name == default else name
        table.add_row(label, url)

    console.print(table)


@config_app.command()
def current(ctx: typer.Context):
    config = ctx.obj
    source = config.ckan.source

    console.print(
        Panel(
            f"Fonte: {source}\nURL: {CKAN_BASE_URLS[source]}",
            title="Configuração Atual",
        )
    )


@config_app.command()
def use(source: str):
    from transparencia_partidaria_br.config.runtime import (
        get_config,
        save_config,
        reset_config_cache,
    )

    if source not in CKAN_BASE_URLS:
        console.print(f"Fonte inválida: {source}")
        raise typer.Exit(1)

    config = get_config()
    config.ckan.source = source

    save_config(config)
    reset_config_cache()

    console.print(f"Fonte definida para: {source}")


# ======================================
# DATASET
# ======================================

@dataset_app.command(name="list", help="Listar datasets disponíveis")
def list_packages(
    ctx: typer.Context,
    source: str | None = None,
    base_url: str | None = None,
):
    client = _get_client(ctx, source, base_url, console)

    packages = client.package_list()

    table = Table(title="Datasets")
    table.add_column("#")
    table.add_column("Nome", style="cyan")

    for i, name in enumerate(packages, start=1):
        table.add_row(str(i), name)

    console.print(table)


@dataset_app.command(name="search", help="Buscar datasets")
def search(
    ctx: typer.Context,
    query: str = "",
    source: str | None = None,
    base_url: str | None = None,
):
    client = _get_client(ctx, source, base_url, console)
    result = client.package_search(query)

    table = Table(title="Resultados")
    table.add_column("Nome")
    table.add_column("Título")

    for r in result.get("results", []):
        table.add_row(r["name"], r.get("title", ""))

    console.print(table)


@dataset_app.command(name="show", help="Mostrar detalhes de um dataset")
def show(
    ctx: typer.Context,
    dataset: str,
    source: str | None = None,
    base_url: str | None = None,
    with_size: bool = typer.Option(False, help="Buscar tamanho real via HTTP")
):
    client = _get_client(ctx, source, base_url, console)

    pkg = client.package_show(dataset)

    # ---------------------------
    # LIMPEZA
    # ---------------------------
    def clean(text: str | None) -> str:
        if not text:
            return "-"
        return re.sub("<.*?>", "", text).strip()

    # ---------------------------
    # METADATA PRINCIPAL
    # ---------------------------
    console.print(
        Panel(
            f"[bold]Nome:[/] {pkg.get('name', '-')}\n"
            f"[bold]Título:[/] {pkg.get('title', '-')}\n"
            f"[bold]Organização:[/] {pkg.get('organization', {}).get('title', '-')}\n"
            f"[bold]Criado em:[/] {pkg.get('metadata_created', '-')}\n"
            f"[bold]Atualizado em:[/] {pkg.get('metadata_modified', '-')}\n"
            f"[bold]Resources:[/] {len(pkg.get('resources', []))}",
            title="Informações Gerais",
        )
    )

    # ---------------------------
    # DESCRIÇÃO
    # ---------------------------
    notes = clean(pkg.get("notes"))

    if notes and notes != "-":
        console.print(Panel(notes, title="Descrição"))

    # ---------------------------
    # TAGS
    # ---------------------------
    tags = pkg.get("tags", [])

    if tags:
        tag_list = ", ".join(t["name"] for t in tags)
        console.print(Panel(tag_list, title="Tags"))

    # ---------------------------
    # RESOURCES
    # ---------------------------
    resources = pkg.get("resources", [])

    if not resources:
        console.print("Nenhum resource disponível")
        return

    table = Table(title="Resources")

    table.add_column("#", justify="center")
    table.add_column("ID", justify="center")
    table.add_column("Nome", style="cyan")
    table.add_column("Tamanho", justify="center")
    table.add_column("URL", overflow="fold", style="blue")

    for i, r in enumerate(resources, start=1):
        size = r.get("size")
        if with_size:
            size_str = get_size_from_url(r.get("url", ""))
        elif size:
            size_str = f"{size/1024/1024:.2f} MB"
        else:
            size_str = "-"

        table.add_row(
            str(i),
            r.get("id", "-"),
            r.get("name", "-"),
            size_str,
            r.get("url", "-"),
        )

    console.print(table)


# ======================================
# QUERY
# ======================================

@query_app.command(name="sql", help="Executar consulta SQL (CKAN DataStore)")
def sql(ctx: typer.Context, query: str):
    client = _get_client(ctx, None, None, console)
    result = client.datastore_sql(query)

    console.print(result)


# ======================================
# EXPORT
# ======================================

@export_app.command(name="parquet", help="Exportar recurso para formato Parquet")
def to_parquet(ctx: typer.Context, resource_id: str, output: str):
    client = _get_client(ctx, None, None, console)
    path = client.to_parquet(resource_id, output)

    console.print(f"Salvo em: {path}")


# ======================================
# DOWNLOAD
# ======================================

@dataset_app.command(name="download", help="Baixar resource de um dataset")
def download(
    ctx: typer.Context,
    dataset: str,
    resource: int | None = typer.Option(
        None, help="Índice do resource (1,2,3...)"
    ),
    resource_id: str | None = typer.Option(
        None, help="ID do resource"
    ),
    output_dir: str = typer.Option(
        "data/raw", help="Diretório de saída"
    ),
    source: str | None = None,
    base_url: str | None = None,
    with_size: bool = typer.Option(False, help="Exibir tamanho real via HTTP"),
):
    client = _get_client(ctx, source, base_url, console)

    pkg = client.package_show(dataset)
    resources = pkg.get("resources", [])

    if not resources:
        console.print("Nenhum resource disponível")
        raise typer.Exit(1)

    # ---------------------------
    # SELEÇÃO DO RESOURCE
    # ---------------------------
    selected = None

    if resource_id:
        selected = next((r for r in resources if r["id"] == resource_id), None)
        if not selected:
            console.print(f"Resource ID não encontrado: {resource_id}")
            raise typer.Exit(1)

    elif resource:
        if not (1 <= resource <= len(resources)):
            console.print("Índice de resource inválido")
            raise typer.Exit(1)
        selected = resources[resource - 1]

    else:
        # fallback: listar e pedir escolha
        table = Table(title="Escolha um resource")
        table.add_column("#", justify="center")
        table.add_column("ID", justify="center")
        table.add_column("Nome", style="cyan")
        table.add_column("Tamanho", justify="center")
        table.add_column("URL", overflow="fold", style="blue")

        for i, r in enumerate(resources, start=1):
            size = r.get("size")
            if with_size:
                size_str = get_size_from_url(r.get("url", ""))
            elif size:
                size_str = f"{size/1024/1024:.2f} MB"
            else:
                size_str = "-"

            table.add_row(
                str(i),
                r.get("id", "-"),
                r.get("name", "-"),
                size_str,
                r.get("url", "-"),
            )

        console.print(table)

        choice = console.input("Escolha o número do resource: ").strip()

        if not choice.isdigit():
            console.print("Entrada inválida")
            raise typer.Exit(1)

        idx = int(choice)

        if not (1 <= idx <= len(resources)):
            console.print("Número inválido")
            raise typer.Exit(1)

        selected = resources[idx - 1]

    # ---------------------------
    # DOWNLOAD
    # ---------------------------
    console.print(f"Baixando: {selected.get('name')}")

    path = client.download_resource(
        resource=selected,
        output_dir=output_dir,
    )

    console.print(f"Salvo em: {path}")

# --------------------------------------
# ENTRYPOINT
# --------------------------------------

if __name__ == "__main__":
    app()