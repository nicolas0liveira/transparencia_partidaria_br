"""
Funções utilitárias reutilizáveis
para pipelines ETL/ELT.

Objetivos:
- reduzir repetição de código
- padronizar logging
- padronizar persistência
- simplificar pipelines
"""

from __future__ import annotations

from pathlib import Path
from typing import Any
from typing import Callable

import pandas as pd

from IPython.display import display

from transparencia_partidaria_br.utils.pipeline.logger import (
    elapsed,
    info,
    log_dataframe,
    log_file_operation,
    log_transformation,
    success,
    timer,
)

from transparencia_partidaria_br.utils.pipeline.parquet_utils import (
    write_parquet,
)

# =============================================================================
# LEITURA
# =============================================================================

def read_and_log_csv(
    path: Path,
    dataframe_name: str,
    *,
    read_func: Callable[..., pd.DataFrame],
    **kwargs: Any,
) -> pd.DataFrame:
    """
    Lê CSV com logging padronizado.

    Parameters
    ----------
    path : Path

    dataframe_name : str

    read_func : Callable
        Função de leitura.

    kwargs : Any
        Argumentos adicionais.

    Returns
    -------
    pd.DataFrame
    """

    start = timer()

    info(
        f"Lendo arquivo: {path.name}"
    )

    log_file_operation(
        operation="READ_CSV",
        source=path,
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
        df=df,
        source=path,
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
    rules: list[Any] | None = None,
    **kwargs: Any,
) -> pd.DataFrame:
    """
    Executa transformação com logging.

    Parameters
    ----------
    df : pd.DataFrame

    func : Callable

    dataframe_name : str

    operation : str

    rules : list[Any] | None

    kwargs : Any

    Returns
    -------
    pd.DataFrame
    """

    start = timer()

    info(
        f"Executando: {operation}"
    )

    transformed_df = func(
        df,
        **kwargs,
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
        rules=rules,
        **kwargs,
    )

    return transformed_df

# =============================================================================
# PERSISTÊNCIA
# =============================================================================

def persist_dataframe(
    df: pd.DataFrame,
    *,
    parquet_path: Path | None = None,
    csv_path: Path | None = None,
    dataframe_name: str,
    csv_sep: str = ";",
    csv_encoding: str = "utf-8",
):
    """
    Persiste dataframe.

    Parameters
    ----------
    df : pd.DataFrame

    parquet_path : Path | None

    csv_path : Path | None

    dataframe_name : str

    csv_sep : str

    csv_encoding : str
    """

    start = timer()

    # -------------------------------------------------------------------------
    # Parquet
    # -------------------------------------------------------------------------

    if parquet_path is not None:

        info(
            f"Persistindo parquet: {parquet_path.name}"
        )

        write_parquet(
            df,
            parquet_path,
        )

        log_file_operation(
            operation="WRITE_PARQUET",
            source=dataframe_name,
            target=parquet_path,
        )

    # -------------------------------------------------------------------------
    # CSV
    # -------------------------------------------------------------------------

    if csv_path is not None:

        info(
            f"Persistindo CSV: {csv_path.name}"
        )

        df.to_csv(
            csv_path,
            sep=csv_sep,
            index=False,
            encoding=csv_encoding,
        )

        log_file_operation(
            operation="WRITE_CSV",
            source=dataframe_name,
            target=csv_path,
        )

    success(
        (
            f"Persistência concluída "
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
):
    """
    Exibe preview dataframe.

    Parameters
    ----------
    df : pd.DataFrame

    title : str

    rows : int
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
            ascending=False
        )
        .to_frame(
            name="missing"
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
            "dtype": df.dtypes.astype(str),
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
# EXPORTAÇÃO AUXILIAR
# =============================================================================

def export_dataframe_csv(
    df: pd.DataFrame,
    output_path: Path,
    *,
    sep: str = ";",
    encoding: str = "utf-8",
    index: bool = True,
):
    """
    Exporta dataframe para CSV
    com logging padronizado.

    Parameters
    ----------
    df : pd.DataFrame

    output_path : Path

    sep : str

    encoding : str

    index : bool
    """

    start = timer()

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    info(
        f"Exportando CSV: {output_path.name}"
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
            f"CSV exportado em "
            f"{elapsed(start)}"
        )
    )


def salvar_plot(
    output_path: Path,
    *,
    dpi: int = 300,
    bbox_inches: str = "tight",
    close: bool = True,
):
    """
    Salva gráfico matplotlib
    com logging padronizado.

    Parameters
    ----------
    output_path : Path

    dpi : int

    bbox_inches : str

    close : bool
    """

    start = timer()

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    info(
        f"Salvando gráfico: {output_path.name}"
    )

    import matplotlib.pyplot as plt

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
            f"Gráfico salvo em "
            f"{elapsed(start)}"
        )
    )