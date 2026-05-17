import typer

from transparencia_partidaria_br.cli.ckan import ckan
from transparencia_partidaria_br.cli import ingest
from transparencia_partidaria_br.config.runtime import get_config


app = typer.Typer(
    help="Transparência Partidária BR CLI",
    no_args_is_help=True,
)


# --------------------------------------
# CALLBACK (GLOBAL CONTEXT)
# --------------------------------------

@app.callback()
def main(ctx: typer.Context):
    """
    CLI principal do projeto de transparência partidária.
    """

    # Carrega config global uma única vez
    config = get_config()

    # Injeta no contexto do Typer
    ctx.obj = config


# --------------------------------------
# Subcomandos
# --------------------------------------

app.add_typer(
    ckan.app,
    name="ckan",
    help="Operações com CKAN",
)

app.add_typer(
    ingest.app,
    name="ingest",
    help="Ingestão de dados",
)


# --------------------------------------
# ENTRYPOINT
# --------------------------------------

if __name__ == "__main__":
    app()