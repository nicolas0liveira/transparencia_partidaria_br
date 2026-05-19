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

RAW_AUX_DIR = (
    BASE_DIR / "data/01-raw/aux"
)

# =============================================================================
# Arquivos
# =============================================================================

ARQ_CLASS_DESPESA = (
    RAW_AUX_DIR / "tse_classificacao_despesa.csv"
)

# =============================================================================
# Classificação de Despesa
# =============================================================================


def ingest_aux_classificacao_despesa() -> pd.DataFrame:
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
        "Ingestão de classificação de despesas TSE"
    )

    df_despesa_class = read_tse_csv(
        ARQ_CLASS_DESPESA
        ,sep=";"
        ,encoding="utf-8"
    )

    success(
        "Classificação de despesas carregada com sucesso."
    )

    return df_despesa_class