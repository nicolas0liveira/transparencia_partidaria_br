import pandas as pd

from transparencia_partidaria_br.preprocessing.common import (
    normalize_columns,
)

from transparencia_partidaria_br.utils.pipeline.logging import (
    log_step,
    success,
)

# =============================================================================
# Schema
# =============================================================================

RENAME_MAP = {
    "Despesa": "nm_despesa",
    "Classificacao": "tp_gasto",
}

# =============================================================================
# Despesa preprocessing
# =============================================================================


def preprocess_classificacao_despesa(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Preprocessamento da classificação de despesa TSE.
    """

    log_step(
        "Preprocessamento classificação de despesa"
    )

    # -------------------------------------------------------------------------
    # Schema
    # -------------------------------------------------------------------------

    df_aux = normalize_columns(
        df=df,
        mapping=RENAME_MAP,
        dataframe_name="df_aux",
    )

    success(
        "Preprocessamento classificação de despesa concluído."
    )

    return df_aux