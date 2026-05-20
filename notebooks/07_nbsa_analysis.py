#%%
# Imports
# ============================================================================

from pathlib import Path

from IPython.display import display

import pandas as pd

from transparencia_partidaria_br.utils.pipeline.logging import (
    info,
    log_dataframe,
    log_step,
    success,
)


#%%
# Configurações
# ============================================================================

BASE_DIR = Path("../")

SILVER_DIR = BASE_DIR / "data/02-silver"

ARQ_CNPJS = (
    SILVER_DIR / "cnpjs_agregados.parquet"
)


#%%
# Leitura
# ============================================================================

log_step(
    "Análises NBSA",
    notebook="05_nbsa_analysis.py",
)

info("Lendo dataset consolidado...")

df = pd.read_parquet(
    ARQ_CNPJS,
)

success("Dataset carregado.")

log_dataframe(
    name="df_cnpjs_agg",
    df=df,
    source=ARQ_CNPJS,
)


#%%
# Estatísticas descritivas
# ============================================================================

log_step(
    "Estatísticas descritivas",
)

print("\nDescribe:")

display(
    df.describe()
)


#%%
# Top registros
# ============================================================================

log_step(
    "Top registros",
)

display(
    df.head(20)
)