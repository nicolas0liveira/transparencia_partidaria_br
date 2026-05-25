import pandas as pd

from transparencia_partidaria_br.utils.pipeline.logging import (
    log_transformation,
)

# =============================================================================
# Agregação Receita Partido
# =============================================================================


def aggregate_revenue_party_year(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Agrega receitas em nível:
    partido x ano.
    """

    group_cols = [
        "sg_partido",
        "aa_exercicio",
    ]

    df_agg = (
        df.groupby(
            group_cols,
            dropna=False,
        )
        .agg(
            vl_receita_total=(
                "vl_receita",
                "sum",
            ),
            qtd_receitas=(
                "vl_receita",
                "count",
            ),
            vl_receita_publica=(
                "vl_receita_publica",
                "sum",
            ),
            qtd_receitas_publicas=(
                "in_receita_publica",
                "sum",
            ),
            vl_receita_privada=(
                "vl_receita_privada",
                "sum",
            ),
            qtd_receitas_privadas=(
                "in_receita_privada",
                "sum",
            ),
            vl_receita_partidaria=(
                "vl_receita_partidaria",
                "sum",
            ),
            qtd_receitas_partidarias=(
                "in_receita_partidaria",
                "sum",
            ),
            qtd_doadores_unicos=(
                "cd_cpf_cnpj_doador",
                "nunique",
            ),
        )
        .reset_index()
    )

    # -------------------------------------------------------------------------
    # Totais seguros
    # -------------------------------------------------------------------------

    total_receita = (
        df_agg["vl_receita_total"]
        .replace(
            0,
            pd.NA,
        )
    )

    qtd_receitas = (
        df_agg["qtd_receitas"]
        .replace(
            0,
            pd.NA,
        )
    )

    # -------------------------------------------------------------------------
    # Percentuais
    # -------------------------------------------------------------------------

    df_agg["pct_receita_publica"] = (
        df_agg["vl_receita_publica"]
        / total_receita
    ) * 100

    df_agg["pct_receita_privada"] = (
        df_agg["vl_receita_privada"]
        / total_receita
    ) * 100

    df_agg["pct_receita_partidaria"] = (
        df_agg["vl_receita_partidaria"]
        / total_receita
    ) * 100

    # -------------------------------------------------------------------------
    # Ticket médio
    # -------------------------------------------------------------------------

    df_agg["ticket_medio_receita"] = (
        df_agg["vl_receita_total"]
        / qtd_receitas
    )


    log_transformation(
        dataframe="partido_ano_receita",
        operation="AGGREGATE_REVENUE_PARTY_YEAR",
        columns=[
            "vl_receita_total",
            "qtd_receitas",
            "vl_receita_publica",
            "vl_receita_privada",
            "vl_receita_partidaria",
            "pct_receita_publica",
            "pct_receita_privada",
            "pct_receita_partidaria",
            "ticket_medio_receita",
            "qtd_doadores_unicos",
        ],
        rules=[
            "GROUPBY_PARTIDO_ANO",
            "REVENUE_AGGREGATION",
            "PERCENTUAL_RECEITA",
            "TICKET_MEDIO_RECEITA",
        ],
    )
    return df_agg