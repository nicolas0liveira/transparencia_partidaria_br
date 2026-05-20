import pandas as pd

from transparencia_partidaria_br.enrichment.classification import (
    classify_expense_type,
)

from transparencia_partidaria_br.enrichment.cnpj import (
    enrich_cnpj_data,
)

from transparencia_partidaria_br.utils.pipeline.logging import (
    log_transformation,
)

# =============================================================================
# Constantes
# =============================================================================

DESPESA_ADMINISTRATIVO = (
    "ADMINISTRATIVO"
)

DESPESA_FINALISTICO = (
    "FINALISTICO"
)

DESPESA_INDEFINIDO = (
    "INDEFINIDO"
)

# =============================================================================
# Features de Despesa
# =============================================================================


def create_expense_features(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Cria métricas derivadas despesa.
    """

    if "vl_gasto" not in df.columns:
        return df

    # -------------------------------------------------------------------------
    # Flags
    # -------------------------------------------------------------------------

    df[
        "in_despesa_administrativa"
    ] = (
        df["tp_gasto"]
        == DESPESA_ADMINISTRATIVO
    )

    df[
        "in_despesa_finalistica"
    ] = (
        df["tp_gasto"]
        == DESPESA_FINALISTICO
    )

    df[
        "in_despesa_indefinida"
    ] = (
        df["tp_gasto"]
        == DESPESA_INDEFINIDO
    )

    # -------------------------------------------------------------------------
    # Valores derivados
    # -------------------------------------------------------------------------

    df[
        "vl_despesa_administrativa"
    ] = (
        df["vl_gasto"]
        .where(
            df[
                "in_despesa_administrativa"
            ],
            0,
        )
    )

    df[
        "vl_despesa_finalistica"
    ] = (
        df["vl_gasto"]
        .where(
            df[
                "in_despesa_finalistica"
            ],
            0,
        )
    )

    df[
        "vl_despesa_indefinida"
    ] = (
        df["vl_gasto"]
        .where(
            df[
                "in_despesa_indefinida"
            ],
            0,
        )
    )

    return df


# =============================================================================
# Agregação Despesa Partido
# =============================================================================


def aggregate_expense_party_year(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Agrega despesas em nível:
    partido x ano
    """

    group_cols = [
        "sg_partido",
        "aa_exercicio",
    ]

    metricas = {
        "vl_gasto": "sum",

        "vl_despesa_administrativa":
            "sum",

        "vl_despesa_finalistica":
            "sum",

        "vl_despesa_indefinida":
            "sum",

        "cd_cpf_cnpj_fornecedor":
            "nunique",
    }

    df_agg = (
        df.groupby(
            group_cols,
            dropna=False,
        )
        .agg(metricas)
        .reset_index()
    )

    # -------------------------------------------------------------------------
    # Rename
    # -------------------------------------------------------------------------

    df_agg = df_agg.rename(
        columns={
            "vl_gasto":
                "vl_despesa_total",

            "cd_cpf_cnpj_fornecedor":
                "qtd_fornecedores_unicos",
        }
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
        / df_agg[
            "qtd_fornecedores_unicos"
        ].replace(
            0,
            pd.NA,
        )
    )

    return df_agg


# =============================================================================
# Pipeline principal
# =============================================================================


def enrich_expense_data(
    df_despesa: pd.DataFrame,
    df_cnpj: pd.DataFrame,
    df_classificacao: pd.DataFrame,
) -> pd.DataFrame:
    """
    Pipeline principal enrichment
    despesas partidárias.
    """

    df = df_despesa.copy()

    # -------------------------------------------------------------------------
    # Validação
    # -------------------------------------------------------------------------

    required_columns = [
        "cd_cpf_cnpj_fornecedor",
        "vl_gasto",
        "sg_partido",
        "ds_gasto",
    ]

    missing_columns = [
        col
        for col in required_columns
        if col not in df.columns
    ]

    if missing_columns:

        raise KeyError(
            (
                "Colunas obrigatórias ausentes "
                f"em despesa: {missing_columns}"
            )
        )

    # -------------------------------------------------------------------------
    # Enriquecimento CNPJ
    # -------------------------------------------------------------------------

    df = enrich_cnpj_data(
        df_base=df,
        df_cnpj=df_cnpj,
        cnpj_column=(
            "cd_cpf_cnpj_fornecedor"
        ),
    )

    # -------------------------------------------------------------------------
    # Cobertura enrichment
    # -------------------------------------------------------------------------

    cobertura_cnpj = (
        df["is_cnpj_enriquecido"]
        .mean()
    )

    # -------------------------------------------------------------------------
    # Classificação
    # -------------------------------------------------------------------------

    df = classify_expense_type(
        df_despesa=df,
        df_classificacao=(
            df_classificacao
        ),
    )

    # -------------------------------------------------------------------------
    # Features
    # -------------------------------------------------------------------------

    df = create_expense_features(df)

    # -------------------------------------------------------------------------
    # Logging
    # -------------------------------------------------------------------------

    log_transformation(
        dataframe="despesa_enriquecida",
        operation="ENRICH_EXPENSE_DATA",
        columns=[
            "tp_gasto",
            "tp_classificacao_origem",
            "vl_despesa_administrativa",
            "vl_despesa_finalistica",
            "vl_despesa_indefinida",
            "tp_porte_empresa",
            "tp_fornecedor",
        ],
        rules=[
            "CLASSIFICACAO_DESPESA",
            "FEATURE_ENGINEERING_DESPESA",
            "ENRICHMENT_CNPJ_FORNECEDOR",
            (
                f"CNPJ_COVERAGE="
                f"{cobertura_cnpj:.2%}"
            ),
        ],
    )

    return df