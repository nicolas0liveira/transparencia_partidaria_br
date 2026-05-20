import pandas as pd

from transparencia_partidaria_br.preprocessing.common import (
    normalize_columns,
)

from transparencia_partidaria_br.utils.pipeline.logging import (
    log_step,
    success,
)

from transparencia_partidaria_br.utils.tse.tse_parser import (
    standardize_nulls,
    standardize_text_columns,
)

# =============================================================================
# Schema
# =============================================================================

RENAME_CNPJ = {
    "nm_empresarial": "nm_razao_social",
}

# =============================================================================
# CNPJ preprocessing
# =============================================================================


def preprocess_cnpj(
    df_cnpj: pd.DataFrame,
) -> pd.DataFrame:
    """
    Preprocessamento da base CNPJ.
    """

    log_step(
        "Preprocessamento CNPJ"
    )

    # -------------------------------------------------------------------------
    # Schema
    # -------------------------------------------------------------------------

    df_cnpj = normalize_columns(
        df=df_cnpj,
        mapping=RENAME_CNPJ,
        dataframe_name="df_cnpj",
    )

    # -------------------------------------------------------------------------
    # NULL
    # -------------------------------------------------------------------------

    df_cnpj = standardize_nulls(
        df_cnpj
    )

    # -------------------------------------------------------------------------
    # Texto
    # -------------------------------------------------------------------------

    df_cnpj = (
        standardize_text_columns(
            df_cnpj
        )
    )

    # -------------------------------------------------------------------------
    # CNPJ como string
    # -------------------------------------------------------------------------

    if "cd_cnpj" in df_cnpj.columns:

        df_cnpj["cd_cnpj"] = (
            df_cnpj["cd_cnpj"]
            .astype(str)
            .str.strip()
        )

    success(
        "Preprocessamento CNPJ concluído."
    )

    return df_cnpj