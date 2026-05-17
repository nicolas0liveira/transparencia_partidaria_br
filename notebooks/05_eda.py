#%%
# Imports
# ============================================================================

from pathlib import Path

from IPython.display import display

import pandas as pd

from transparencia_partidaria_br.utils.pipeline.logger import (
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
    "Análise exploratória inicial",
    notebook="04_eda.py",
)

info("Lendo dataset agregado...")

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
# Estatísticas iniciais
# ============================================================================

log_step(
    "Estatísticas iniciais",
)

print("\nDescribe:")

display(
    df.describe()
)

print("\nTop 10 registros:")

display(
    df.head(10)
)