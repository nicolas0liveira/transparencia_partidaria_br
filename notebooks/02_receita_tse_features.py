#%%
# Enriquecimento funcional - Receitas TSE
# ============================================================================

"""
Pipeline complementar para criação
de novas colunas analíticas
relacionadas às receitas partidárias.

Objetivos:
- classificação funcional
- engenharia de atributos
- preparação analítica
- suporte para:
    - EDA
    - transparência
    - eficiência
    - clusterização
    - amostragem
    - análise multivariada

IMPORTANTE:
Executar após:
01_ingestion_tse.py
"""

#%%
# Imports
# ============================================================================

from pathlib import Path

import pandas as pd
import numpy as np

from IPython.display import display

from transparencia_partidaria_br.utils.pipeline.logger import (
    elapsed,
    info,
    log_dataframe,
    log_file_operation,
    log_step,
    log_transformation,
    success,
    timer,
)

from transparencia_partidaria_br.utils.pipeline.parquet_utils import (
    write_parquet,
)

from transparencia_partidaria_br.utils.pipeline.rules import (
    RULE_SILVER_LAYER,
)

from transparencia_partidaria_br.utils.tse.tse_classify_utils import (
    COLUNAS_CLASSIFICACAO_RECEITA,
    apply_functional_classification,
)

#%%
# Configurações
# ============================================================================

BASE_DIR = Path("../")

SILVER_DIR = (
    BASE_DIR / "data/02-silver"
)

FEATURE_DIR = (
    BASE_DIR / "data/03-feature"
)

FEATURE_DIR.mkdir(
    parents=True,
    exist_ok=True,
)

# -----------------------------------------------------------------------------
# Entrada
# -----------------------------------------------------------------------------

ARQ_RECEITA_SILVER = (
    SILVER_DIR / "receita_2025.parquet"
)

# -----------------------------------------------------------------------------
# Saída
# -----------------------------------------------------------------------------

ARQ_RECEITA_FEATURE = (
    FEATURE_DIR / "receita_2025_feature.parquet"
)

ARQ_RECEITA_FEATURE_CSV = (
    FEATURE_DIR / "receita_2025_feature.csv"
)

#%%
# Leitura parquet silver
# ============================================================================

log_step(
    "Leitura parquet silver"
)

start = timer()

info(
    "Lendo receitas silver..."
)

df_receita = pd.read_parquet(
    ARQ_RECEITA_SILVER
)

success(
    f"Arquivo carregado em {elapsed(start)}"
)

log_dataframe(
    name="df_receita",
    df=df_receita,
    source=ARQ_RECEITA_SILVER,
)

display(
    df_receita.head()
)

#%%
# Classificação funcional
# ============================================================================

log_step(
    "Classificação funcional"
)

start = timer()

info(
    "Aplicando classificação funcional..."
)

df_receita = (
    apply_functional_classification(
        df_receita,
        columns=(
            COLUNAS_CLASSIFICACAO_RECEITA
        ),
        target_column=(
            "DS_CLASSIFICACAO_FUNCIONAL"
        ),
    )
)

success(
    f"Classificação concluída em {elapsed(start)}"
)

log_transformation(
    dataframe="df_receita",
    operation="FUNCTIONAL_CLASSIFICATION",
    columns=(
        COLUNAS_CLASSIFICACAO_RECEITA
    ),
    rules=[
        "CLASSIFY_ADMINISTRATIVA",
        "CLASSIFY_FINALISTICA",
        "MULTI_COLUMN_TEXT_ANALYSIS",
        "KEYWORD_BASED_CLASSIFICATION",
    ],
)

display(
    df_receita[
        [
            "DS_CLASSIFICACAO_FUNCIONAL",
        ]
    ]
    .head(20)
)

#%%
# Indicadores derivados
# ============================================================================

log_step(
    "Indicadores derivados"
)

start = timer()

# -----------------------------------------------------------------------------
# Indicador finalístico
# -----------------------------------------------------------------------------

df_receita[
    "FL_FINALISTICA"
] = (
    df_receita[
        "DS_CLASSIFICACAO_FUNCIONAL"
    ]
    .eq("FINALISTICA")
    .astype("int8")
)

