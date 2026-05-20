#%%
# Enriquecimento funcional - Despesas TSE
# ============================================================================

"""
Pipeline complementar para criação
de novas colunas analíticas.

Objetivos:
- classificação funcional
- classificação categoria/subcategoria
- enriquecimento semântico
- engenharia de atributos
- preparação para:
    - EDA
    - clusterização
    - modelos estatísticos
    - amostragem
    - análise multivariada

IMPORTANTE:
Este pipeline deve ser executado
após a ingestão silver.
"""

#%%
# Imports
# ============================================================================

from pathlib import Path

import numpy as np
import pandas as pd
from IPython.display import display

from transparencia_partidaria_br.utils.pipeline.loggingg import (
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
    apply_value_classification,
    summarize_categories,
    summarize_classification,
    summarize_financial_values,
    summarize_subcategories,
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

ARQ_DESPESA_SILVER = (
    SILVER_DIR / "01_despesa_2025.parquet"
)

# -----------------------------------------------------------------------------
# Saída
# -----------------------------------------------------------------------------

ARQ_DESPESA_FEATURE = (
    FEATURE_DIR / "02_despesa_2025_feature.parquet"
)

ARQ_DESPESA_FEATURE_CSV = (
    FEATURE_DIR / "02_despesa_2025_feature.csv"
)

#%%
# Leitura parquet silver
# ============================================================================

log_step(
    "Leitura parquet silver"
)

start = timer()

info(
    "Lendo despesas silver..."
)

df_despesa = pd.read_parquet(
    ARQ_DESPESA_SILVER
)

success(
    f"Arquivo carregado em {elapsed(start)}"
)

log_dataframe(
    name="df_despesa",
    df=df_despesa,
    source=ARQ_DESPESA_SILVER,
)

display(
    df_despesa.head()
)

#%%
# Leitura parquet silver
# ============================================================================

log_step(
    "Verifica valores distintos do DS_GASTO"
)

start = timer()

info(
    "Verificando valores distintos do DS_GASTO..."
)

distinct_values = df_despesa["DS_GASTO"].unique()
distinct_values_df = pd.DataFrame(
    distinct_values,
    columns=["DS_GASTO_DISTINCT"],
)
info(f"Valores distintos do DS_GASTO: {distinct_values}")

display(
    distinct_values_df
)



success(
    f"Verificação concluída em {elapsed(start)}"
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

# -----------------------------------------------------------------------------
# DS_GASTO
# -----------------------------------------------------------------------------

df_despesa = apply_value_classification(
    df_despesa,
    source_column="DS_GASTO",
    classification_column=(
        "DS_CLASSIFICACAO"
    ),
    category_column=(
        "DS_CATEGORIA"
    ),
    subcategory_column=(
        "DS_SUBCATEGORIA"
    ),
)

# -----------------------------------------------------------------------------
# Normalização categórica
# -----------------------------------------------------------------------------

for col in [
    "DS_CLASSIFICACAO",
    "DS_CATEGORIA",
    "DS_SUBCATEGORIA",
]:

    df_despesa[col] = (
        df_despesa[col]
        .astype("category")
    )

success(
    f"Classificação concluída em {elapsed(start)}"
)

log_transformation(
    dataframe="df_despesa",
    operation="VALUE_CLASSIFICATION",
    columns=[
        "DS_GASTO",
    ],
    rules=[
        "CATEGORY_PARSER",
        "SUBCATEGORY_PARSER",
        "FUNCTIONAL_CLASSIFICATION",
        "CATEGORICAL_ENCODING",
    ],
)

display(
    df_despesa[
        [
            "DS_GASTO",
            "DS_CLASSIFICACAO",
            "DS_CATEGORIA",
            "DS_SUBCATEGORIA",
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
# Indicador binário finalística
# -----------------------------------------------------------------------------

df_despesa[
    "FL_FINALISTICA"
] = (
    df_despesa[
        "DS_CLASSIFICACAO"
    ]
    .eq("FINALISTICA")
    .astype("int8")
)

# -----------------------------------------------------------------------------
# Indicador binário administrativa
# -----------------------------------------------------------------------------

df_despesa[
    "FL_ADMINISTRATIVA"
] = (
    df_despesa[
        "DS_CLASSIFICACAO"
    ]
    .eq("ADMINISTRATIVA")
    .astype("int8")
)

# -----------------------------------------------------------------------------
# Conversão monetária
# -----------------------------------------------------------------------------

df_despesa[
    "VR_PAGAMENTO"
] = pd.to_numeric(
    df_despesa[
        "VR_PAGAMENTO"
    ],
    errors="coerce",
)

# -----------------------------------------------------------------------------
# Valor absoluto
# -----------------------------------------------------------------------------

df_despesa[
    "VR_PAGAMENTO_ABS"
] = (
    df_despesa[
        "VR_PAGAMENTO"
    ]
    .abs()
)

# -----------------------------------------------------------------------------
# Log do valor
# -----------------------------------------------------------------------------

df_despesa[
    "LOG_VR_PAGAMENTO"
] = np.log1p(
    df_despesa[
        "VR_PAGAMENTO_ABS"
    ]
)

# -----------------------------------------------------------------------------
# Faixas monetárias
# -----------------------------------------------------------------------------

bins = [
    -1,
    100,
    1000,
    10000,
    100000,
    float("inf"),
]

labels = [
    "MICRO",
    "PEQUENO",
    "MEDIO",
    "ALTO",
    "MUITO_ALTO",
]

df_despesa[
    "DS_FAIXA_VALOR"
] = pd.cut(
    df_despesa[
        "VR_PAGAMENTO_ABS"
    ],
    bins=bins,
    labels=labels,
)

# -----------------------------------------------------------------------------
# Quartis globais
# -----------------------------------------------------------------------------

df_despesa[
    "NR_QUARTIL_VALOR"
] = pd.qcut(
    df_despesa[
        "VR_PAGAMENTO_ABS"
    ]
    .fillna(0),
    q=4,
    labels=False,
    duplicates="drop",
)

# -----------------------------------------------------------------------------
# Percentil do gasto
# -----------------------------------------------------------------------------

df_despesa[
    "PCT_VALOR"
] = (
    df_despesa[
        "VR_PAGAMENTO_ABS"
    ]
    .rank(
        pct=True
    )
    .round(4)
)

# -----------------------------------------------------------------------------
# Indicador alto valor
# -----------------------------------------------------------------------------

p95 = (
    df_despesa[
        "VR_PAGAMENTO_ABS"
    ]
    .quantile(0.95)
)

df_despesa[
    "FL_ALTO_VALOR"
] = (
    df_despesa[
        "VR_PAGAMENTO_ABS"
    ]
    .ge(p95)
    .astype("int8")
)

# -----------------------------------------------------------------------------
# Indicador outlier (IQR)
# -----------------------------------------------------------------------------

q1 = (
    df_despesa[
        "VR_PAGAMENTO_ABS"
    ]
    .quantile(0.25)
)

q3 = (
    df_despesa[
        "VR_PAGAMENTO_ABS"
    ]
    .quantile(0.75)
)

iqr = q3 - q1

limite_superior = (
    q3 + (1.5 * iqr)
)

df_despesa[
    "FL_OUTLIER_VALOR"
] = (
    df_despesa[
        "VR_PAGAMENTO_ABS"
    ]
    .gt(limite_superior)
    .astype("int8")
)

# -----------------------------------------------------------------------------
# Estrato para amostragem
# -----------------------------------------------------------------------------

df_despesa[
    "DS_ESTRATO_VALOR"
] = pd.qcut(
    df_despesa[
        "VR_PAGAMENTO_ABS"
    ]
    .fillna(0),
    q=5,
    labels=[
        "ESTRATO_1",
        "ESTRATO_2",
        "ESTRATO_3",
        "ESTRATO_4",
        "ESTRATO_5",
    ],
    duplicates="drop",
)

# -----------------------------------------------------------------------------
# Valor padronizado (z-score)
# -----------------------------------------------------------------------------

media_valor = (
    df_despesa[
        "VR_PAGAMENTO_ABS"
    ]
    .mean()
)

desvio_valor = (
    df_despesa[
        "VR_PAGAMENTO_ABS"
    ]
    .std()
)

df_despesa[
    "Z_SCORE_VR_PAGAMENTO"
] = (
    (
        df_despesa[
            "VR_PAGAMENTO_ABS"
        ] - media_valor
    )
    / desvio_valor
)

# -----------------------------------------------------------------------------
# Classe estatística do gasto
# -----------------------------------------------------------------------------

df_despesa[
    "DS_CLASSE_ESTATISTICA"
] = pd.cut(
    df_despesa[
        "Z_SCORE_VR_PAGAMENTO"
    ],
    bins=[
        -float("inf"),
        -2,
        -1,
        1,
        2,
        float("inf"),
    ],
    labels=[
        "MUITO_BAIXO",
        "BAIXO",
        "NORMAL",
        "ALTO",
        "EXTREMO",
    ],
)

# -----------------------------------------------------------------------------
# Percentual relativo do gasto
# -----------------------------------------------------------------------------

valor_total = (
    df_despesa[
        "VR_PAGAMENTO_ABS"
    ]
    .sum()
)

df_despesa[
    "PCT_PARTICIPACAO_VALOR"
] = (
    (
        df_despesa[
            "VR_PAGAMENTO_ABS"
        ]
        / valor_total
    ) * 100
).round(8)

# -----------------------------------------------------------------------------
# Ano competência
# -----------------------------------------------------------------------------

if (
    "DT_PAGAMENTO"
    in df_despesa.columns
):

    df_despesa[
        "NR_ANO"
    ] = (
        df_despesa[
            "DT_PAGAMENTO"
        ]
        .dt.year
    )

# -----------------------------------------------------------------------------
# Mês competência
# -----------------------------------------------------------------------------

if (
    "DT_PAGAMENTO"
    in df_despesa.columns
):

    df_despesa[
        "NR_MES"
    ] = (
        df_despesa[
            "DT_PAGAMENTO"
        ]
        .dt.month
    )

success(
    f"Indicadores derivados criados em {elapsed(start)}"
)

log_transformation(
    dataframe="df_despesa",
    operation="FEATURE_ENGINEERING",
    rules=[
        "CREATE_BINARY_FLAGS",
        "CREATE_TEMPORAL_FEATURES",
        "CREATE_MONETARY_FEATURES",
        "CREATE_OUTLIER_FLAGS",
        "CREATE_SAMPLING_STRATA",
        RULE_SILVER_LAYER.STANDARDIZE_TYPES,
    ],
)

display(
    df_despesa[
        [
            "VR_PAGAMENTO",
            "VR_PAGAMENTO_ABS",
            "LOG_VR_PAGAMENTO",
            "DS_FAIXA_VALOR",
            "NR_QUARTIL_VALOR",
            "PCT_VALOR",
            "FL_ALTO_VALOR",
            "FL_OUTLIER_VALOR",
            "DS_ESTRATO_VALOR",
            "Z_SCORE_VR_PAGAMENTO",
            "DS_CLASSE_ESTATISTICA",
            "PCT_PARTICIPACAO_VALOR",
            "DS_CLASSIFICACAO",
            "FL_FINALISTICA",
            "FL_ADMINISTRATIVA",
        ]
    ]
    .head(20)
)

#%%
# Distribuição funcional
# ============================================================================

log_step(
    "Distribuição funcional"
)

# -----------------------------------------------------------------------------
# Resumo classificação
# -----------------------------------------------------------------------------

resumo_classificacao = (
    summarize_classification(
        df_despesa,
        classification_column=(
            "DS_CLASSIFICACAO"
        ),
    )
)

display(
    resumo_classificacao
)

# -----------------------------------------------------------------------------
# Resumo categorias
# -----------------------------------------------------------------------------

resumo_categoria = (
    summarize_categories(
        df_despesa,
        category_column=(
            "DS_CATEGORIA"
        ),
    )
)

display(
    resumo_categoria.head(20)
)

# -----------------------------------------------------------------------------
# Resumo subcategorias
# -----------------------------------------------------------------------------

resumo_subcategoria = (
    summarize_subcategories(
        df_despesa,
        category_column=(
            "DS_CATEGORIA"
        ),
        subcategory_column=(
            "DS_SUBCATEGORIA"
        ),
    )
)

display(
    resumo_subcategoria.head(20)
)

# -----------------------------------------------------------------------------
# Resumo financeiro
# -----------------------------------------------------------------------------

resumo_financeiro = (
    summarize_financial_values(
        df_despesa,
        value_column="VR_PAGAMENTO_ABS",
        classification_column=(
            "DS_CLASSIFICACAO"
        ),
    )
)

display(
    resumo_financeiro
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
    df_despesa,
    ARQ_DESPESA_FEATURE,
)

log_file_operation(
    operation="WRITE_PARQUET",
    source="df_despesa",
    target=ARQ_DESPESA_FEATURE,
)

# -----------------------------------------------------------------------------
# CSV
# -----------------------------------------------------------------------------

info(
    "Persistindo CSV..."
)

df_despesa.to_csv(
    ARQ_DESPESA_FEATURE_CSV,
    sep=";",
    index=False,
    encoding="utf-8",
)

log_file_operation(
    operation="WRITE_CSV",
    source="df_despesa",
    target=ARQ_DESPESA_FEATURE_CSV,
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
    "Enriquecimento funcional concluído."
)

#%%