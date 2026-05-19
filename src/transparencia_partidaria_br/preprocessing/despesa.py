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
    # Valores monetários
    "vr_gasto": "vl_gasto",
    "vr_pagamento": "vl_pagamento",
    "vr_documento": "vl_documento",
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
            "dt_geracao",
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

    numeric_columns = [
        "aa_exercicio",
        "nr_zona",
        "aa_aidf",
        "sq_despesa",
    ]

    for col in numeric_columns:

        if col in df_despesa.columns:

            df_despesa[col] = (
                pd.to_numeric(
                    df_despesa[col],
                    errors="coerce",
                )
            )

    # -------------------------------------------------------------------------
    # CNPJ/CPF como string
    # -------------------------------------------------------------------------

    cnpj_columns = [
        "cd_cnpj_prestador_conta",
        "cd_cpf_cnpj_fornecedor",
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