# -----------------------------------------------------------------------------
# Indicador administrativo
# -----------------------------------------------------------------------------

df_receita[
    "FL_ADMINISTRATIVA"
] = (
    df_receita[
        "DS_CLASSIFICACAO_FUNCIONAL"
    ]
    .eq("ADMINISTRATIVA")
    .astype("int8")
)

# -----------------------------------------------------------------------------
# Ano da receita
# -----------------------------------------------------------------------------

if (
    "DT_RECEITA"
    in df_receita.columns
):

    df_receita[
        "NR_ANO"
    ] = (
        df_receita[
            "DT_RECEITA"
        ]
        .dt.year
    )

# -----------------------------------------------------------------------------
# Mês da receita
# -----------------------------------------------------------------------------

if (
    "DT_RECEITA"
    in df_receita.columns
):

    df_receita[
        "NR_MES"
    ] = (
        df_receita[
            "DT_RECEITA"
        ]
        .dt.month
    )

# -----------------------------------------------------------------------------
# Faixa de valor
# -----------------------------------------------------------------------------

if (
    "VR_RECEITA"
    in df_receita.columns
):

    df_receita[
        "DS_FAIXA_VALOR"
    ] = pd.cut(
        df_receita[
            "VR_RECEITA"
        ],
        bins=[
            -1,
            100,
            1000,
            10000,
            100000,
            float("inf"),
        ],
        labels=[
            "ATE_100",
            "100_A_1K",
            "1K_A_10K",
            "10K_A_100K",
            "ACIMA_100K",
        ],
    )

# -----------------------------------------------------------------------------
# Log valor receita
# -----------------------------------------------------------------------------

if (
    "VR_RECEITA"
    in df_receita.columns
):

    df_receita[
        "VR_RECEITA_LOG"
    ] = (
        df_receita[
            "VR_RECEITA"
        ]
        .fillna(0)
        .apply(
            lambda x: (
                0
                if x <= 0
                else np.log1p(x)
            )
        )
    )

success(
    f"Features criadas em {elapsed(start)}"
)

log_transformation(
    dataframe="df_receita",
    operation="FEATURE_ENGINEERING",
    rules=[
        "CREATE_BINARY_FLAGS",
        "CREATE_TEMPORAL_FEATURES",
        "CREATE_MONETARY_BUCKETS",
        "CREATE_LOG_FEATURES",
        RULE_SILVER_LAYER.STANDARDIZE_TYPES,
    ],
)

display(
    df_receita.head()
)

#%%
# Distribuição funcional
# ============================================================================

log_step(
    "Distribuição funcional"
)

resumo = (
    df_receita[
        "DS_CLASSIFICACAO_FUNCIONAL"
    ]
    .value_counts(
        dropna=False,
        normalize=True,
    )
    .mul(100)
    .round(2)
    .rename("PERCENTUAL")
    .to_frame()
)

display(
    resumo
)

#%%
# Persistência
# ============================================================================

log_step(
    "Persistência feature layer"
)

start = timer()

# -----------------------------------------------------------------------------
# Parquet
# -----------------------------------------------------------------------------

info(
    "Persistindo parquet..."
)

write_parquet(
    df_receita,
    ARQ_RECEITA_FEATURE,
)

log_file_operation(
    operation="WRITE_PARQUET",
    source="df_receita",
    target=ARQ_RECEITA_FEATURE,
)

# -----------------------------------------------------------------------------
# CSV
# -----------------------------------------------------------------------------

info(
    "Persistindo CSV..."
)

df_receita.to_csv(
    ARQ_RECEITA_FEATURE_CSV,
    sep=";",
    index=False,
    encoding="utf-8",
)

log_file_operation(
    operation="WRITE_CSV",
    source="df_receita",
    target=ARQ_RECEITA_FEATURE_CSV,
)

success(
    f"Persistência concluída em {elapsed(start)}"
)

#%%
# Finalização
# ============================================================================

log_step(
    "Pipeline finalizada"
)

success(
    "Enriquecimento funcional de receitas concluído."
)

#%%