"""
Logger para pipelines analíticas e ETL.

Objetivos:
- rastreabilidade
- reproducibilidade
- auditoria
- observabilidade
- documentação metodológica
"""

from __future__ import annotations

import time

from datetime import datetime
from pathlib import Path
from typing import Any

import pandas as pd


# =============================================================================
# CONFIGURAÇÕES
# =============================================================================

VERBOSE = True

BASE_DIR = Path("../")

LOG_DIR = BASE_DIR / "outputs/logs"

LOG_DIR.mkdir(
    parents=True,
    exist_ok=True,
)

PIPELINE_LOG = LOG_DIR / "pipeline.log"


# =============================================================================
# HELPERS
# =============================================================================

def now() -> str:

    return datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )


def separator() -> str:

    return "=" * 100


def write_log(content: str) -> None:

    with open(
        PIPELINE_LOG,
        "a",
        encoding="utf-8",
    ) as f:

        f.write(content)


# =============================================================================
# FEEDBACK VISUAL
# =============================================================================

def info(message: str) -> None:

    if VERBOSE:
        print(f"[INFO] {message}")


def success(message: str) -> None:

    if VERBOSE:
        print(f"[OK] {message}")


def warning(message: str) -> None:

    if VERBOSE:
        print(f"[WARN] {message}")


# =============================================================================
# TIMER
# =============================================================================

def timer() -> float:

    return time.perf_counter()


def elapsed(start: float) -> str:

    total = time.perf_counter() - start

    return f"{total:.2f}s"


# =============================================================================
# LOG PRINCIPAL
# =============================================================================

def log_step(
    title: str,
    *,
    notebook: str | None = None,
    message: str | None = None,
) -> None:
    """
    Registra etapa da pipeline.
    """

    lines = [
        "\n",
        separator(),
        f"[{now()}] {title.upper()}",
        separator(),
    ]

    if notebook:
        lines.append(f"NOTEBOOK : {notebook}")

    if message:
        lines.append(message)

    lines.append("\n")

    content = "\n".join(lines)

    write_log(content)

    if VERBOSE:

        print("\n")
        print(separator())
        print(title.upper())
        print(separator())

        if notebook:
            print(f"NOTEBOOK : {notebook}")

        if message:
            print(message)


# =============================================================================
# LOG DE ARQUIVO
# =============================================================================

def log_file_operation(
    *,
    operation: str,
    source: str | Path | None = None,
    target: str | Path | None = None,
) -> None:
    """
    Registra operações de arquivo.
    """

    lines = [
        f"[{now()}] FILE_OPERATION",
        f"OPERATION : {operation}",
    ]

    if source:
        lines.append(f"SOURCE    : {source}")

    if target:
        lines.append(f"TARGET    : {target}")

    lines.append("\n")

    content = "\n".join(lines)

    write_log(content)

    if VERBOSE:

        print(f"\n[{operation}]")

        if source:
            print(f"Arquivo origem : {source}")

        if target:
            print(f"Arquivo destino: {target}")


# =============================================================================
# LOG DE DATAFRAME
# =============================================================================

def log_dataframe(
    *,
    name: str,
    df: pd.DataFrame,
    source: str | Path | None = None,
    target: str | Path | None = None,
    transformation: str | None = None,
    preview_rows: int = 5,
    show_preview: bool = True,
    show_dtypes: bool = True,
    show_nulls: bool = True,
) -> None:

    info("=" * 80)

    info(
        f"DATAFRAME : {name}"
    )

    if source:

        info(
            f"SOURCE    : {source}"
        )

    if target:

        info(
            f"TARGET    : {target}"
        )

    if transformation:

        info(
            f"TRANSFORM : {transformation}"
        )

    info(
        f"SHAPE     : {df.shape}"
    )

    info(
        f"MEMORY_MB : "
        f"{df.memory_usage(deep=True).sum() / 1024**2:.2f}"
    )

    # -------------------------------------------------------------------------
    # DTYPES
    # -------------------------------------------------------------------------

    if show_dtypes:

        info("\nDTYPES")

        for col, dtype in df.dtypes.items():

            info(
                f"  - {col:<45} "
                f"{dtype}"
            )

    # -------------------------------------------------------------------------
    # NULLS
    # -------------------------------------------------------------------------

    if show_nulls:

        nulls = (
            df.isna()
            .sum()
        )

        nulls = (
            nulls[
                nulls > 0
            ]
            .sort_values(
                ascending=False
            )
        )

        if len(nulls):

            info("\nNULLS")

            for col, qtd in nulls.items():

                pct = (
                    qtd / len(df)
                ) * 100

                info(
                    f"  - {col:<45} "
                    f"{qtd:>10,} "
                    f"({pct:.2f}%)"
                )

    # -------------------------------------------------------------------------
    # PREVIEW
    # -------------------------------------------------------------------------

    if show_preview:

        info("\nPREVIEW")

        preview = (
            df.head(preview_rows)
            .to_string()
        )

        info(
            f"\n{preview}"
        )

    info("=" * 80)

# =============================================================================
# LOG DE TRANSFORMAÇÃO
# =============================================================================

def log_transformation(
    *,
    dataframe: str,
    operation: str,
    columns: list[str] | None = None,
    before_dtype: str | None = None,
    after_dtype: str | None = None,
    rows_before: int | None = None,
    rows_after: int | None = None,
    rules: list[str] | None = None,
    details: str | None = None,
) -> None:
    """
    Registra transformação aplicada.
    """

    lines = [
        "\n",
        separator(),
        f"[{now()}] TRANSFORMATION",
        separator(),
        f"DATAFRAME : {dataframe}",
        f"OPERATION : {operation}",
    ]

    if columns:
        lines.append(
            f"COLUMNS   : {', '.join(columns)}"
        )

    if before_dtype:
        lines.append(
            f"BEFORE    : {before_dtype}"
        )

    if after_dtype:
        lines.append(
            f"AFTER     : {after_dtype}"
        )

    if rows_before is not None:
        lines.append(
            f"ROWS_BEFORE : {rows_before:,}"
        )

    if rows_after is not None:
        lines.append(
            f"ROWS_AFTER  : {rows_after:,}"
        )

    if rules:

        lines.append("\nREGRAS")

        for rule in rules:

            lines.append(f"  - {rule}")

    if details:

        lines.append("\nDETAILS")
        lines.append(details)

    lines.append("\n")

    content = "\n".join(lines)

    write_log(content)

    if VERBOSE:

        print(
            f"\n[TRANSFORMATION] {operation}"
        )

        print(
            f"DataFrame : {dataframe}"
        )

        if columns:
            print(
                f"Colunas   : {', '.join(columns)}"
            )

        if rows_before is not None:
            print(
                f"Linhas antes : {rows_before:,}"
            )

        if rows_after is not None:
            print(
                f"Linhas depois: {rows_after:,}"
            )

        if rules:

            print("\nRegras aplicadas:")

            for rule in rules:

                print(f"- {rule}")

