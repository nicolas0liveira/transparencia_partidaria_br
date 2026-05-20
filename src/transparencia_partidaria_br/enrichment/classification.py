import pandas as pd

from transparencia_partidaria_br.utils.pipeline.logging import (
    log_transformation,
)

# =============================================================================
# Constantes
# =============================================================================

GASTO_INDEFINIDO = (
    "INDEFINIDO"
)

# =============================================================================
# Classificação
# =============================================================================


def classify_expense_type(
    df_despesa: pd.DataFrame,
    df_classificacao: pd.DataFrame,
) -> pd.DataFrame:
    """
    Classifica despesas utilizando
    tabela oficial de classificação.

    Estratégia:
    1. Lookup exato
    2. Não classificados:
       INDEFINIDO
    """

    df = df_despesa.copy()

    classificacao = (
        df_classificacao.copy()
    )

    # -------------------------------------------------------------------------
    # Validação
    # -------------------------------------------------------------------------

    required_columns = [
        "ds_despesa",
        "tp_gasto",
    ]

    missing_columns = [
        col
        for col in required_columns
        if col not in classificacao.columns
    ]

    if missing_columns:

        raise KeyError(
            (
                "Colunas obrigatórias ausentes "
                "na classificação despesa: "
                f"{missing_columns}"
            )
        )

    # -------------------------------------------------------------------------
    # Normalização
    # -------------------------------------------------------------------------

    df["ds_gasto"] = (
        df["ds_gasto"]
        .fillna("")
        .astype(str)
        .str.upper()
        .str.strip()
    )

    classificacao["ds_despesa"] = (
        classificacao["ds_despesa"]
        .fillna("")
        .astype(str)
        .str.upper()
        .str.strip()
    )

    classificacao["tp_gasto"] = (
        classificacao["tp_gasto"]
        .fillna("")
        .astype(str)
        .str.upper()
        .str.strip()
    )

    # -------------------------------------------------------------------------
    # Lookup exato
    # -------------------------------------------------------------------------

    df = df.merge(
        classificacao[
            [
                "ds_despesa",
                "tp_gasto",
            ]
        ],
        how="left",
        left_on="ds_gasto",
        right_on="ds_despesa",
    )

    # -------------------------------------------------------------------------
    # Origem classificação
    # -------------------------------------------------------------------------

    df["tp_classificacao_origem"] = (
        "LOOKUP_EXATO"
    )

    # -------------------------------------------------------------------------
    # Não classificados
    # -------------------------------------------------------------------------

    mask_indefinido = (
        df["tp_gasto"].isna()
    )

    df.loc[
        mask_indefinido,
        "tp_gasto",
    ] = GASTO_INDEFINIDO

    df.loc[
        mask_indefinido,
        "tp_classificacao_origem",
    ] = "NAO_CLASSIFICADO"

    # -------------------------------------------------------------------------
    # Limpeza
    # -------------------------------------------------------------------------

    df = df.drop(
        columns=["ds_despesa"],
        errors="ignore",
    )

    # -------------------------------------------------------------------------
    # Logging
    # -------------------------------------------------------------------------

    log_transformation(
        dataframe="df_despesa",
        operation="CLASSIFY_EXPENSE_TYPE",
        columns=[
            "ds_gasto",
            "tp_gasto",
            "tp_classificacao_origem",
        ],
        rules=[
            "LOOKUP_EXATO",
            "INDEFINIDO",
        ],
    )

    return df