import pandas as pd


def create_financial_features(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Cria variáveis derivadas financeiras.
    """

    df = df.copy()

    # =========================================================================
    # Percentual despesa administrativa
    # =========================================================================

    df[
        "pct_despesa_administrativa"
    ] = (
        df[
            "vl_despesa_administrativa"
        ]
        / df[
            "vl_despesa_total"
        ]
    )

    # =========================================================================
    # Ticket médio despesa
    # =========================================================================

    df[
        "ticket_medio_despesa"
    ] = (
        df[
            "vl_despesa_total"
        ]
        / df[
            "qtd_despesas"
        ]
    )

    # =========================================================================
    # Ticket médio receita
    # =========================================================================

    df[
        "ticket_medio_receita"
    ] = (
        df[
            "vl_receita_total"
        ]
        / df[
            "qtd_receitas"
        ]
    )

    return df

# TODO: explicar o uso do qcut para gerar porte financeiro baseado em quartis
def create_financial_size_feature(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Cria variável de porte financeiro.
    """

    df = df.copy()

    df[
        "porte_financeiro"
    ] = pd.qcut(
            df["vl_receita_total"],
            q=4,
            labels=[
                "pequeno",
                "medio",
                "grande",
                "muito_grande",
            ],
            duplicates="drop",
        )

    return df