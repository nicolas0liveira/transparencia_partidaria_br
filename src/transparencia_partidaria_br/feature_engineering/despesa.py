import pandas as pd

from transparencia_partidaria_br.utils.pipeline.logging import (
    log_transformation,
)

# =============================================================================
# Agregação Despesa Partido
# =============================================================================


def aggregate_expense_party_year(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Agrega despesas em nível:
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
            vl_despesa_total=(
                "vl_gasto",
                "sum",
            ),
            qtd_despesas=(
                "vl_gasto",
                "count",
            ),
            vl_despesa_administrativa=(
                "vl_despesa_administrativa",
                "sum",
            ),
            qtd_despesas_administrativas=(
                "in_despesa_administrativa",
                "sum",
            ),
            vl_despesa_finalistica=(
                "vl_despesa_finalistica",
                "sum",
            ),
            qtd_despesas_finalisticas=(
                "in_despesa_finalistica",
                "sum",
            ),
            vl_despesa_indefinida=(
                "vl_despesa_indefinida",
                "sum",
            ),
            qtd_despesas_indefinidas=(
                "in_despesa_indefinida",
                "sum",
            ),
            qtd_fornecedores_unicos=(
                "cd_cpf_cnpj_fornecedor",
                "nunique",
            ),
        )
        .reset_index()
    )

    # -------------------------------------------------------------------------
    # Totais seguros
    # -------------------------------------------------------------------------

    total_despesa = (
        df_agg["vl_despesa_total"]
        .replace(
            0,
            pd.NA,
        )
    )

    qtd_despesas = (
        df_agg["qtd_despesas"]
        .replace(
            0,
            pd.NA,
        )
    )

    # -------------------------------------------------------------------------
    # Percentuais
    # -------------------------------------------------------------------------

    df_agg[
        "pct_despesa_administrativa"
    ] = (
        df_agg[
            "vl_despesa_administrativa"
        ]
        / total_despesa
    ) * 100

    df_agg[
        "pct_despesa_finalistica"
    ] = (
        df_agg[
            "vl_despesa_finalistica"
        ]
        / total_despesa
    ) * 100

    df_agg[
        "pct_despesa_indefinida"
    ] = (
        df_agg[
            "vl_despesa_indefinida"
        ]
        / total_despesa
    ) * 100

    # -------------------------------------------------------------------------
    # Ticket médio
    # -------------------------------------------------------------------------

    df_agg[
        "ticket_medio_despesa"
    ] = (
        df_agg["vl_despesa_total"]
        / qtd_despesas
    )

    # -------------------------------------------------------------------------
    # Logging
    # -------------------------------------------------------------------------

    log_transformation(
        dataframe="partido_ano_despesa",
        operation="AGGREGATE_EXPENSE_PARTY_YEAR",
        columns=[
            "vl_despesa_total",
            "qtd_despesas",
            "vl_despesa_administrativa",
            "vl_despesa_finalistica",
            "vl_despesa_indefinida",
            "pct_despesa_administrativa",
            "pct_despesa_finalistica",
            "pct_despesa_indefinida",
            "ticket_medio_despesa",
            "qtd_fornecedores_unicos",
        ],
        rules=[
            "GROUPBY_PARTIDO_ANO",
            "EXPENSE_AGGREGATION",
            "PERCENTUAL_DESPESA",
            "TICKET_MEDIO_DESPESA",
        ],
    )

    return df_agg