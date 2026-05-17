"""
Classificação simples de receitas/despesas TSE.

Estrutura:
- classificacao:
    - ADMINISTRATIVA
    - FINALISTICA
    - OUTROS

- categoria:
    - primeiro nível textual

- subcategoria:
    - segundo nível textual

Exemplo:

"PESSOAL - SALARIOS E ORDENADOS - ORDINARIAS"

-> classificacao:
   ADMINISTRATIVA

-> categoria:
   PESSOAL

-> subcategoria:
   SALARIOS E ORDENADOS
"""

from __future__ import annotations

from typing import Any

import pandas as pd

from .tse_parser import (
    clean_string,
    is_null,
)

# =============================================================================
# CONSTANTES
# =============================================================================

CLASSIFICACAO_ADMINISTRATIVA = (
    "ADMINISTRATIVA"
)

CLASSIFICACAO_FINALISTICA = (
    "FINALISTICA"
)

CLASSIFICACAO_OUTROS = (
    "OUTROS"
)

CATEGORIA_OUTROS = (
    "OUTROS"
)

SUBCATEGORIA_OUTROS = (
    "OUTROS"
)

# =============================================================================
# REGRAS
# =============================================================================

FINALISTICO_CATEGORIAS = {
    "PROPAGANDA E PUBLICIDADE",
    "PRODUCAO DE AUDIOVISUAIS",
    "PESQUISAS E TESTES DE OPINIAO PUBLICA",
    "FUNDACAO DE PESQUISA OU DE DOUTRINACAO E EDUCACAO POLITICA",
    "DOACOES PARA CAMPANHAS ELEITORAIS",
    "DOACOES/TRANSFERENCIAS PARA CAMPANHAS ELEITORAIS",
    "SOBRAS FINANCEIRAS DE CAMPANHA",
}

ADMINISTRATIVO_CATEGORIAS = {
    "PESSOAL",
    "SERVICOS TECNICO-PROFISSIONAIS",
    "ALUGUEIS E CONDOMINIOS",
    "DESPESAS JUDICIAIS",
    "DESPESAS FINANCEIRAS",
    "TRANSFERENCIAS FINANCEIRAS EFETUADAS",
    "TRANSFERENCIAS DE RECURSOS FINANCEIROS PARA MANUTENCAO DO PARTIDO",
    "TRANSFERENCIAS INTRAPARTIDARIAS DE ATIVO IMOBILIZADO OU MATERIAIS PARA DIVULGACAO/COMERCIALIZACAO",
    "TRANSFERENCIAS INTRAPARTIDARIAS DE RECURSOS ESTIMAVEIS EM DINHEIRO",
    "CONTRIBUICOES",
    "FUNDO PARTIDARIO",
    "GANHOS COM ATIVOS",
    "JUROS E OUTRAS RENDAS",
    "OBTENCAO DE RECURSOS POR MEIO DE EMPRESTIMOS BANCARIOS A PAGAR",
    "OUTRAS RECEITAS DIVERSAS",
    "RECUPERACAO DE DEPOSITOS RESTITUIVEIS E VALORES VINCULADOS",
    "RECURSOS DE ORIGEM NAO IDENTIFICADA",
    "RECURSOS RECEBIDOS DE FONTES VEDADAS",
    "REEMBOLSO DE ADIANTAMENTOS A FORNECEDORES",
    "REEMBOLSO DE OUTROS ADIANTAMENTOS DIVERSOS",
    "TRANSPORTES E VIAGENS",
    "RECOLHIMENTOS AO ERARIO",
}

# =============================================================================
# NORMALIZAÇÃO
# =============================================================================

def normalize_text(
    value: Any,
) -> str | None:
    """
    Normaliza texto.
    """

    if is_null(value):
        return None

    value = clean_string(value)

    if not value:
        return None

    return value

# =============================================================================
# PARSER
# =============================================================================

def split_category_subcategory(
    text: str,
) -> tuple[str, str]:
    """
    Extrai categoria/subcategoria.

    Estratégia:
    - categoria:
        primeiro bloco
    - subcategoria:
        segundo bloco
    """

    parts = [
        part.strip()
        for part in text.split(" - ")
        if part.strip()
    ]

    if not parts:

        return (
            CATEGORIA_OUTROS,
            SUBCATEGORIA_OUTROS,
        )

    categoria = parts[0]

    subcategoria = (
        parts[1]
        if len(parts) > 1
        else SUBCATEGORIA_OUTROS
    )

    return (
        categoria,
        subcategoria,
    )

# =============================================================================
# CLASSIFICAÇÃO FUNCIONAL
# =============================================================================

