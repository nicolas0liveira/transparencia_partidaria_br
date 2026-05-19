from pathlib import Path

import pandas as pd

from transparencia_partidaria_br.utils.pipeline.logging import (
    log_step,
    success,
)

from transparencia_partidaria_br.utils.tse.tse_parser import (
    read_tse_csv,
)

# =============================================================================
# Diretórios
# =============================================================================

BASE_DIR = Path(".")

RAW_TSE_DIR = (
    BASE_DIR / "data/01-raw/tse"
)

# =============================================================================
# Arquivos
# =============================================================================

ARQ_RECEITA = (
    RAW_TSE_DIR / "receita_anual_2025_BRASIL.csv"
)

ARQ_DESPESA = (
    RAW_TSE_DIR / "despesa_anual_2025_BRASIL.csv"
)

# =============================================================================
# Receita
# =============================================================================


def ingest_receita() -> pd.DataFrame:
    """
    Realiza ingestão da base de receitas do TSE.

    Responsabilidades:
    - leitura do CSV
    - parsing inicial
    - retorno do dataframe bruto

    Não realiza:
    - preprocessing
    - enriquecimento
    - feature engineering
    """

    log_step(
        "Ingestão de receitas TSE"
    )

    df_receita = read_tse_csv(
        ARQ_RECEITA
    )

    success(
        "Receitas carregadas com sucesso."
    )

    return df_receita


# =============================================================================
# Despesa
# =============================================================================


def ingest_despesa() -> pd.DataFrame:
    """
    Realiza ingestão da base de despesas do TSE.

    Responsabilidades:
    - leitura do CSV
    - parsing inicial
    - retorno do dataframe bruto

    Não realiza:
    - preprocessing
    - enriquecimento
    - feature engineering
    """

    log_step(
        "Ingestão de despesas TSE"
    )

    df_despesa = read_tse_csv(
        ARQ_DESPESA
    )

    success(
        "Despesas carregadas com sucesso."
    )

    return df_despesa
