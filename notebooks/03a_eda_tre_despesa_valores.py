#%%
# ============================================================================
# EDA - ANÁLISE DE VALORES DAS DESPESAS
# ============================================================================

"""
Análise exploratória focada nos valores monetários
das despesas partidárias.

Objetivos:
- analisar concentração financeira
- identificar padrões de gasto
- avaliar distribuição:
    - por fonte
    - por tipo
    - por descrição de gasto
- apoiar:
    - transparência
    - eficiência
    - análise multivariada
    - clusterização
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

from transparencia_partidaria_br.utils.pipeline.pipeline_utils import (
    export_dataframe_csv,
    salvar_plot,
)

#%%
# Configurações
# ============================================================================

BASE_DIR = Path("../")

FEATURE_DIR = (
    BASE_DIR / "data/03-feature"
)

EDA_DIR = (
    BASE_DIR / "data/04-eda/despesa_valores"
)

EDA_DIR.mkdir(
    parents=True,
    exist_ok=True,
)

ARQ_DESPESA = (
    FEATURE_DIR / "despesa_2025_feature.parquet"
)

#%%
# Colunas
# ============================================================================

COLUNAS_VALORES = [
    "VR_GASTO",
    "VR_PAGAMENTO",
    "VR_DOCUMENTO",
]

COLUNAS_AGRUPAMENTO = [
    "DS_FONTE_DESPESA",
    "TP_DESPESA",
    "DS_GASTO",
]

#%%
# Funções auxiliares
# ============================================================================

def salvar_dataframe(
    df: pd.DataFrame,
    nome_arquivo: str,
):
    """
    Salva dataframe CSV.
    """

    caminho = (
        EDA_DIR / nome_arquivo
    )

    export_dataframe_csv(
        df=df,
        output_path=caminho,
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

    salvar_plot(
        output_path=caminho,
        dpi=300,
    )

    info(
        f"Gráfico salvo: {caminho}"
    )


def gerar_analise_agrupada(
    df: pd.DataFrame,
    coluna_grupo: str,
    coluna_valor: str,
):
    """
    Gera análise agregada.
    """

    if coluna_grupo not in df.columns:
        return

    if coluna_valor not in df.columns:
        return

    log_step(
        f"Agrupamento: {coluna_grupo} x {coluna_valor}"
    )

    resumo = (
        df.groupby(
            coluna_grupo
        )[coluna_valor]
        .agg(
            [
                "count",
                "sum",
                "mean",
                "median",
                "std",
                "min",
                "max",
            ]
        )
        .sort_values(
            by="sum",
            ascending=False,
        )
    )

    resumo["proporcao_pct"] = (
        (
            resumo["sum"]
            / resumo["sum"].sum()
        ) * 100
    ).round(2)

    display(
        resumo.head(20)
    )

    salvar_dataframe(
        resumo,
        (
            f"{coluna_grupo.lower()}_"
            f"{coluna_valor.lower()}.csv"
        ),
    )

    # -------------------------------------------------------------------------
    # Gráfico
    # -------------------------------------------------------------------------

    top_df = resumo.head(20)

    plt.figure(
        figsize=(14, 6)
    )

    top_df["sum"].plot(
        kind="bar"
    )

    plt.title(
        (
            f"{coluna_valor} por "
            f"{coluna_grupo}"
        )
    )

    plt.ylabel(
        "Valor total"
    )

    plt.xlabel(
        coluna_grupo
    )

    salvar_grafico(
        (
            f"{coluna_grupo.lower()}_"
            f"{coluna_valor.lower()}.png"
        ),
    )


def gerar_distribuicao_categorica(
    df: pd.DataFrame,
    coluna: str,
    top_n: int = 20,
):
    """
    Gera distribuição categórica
    para variáveis textuais.
    """

    if coluna not in df.columns:
        return

    log_step(
        f"Distribuição categórica: {coluna}"
    )

    distribuicao = (
        df[coluna]
        .fillna("NAO_INFORMADO")
        .value_counts(dropna=False)
        .head(top_n)
        .to_frame(name="quantidade")
    )

    distribuicao["proporcao_pct"] = (
        (
            distribuicao["quantidade"]
            / distribuicao["quantidade"].sum()
        ) * 100
    ).round(2)

    display(
        distribuicao
    )

    salvar_dataframe(
        distribuicao,
        f"distribuicao_{coluna.lower()}.csv",
    )

    # -------------------------------------------------------------------------
    # Gráfico
    # -------------------------------------------------------------------------

    plt.figure(
        figsize=(14, 6)
    )

    distribuicao["quantidade"].plot(
        kind="bar"
    )

    plt.title(
        f"Distribuição - {coluna}"
    )

    plt.ylabel(
        "Quantidade"
    )

    plt.xlabel(
        coluna
    )

    salvar_grafico(
        f"distribuicao_{coluna.lower()}.png"
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
    df_despesa.head()
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
    df_despesa.shape
)

#%%
# Estatísticas monetárias
# ============================================================================

log_step(
    "Estatísticas monetárias"
)

estatisticas = (
    df_despesa[
        COLUNAS_VALORES
    ]
    .describe()
    .T
)

estatisticas["missing"] = (
    df_despesa[
        COLUNAS_VALORES
    ]
    .isna()
    .sum()
)

estatisticas["missing_pct"] = (
    (
        estatisticas["missing"]
        / len(df_despesa)
    ) * 100
).round(2)

display(
    estatisticas
)

salvar_dataframe(
    estatisticas,
    "estatisticas_valores.csv",
)

#%%
# Histogramas
# ============================================================================

log_step(
    "Histogramas"
)

for coluna in COLUNAS_VALORES:

    serie = (
        df_despesa[coluna]
        .dropna()
    )

    if serie.empty:
        continue

    plt.figure(
        figsize=(10, 5)
    )

    serie.hist(
        bins=50
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
        f"hist_{coluna.lower()}.png"
    )

#%%
# Distribuições categóricas
# ============================================================================

log_step(
    "Distribuições categóricas"
)

for coluna in COLUNAS_AGRUPAMENTO:

    gerar_distribuicao_categorica(
        df=df_despesa,
        coluna=coluna,
        top_n=20,
    )

#%%
# Análises agrupadas
# ============================================================================

for coluna_grupo in COLUNAS_AGRUPAMENTO:

    for coluna_valor in COLUNAS_VALORES:

        gerar_analise_agrupada(
            df=df_despesa,
            coluna_grupo=coluna_grupo,
            coluna_valor=coluna_valor,
        )

#%%
# Correlação monetária
# ============================================================================

log_step(
    "Correlação monetária"
)

correlacao = (
    df_despesa[
        COLUNAS_VALORES
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
    "correlacao_valores.csv",
)

plt.figure(
    figsize=(8, 6)
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
    "Correlação monetária"
)

salvar_grafico(
    "correlacao_valores.png"
)

#%%
# Top registros financeiros
# ============================================================================

log_step(
    "Top registros financeiros"
)

for coluna in COLUNAS_VALORES:

    top_df = (
        df_despesa.sort_values(
            by=coluna,
            ascending=False,
        )
        .head(50)
    )

    display(
        top_df.head(10)
    )

    salvar_dataframe(
        top_df,
        f"top_{coluna.lower()}.csv",
    )

#%%
# Finalização
# ============================================================================

log_step(
    "EDA finalizada"
)

success(
    "EDA de valores concluída."
)

#%%