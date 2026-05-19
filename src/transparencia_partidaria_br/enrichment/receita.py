import pandas as pd

from transparencia_partidaria_br.enrichment.cnpj import (
    enrich_cnpj_data,
)

from transparencia_partidaria_br.utils.pipeline.logging import (
    log_transformation,
)

# =============================================================================
# Classificação de Receita
# =============================================================================


def classify_revenue_source(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Classifica origem da receita.

    Categorias:
    - PUBLICA
    - PRIVADA
    - PARTIDARIA
    - OUTROS
    """

    if "ds_tp_origem_doacao" not in df.columns:
        return df

    origem = (
        df["ds_tp_origem_doacao"]
        .fillna("")
        .str.upper()
    )

    df["tp_receita"] = "OUTROS"

    # -------------------------------------------------------------------------
    # Receita pública
    # -------------------------------------------------------------------------

    mask_publica = origem.str.contains(
        (
            "FUNDO PARTIDARIO|"
            "FUNDO ESPECIAL"
        ),
        regex=True,
    )

    df.loc[
        mask_publica,
        "tp_receita",
    ] = "PUBLICA"

    # -------------------------------------------------------------------------
    # Receita privada
    # -------------------------------------------------------------------------

    mask_privada = origem.str.contains(
        (
            "PESSOAS FISICAS|"
            "PESSOAS JURIDICAS"
        ),
        regex=True,
    )

    df.loc[
        mask_privada,
        "tp_receita",
    ] = "PRIVADA"

    # -------------------------------------------------------------------------
    # Receita partidária
    # -------------------------------------------------------------------------

    mask_partidaria = origem.str.contains(
        "PARTIDOS POLITICOS",
        regex=True,
    )

    df.loc[
        mask_partidaria,
        "tp_receita",
    ] = "PARTIDARIA"

    return df


# =============================================================================
# Features de Receita
# =============================================================================


def create_revenue_features(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Cria métricas derivadas de receita.
    """

    if "vr_receita" not in df.columns:
        return df

    # -------------------------------------------------------------------------
    # Flags
    # -------------------------------------------------------------------------

    df["in_receita_publica"] = (
        df["tp_receita"] == "PUBLICA"
    )

    df["in_receita_privada"] = (
        df["tp_receita"] == "PRIVADA"
    )

    df["in_receita_partidaria"] = (
        df["tp_receita"] == "PARTIDARIA"
    )

    # -------------------------------------------------------------------------
    # Valores derivados
    # -------------------------------------------------------------------------

    df["vl_receita_publica"] = (
        df["vr_receita"]
        .where(
            df["in_receita_publica"],
            0,
        )
    )

    df["vl_receita_privada"] = (
        df["vr_receita"]
        .where(
            df["in_receita_privada"],
            0,
        )
    )

    df["vl_receita_partidaria"] = (
        df["vr_receita"]
        .where(
            df["in_receita_partidaria"],
            0,
        )
    )

    return df


# =============================================================================
# Agregação Receita Partido
# =============================================================================


def aggregate_revenue_party_year(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Agrega receitas em nível:
    partido x ano
    """

    group_cols = [
        "sg_partido",
        "aa_exercicio",
    ]

    metricas = {
        "vr_receita": "sum",
        "vl_receita_publica": "sum",
        "vl_receita_privada": "sum",
        "vl_receita_partidaria": "sum",
        "nr_cpf_cnpj_doador": "nunique",
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
            "vr_receita": "vl_receita_total",
            "nr_cpf_cnpj_doador": "qtd_doadores",
        }
    )

    # -------------------------------------------------------------------------
    # Percentuais
    # -------------------------------------------------------------------------

    df_agg["pct_receita_publica"] = (
        df_agg["vl_receita_publica"]
        / df_agg["vl_receita_total"]
    ) * 100

    df_agg["pct_receita_privada"] = (
        df_agg["vl_receita_privada"]
        / df_agg["vl_receita_total"]
    ) * 100

    # -------------------------------------------------------------------------
    # Ticket médio
    # -------------------------------------------------------------------------

    df_agg["ticket_medio_receita"] = (
        df_agg["vl_receita_total"]
        / df_agg["qtd_doadores"]
    )

    return df_agg


# =============================================================================
# Pipeline principal
# =============================================================================


def enrich_revenue_data(
    df_receita: pd.DataFrame,
    df_cnpj: pd.DataFrame,
) -> pd.DataFrame:
    """
    Pipeline principal de enriquecimento
    de receitas partidárias.
    """

    df = df_receita.copy()

    # -------------------------------------------------------------------------
    # Validação
    # -------------------------------------------------------------------------

    required_columns = [
        "nr_cpf_cnpj_doador",
        "vr_receita",
        "sg_partido",
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
                f"em receita: {missing_columns}"
            )
        )

    # -------------------------------------------------------------------------
    # Enriquecimento CNPJ
    # -------------------------------------------------------------------------

    df = enrich_cnpj_data(
        df_base=df,
        df_cnpj=df_cnpj,
        cnpj_column="nr_cpf_cnpj_doador",
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
        ],
    )

    return df