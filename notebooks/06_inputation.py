#%%
# Imports
# ============================================================================

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from IPython.display import display

from transparencia_partidaria_br.utils.pipeline.logger import (
    elapsed,
    info,
    log_dataframe,
    log_step,
    success,
    timer,
)


#%%
# Configurações
# ============================================================================

BASE_DIR = Path("../")

SILVER_DIR = (
    BASE_DIR / "data/02-silver"
)

EDA_DIR = (
    BASE_DIR / "data/03-eda"
)

EDA_DIR.mkdir(
    parents=True,
    exist_ok=True,
)

ARQ_RECEITA = (
    SILVER_DIR / "receita_2025.parquet"
)

ARQ_DESPESA = (
    SILVER_DIR / "despesa_2025.parquet"
)


#%%
# Funções auxiliares
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
        index=True,
        encoding="utf-8",
    )

    info(
        f"Arquivo salvo: {caminho}"
    )


def salvar_grafico(
    nome_arquivo: str,
):
    """
    Salva gráfico no diretório de EDA.
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


def analisar_variaveis_numericas(
    df: pd.DataFrame,
    nome_dataset: str,
):
    """
    Estatísticas descritivas para variáveis numéricas.
    """

    log_step(
        f"Análise numérica - {nome_dataset}"
    )

    colunas_numericas = (
        df.select_dtypes(
            include=["number"]
        )
        .columns
        .tolist()
    )

    if not colunas_numericas:
        info(
            "Nenhuma variável numérica encontrada."
        )
        return

    info(
        f"Variáveis numéricas encontradas: {len(colunas_numericas)}"
    )

    estatisticas = (
        df[colunas_numericas]
        .describe()
        .T
    )

    estatisticas["missing"] = (
        df[colunas_numericas]
        .isna()
        .sum()
    )

    estatisticas["missing_pct"] = (
        (
            estatisticas["missing"]
            / len(df)
        ) * 100
    ).round(2)

    display(
        estatisticas
    )

    salvar_dataframe(
        estatisticas,
        f"{nome_dataset}_estatisticas_numericas.csv",
    )

    # -------------------------------------------------------------------------
    # Histogramas
    # -------------------------------------------------------------------------

    for coluna in colunas_numericas:

        info(
            f"Gerando histograma: {coluna}"
        )

        plt.figure(
            figsize=(10, 5)
        )

        df[coluna].dropna().hist(
            bins=30
        )

        plt.title(
            f"{nome_dataset} - Distribuição de {coluna}"
        )

        plt.xlabel(
            coluna
        )

        plt.ylabel(
            "Frequência"
        )

        salvar_grafico(
            f"{nome_dataset}_hist_{coluna}.png"
        )

    # -------------------------------------------------------------------------
    # Correlação
    # -------------------------------------------------------------------------

    if len(colunas_numericas) > 1:

        correlacao = (
            df[colunas_numericas]
            .corr(numeric_only=True)
        )

        display(
            correlacao
        )

        salvar_dataframe(
            correlacao,
            f"{nome_dataset}_correlacao.csv",
        )

        plt.figure(
            figsize=(10, 8)
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
            f"{nome_dataset} - Correlação"
        )

        salvar_grafico(
            f"{nome_dataset}_correlacao.png"
        )


def analisar_variaveis_categoricas(
    df: pd.DataFrame,
    nome_dataset: str,
    top_n: int = 20,
):
    """
    Estatísticas para variáveis categóricas.
    """

    log_step(
        f"Análise categórica - {nome_dataset}"
    )

    colunas_categoricas = (
        df.select_dtypes(
            include=[
                "object",
                "category",
            ]
        )
        .columns
        .tolist()
    )

    if not colunas_categoricas:
        info(
            "Nenhuma variável categórica encontrada."
        )
        return

    info(
        f"Variáveis categóricas encontradas: {len(colunas_categoricas)}"
    )

    resumo = []

    for coluna in colunas_categoricas:

        info(
            f"Analisando variável: {coluna}"
        )

        qtd_missing = (
            df[coluna]
            .isna()
            .sum()
        )

        qtd_unicos = (
            df[coluna]
            .nunique()
        )

        resumo.append(
            {
                "coluna": coluna,
                "missing": qtd_missing,
                "missing_pct": round(
                    (qtd_missing / len(df)) * 100,
                    2,
                ),
                "valores_unicos": qtd_unicos,
            }
        )

        frequencia = (
            df[coluna]
            .value_counts(
                dropna=False,
                normalize=True,
            )
            .head(top_n)
            .mul(100)
            .round(2)
            .rename("percentual")
            .to_frame()
        )

        display(
            frequencia
        )

        salvar_dataframe(
            frequencia,
            f"{nome_dataset}_freq_{coluna}.csv",
        )

        # ---------------------------------------------------------------------
        # Gráfico
        # ---------------------------------------------------------------------

        serie_plot = (
            df[coluna]
            .dropna()
            .astype(str)
            .value_counts()
            .head(top_n)
        )

        if serie_plot.empty:

            info(
                f"Coluna {coluna} sem dados para gráfico."
            )

        else:

            plt.figure(
                figsize=(12, 5)
            )

            serie_plot.plot(
                kind="bar"
            )

            plt.title(
                f"{nome_dataset} - Top categorias - {coluna}"
            )

            plt.xlabel(
                coluna
            )

            plt.ylabel(
                "Frequência"
            )

            salvar_grafico(
                f"{nome_dataset}_bar_{coluna}.png"
            )

    resumo_df = pd.DataFrame(
        resumo
    )

    display(
        resumo_df
    )

    salvar_dataframe(
        resumo_df,
        f"{nome_dataset}_resumo_categoricas.csv",
    )


def analisar_proporcoes_financeiras(
    df: pd.DataFrame,
    nome_dataset: str,
):
    """
    Análises proporcionais para valores monetários.
    """

    log_step(
        f"Análise proporcional - {nome_dataset}"
    )

    colunas_numericas = (
        df.select_dtypes(
            include=["number"]
        )
        .columns
        .tolist()
    )

    for coluna in colunas_numericas:

        total = (
            df[coluna]
            .sum()
        )

        if total == 0:
            continue

        info(
            f"Analisando proporções de {coluna}"
        )

        # ---------------------------------------------------------------------
        # Top registros
        # ---------------------------------------------------------------------

        top_registros = (
            df[
                [coluna]
            ]
            .sort_values(
                by=coluna,
                ascending=False,
            )
            .head(20)
        )

        top_registros[
            "proporcao_pct"
        ] = (
            (
                top_registros[coluna]
                / total
            ) * 100
        ).round(4)

        display(
            top_registros
        )

        salvar_dataframe(
            top_registros,
            f"{nome_dataset}_top_{coluna}.csv",
        )


#%%
# Leitura dos arquivos parquet
# ============================================================================

log_step(
    "Leitura dos arquivos parquet"
)

start = timer()

info(
    "Lendo receita parquet..."
)

df_receita = pd.read_parquet(
    ARQ_RECEITA
)

info(
    "Lendo despesa parquet..."
)

df_despesa = pd.read_parquet(
    ARQ_DESPESA
)

success(
    f"Arquivos carregados em {elapsed(start)}"
)

log_dataframe(
    name="df_receita",
    df=df_receita,
    source=ARQ_RECEITA,
)

log_dataframe(
    name="df_despesa",
    df=df_despesa,
    source=ARQ_DESPESA,
)

print("\nShape Receita:")

display(
    df_receita.shape
)

print("\nShape Despesa:")

display(
    df_despesa.shape
)


#%%
# Informações gerais
# ============================================================================

log_step(
    "Informações gerais"
)

info(
    "Informações dataset receita"
)

display(
    df_receita.info()
)

info(
    "Informações dataset despesa"
)

display(
    df_despesa.info()
)


#%%
# Análise Receita
# ============================================================================

log_step(
    "EDA Receita"
)

analisar_variaveis_numericas(
    df_receita,
    "receita",
)

analisar_variaveis_categoricas(
    df_receita,
    "receita",
)

analisar_proporcoes_financeiras(
    df_receita,
    "receita",
)


#%%
# Análise Despesa
# ============================================================================

log_step(
    "EDA Despesa"
)

analisar_variaveis_numericas(
    df_despesa,
    "despesa",
)

analisar_variaveis_categoricas(
    df_despesa,
    "despesa",
)

analisar_proporcoes_financeiras(
    df_despesa,
    "despesa",
)


#%%
# Finalização
# ============================================================================

log_step(
    "EDA finalizada"
)

success(
    "Análise exploratória concluída com sucesso."
)

#%%