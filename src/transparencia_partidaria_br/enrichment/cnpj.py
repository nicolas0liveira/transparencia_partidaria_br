import numpy as np
import pandas as pd

from transparencia_partidaria_br.utils.pipeline.logging import (
    log_transformation,
)

# =============================================================================
# Constantes
# =============================================================================

FORNECEDOR_PUBLICO = "PUBLICO"

FORNECEDOR_PRIVADO = "PRIVADO"

FORNECEDOR_TERCEIRO_SETOR = (
    "TERCEIRO_SETOR"
)

FORNECEDOR_PARTIDARIO = (
    "PARTIDARIO"
)

FORNECEDOR_OUTROS = "OUTROS"

PORTE_MICRO = "MICRO"

PORTE_PEQUENA = "PEQUENA"

PORTE_MEDIA = "MEDIA"

PORTE_GRANDE = "GRANDE"

PORTE_NAO_IDENTIFICADO = (
    "NAO_IDENTIFICADO"
)


# =============================================================================
# Derivações
# =============================================================================


def derive_company_size(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Deriva porte simplificado empresa.
    """

    if "ds_porte_empresa" not in df.columns:
        return df

    porte = (
        df["ds_porte_empresa"]
        .fillna("")
        .str.upper()
    )

    conditions = [
        porte.str.contains(
            r"MICRO|MEI|\bME\b",
            regex=True,
            na=False,
        ),

        porte.str.contains(
            r"PEQUENA|EPP",
            regex=True,
            na=False,
        ),

        porte.str.contains(
            r"MEDIA",
            regex=True,
            na=False,
        ),

        porte.str.contains(
            r"GRANDE|S/A|\bSA\b",
            regex=True,
            na=False,
        ),
    ]

    choices = [
        PORTE_MICRO,
        PORTE_PEQUENA,
        PORTE_MEDIA,
        PORTE_GRANDE,
    ]

    df["tp_porte_empresa"] = (
        np.select(
            conditions,
            choices,
            default=PORTE_NAO_IDENTIFICADO,
        )
    )

    return df


def derive_supplier_type(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Classifica tipo institucional
    com base natureza jurídica.
    """

    if (
        "ds_natureza_juridica"
        not in df.columns
    ):
        return df

    natureza = (
        df["ds_natureza_juridica"]
        .fillna("")
        .str.upper()
    )

    conditions = [
        # Público
        natureza.str.contains(
            (
                "ADMINISTRACAO PUBLICA|"
                "MUNICIPIO|"
                "ESTADO|"
                "UNIAO|"
                "AUTARQUIA|"
                "FUNDACAO PUBLICA|"
                "ORGAO PUBLICO"
            ),
            regex=True,
            na=False,
        ),

        # Terceiro setor
        natureza.str.contains(
            (
                "ASSOCIACAO|"
                "FUNDACAO PRIVADA|"
                "ORGANIZACAO RELIGIOSA|"
                "SINDICATO"
            ),
            regex=True,
            na=False,
        ),

        # Partidário
        natureza.str.contains(
            "PARTIDO POLITICO",
            regex=True,
            na=False,
        ),

        # Privado
        natureza.str.contains(
            (
                "EMPRESARIO|"
                "SOCIEDADE EMPRESARIA|"
                "SOCIEDADE LIMITADA|"
                "SOCIEDADE ANONIMA|"
                "EIRELI|"
                "COOPERATIVA"
            ),
            regex=True,
            na=False,
        ),
    ]

    choices = [
        FORNECEDOR_PUBLICO,
        FORNECEDOR_TERCEIRO_SETOR,
        FORNECEDOR_PARTIDARIO,
        FORNECEDOR_PRIVADO,
    ]

    df["tp_fornecedor"] = (
        np.select(
            conditions,
            choices,
            default=FORNECEDOR_OUTROS,
        )
    )

    return df


# =============================================================================
# Enrichment principal
# =============================================================================


def enrich_cnpj_data(
    df_base: pd.DataFrame,
    df_cnpj: pd.DataFrame,
    cnpj_column: str,
) -> pd.DataFrame:
    """
    Enriquece dataset principal com
    informações da base CNPJ.

    Estratégia:
    - normalização identificadores
    - merge
    - derivação features
    - métricas cobertura
    """

    df = df_base.copy()

    cnpj = df_cnpj.copy()

    # -------------------------------------------------------------------------
    # Validação
    # -------------------------------------------------------------------------

    required_columns = [
        "cd_cnpj",
    ]

    missing_columns = [
        col
        for col in required_columns
        if col not in cnpj.columns
    ]

    if missing_columns:

        raise KeyError(
            (
                "Colunas obrigatórias ausentes "
                f"na base CNPJ: {missing_columns}"
            )
        )

    if cnpj_column not in df.columns:

        raise KeyError(
            (
                "Coluna de enrichment "
                f"não encontrada: {cnpj_column}"
            )
        )

    # -------------------------------------------------------------------------
    # Merge
    # -------------------------------------------------------------------------

    colunas_cnpj = [
        "cd_cnpj",
        "nm_razao_social",
        "nm_fantasia",
        "sg_uf",
        "nm_municipio",
        "ds_porte_empresa",
        "ds_natureza_juridica",
    ]

    colunas_existentes = [
        col
        for col in colunas_cnpj
        if col in cnpj.columns
    ]

    df = df.merge(
        cnpj[colunas_existentes],
        how="left",
        left_on=cnpj_column,
        right_on="cd_cnpj",
    )

    # -------------------------------------------------------------------------
    # Remove coluna redundante
    # -------------------------------------------------------------------------

    if (
        cnpj_column != "cd_cnpj"
        and "cd_cnpj" in df.columns
    ):

        df = df.drop(
            columns=["cd_cnpj"]
        )

    # -------------------------------------------------------------------------
    # Métrica cobertura
    # -------------------------------------------------------------------------

    coluna_cobertura = next(
        (
            col
            for col in [
                "nm_razao_social",
                "nm_fantasia",
                "ds_natureza_juridica",
            ]
            if col in df.columns
        ),
        None,
    )

    if coluna_cobertura:

        df["is_cnpj_enriquecido"] = (
            df[coluna_cobertura]
            .notna()
        )

    else:

        df["is_cnpj_enriquecido"] = False

    cobertura = (
        df["is_cnpj_enriquecido"]
        .mean()
    )

    # -------------------------------------------------------------------------
    # Derivações
    # -------------------------------------------------------------------------

    df = derive_company_size(df)

    df = derive_supplier_type(df)

    # -------------------------------------------------------------------------
    # Logging
    # -------------------------------------------------------------------------

    columns_log = [
        col
        for col in [
            cnpj_column,
            "nm_razao_social",
            "nm_fantasia",
            "sg_uf",
            "nm_municipio",
            "ds_porte_empresa",
            "ds_natureza_juridica",
            "tp_porte_empresa",
            "tp_fornecedor",
        ]
        if col in df.columns
    ]

    log_transformation(
        dataframe="df_base",
        operation="ENRICH_CNPJ_DATA",
        columns=columns_log,
        rules=[
            (
                f"CNPJ_COVERAGE="
                f"{cobertura:.2%}"
            ),
        ],
    )

    return df