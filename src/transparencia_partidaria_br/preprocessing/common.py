import pandas as pd

from transparencia_partidaria_br.utils.pipeline.logging import (
    log_transformation,
)

# =============================================================================
# Generic transformations
# =============================================================================


import re
import unicodedata

import pandas as pd

from transparencia_partidaria_br.utils.pipeline.logging import (
    log_transformation,
)

# =============================================================================
# Column normalization
# =============================================================================


def normalize_column_name(
    column: str,
) -> str:
    """
    Normaliza nome de coluna:
    - lowercase
    - remove acentos
    - snake_case
    - remove caracteres especiais
    """

    # -------------------------------------------------------------------------
    # Lowercase
    # -------------------------------------------------------------------------

    column = column.lower()

    # -------------------------------------------------------------------------
    # Remove acentos
    # -------------------------------------------------------------------------

    column = unicodedata.normalize(
        "NFKD",
        column,
    ).encode(
        "ascii",
        "ignore",
    ).decode(
        "utf-8"
    )

    # -------------------------------------------------------------------------
    # Snake case
    # -------------------------------------------------------------------------

    column = re.sub(
        r"[^a-z0-9]+",
        "_",
        column,
    )

    # -------------------------------------------------------------------------
    # Remove underscores duplicados
    # -------------------------------------------------------------------------

    column = re.sub(
        r"_+",
        "_",
        column,
    )

    # -------------------------------------------------------------------------
    # Remove bordas
    # -------------------------------------------------------------------------

    column = column.strip("_")

    return column


def normalize_columns(
    df: pd.DataFrame,
    mapping: dict[str, str] | None = None,
    dataframe_name: str = "dataframe",
) -> pd.DataFrame:
    """
    Padroniza nomes de colunas.

    Etapas:
    - lowercase
    - remove acentos
    - snake_case
    - aplica mapping customizado
    """

    df = df.copy()

    original_columns = df.columns.tolist()

    # -------------------------------------------------------------------------
    # Normalização automática
    # -------------------------------------------------------------------------

    df.columns = [
        normalize_column_name(col)
        for col in df.columns
    ]

    # -------------------------------------------------------------------------
    # Mapping customizado
    # -------------------------------------------------------------------------

    if mapping:

        mapping_normalized = {
            normalize_column_name(k): v
            for k, v in mapping.items()
        }

        df = df.rename(
            columns=mapping_normalized
        )

    # -------------------------------------------------------------------------
    # Logging
    # -------------------------------------------------------------------------

    log_transformation(
        dataframe=dataframe_name,
        operation="NORMALIZE_COLUMNS",
        columns=original_columns,
        rules=[
            "STANDARDIZE_SCHEMA",
            "CONVERT_TO_SNAKE_CASE",
            "REMOVE_ACCENTS",
            "NORMALIZE_SPECIAL_CHARACTERS",
        ],
    )

    return df


# =============================================================================
# Normalização
# =============================================================================


def normalize_cnpj(
    serie: pd.Series,
) -> pd.Series:
    """
    Normaliza CPF/CNPJ:
    - remove caracteres especiais
    - mantém apenas números
    - preserva null
    - remove identificadores inválidos
    """

    serie = (
        serie.astype("string")
        .str.replace(
            r"\D",
            "",
            regex=True,
        )
        .str.strip()
    )

    # -------------------------------------------------------------------------
    # Strings vazias
    # -------------------------------------------------------------------------

    serie = serie.mask(
        serie == "",
        pd.NA,
    )

    # -------------------------------------------------------------------------
    # Mantém apenas CPF/CNPJ válidos
    # -------------------------------------------------------------------------

    serie = serie.where(
        serie.str.len().isin(
            [11, 14]
        ),
        pd.NA,
    )

    return serie