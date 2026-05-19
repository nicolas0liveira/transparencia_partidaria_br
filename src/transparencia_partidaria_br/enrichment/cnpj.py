import pandas as pd

from transparencia_partidaria_br.utils.pipeline.logging import (
    log_transformation,
)

# =============================================================================
# Normalização
# =============================================================================


def normalize_cnpj(
    serie: pd.Series,
) -> pd.Series:
    """
    Normaliza CNPJ:
    - remove caracteres especiais
    - mantém apenas números
    - preenche zeros à esquerda
    """

    return (
        serie.astype(str)
        .str.replace(
            r"\D",
            "",
            regex=True,
        )
        .str.zfill(14)
    )


# =============================================================================
# Derivações
# =============================================================================


def derive_company_size(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Deriva porte simplificado da empresa.
    """

    if "ds_porte_empresa" not in df.columns:
        return df

    porte = (
        df["ds_porte_empresa"]
        .fillna("")
        .str.upper()
    )

    df["tp_porte_empresa"] = (
        "NAO_IDENTIFICADO"
    )

    df.loc[
        porte.str.contains(
            "MICRO|MEI|ME ",
            regex=True,
        ),
        "tp_porte_empresa",
    ] = "MICRO"

    df.loc[
        porte.str.contains(
            "PEQUENA|EPP",
            regex=True,
        ),
        "tp_porte_empresa",
    ] = "PEQUENA"

    df.loc[
        porte.str.contains(
            "MEDIA",
            regex=True,
        ),
        "tp_porte_empresa",
    ] = "MEDIA"

    df.loc[
        porte.str.contains(
            "GRANDE|S/A|SA",
            regex=True,
        ),
        "tp_porte_empresa",
    ] = "GRANDE"

    return df


def derive_supplier_type(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Classifica tipo do fornecedor
    com base na natureza jurídica.
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

    df["tp_fornecedor"] = "OUTROS"

    # -------------------------------------------------------------------------
    # Público
    # -------------------------------------------------------------------------

    mask_publico = natureza.str.contains(
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
    )

    df.loc[
        mask_publico,
        "tp_fornecedor",
    ] = "PUBLICO"

    # -------------------------------------------------------------------------
    # Terceiro setor
    # -------------------------------------------------------------------------

    mask_terceiro_setor = natureza.str.contains(
        (
            "ASSOCIACAO|"
            "FUNDACAO PRIVADA|"
            "ORGANIZACAO RELIGIOSA|"
            "SINDICATO"
        ),
        regex=True,
    )

    df.loc[
        mask_terceiro_setor,
        "tp_fornecedor",
    ] = "TERCEIRO_SETOR"

    # -------------------------------------------------------------------------
    # Partidário
    # -------------------------------------------------------------------------

    mask_partidario = natureza.str.contains(
        "PARTIDO POLITICO",
        regex=True,
    )

    df.loc[
        mask_partidario,
        "tp_fornecedor",
    ] = "PARTIDARIO"

    # -------------------------------------------------------------------------
    # Privado
    # -------------------------------------------------------------------------

    mask_privado = natureza.str.contains(
        (
            "EMPRESARIO|"
            "SOCIEDADE EMPRESARIA|"
            "SOCIEDADE LIMITADA|"
            "SOCIEDADE ANONIMA|"
            "EIRELI|"
            "COOPERATIVA"
        ),
        regex=True,
    )

    df.loc[
        mask_privado,
        "tp_fornecedor",
    ] = "PRIVADO"

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
    informações de CNPJ.

    Estratégia:
    - normalização
    - merge
    - derivação de features
    - métricas de cobertura

    Parameters
    ----------
    df_base:
        Dataset principal.

    df_cnpj:
        Base enriquecimento CNPJ.

    cnpj_column:
        Nome da coluna CNPJ no dataset principal.
    """

    df = df_base.copy()

    cnpj = df_cnpj.copy()

    # -------------------------------------------------------------------------
    # Validação
    # -------------------------------------------------------------------------

    if cnpj_column not in df.columns:

        raise KeyError(
            (
                f"Coluna '{cnpj_column}' "
                "não encontrada no dataframe base."
            )
        )

    if "nr_cnpj" not in cnpj.columns:

        raise KeyError(
            (
                "Coluna 'nr_cnpj' "
                "não encontrada na base CNPJ."
            )
        )

    # -------------------------------------------------------------------------
    # Normalização
    # -------------------------------------------------------------------------

    df[cnpj_column] = normalize_cnpj(
        df[cnpj_column]
    )

    cnpj["nr_cnpj"] = normalize_cnpj(
        cnpj["nr_cnpj"]
    )

    # -------------------------------------------------------------------------
    # Merge
    # -------------------------------------------------------------------------

    colunas_cnpj = [
        "nr_cnpj",
        "nm_razao_social",
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
        right_on="nr_cnpj",
    )

    # -------------------------------------------------------------------------
    # Métrica cobertura
    # -------------------------------------------------------------------------

    df["is_cnpj_enriquecido"] = (
        df["nm_razao_social"]
        .notna()
    )

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

    log_transformation(
        dataframe="df_base",
        operation="ENRICH_CNPJ_DATA",
        columns=[
            cnpj_column,
            "nm_razao_social",
            "sg_uf",
            "nm_municipio",
            "ds_porte_empresa",
            "ds_natureza_juridica",
            "tp_porte_empresa",
            "tp_fornecedor",
        ],
        rules=[
            f"CNPJ_COVERAGE={cobertura:.2%}",
        ],
    )

    return df