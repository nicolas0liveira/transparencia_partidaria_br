import pandas as pd

from transparencia_partidaria_br.enrichment.cnpj import (
    enrich_cnpj_data,
)

from transparencia_partidaria_br.utils.pipeline.logging import (
    log_transformation,
)

# =============================================================================
# Constantes
# =============================================================================

RECEITA_PUBLICA = "PUBLICA"

RECEITA_PRIVADA = "PRIVADA"

RECEITA_PARTIDARIA = "PARTIDARIA"

RECEITA_OUTROS = "OUTROS"

# =============================================================================
# Classificação de Receita
# =============================================================================


def classify_revenue_source(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Classifica origem da receita.
    """

    if "ds_tp_origem_doacao" not in df.columns:
        return df

    origem = (
        df["ds_tp_origem_doacao"]
        .fillna("")
        .str.upper()
    )

    df["tp_receita"] = RECEITA_OUTROS

    # -------------------------------------------------------------------------
    # Receita pública
    # -------------------------------------------------------------------------

    mask_publica = origem.str.contains(
        "FUNDO PARTIDARIO|FUNDO ESPECIAL",
        regex=True,
        na=False,
    )

    df.loc[
        mask_publica,
        "tp_receita",
    ] = RECEITA_PUBLICA

    # -------------------------------------------------------------------------
    # Receita privada
    # -------------------------------------------------------------------------

    mask_privada = origem.str.contains(
        "PESSOAS FISICAS|PESSOAS JURIDICAS",
        regex=True,
        na=False,
    )

    df.loc[
        mask_privada,
        "tp_receita",
    ] = RECEITA_PRIVADA

    # -------------------------------------------------------------------------
    # Receita partidária
    # -------------------------------------------------------------------------

    mask_partidaria = origem.str.contains(
        "PARTIDOS POLITICOS",
        regex=True,
        na=False,
    )

    df.loc[
        mask_partidaria,
        "tp_receita",
    ] = RECEITA_PARTIDARIA

    return df


# =============================================================================
# Features de Receita
# =============================================================================


def create_revenue_features(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Cria features linha-a-linha de receita.
    """

    if "vl_receita" not in df.columns:
        return df

    # -------------------------------------------------------------------------
    # Flags
    # -------------------------------------------------------------------------

    df["in_receita_publica"] = (
        df["tp_receita"]
        == RECEITA_PUBLICA
    )

    df["in_receita_privada"] = (
        df["tp_receita"]
        == RECEITA_PRIVADA
    )

    df["in_receita_partidaria"] = (
        df["tp_receita"]
        == RECEITA_PARTIDARIA
    )

    # -------------------------------------------------------------------------
    # Valores derivados
    # -------------------------------------------------------------------------

    df["vl_receita_publica"] = (
        df["vl_receita"]
        .where(
            df["in_receita_publica"],
            0,
        )
    )

    df["vl_receita_privada"] = (
        df["vl_receita"]
        .where(
            df["in_receita_privada"],
            0,
        )
    )

    df["vl_receita_partidaria"] = (
        df["vl_receita"]
        .where(
            df["in_receita_partidaria"],
            0,
        )
    )

    return df


# =============================================================================
# Pipeline principal
# =============================================================================


def enrich_revenue_data(
    df_receita: pd.DataFrame,
    df_cnpj: pd.DataFrame,
) -> pd.DataFrame:
    """
    Pipeline principal enrichment
    receitas partidárias.
    """

    df = df_receita.copy()

    # -------------------------------------------------------------------------
    # Validação
    # -------------------------------------------------------------------------

    required_columns = [
        "cd_cpf_cnpj_doador",
        "vl_receita",
        "sg_partido",
    ]

    missing_columns = [
        col
        for col in required_columns
        if col not in df.columns
    ]

    if missing_columns:

        raise KeyError(
            "Colunas obrigatórias ausentes "
            f"em receita: {missing_columns}"
        )

    # -------------------------------------------------------------------------
    # Enriquecimento CNPJ
    # -------------------------------------------------------------------------

    df = enrich_cnpj_data(
        df_base=df,
        df_cnpj=df_cnpj,
        cnpj_column="cd_cpf_cnpj_doador",
    )

    cobertura_cnpj = (
        df["is_cnpj_enriquecido"]
        .mean()
    )

    # -------------------------------------------------------------------------
    # Classificação
    # -------------------------------------------------------------------------

    df = classify_revenue_source(df)

    # -------------------------------------------------------------------------
    # Features
    # -------------------------------------------------------------------------

    df = create_revenue_features(df)

    # -------------------------------------------------------------------------
    # Logging
    # -------------------------------------------------------------------------

    log_transformation(
        dataframe="receita_enriquecida",
        operation="ENRICH_REVENUE_DATA",
        columns=[
            "tp_receita",
            "vl_receita_publica",
            "vl_receita_privada",
            "vl_receita_partidaria",
            "tp_porte_empresa",
            "tp_fornecedor",
        ],
        rules=[
            "CLASSIFICACAO_RECEITA",
            "FEATURE_ENGINEERING_RECEITA",
            "ENRICHMENT_CNPJ_DOADOR",
            f"CNPJ_COVERAGE={cobertura_cnpj:.2%}",
        ],
    )

    return df