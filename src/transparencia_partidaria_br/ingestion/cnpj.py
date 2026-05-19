from pathlib import Path

import pandas as pd

from transparencia_partidaria_br.utils.pipeline.logging import (
    log_step,
    success,
)

# =============================================================================
# Diretórios
# =============================================================================

BASE_DIR = Path(".")

RAW_CNPJ_DIR = (
    BASE_DIR / "data/01-raw/cnpj"
)

# =============================================================================
# Arquivos
# =============================================================================

ARQ_CNPJ = (
    RAW_CNPJ_DIR / "pjrfb_cnpj.csv"
)

# =============================================================================
# CNPJ Receita Federal
# =============================================================================


def ingest_cnpj() -> pd.DataFrame:
    """
    Realiza ingestão da base pública de CNPJs.

    Responsabilidades:
    - leitura do CSV
    - carregamento bruto da RFB
    - retorno dataframe raw

    Não realiza:
    - enriquecimento
    - joins
    - feature engineering
    """

    log_step(
        "Ingestão base CNPJ Receita Federal"
    )

    df_cnpj = pd.read_csv(
        ARQ_CNPJ,
        dtype=str,
        low_memory=False,
    )

    success(
        "Base CNPJ carregada com sucesso."
    )

    return df_cnpj
