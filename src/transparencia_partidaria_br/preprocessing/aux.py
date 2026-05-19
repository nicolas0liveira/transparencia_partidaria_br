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
    "Classificacao": "nm_classificacao",
}

# =============================================================================
# Despesa preprocessing
# =============================================================================


def preprocess_classificacao_despesa(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Preprocessamento da receita TSE.
    """

    log_step(
        "Preprocessamento receita"
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
        "Preprocessamento receita concluído."
    )

    return df