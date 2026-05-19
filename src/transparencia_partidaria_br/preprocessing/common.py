import pandas as pd

from transparencia_partidaria_br.utils.pipeline.logging import (
    log_transformation,
)

# =============================================================================
# Generic transformations
# =============================================================================


def normalize_columns(
    df: pd.DataFrame,
    mapping: dict[str, str],
    dataframe_name: str,
) -> pd.DataFrame:
    """
    Padroniza nomes de colunas.
    """

    df = df.rename(
        columns=mapping
    )

    log_transformation(
        dataframe=dataframe_name,
        operation="NORMALIZE_COLUMNS",
        columns=list(mapping.keys()),
        rules=[
            "STANDARDIZE_SCHEMA",
            "CONVERT_TO_SNAKE_CASE",
        ],
    )

    return df