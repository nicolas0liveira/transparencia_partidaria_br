#%%
# ============================================================================
# EDA - DESPESAS PARTIDÁRIAS
# ============================================================================

"""
Análise exploratória de despesas partidárias.

Objetivos:
- entender distribuição das despesas
- avaliar concentração de gastos
- analisar perfil administrativo/finalístico
- gerar insumos para:
    - transparência
    - eficiência
    - clusterização
    - amostragem
    - análise multivariada

Base teórica:
- NBSA
- Estimadores tipo razão
- Estratificação
- Clusterização
"""

#%%
# Imports
# ============================================================================

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from IPython.display import display

from transparencia_partidaria_br.utils.pipeline.logging import (
    elapsed,
    info,
    log_dataframe,
    log_step,
    success,
    timer,
)

from transparencia_partidaria_br.utils.tse.tse_classify_utils import (
    summarize_categories,
    summarize_classification,
    summarize_financial_values,
    summarize_subcategories,
)

#%%
# Configurações
# ============================================================================

BASE_DIR = Path("../")

FEATURE_DIR = (
    BASE_DIR / "data/03-feature"
)

EDA_DIR = (
    BASE_DIR / "data/04-eda/despesa"
)

EDA_DIR.mkdir(
    parents=True,
    exist_ok=True,
)

ARQ_DESPESA = (
    FEATURE_DIR / "02_despesa_2025_feature.parquet"
)

#%%
# Configuração dinâmica de colunas
# ============================================================================

POSSIBLE_VALUE_COLUMNS = [
    "VR_PAGAMENTO_ABS",
    "VR_PAGAMENTO",
    "vr_despesa",
]

COLUNA_VALOR = next(
    (
        col
        for col in POSSIBLE_VALUE_COLUMNS
        if col in pd.read_parquet(
            ARQ_DESPESA,
            columns=None,
        ).columns
    ),
    None,
)

if COLUNA_VALOR is None:

    raise ValueError(
        (
            "Nenhuma coluna monetária "
            "foi encontrada."
        )
    )

#%%
# Funções de visualização
# ============================================================================

def salvar_dataframe(
    df: pd.DataFrame,
    nome_arquivo: str,
):
    """
    Salva dataframe em CSV.
    """

    caminho = (
        EDA_DIR / nome_arquivo
    )

    df.to_csv(
        caminho,
        sep=";",
        encoding="utf-8",
        index=True,
    )

    info(
        f"Arquivo salvo: {caminho}"
    )


def salvar_grafico(
    nome_arquivo: str,
):
    """
    Salva gráfico.
    """

    caminho = (
        EDA_DIR / nome_arquivo
    )

    plt.tight_layout()

    plt.savefig(
        caminho,
        dpi=300,
        bbox_inches="tight",
    )

    plt.close()

    info(
        f"Gráfico salvo: {caminho}"
    )


def plot_histogramas_numericos(
    df: pd.DataFrame,
):
    """
    Histogramas variáveis numéricas.
    """

    log_step(
        "Histogramas numéricos"
    )

    colunas_numericas = (
        df.select_dtypes(
            include=["number"]
        )
        .columns
        .tolist()
    )

    for coluna in colunas_numericas:

        serie = (
            df[coluna]
            .dropna()
        )

        if serie.empty:
            continue

        plt.figure(
            figsize=(10, 5)
        )

        serie.hist(
            bins=30
        )

        plt.title(
            f"Distribuição - {coluna}"
        )

        plt.xlabel(
            coluna
        )

        plt.ylabel(
            "Frequência"
        )

        salvar_grafico(
            f"hist_{coluna}.png"
        )


def plot_top_categorias(
    df: pd.DataFrame,
    coluna: str,
    top_n: int = 20,
):
    """
    Gráfico barras categorias.
    """

    if coluna not in df.columns:
        return

    serie = (
        df[coluna]
        .astype(str)
        .value_counts()
        .head(top_n)
    )

    if serie.empty:
        return

    plt.figure(
        figsize=(14, 6)
    )

    serie.plot(
        kind="bar"
    )

    plt.title(
        f"Top categorias - {coluna}"
    )

    plt.ylabel(
        "Frequência"
    )

    salvar_grafico(
        f"bar_{coluna}.png"
    )


def plot_correlacao(
    df: pd.DataFrame,
):
    """
    Heatmap simples correlação.
    """

    log_step(
        "Correlação"
    )

    colunas_numericas = (
        df.select_dtypes(
            include=["number"]
        )
        .columns
    )

    if len(colunas_numericas) < 2:
        return

    correlacao = (
        df[
            colunas_numericas
        ]
        .corr(
            numeric_only=True
        )
    )

    display(
        correlacao
    )

    salvar_dataframe(
        correlacao,
        "correlacao.csv",
    )

    plt.figure(
        figsize=(12, 10)
    )

    plt.imshow(
        correlacao,
        aspect="auto",
    )

    plt.colorbar()

    colunas_corr = list(
        correlacao.columns
    )

    plt.xticks(
        range(len(colunas_corr)),
        colunas_corr,
        rotation=90,
    )

    plt.yticks(
        range(len(colunas_corr)),
        colunas_corr,
    )

    plt.title(
        "Correlação"
    )

    salvar_grafico(
        "correlacao.png"
    )


def plot_classificacao_funcional(
    resumo: pd.DataFrame,
):
    """
    Gráfico classificação funcional.
    """

    plt.figure(
        figsize=(8, 5)
    )

    resumo.set_index(
        "classificacao"
    )["quantidade"].plot(
        kind="bar"
    )

    plt.title(
        "Classificação funcional"
    )

    plt.ylabel(
        "Quantidade"
    )

    salvar_grafico(
        "classificacao_funcional.png"
    )