def classify_functional(
    categoria: str,
) -> str:
    """
    Classificação funcional simples.
    """

    if categoria in FINALISTICO_CATEGORIAS:

        return (
            CLASSIFICACAO_FINALISTICA
        )

    if categoria in ADMINISTRATIVO_CATEGORIAS:

        return (
            CLASSIFICACAO_ADMINISTRATIVA
        )

    return (
        CLASSIFICACAO_OUTROS
    )

# =============================================================================
# CLASSIFICAÇÃO
# =============================================================================

def classify_value(
    value: Any,
) -> dict[str, str]:
    """
    Classifica valor textual.

    Retorno:
    {
        "classificacao": ...,
        "categoria": ...,
        "subcategoria": ...,
    }
    """

    text = normalize_text(
        value
    )

    if text is None:

        return {
            "classificacao": (
                CLASSIFICACAO_OUTROS
            ),
            "categoria": (
                CATEGORIA_OUTROS
            ),
            "subcategoria": (
                SUBCATEGORIA_OUTROS
            ),
        }

    categoria, subcategoria = (
        split_category_subcategory(
            text
        )
    )

    classificacao = (
        classify_functional(
            categoria
        )
    )

    return {
        "classificacao": classificacao,
        "categoria": categoria,
        "subcategoria": subcategoria,
    }

# =============================================================================
# DATAFRAME
# =============================================================================

def apply_value_classification(
    df: pd.DataFrame,
    *,
    source_column: str,
    classification_column: str = (
        "ds_classificacao"
    ),
    category_column: str = (
        "ds_categoria"
    ),
    subcategory_column: str = (
        "ds_subcategoria"
    ),
) -> pd.DataFrame:
    """
    Aplica classificação
    em DataFrame.
    """

    if source_column not in df.columns:

        df[classification_column] = (
            CLASSIFICACAO_OUTROS
        )

        df[category_column] = (
            CATEGORIA_OUTROS
        )

        df[subcategory_column] = (
            SUBCATEGORIA_OUTROS
        )

        return df

    result = df[source_column].apply(
        classify_value
    )

    result_df = pd.DataFrame(
        result.tolist(),
        index=df.index,
    )

    df[classification_column] = (
        result_df["classificacao"]
    )

    df[category_column] = (
        result_df["categoria"]
    )

    df[subcategory_column] = (
        result_df["subcategoria"]
    )

    return df

# =============================================================================
# MÉTRICAS
# =============================================================================

def summarize_classification(
    df: pd.DataFrame,
    classification_column: str = (
        "ds_classificacao"
    ),
) -> pd.DataFrame:
    """
    Resume classificação funcional.
    """

    resumo = (
        df[classification_column]
        .value_counts(
            dropna=False,
        )
        .rename_axis(
            "classificacao"
        )
        .reset_index(
            name="quantidade"
        )
    )

    resumo["percentual"] = (
        (
            resumo["quantidade"]
            / resumo["quantidade"].sum()
        ) * 100
    ).round(2)

    return resumo


def summarize_categories(
    df: pd.DataFrame,
    category_column: str = (
        "ds_categoria"
    ),
) -> pd.DataFrame:
    """
    Resume categorias.
    """

    resumo = (
        df[category_column]
        .value_counts(
            dropna=False,
        )
        .rename_axis(
            "categoria"
        )
        .reset_index(
            name="quantidade"
        )
    )

    resumo["percentual"] = (
        (
            resumo["quantidade"]
            / resumo["quantidade"].sum()
        ) * 100
    ).round(2)

    return resumo


def summarize_subcategories(
    df: pd.DataFrame,
    category_column: str = (
        "ds_categoria"
    ),
    subcategory_column: str = (
        "ds_subcategoria"
    ),
) -> pd.DataFrame:
    """
    Resume categorias/subcategorias.
    """

    resumo = (
        df.groupby(
            [
                category_column,
                subcategory_column,
            ]
        )
        .size()
        .reset_index(
            name="quantidade"
        )
        .sort_values(
            [
                category_column,
                "quantidade",
            ],
            ascending=[
                True,
                False,
            ],
        )
    )

    return resumo


def summarize_financial_values(
    df: pd.DataFrame,
    value_column: str,
    classification_column: str = (
        "ds_classificacao"
    ),
) -> pd.DataFrame:
    """
    Resume valores financeiros
    por classificação.
    """

    resumo = (
        df.groupby(
            classification_column
        )[value_column]
        .agg(
            [
                "count",
                "sum",
                "mean",
                "median",
            ]
        )
        .reset_index()
    )

    total = (
        resumo["sum"]
        .sum()
    )

    resumo["proporcao_pct"] = (
        (
            resumo["sum"]
            / total
        ) * 100
    ).round(2)

    return resumo