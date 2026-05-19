import pandas as pd

from transparencia_partidaria_br.preprocessing.common import (
    normalize_columns,
)

from transparencia_partidaria_br.utils.pipeline.logging import (
    log_step,
    success,
)

from transparencia_partidaria_br.utils.tse.tse_parser import (
    apply_date_parser,
    apply_number_parser,
    standardize_nulls,
    standardize_text_columns,
)

# =============================================================================
# Schema
# =============================================================================

RENAME_DESPESA = {
    # Partido
    "SG_PARTIDO": "sg_partido",
    "NM_PARTIDO": "nm_partido",

    # Prestador
    "NR_CNPJ_PRESTADOR_CONTA":
        "nr_cnpj_prestador_conta",

    # Fornecedor
    "NR_CPF_CNPJ_FORNECEDOR":
        "nr_cpf_cnpj_fornecedor",

    "NM_FORNECEDOR": "nm_fornecedor",

    # Despesa
    "TP_DESPESA": "tp_despesa",
    "DT_PAGAMENTO": "dt_pagamento",
    "DS_GASTO": "ds_gasto",

    "VR_GASTO": "vl_gasto",
    "VR_PAGAMENTO": "vl_pagamento",
    "VR_DOCUMENTO": "vl_documento",

    # Documento
    "CD_TP_DOCUMENTO":
        "cd_tp_documento",

    "DS_TP_DOCUMENTO":
        "ds_tp_documento",

    "NR_DOCUMENTO":
        "nr_documento",

    # Fornecedor tipo
    "CD_TP_FORNECEDOR":
        "cd_tp_fornecedor",

    "DS_TP_FORNECEDOR":
        "ds_tp_fornecedor",

    # Fonte despesa
    "CD_FONTE_DESPESA":
        "cd_fonte_despesa",

    "DS_FONTE_DESPESA":
        "ds_fonte_despesa",

    # Geografia
    "SG_UF": "sg_uf",
    "CD_MUNICIPIO": "cd_municipio",
    "NM_MUNICIPIO": "nm_municipio",

    # Exercício
    "AA_EXERCICIO": "aa_exercicio",

    # Chave
    "SQ_DESPESA": "sq_despesa",
}

# =============================================================================
# Despesa preprocessing
# =============================================================================


def preprocess_despesa(
    df_despesa: pd.DataFrame,
) -> pd.DataFrame:
    """
    Preprocessamento da despesa TSE.

    Responsabilidades:
    - normalização schema
    - tratamento NULL
    - padronização textual
    - parsing datas
    - parsing monetário
    """

    log_step(
        "Preprocessamento despesa"
    )

    # -------------------------------------------------------------------------
    # Schema
    # -------------------------------------------------------------------------

    df_despesa = normalize_columns(
        df=df_despesa,
        mapping=RENAME_DESPESA,
        dataframe_name="df_despesa",
    )

    # -------------------------------------------------------------------------
    # NULL
    # -------------------------------------------------------------------------

    df_despesa = standardize_nulls(
        df_despesa
    )

    # -------------------------------------------------------------------------
    # Texto
    # -------------------------------------------------------------------------

    df_despesa = (
        standardize_text_columns(
            df_despesa
        )
    )

    # -------------------------------------------------------------------------
    # Datas
    # -------------------------------------------------------------------------

    df_despesa = apply_date_parser(
        df_despesa,
        columns=[
            "dt_pagamento",
        ],
    )

    # -------------------------------------------------------------------------
    # Valores monetários
    # -------------------------------------------------------------------------

    df_despesa = apply_number_parser(
        df_despesa,
        columns=[
            "vl_gasto",
            "vl_pagamento",
            "vl_documento",
        ],
    )

    # -------------------------------------------------------------------------
    # Exercício
    # -------------------------------------------------------------------------

    if "aa_exercicio" in df_despesa.columns:

        df_despesa[
            "aa_exercicio"
        ] = pd.to_numeric(
            df_despesa[
                "aa_exercicio"
            ],
            errors="coerce",
        )

    # -------------------------------------------------------------------------
    # CNPJ/CPF como string
    # -------------------------------------------------------------------------

    cnpj_columns = [
        "nr_cnpj_prestador_conta",
        "nr_cpf_cnpj_fornecedor",
    ]

    for col in cnpj_columns:

        if col in df_despesa.columns:

            df_despesa[col] = (
                df_despesa[col]
                .astype(str)
                .str.strip()
            )

    success(
        "Preprocessamento despesa concluído."
    )

    return df_despesa