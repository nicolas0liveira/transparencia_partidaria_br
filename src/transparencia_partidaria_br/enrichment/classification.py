import pandas as pd

from transparencia_partidaria_br.utils.pipeline.logging import (
    log_transformation,
)

# =============================================================================
# Regras de fallback
# =============================================================================

FALLBACK_RULES = {
    # -------------------------------------------------------------------------
    # FINALISTICO
    # -------------------------------------------------------------------------
    "DESPESAS ELEITORAIS": "FINALISTICO",
    "COM FINS ELEITORAIS": "FINALISTICO",
    "CANDIDATO": "FINALISTICO",
    "CANDIDATAS": "FINALISTICO",
    "CANDIDATOS NEGROS": "FINALISTICO",
    "CAMPANHA": "FINALISTICO",
    "MULHERES": "FINALISTICO",
    "PROPAGANDA": "FINALISTICO",
    "PUBLICIDADE": "FINALISTICO",
    "EVENTOS PROMOCIONAIS": "FINALISTICO",
    "RADIO E TELEVISAO": "FINALISTICO",
    "IMPULSIONAMENTO": "FINALISTICO",

    # -------------------------------------------------------------------------
    # ADMINISTRATIVO
    # -------------------------------------------------------------------------
    "ENERGIA ELETRICA": "ADMINISTRATIVO",
    "AGUA E ESGOTO": "ADMINISTRATIVO",
    "TELECOMUNICACOES E INTERNET": "ADMINISTRATIVO",
    "ALUGUEIS E CONDOMINIOS": "ADMINISTRATIVO",
    "SERVICOS CONTABEIS": "ADMINISTRATIVO",
    "SERVICOS DE LIMPEZA": "ADMINISTRATIVO",
    "SEGURANCA E VIGILANCIA": "ADMINISTRATIVO",
    "PESSOAL": "ADMINISTRATIVO",
    "TRIBUTOS": "ADMINISTRATIVO",
}

# =============================================================================
# Classificação
# =============================================================================


def classify_expense_type(
    df_despesa: pd.DataFrame,
    df_classificacao: pd.DataFrame,
) -> pd.DataFrame:
    """
    Classifica despesas entre:
    - ADMINISTRATIVO
    - FINALISTICO
    - INDEFINIDO

    Estratégia:
    1. Lookup exato via merge
    2. Fallback por palavras-chave
    3. INDEFINIDO para não classificados
    """

    df = df_despesa.copy()

    # -------------------------------------------------------------------------
    # Normalização
    # -------------------------------------------------------------------------

    df["ds_gasto"] = (
        df["ds_gasto"]
        .fillna("")
        .str.upper()
        .str.strip()
    )

    df_classificacao = (
        df_classificacao.copy()
    )

    df_classificacao["DESPESA"] = (
        df_classificacao["DESPESA"]
        .fillna("")
        .str.upper()
        .str.strip()
    )

    # -------------------------------------------------------------------------
    # Lookup exato
    # -------------------------------------------------------------------------

    df = df.merge(
        df_classificacao[
            [
                "DESPESA",
                "tp_gasto",
            ]
        ],
        how="left",
        left_on="ds_gasto",
        right_on="DESPESA",
    )

    # -------------------------------------------------------------------------
    # Origem da classificação
    # -------------------------------------------------------------------------

    df["tp_classificacao_origem"] = (
        pd.NA
    )

    df.loc[
        df["tp_gasto"].notna(),
        "tp_classificacao_origem",
    ] = "LOOKUP_EXATO"

    # -------------------------------------------------------------------------
    # Fallback
    # -------------------------------------------------------------------------

    descricao = df["ds_gasto"]

    for regra, classificacao in FALLBACK_RULES.items():

        mask = (
            df["tp_gasto"].isna()
            &
            descricao.str.contains(
                regra,
                regex=False,
            )
        )

        df.loc[
            mask,
            "tp_gasto",
        ] = classificacao

        df.loc[
            mask,
            "tp_classificacao_origem",
        ] = f"FALLBACK::{regra}"

    # -------------------------------------------------------------------------
    # INDEFINIDO
    # -------------------------------------------------------------------------

    mask_indefinido = (
        df["tp_gasto"].isna()
    )

    df.loc[
        mask_indefinido,
        "tp_gasto",
    ] = "INDEFINIDO"

    df.loc[
        mask_indefinido,
        "tp_classificacao_origem",
    ] = "NAO_CLASSIFICADO"

    # -------------------------------------------------------------------------
    # Limpeza
    # -------------------------------------------------------------------------

    df = df.drop(
        columns=["DESPESA"],
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
            "FALLBACK",
            "INDEFINIDO",
        ],
    )

    return df