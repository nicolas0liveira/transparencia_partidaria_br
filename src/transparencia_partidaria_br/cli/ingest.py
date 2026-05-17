import typer

app = typer.Typer(help="Ingestão de dados")


@app.command()
def tse():
    print("Ingestão do TSE")