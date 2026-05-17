import typer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from transparencia_partidaria_br.cli.ckan.helpers import _get_client


app = typer.Typer(help="Exploração interativa de datasets CKAN")

console = Console()

# --------------------------------------
# EXPLORE
# --------------------------------------

@app.command(help="Modo interativo para explorar datasets CKAN")
def explore(
    ctx: typer.Context,
    source: str | None = typer.Option(None, help="Fonte CKAN"),
    base_url: str | None = typer.Option(None),
    rows: int = typer.Option(30, help="Itens por página"),
):
    client = _get_client(ctx, source, base_url, console)

    page = 1

    while True:
        start = (page - 1) * rows
        result = client.package_search("", rows=rows, start=start)

        total = result.get("count", 0)
        datasets = result.get("results", [])
        total_pages = (total + rows - 1) // rows

        if not datasets:
            console.print("Nenhum dataset encontrado")
            break

        # tabela datasets
        table = Table(title=f"Datasets | Página {page}/{total_pages}")
        table.add_column("#", justify="right")
        table.add_column("Nome", style="cyan")
        table.add_column("Título")

        for i, pkg in enumerate(datasets, start=start + 1):
            table.add_row(str(i), pkg.get("name", ""), pkg.get("title", ""))

        console.print(table)

        # ajuda
        console.print(
            f"\nComandos: [a] anterior | [p] próxima | [s] sair | [número] {start+1}-{start+len(datasets)}",
            markup=False,
        )

        choice = console.input("Escolha: ").strip().lower()

        # sair
        if choice == "s":
            break

        # próxima página
        elif choice == "p":
            if page < total_pages:
                page += 1
            else:
                console.print("Já está na última página")

        # página anterior
        elif choice == "a":
            if page > 1:
                page -= 1
            else:
                console.print("Já está na primeira página")

        # seleção dataset
        elif choice.isdigit():
            idx = int(choice)
            local_index = idx - start - 1

            if not (0 <= local_index < len(datasets)):
                console.print("Número fora da página atual")
                continue

            selected = datasets[local_index]["name"]

            console.print(f"\nCarregando: {selected}\n")

            pkg = client.package_show(selected)

            console.print(
                Panel(
                    f"Nome: {pkg.get('name', '-')}\n"
                    f"Título: {pkg.get('title', '-')}\n"
                    f"Organização: {pkg.get('organization', {}).get('title', '-')}",
                    title="Dataset Info",
                )
            )

            resources = pkg.get("resources", [])

            if not resources:
                console.print("Nenhum resource disponível")
                console.input("\nPressione ENTER para voltar...")
                continue

            # tabela resources
            res_table = Table(title="Resources")
            res_table.add_column("#", justify="right")
            res_table.add_column("ID", style="green")
            res_table.add_column("Nome", style="cyan")
            res_table.add_column("Descrição", overflow="fold")
            res_table.add_column("Formato")
            res_table.add_column("URL", style="blue", overflow="fold")

            for i, r in enumerate(resources, start=1):
                desc = r.get("description") or "-"
                res_table.add_row(
                    str(i),
                    r.get("id", ""),
                    r.get("name", ""),
                    desc,
                    r.get("format", ""),
                    r.get("url", ""),
                )

            console.print(res_table)

            console.print("\nPressione ENTER para voltar à lista")
            console.input()

        else:
            console.print("Opção inválida")