def plot_ratio_financeiro(
    resumo: pd.DataFrame,
):
    """
    Distribuição financeira funcional.
    """

    plt.figure(
        figsize=(8, 5)
    )

    resumo.set_index(
        "DS_CLASSIFICACAO"
    )["sum"].plot(
        kind="bar"
    )

    plt.title(
        "Distribuição financeira"
    )

    plt.ylabel(
        "Valor total"
    )

    salvar_grafico(
        "ratio_financeiro.png"
    )


def plot_top_despesas(
    df: pd.DataFrame,
    coluna_valor: str,
    top_n: int = 20,
):
    """
    Top despesas.
    """

    if coluna_valor not in df.columns:
        return

    top_df = (
        df.sort_values(
            by=coluna_valor,
            ascending=False,
        )
        .head(top_n)
    )

    plt.figure(
        figsize=(14, 6)
    )

    top_df[
        coluna_valor
    ].plot(
        kind="bar"
    )

    plt.title(
        "Top despesas"
    )

    plt.ylabel(
        "Valor"
    )

    salvar_grafico(
        "top_despesas.png"
    )

#%%
# Leitura parquet
# ============================================================================

log_step(
    "Leitura parquet"
)

start = timer()

df_despesa = pd.read_parquet(
    ARQ_DESPESA
)

success(
    f"Arquivo carregado em {elapsed(start)}"
)

log_dataframe(
    name="df_despesa",
    df=df_despesa,
    source=ARQ_DESPESA,
)

display(
    df_despesa.shape
)

#%%
# Informações gerais
# ============================================================================

log_step(
    "Informações gerais"
)

display(
    df_despesa.info()
)

display(
    df_despesa.head()
)

#%%
# Estatísticas numéricas
# ============================================================================

log_step(
    "Estatísticas numéricas"
)

estatisticas = (
    df_despesa.describe(
        include="all"
    ).T
)

display(
    estatisticas
)

salvar_dataframe(
    estatisticas,
    "estatisticas.csv",
)

#%%
# Histogramas
# ============================================================================

plot_histogramas_numericos(
    df_despesa
)

#%%
# Classificação funcional
# ============================================================================

log_step(
    "Resumo funcional"
)

resumo_funcional = (
    summarize_classification(
        df_despesa,
        classification_column=(
            "DS_CLASSIFICACAO"
        ),
    )
)

display(
    resumo_funcional
)

salvar_dataframe(
    resumo_funcional,
    "classificacao_funcional.csv",
)

plot_classificacao_funcional(
    resumo_funcional
)

#%%
# Resumo categorias
# ============================================================================

log_step(
    "Resumo categorias"
)

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

salvar_dataframe(
    resumo_categoria,
    "categorias.csv",
)

#%%
# Resumo subcategorias
# ============================================================================

log_step(
    "Resumo subcategorias"
)

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

salvar_dataframe(
    resumo_subcategoria,
    "subcategorias.csv",
)

#%%
# Ratio financeiro
# ============================================================================

log_step(
    "Ratio financeiro"
)

ratio_financeiro = (
    summarize_financial_values(
        df_despesa,
        value_column=COLUNA_VALOR,
        classification_column=(
            "DS_CLASSIFICACAO"
        ),
    )
)

display(
    ratio_financeiro
)

salvar_dataframe(
    ratio_financeiro,
    "ratio_financeiro.csv",
)

plot_ratio_financeiro(
    ratio_financeiro
)

#%%
# Top despesas
# ============================================================================

plot_top_despesas(
    df_despesa,
    COLUNA_VALOR,
)

#%%
# Análise categórica
# ============================================================================

log_step(
    "Análise categórica"
)

colunas_categoricas = (
    df_despesa.select_dtypes(
        include=[
            "object",
            "category",
        ]
    )
    .columns
    .tolist()
)

for coluna in colunas_categoricas:

    frequencia = (
        df_despesa[coluna]
        .value_counts(
            dropna=False,
            normalize=True,
        )
        .mul(100)
        .round(2)
        .head(20)
        .rename("percentual")
        .to_frame()
    )

    display(
        frequencia
    )

    salvar_dataframe(
        frequencia,
        f"freq_{coluna}.csv",
    )

    plot_top_categorias(
        df_despesa,
        coluna,
    )

#%%
# Correlação
# ============================================================================

plot_correlacao(
    df_despesa
)

#%%
# Top partidos
# ============================================================================

log_step(
    "Top partidos"
)

possible_party_columns = [
    "SG_PARTIDO",
    "sg_partido",
]

party_column = next(
    (
        col
        for col in possible_party_columns
        if col in df_despesa.columns
    ),
    None,
)

if party_column is not None:

    resumo_partidos = (
        df_despesa.groupby(
            party_column
        )[COLUNA_VALOR]
        .agg(
            [
                "count",
                "sum",
                "mean",
            ]
        )
        .sort_values(
            by="sum",
            ascending=False,
        )
        .head(20)
    )

    display(
        resumo_partidos
    )

    salvar_dataframe(
        resumo_partidos,
        "top_partidos.csv",
    )

#%%
# Missing values
# ============================================================================

log_step(
    "Missing values"
)

missing = (
    df_despesa.isna()
    .sum()
    .sort_values(
        ascending=False
    )
    .to_frame(
        name="missing"
    )
)

missing["missing_pct"] = (
    (
        missing["missing"]
        / len(df_despesa)
    ) * 100
).round(2)

display(
    missing
)

salvar_dataframe(
    missing,
    "missing_values.csv",
)

#%%
# Finalização
# ============================================================================

log_step(
    "EDA finalizada"
)

success(
    "EDA despesa concluída com sucesso."
)

#%%