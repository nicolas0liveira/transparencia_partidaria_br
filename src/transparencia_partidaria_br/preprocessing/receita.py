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

RENAME_RECEITA = {
    # Valores monetários
    "vr_receita": "vl_receita",
    "nr_cnpj_prestador_conta":"cd_cnpj_prestador_conta",
    "nr_cpf_cnpj_doador":"cd_cpf_cnpj_doador",
}

# =============================================================================
# Receita preprocessing
# =============================================================================


def preprocess_receita(
    df_receita: pd.DataFrame,
) -> pd.DataFrame:
    """
    Preprocessamento da receita TSE.

    Responsabilidades:
    - normalização schema
    - tratamento NULL
    - padronização textual
    - parsing datas
    - parsing monetário
    """

    log_step(
        "Preprocessamento receita"
    )

    # -------------------------------------------------------------------------
    # Schema
    # -------------------------------------------------------------------------

    df_receita = normalize_columns(
        df=df_receita,
        mapping=RENAME_RECEITA,
        dataframe_name="df_receita",
    )

    # -------------------------------------------------------------------------
    # NULL
    # -------------------------------------------------------------------------

    df_receita = standardize_nulls(
        df_receita
    )

    # -------------------------------------------------------------------------
    # Texto
    # -------------------------------------------------------------------------

    df_receita = (
        standardize_text_columns(
            df_receita
        )
    )

    # -------------------------------------------------------------------------
    # Datas
    # -------------------------------------------------------------------------

    df_receita = apply_date_parser(
        df_receita,
        columns=[
            "dt_geracao",
            "dt_receita",
        ],
    )

    # -------------------------------------------------------------------------
    # Valores monetários
    # -------------------------------------------------------------------------

    df_receita = apply_number_parser(
        df_receita,
        columns=[
            "vl_receita",
        ],
    )

    # -------------------------------------------------------------------------
    # Conversões numéricas
    # -------------------------------------------------------------------------

    numeric_columns = [
        "aa_exercicio",
        "nr_zona",
        "nr_zona_doador",
        "sq_candidato_doador",
        "nr_candidato_doador",
    ]

    for col in numeric_columns:

        if col in df_receita.columns:

            df_receita[col] = (
                pd.to_numeric(
                    df_receita[col],
                    errors="coerce",
                )
            )

    # -------------------------------------------------------------------------
    # CNPJ/CPF como string
    # -------------------------------------------------------------------------

    cnpj_columns = [
        "cd_cnpj_prestador_conta",
        "cd_cpf_cnpj_doador",
    ]

    for col in cnpj_columns:

        if col in df_receita.columns:

            df_receita[col] = (
                df_receita[col]
                .astype(str)
                .str.strip()
            )

    success(
        "Preprocessamento receita concluído."
    )

    # -------------------------------------------------------------------------
    # Exercício
    # -------------------------------------------------------------------------

    df_receita["aa_exercicio"] = 2025

    # -------------------------------------------------------------------------
    # Inficadores
    # -------------------------------------------------------------------------

    #dt_receita  nula
    df_receita["ind_dt_receita_nula"] = (
        df_receita["dt_receita"].isna()
    )

    


    return df_receita
