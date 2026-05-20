"""
Funções utilitárias reutilizáveis
para pipelines ETL/ELT.

Objetivos:
- reduzir repetição
- padronizar persistência
- simplificar pipelines
- centralizar diagnósticos
"""

from __future__ import annotations

from pathlib import Path
from typing import Any
from typing import Callable

import matplotlib.pyplot as plt
import pandas as pd

from IPython.display import display

from transparencia_partidaria_br.utils.pipeline.io import (
    read_parquet,
    write_parquet,
)

from transparencia_partidaria_br.utils.pipeline.logging import (
    elapsed,
    info,
    log_dataframe,
    log_dataframe_profile,
    log_file_operation,
    log_transformation,
    success,
    timer,
)

# =============================================================================
# LEITURA
# =============================================================================


def read_and_log_parquet(
    path: Path,
    dataframe_name: str,
    profile: bool = False,
) -> pd.DataFrame:
    """
    Lê parquet com logging padronizado.
    """

    start = timer()

    info(
        f"Lendo parquet: {path.name}"
    )

    df = read_parquet(path)

    success(
        (
            f"{dataframe_name} carregado "
            f"em {elapsed(start)}"
        )
    )

    log_dataframe(
        name=dataframe_name,
        rows=len(df),
        columns=len(df.columns),
    )

    if profile:

        log_dataframe_profile(
            name=dataframe_name,
            df=df,
        )

    return df


def read_and_log_csv(
    path: Path,
    dataframe_name: str,
    *,
    read_func: Callable[..., pd.DataFrame],
    profile: bool = False,
    **kwargs: Any,
) -> pd.DataFrame:
    """
    Lê CSV com logging padronizado.
    """

    start = timer()

    info(
        f"Lendo CSV: {path.name}"
    )

    df = read_func(
        path,
        **kwargs,
    )

    success(
        (
            f"{dataframe_name} carregado "
            f"em {elapsed(start)}"
        )
    )

    log_dataframe(
        name=dataframe_name,
        rows=len(df),
        columns=len(df.columns),
    )

    if profile:

        log_dataframe_profile(
            name=dataframe_name,
            df=df,
        )

    return df


# =============================================================================
# TRANSFORMAÇÃO
# =============================================================================


def process_dataframe(
    df: pd.DataFrame,
    func: Callable[..., pd.DataFrame],
    *,
    dataframe_name: str,
    operation: str,
    rules: list[str] | None = None,
    details: str | None = None,
    **kwargs: Any,
) -> pd.DataFrame:
    """
    Executa transformação com logging.
    """

    start = timer()

    rows_before = len(df)

    info(
        f"Executando: {operation}"
    )

    transformed_df = func(
        df,
        **kwargs,
    )

    rows_after = len(
        transformed_df
    )

    success(
        (
            f"{operation} concluída "
            f"em {elapsed(start)}"
        )
    )

    log_transformation(
        dataframe=dataframe_name,
        operation=operation,
        rows_before=rows_before,
        rows_after=rows_after,
        rules=rules,
        details=details,
    )

    return transformed_df


# =============================================================================
# PERSISTÊNCIA
# =============================================================================


def persist_dataset(
    df: pd.DataFrame,
    path: Path,
    *,
    dataset_name: str,
) -> None:
    """
    Persiste dataset parquet
    com logging padronizado.
    """

    start = timer()

    info(
        (
            f"Salvando "
            f"{dataset_name}..."
        )
    )

    write_parquet(
        df=df,
        path=path,
    )

    log_file_operation(
        operation="WRITE_PARQUET",
        source=dataset_name,
        target=path,
    )

    success(
        (
            f"{dataset_name} salvo "
            f"em {elapsed(start)}"
        )
    )


def export_dataframe_csv(
    df: pd.DataFrame,
    output_path: Path,
    *,
    sep: str = ";",
    encoding: str = "utf-8",
    index: bool = False,
) -> None:
    """
    Exporta dataframe CSV
    com logging padronizado.
    """

    start = timer()

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    info(
        (
            f"Exportando CSV: "
            f"{output_path.name}"
        )
    )

    df.to_csv(
        output_path,
        sep=sep,
        encoding=encoding,
        index=index,
    )

    log_file_operation(
        operation="EXPORT_CSV",
        source="dataframe",
        target=output_path,
    )

    success(
        (
            f"CSV exportado "
            f"em {elapsed(start)}"
        )
    )


# =============================================================================
# DISPLAY
# =============================================================================


def log_dataframe_preview(
    df: pd.DataFrame,
    *,
    title: str,
    rows: int = 5,
) -> None:
    """
    Exibe preview dataframe.
    """

    print(
        f"\n{title}:"
    )

    display(
        df.head(rows)
    )


# =============================================================================
# DIAGNÓSTICOS
# =============================================================================


def build_missing_summary(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Resumo de valores nulos.
    """

    summary = (
        df.isna()
        .sum()
        .sort_values(
            ascending=False,
        )
        .to_frame(
            name="missing",
        )
    )

    summary["missing_pct"] = (
        (
            summary["missing"]
            / len(df)
        ) * 100
    ).round(2)

    return summary


def build_dtype_summary(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Resumo de tipos.
    """

    return pd.DataFrame(
        {
            "column": df.columns,
            "dtype": (
                df.dtypes.astype(str)
            ),
        }
    )


def build_numeric_summary(
    df: pd.DataFrame,
    columns: list[str],
) -> pd.DataFrame:
    """
    Estatísticas numéricas.
    """

    summary = (
        df[columns]
        .describe()
        .T
    )

    summary["missing"] = (
        df[columns]
        .isna()
        .sum()
    )

    summary["missing_pct"] = (
        (
            summary["missing"]
            / len(df)
        ) * 100
    ).round(2)

    return summary


# =============================================================================
# VISUALIZAÇÃO
# =============================================================================


def save_plot(
    output_path: Path,
    *,
    dpi: int = 300,
    bbox_inches: str = "tight",
    close: bool = True,
) -> None:
    """
    Salva gráfico matplotlib.
    """

    start = timer()

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    info(
        (
            f"Salvando gráfico: "
            f"{output_path.name}"
        )
    )

    plt.tight_layout()

    plt.savefig(
        output_path,
        dpi=dpi,
        bbox_inches=bbox_inches,
    )

    if close:

        plt.close()

    log_file_operation(
        operation="SAVE_PLOT",
        source="matplotlib",
        target=output_path,
    )

    success(
        (
            f"Gráfico salvo "
            f"em {elapsed(start)}"
        )
    )