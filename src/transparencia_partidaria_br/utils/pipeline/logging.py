"""
Infraestrutura de logging para pipelines analíticas.

Objetivos:
- rastreabilidade
- reproducibilidade
- auditoria
- observabilidade
- documentação metodológica
"""

from __future__ import annotations

import logging
import sys

from pathlib import Path
from time import perf_counter
from typing import Any

import pandas as pd

# =============================================================================
# Diretórios
# =============================================================================

BASE_DIR = Path(".")

LOG_DIR = (
    BASE_DIR / "logs"
)

LOG_DIR.mkdir(
    parents=True,
    exist_ok=True,
)

LOG_FILE = (
    LOG_DIR / "pipeline.log"
)

# =============================================================================
# Logger
# =============================================================================

LOGGER_NAME = (
    "transparencia_partidaria_br"
)

logger = logging.getLogger(
    LOGGER_NAME
)

logger.setLevel(
    logging.INFO
)

logger.propagate = False

# -----------------------------------------------------------------------------
# Evita handlers duplicados
# -----------------------------------------------------------------------------

if not logger.handlers:

    # -------------------------------------------------------------------------
    # Formatter
    # -------------------------------------------------------------------------

    formatter = logging.Formatter(
        (
            "%(asctime)s | "
            "%(levelname)s | "
            "%(message)s"
        ),
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # -------------------------------------------------------------------------
    # File handler
    # -------------------------------------------------------------------------

    file_handler = logging.FileHandler(
        LOG_FILE,
        encoding="utf-8",
    )

    file_handler.setFormatter(
        formatter
    )

    # -------------------------------------------------------------------------
    # Console handler
    # -------------------------------------------------------------------------

    console_handler = logging.StreamHandler(
        sys.stdout
    )

    console_handler.setFormatter(
        formatter
    )

    # -------------------------------------------------------------------------
    # Add handlers
    # -------------------------------------------------------------------------

    logger.addHandler(
        file_handler
    )

    logger.addHandler(
        console_handler
    )

# =============================================================================
# Public API
# =============================================================================

__all__ = [
    "timer",
    "elapsed",
    "debug",
    "info",
    "success",
    "warning",
    "error",
    "exception",
    "log_step",
    "log_pipeline_start",
    "log_pipeline_end",
    "log_dataframe",
    "log_dataframe_profile",
    "log_file_operation",
    "log_transformation",
    "log_metric",
    "log_dict",
]

# =============================================================================
# Timers
# =============================================================================


def timer() -> float:
    """
    Retorna timestamp alta precisão.
    """

    return perf_counter()


def elapsed(
    start_time: float,
) -> str:
    """
    Retorna tempo decorrido formatado.
    """

    total_seconds = (
        perf_counter() - start_time
    )

    return f"{total_seconds:.2f}s"


# =============================================================================
# Logging básicos
# =============================================================================


def debug(
    message: str,
) -> None:
    """
    Log DEBUG.
    """

    logger.debug(
        f"[DEBUG] {message}"
    )


def info(
    message: str,
) -> None:
    """
    Log INFO.
    """

    logger.info(
        message
    )


def success(
    message: str,
) -> None:
    """
    Log SUCCESS.
    """

    logger.info(
        f"[SUCCESS] {message}"
    )


def warning(
    message: str,
) -> None:
    """
    Log WARNING.
    """

    logger.warning(
        f"[WARNING] {message}"
    )


def error(
    message: str,
) -> None:
    """
    Log ERROR.
    """

    logger.error(
        f"[ERROR] {message}"
    )


def exception(
    message: str,
    error: Exception,
) -> None:
    """
    Log EXCEPTION.
    """

    logger.exception(
        f"[EXCEPTION] {message}: {error}"
    )


# =============================================================================
# Pipeline
# =============================================================================


def log_pipeline_start(
    pipeline_name: str,
) -> None:
    """
    Log início pipeline.
    """

    logger.info(
        (
            "\n"
            "############################################################\n"
            f"[PIPELINE_START] {pipeline_name}\n"
            "############################################################"
        )
    )


def log_pipeline_end(
    pipeline_name: str,
) -> None:
    """
    Log final pipeline.
    """

    logger.info(
        (
            "\n"
            "############################################################\n"
            f"[PIPELINE_END] {pipeline_name}\n"
            "############################################################"
        )
    )


def log_step(
    step_name: str,
) -> None:
    """
    Log etapa pipeline.
    """

    logger.info(
        (
            "\n"
            "============================================================\n"
            f"[STEP] {step_name}\n"
            "============================================================"
        )
    )


# =============================================================================
# DataFrames
# =============================================================================


def log_dataframe(
    name: str,
    rows: int,
    columns: int,
) -> None:
    """
    Log simplificado dataframe.
    """

    logger.info(
        (
            f"[DATAFRAME] "
            f"{name} | "
            f"rows={rows:,} | "
            f"columns={columns:,}"
        )
    )


def log_dataframe_profile(
    name: str,
    df: pd.DataFrame,
    preview_rows: int = 5,
    show_nulls: bool = True,
    show_dtypes: bool = True,
) -> None:
    """
    Log detalhado dataframe.
    """

    logger.info(
        (
            "\n"
            "------------------------------------------------------------\n"
            f"[DATAFRAME_PROFILE] {name}\n"
            "------------------------------------------------------------"
        )
    )

    # -------------------------------------------------------------------------
    # Shape
    # -------------------------------------------------------------------------

    logger.info(
        f"shape={df.shape}"
    )

    # -------------------------------------------------------------------------
    # Memory
    # -------------------------------------------------------------------------

    memory_mb = (
        df.memory_usage(
            deep=True
        ).sum() / 1024**2
    )

    logger.info(
        f"memory_mb={memory_mb:.2f}"
    )

    # -------------------------------------------------------------------------
    # Dtypes
    # -------------------------------------------------------------------------

    if show_dtypes:

        logger.info(
            "\n[DTYPES]"
        )

        for col, dtype in df.dtypes.items():

            logger.info(
                f"{col}={dtype}"
            )

    # -------------------------------------------------------------------------
    # Nulls
    # -------------------------------------------------------------------------

    if show_nulls:

        logger.info(
            "\n[NULLS]"
        )

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

        for col, qtd in nulls.items():

            pct = (
                qtd / len(df)
            ) * 100

            logger.info(
                (
                    f"{col}="
                    f"{qtd:,} "
                    f"({pct:.2f}%)"
                )
            )

    # -------------------------------------------------------------------------
    # Preview
    # -------------------------------------------------------------------------

    preview = (
        df.head(preview_rows)
        .to_string()
    )

    logger.info(
        (
            "\n[PREVIEW]\n"
            f"{preview}"
        )
    )


# =============================================================================
# Arquivos
# =============================================================================


def log_file_operation(
    operation: str,
    source: str | Path,
    target: str | Path,
) -> None:
    """
    Log operação arquivo.
    """

    logger.info(
        (
            f"[FILE] "
            f"{operation} | "
            f"source={source} | "
            f"target={target}"
        )
    )


# =============================================================================
# Transformações
# =============================================================================


def log_transformation(
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
    Log transformação pipeline.
    """

    logger.info(
        (
            "\n"
            "------------------------------------------------------------\n"
            "[TRANSFORMATION]\n"
            "------------------------------------------------------------"
        )
    )

    logger.info(
        f"dataframe={dataframe}"
    )

    logger.info(
        f"operation={operation}"
    )

    if columns:

        logger.info(
            f"columns={columns}"
        )

    if before_dtype:

        logger.info(
            f"before_dtype={before_dtype}"
        )

    if after_dtype:

        logger.info(
            f"after_dtype={after_dtype}"
        )

    if rows_before is not None:

        logger.info(
            f"rows_before={rows_before:,}"
        )

    if rows_after is not None:

        logger.info(
            f"rows_after={rows_after:,}"
        )

    if rules:

        logger.info(
            f"rules={rules}"
        )

    if details:

        logger.info(
            f"details={details}"
        )


# =============================================================================
# Métricas
# =============================================================================


def log_metric(
    metric_name: str,
    metric_value: Any,
) -> None:
    """
    Log métrica individual.
    """

    logger.info(
        (
            f"[METRIC] "
            f"{metric_name}="
            f"{metric_value}"
        )
    )


def log_dict(
    title: str,
    values: dict[str, Any],
) -> None:
    """
    Log estruturado dict.
    """

    logger.info(
        f"[DICT] {title}"
    )

    for key, value in values.items():

        logger.info(
            f"{key}={value}"
        )


        