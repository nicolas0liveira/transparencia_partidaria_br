#%%
# Enriquecimento de CNPJs
# ============================================================================

"""
Pipeline de enriquecimento de fornecedores
via base pública da Receita Federal.

Objetivos:
- enriquecer CNPJs distintos
- adicionar informações cadastrais
- criar features analíticas
- preparar dados para:
    - EDA
    - clusterização
    - análise multivariada
    - análise de risco
"""

#%%
# Imports
# ============================================================================

from pathlib import Path

import numpy as np
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

RAW_CNPJ_DIR = (
    BASE_DIR / "data/01-raw/cnpj"
)

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

ARQ_CNPJS_DISTINTOS = (
    SILVER_DIR / "01a_cnpjs_distintos.parquet"
)

ARQ_CNPJ_RFB = (
    RAW_CNPJ_DIR / "pjrfb_cnpj.csv"
)

ARQ_CNPJ_ENRICHED_PARQUET = (
    FEATURE_DIR / "01b_cnpj_enrichment.parquet"
)

ARQ_CNPJ_ENRICHED_CSV = (
    FEATURE_DIR / "01b_cnpj_enrichment.csv"
)

#%%
# Leitura de CNPJs distintos
# ============================================================================

log_step(
    "Leitura de CNPJs distintos",
    notebook="01b_cnpj_enrichment.py",
)

info(
    "Lendo CNPJs distintos..."
)

df_cnpjs = pd.read_parquet(
    ARQ_CNPJS_DISTINTOS,
)

success(
    "Leitura de CNPJs distintos concluída."
)

info(
    f"Registros carregados: "
    f"{len(df_cnpjs):,}"
)

log_dataframe(
    name="df_cnpjs",
    df=df_cnpjs,
    source=ARQ_CNPJS_DISTINTOS,
)

#%%
# Leitura base RFB
# ============================================================================

log_step(
    "Leitura da base CNPJ RFB",
)

info(
    "Lendo base pjrfb_cnpj.csv..."
)

df_rfb = pd.read_csv(
    ARQ_CNPJ_RFB,
    dtype=str,
    low_memory=False,
)

success(
    "Leitura da base RFB concluída."
)

info(
    f"Registros RFB carregados: "
    f"{len(df_rfb):,}"
)

log_dataframe(
    name="df_rfb",
    df=df_rfb,
    source=ARQ_CNPJ_RFB,
)

#%%
# Seleção de colunas relevantes
# ============================================================================

log_step(
    "Seleção de colunas relevantes",
)

info(
    "Selecionando colunas relevantes..."
)

COLUNAS_RFB = [
    "cd_cnpj",
    "nm_empresarial",
    "nm_fantasia",
    "ed_uf",
    "nm_regiao_politica",
    "nm_tipo_estabelecimento",
    "nm_situacao_cadastral",
    "cd_natureza_juridica",
    "nm_natureza_juridica",
    "nm_porte",
    "vl_capital_social",
    "cd_cnae",
    "nm_nivel1_secao",
    "nm_nivel2_divisao",
    "nm_nivel3_grupo",
    "nm_nivel4_classe",
    "nm_nivel5_subclasse",
    "dt_abertura",
]

df_rfb = df_rfb[
    COLUNAS_RFB
].copy()

success(
    "Colunas relevantes selecionadas."
)

info(
    f"Quantidade colunas: "
    f"{len(df_rfb.columns)}"
)

log_dataframe(
    name="df_rfb_reduzido",
    df=df_rfb,
    transformation="COLUMN_SELECTION",
)

#%%
# Conversões
# ============================================================================

log_step(
    "Conversões",
)

info(
    "Convertendo tipos..."
)

# -----------------------------------------------------------------------------
# Data abertura
# -----------------------------------------------------------------------------

df_rfb[
    "dt_abertura"
] = pd.to_datetime(
    df_rfb[
        "dt_abertura"
    ],
    format="%Y-%m-%d %H:%M:%S",
    errors="coerce",
)

qt_datas_validas = (
    df_rfb[
        "dt_abertura"
    ]
    .notna()
    .sum()
)

# -----------------------------------------------------------------------------
# Capital social
# -----------------------------------------------------------------------------

df_rfb[
    "vl_capital_social"
] = pd.to_numeric(
    df_rfb[
        "vl_capital_social"
    ],
    errors="coerce",
)

