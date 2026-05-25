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

DESPESA_ADMINISTRATIVO = "ADMINISTRATIVO"
DESPESA_FINALISTICO = "FINALISTICO"
DESPESA_INDEFINIDO = "INDEFINIDO"

# =============================================================================
# Features de Despesa
# =============================================================================

def create_expense_features(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Cria features linha-a-linha de despesa.
    """

    if "vl_gasto" not in df.columns:
        return df

    # -------------------------------------------------------------------------
    # Flags
    # -------------------------------------------------------------------------

    df["in_despesa_administrativa"] = (
        df["tp_gasto"]
        == DESPESA_ADMINISTRATIVO
    )

    df["in_despesa_finalistica"] = (
        df["tp_gasto"]
        == DESPESA_FINALISTICO
    )

    df["in_despesa_indefinida"] = (
        df["tp_gasto"]
        == DESPESA_INDEFINIDO
    )

    # -------------------------------------------------------------------------
    # Valores derivados
    # -------------------------------------------------------------------------

    df["vl_despesa_administrativa"] = (
        df["vl_gasto"]
        .where(
            df["in_despesa_administrativa"],
            0,
        )
    )

    df["vl_despesa_finalistica"] = (
        df["vl_gasto"]
        .where(
            df["in_despesa_finalistica"],
            0,
        )
    )

    df["vl_despesa_indefinida"] = (
        df["vl_gasto"]
        .where(
            df["in_despesa_indefinida"],
            0,
        )
    )

    return df


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
            "Colunas obrigatórias ausentes "
            f"em despesa: {missing_columns}"
        )

    # -------------------------------------------------------------------------
    # Enriquecimento CNPJ
    # -------------------------------------------------------------------------

    df = enrich_cnpj_data(
        df_base=df,
        df_cnpj=df_cnpj,
        cnpj_column="cd_cpf_cnpj_fornecedor",
    )

    cobertura_cnpj = (
        df["is_cnpj_enriquecido"]
        .mean()
    )

    # -------------------------------------------------------------------------
    # Classificação
    # -------------------------------------------------------------------------

    df = classify_expense_type(
        df_despesa=df,
        df_classificacao=df_classificacao,
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
            f"CNPJ_COVERAGE={cobertura_cnpj:.2%}",
        ],
    )

    return df