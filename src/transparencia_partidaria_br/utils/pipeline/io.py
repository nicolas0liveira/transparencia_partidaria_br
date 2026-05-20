from __future__ import annotations

from pathlib import Path

import pandas as pd

from transparencia_partidaria_br.utils.pipeline.logging import (
    info,
    log_file_operation,
    success,
)

# =============================================================================
# Parquet
# =============================================================================


def write_parquet(
    df: pd.DataFrame,
    path: str | Path,
    *,
    index: bool = False,
) -> None:
    """
    Persiste dataframe em parquet.
    """

    path = Path(path)

    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    df.to_parquet(
        path,
        index=index,
    )

    log_file_operation(
        operation="WRITE_PARQUET",
        source="dataframe",
        target=path,
    )


def read_parquet(
    path: str | Path,
) -> pd.DataFrame:
    """
    Lê parquet.
    """

    path = Path(path)

    df = pd.read_parquet(
        path
    )

    log_file_operation(
        operation="READ_PARQUET",
        source=path,
        target="dataframe",
    )

    return df


# =============================================================================
# CSV
# =============================================================================


def write_csv(
    df: pd.DataFrame,
    path: str | Path,
    *,
    index: bool = False,
    sep: str = ";",
) -> None:
    """
    Persiste dataframe CSV.
    """

    path = Path(path)

    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    df.to_csv(
        path,
        sep=sep,
        index=index,
    )

    log_file_operation(
        operation="WRITE_CSV",
        source="dataframe",
        target=path,
    )


def read_csv(
    path: str | Path,
    **kwargs,
) -> pd.DataFrame:
    """
    Leitura CSV genérica.
    """

    path = Path(path)

    df = pd.read_csv(
        path,
        **kwargs,
    )

    log_file_operation(
        operation="READ_CSV",
        source=path,
        target="dataframe",
    )

    return df