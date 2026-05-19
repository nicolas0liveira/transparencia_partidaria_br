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
    # Partido
    "SG_PARTIDO": "sg_partido",
    "NM_PARTIDO": "nm_partido",
    # Prestador
    "NR_CNPJ_PRESTADOR_CONTA": "nr_cnpj_prestador_conta",
    # Doador
    "NR_CPF_CNPJ_DOADOR": "nr_cpf_cnpj_doador",
    "NM_DOADOR": "nm_doador",
    # Receita
    "DT_RECEITA": "dt_receita",
    "VR_RECEITA": "vl_receita",
    "DS_RECEITA": "ds_receita",
    # Origem
    "CD_TP_ORIGEM_DOACAO": "cd_tp_origem_doacao",
    "DS_TP_ORIGEM_DOACAO": "ds_tp_origem_doacao",
    # Fonte recurso
    "CD_TP_FONTE_RECURSO": "cd_tp_fonte_recurso",
    "DS_TP_FONTE_RECURSO": "ds_tp_fonte_recurso",
    # Natureza recurso
    "CD_TP_NATUREZA_RECURSO": "cd_tp_natureza_recurso",
    "DS_TP_NATUREZA_RECURSO": "ds_tp_natureza_recurso",
    # Espécie recurso
    "CD_TP_ESPECIE_RECURSO": "cd_tp_especie_recurso",
    "DS_TP_ESPECIE_RECURSO": "ds_tp_especie_recurso",
    # Geografia
    "SG_UF": "sg_uf",
    "CD_MUNICIPIO": "cd_municipio",
    "NM_MUNICIPIO": "nm_municipio",
    # Exercício
    "AA_EXERCICIO": "aa_exercicio",
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
    # Exercício
    # -------------------------------------------------------------------------

    if "aa_exercicio" in df_receita.columns:

        df_receita[
            "aa_exercicio"
        ] = pd.to_numeric(
            df_receita[
                "aa_exercicio"
            ],
            errors="coerce",
        )

    # -------------------------------------------------------------------------
    # CNPJ/CPF como string
    # -------------------------------------------------------------------------

    cnpj_columns = [
        "nr_cnpj_prestador_conta",
        "nr_cpf_cnpj_doador",
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

    return df_receita