qt_capital_valido = (
    df_rfb[
        "vl_capital_social"
    ]
    .notna()
    .sum()
)

# -----------------------------------------------------------------------------
# Data referência
# -----------------------------------------------------------------------------

DT_REFERENCIA = pd.Timestamp(
    "2025-12-31"
)

success(
    "Conversões concluídas."
)

info(
    f"Datas válidas      : "
    f"{qt_datas_validas:,}"
)

info(
    f"Capital válido     : "
    f"{qt_capital_valido:,}"
)

info(
    f"Capital mínimo     : "
    f"R$ {df_rfb['vl_capital_social'].min():,.2f}"
)

info(
    f"Capital máximo     : "
    f"R$ {df_rfb['vl_capital_social'].max():,.2f}"
)

log_dataframe(
    name="df_rfb_convertido",
    df=df_rfb,
    transformation="TYPE_CONVERSION",
)

#%%
# Join enriquecimento
# ============================================================================

log_step(
    "Enriquecimento de CNPJs",
)

info(
    "Realizando join com base RFB..."
)

df_enriched = (
    df_cnpjs.merge(
        df_rfb,
        left_on="documento",
        right_on="cd_cnpj",
        how="left",
    )
)

qt_match = (
    df_enriched[
        "cd_cnpj"
    ]
    .notna()
    .sum()
)

pc_match = round(
    (
        qt_match
        / len(df_enriched)
    ) * 100,
    2,
)

success(
    "Join de enriquecimento concluído."
)

info(
    f"Matches encontrados : "
    f"{qt_match:,}"
)

info(
    f"Percentual match    : "
    f"{pc_match}%"
)

log_dataframe(
    name="df_enriched",
    df=df_enriched,
    transformation="RFB_ENRICHMENT_JOIN",
)

#%%
# Feature engineering
# ============================================================================

log_step(
    "Feature engineering",
)

info(
    "Criando features analíticas..."
)

# -----------------------------------------------------------------------------
# Idade empresa
# -----------------------------------------------------------------------------

df_enriched[
    "nr_idade_empresa"
] = (
    (
        DT_REFERENCIA
        - df_enriched[
            "dt_abertura"
        ]
    )
    .dt.days
    .div(365.25)
    .round(2)
)

# -----------------------------------------------------------------------------
# Faixas idade empresa
# -----------------------------------------------------------------------------

QT_BINS_IDADE = 5

bins_idade = pd.qcut(
    df_enriched[
        "nr_idade_empresa"
    ],
    q=QT_BINS_IDADE,
    duplicates="drop",
)

intervalos_idade = (
    bins_idade
    .cat
    .categories
)

labels_idade = []

for intervalo in intervalos_idade:

    inicio = round(
        intervalo.left
    )

    fim = round(
        intervalo.right
    )

    labels_idade.append(
        f"{inicio} ~ {fim} anos"
    )

df_enriched[
    "ds_faixa_idade_empresa"
] = pd.qcut(
    df_enriched[
        "nr_idade_empresa"
    ],
    q=QT_BINS_IDADE,
    labels=labels_idade,
    duplicates="drop",
)

# -----------------------------------------------------------------------------
# Capital social - bins logarítmicos
# -----------------------------------------------------------------------------

capital_min = (
    df_enriched[
        "vl_capital_social"
    ]
    .dropna()
    .loc[
        lambda s: s > 0
    ]
    .min()
)

capital_max = (
    df_enriched[
        "vl_capital_social"
    ]
    .dropna()
    .max()
)

QT_BINS_CAPITAL = 5

bins_capital = np.logspace(
    np.log10(
        max(capital_min, 1)
    ),
    np.log10(
        capital_max
    ),
    num=QT_BINS_CAPITAL + 1,
)

labels_capital = []

for i in range(
    len(bins_capital) - 1
):

    inicio = round(
        bins_capital[i]
    )

    fim = round(
        bins_capital[i + 1]
    )

    labels_capital.append(
        f"R$ {inicio:,.0f} ~ "
        f"R$ {fim:,.0f}"
    )

df_enriched[
    "ds_faixa_capital_social"
] = pd.cut(
    df_enriched[
        "vl_capital_social"
    ],
    bins=bins_capital,
    labels=labels_capital,
    include_lowest=True,
)

