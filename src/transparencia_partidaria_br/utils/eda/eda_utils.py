"""
Funções utilitárias para EDA.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from transparencia_partidaria_br.utils.pipeline.logger import (
    info,
)

# =============================================================================
# IO
# =============================================================================

def save_dataframe(
    df: pd.DataFrame,
    output_dir: Path,
    filename: str,
):
    """
    Salva dataframe CSV.
    """

    path = output_dir / filename

    df.to_csv(
        path,
        sep=";",
        encoding="utf-8",
        index=True,
    )

    info(
        f"Arquivo salvo: {path}"
    )


def save_plot(
    output_dir: Path,
    filename: str,
):
    """
    Salva gráfico.
    """

    path = output_dir / filename

    plt.tight_layout()

    plt.savefig(
        path,
        dpi=300,
        bbox_inches="tight",
    )

    plt.close()

    info(
        f"Gráfico salvo: {path}"
    )

# =============================================================================
# STATS
# =============================================================================

def build_numeric_summary(
    df: pd.DataFrame,
    columns: list[str],
) -> pd.DataFrame:
    """
    Estatísticas descritivas.
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
# GROUPBY
# =============================================================================

def build_grouped_summary(
    df: pd.DataFrame,
    group_column: str,
    value_column: str,
) -> pd.DataFrame:
    """
    Resumo agrupado.
    """

    grouped = (
        df.groupby(
            group_column
        )[value_column]
        .agg(
            [
                "count",
                "sum",
                "mean",
                "median",
                "std",
                "min",
                "max",
            ]
        )
        .sort_values(
            by="sum",
            ascending=False,
        )
    )

    grouped["proporcao_pct"] = (
        (
            grouped["sum"]
            / grouped["sum"].sum()
        ) * 100
    ).round(2)

    return grouped