success(
    "Features criadas."
)

info(
    f"Quantidade bins idade   : "
    f"{len(labels_idade)}"
)

info(
    f"Quantidade bins capital : "
    f"{len(labels_capital)}"
)

info(
    "Labels idade empresa:"
)

for label in labels_idade:

    info(
        f"  - {label}"
    )

info(
    "Labels capital social:"
)

for label in labels_capital:

    info(
        f"  - {label}"
    )

log_dataframe(
    name="df_enriched_featured",
    df=df_enriched,
    transformation="FEATURE_ENGINEERING",
)

#%%
# Estatísticas enriquecimento
# ============================================================================

log_step(
    "Estatísticas do enriquecimento",
)

info(
    "Calculando estatísticas..."
)

qt_total = len(df_enriched)

qt_match = (
    df_enriched[
        "cd_cnpj"
    ]
    .notna()
    .sum()
)

pc_match = round(
    (qt_match / qt_total) * 100,
    2,
)

success(
    "Estatísticas calculadas."
)

info(
    "Resumo do enriquecimento"
)

info(
    f"Total registros : "
    f"{qt_total:,}"
)

info(
    f"Com match RFB   : "
    f"{qt_match:,}"
)

info(
    f"Percentual match: "
    f"{pc_match}%"
)

#%%
# Distribuições
# ============================================================================

log_step(
    "Distribuições",
)

info(
    "Gerando distribuições..."
)

# -----------------------------------------------------------------------------
# Distribuição idade empresa
# -----------------------------------------------------------------------------

dist_idade = (
    df_enriched[
        "ds_faixa_idade_empresa"
    ]
    .value_counts(
        dropna=False,
    )
    .to_frame(
        "quantidade"
    )
)

log_dataframe(
    name="dist_faixa_idade_empresa",
    df=dist_idade.reset_index(),
    transformation="VALUE_COUNTS",
)

# -----------------------------------------------------------------------------
# Distribuição capital social
# -----------------------------------------------------------------------------

dist_capital = (
    df_enriched[
        "ds_faixa_capital_social"
    ]
    .value_counts(
        dropna=False,
    )
    .to_frame(
        "quantidade"
    )
)

log_dataframe(
    name="dist_faixa_capital_social",
    df=dist_capital.reset_index(),
    transformation="VALUE_COUNTS",
)

success(
    "Distribuições geradas."
)

#%%
# Persistência
# ============================================================================

log_step(
    "Persistência",
)

info(
    "Persistindo arquivos..."
)

# -----------------------------------------------------------------------------
# Parquet
# -----------------------------------------------------------------------------

df_enriched.to_parquet(
    ARQ_CNPJ_ENRICHED_PARQUET,
    index=False,
)

success(
    "Parquet persistido."
)

info(
    f"Arquivo parquet: "
    f"{ARQ_CNPJ_ENRICHED_PARQUET}"
)

# -----------------------------------------------------------------------------
# CSV
# -----------------------------------------------------------------------------

df_enriched.to_csv(
    ARQ_CNPJ_ENRICHED_CSV,
    sep=";",
    encoding="utf-8",
    index=False,
)

success(
    "CSV persistido."
)

info(
    f"Arquivo CSV: "
    f"{ARQ_CNPJ_ENRICHED_CSV}"
)

info(
    f"Quantidade registros: "
    f"{len(df_enriched):,}"
)

info(
    f"Quantidade colunas : "
    f"{len(df_enriched.columns)}"
)

#%%
# Layout final
# ============================================================================

log_step(
    "Layout final",
)

layout_df = pd.DataFrame(
    {
        "coluna": df_enriched.columns,
        "dtype": [
            str(dtype)
            for dtype in df_enriched.dtypes
        ],
    }
)

log_dataframe(
    name="layout_final",
    df=layout_df,
    transformation="DATASET_SCHEMA",
)

log_dataframe(
    name="df_enriched_final",
    df=df_enriched,
    transformation="FINAL_FEATURE_LAYOUT",
)

info(
    f"Quantidade de colunas: "
    f"{len(df_enriched.columns)}"
)

info(
    f"Quantidade de registros: "
    f"{len(df_enriched):,}"
)

#%%
# Finalização
# ============================================================================

log_step(
    "Pipeline finalizada",
)

success(
    "Enriquecimento de CNPJs concluído."
)

#%%