"""
Catálogo centralizado de regras e descrições da pipeline.

Objetivos:
- padronização textual
- reutilização
- internacionalização futura
- documentação metodológica
"""

from __future__ import annotations


# =============================================================================
# PADRONIZAÇÃO TEXTUAL
# =============================================================================

class RULE_STANDARDIZE_TEXT:

    TO_UPPERCASE = (
        "padronização textual em caixa alta"
    )

    REMOVE_ACCENTS = (
        "remoção de acentuação"
    )

    REMOVE_EXTRA_SPACES = (
        "remoção de espaços excedentes"
    )

    NORMALIZE_STRING = (
        "normalização de strings"
    )


# =============================================================================
# PADRONIZAÇÃO DE NULOS
# =============================================================================

class RULE_STANDARDIZE_NULLS:

    REPLACE_NULO = (
        'substituição de "#NULO#" por valores nulos'
    )

    REPLACE_EMPTY = (
        "substituição de strings vazias por nulos"
    )

    NORMALIZE_NULLS = (
        "padronização de valores ausentes"
    )


# =============================================================================
# PARSING NUMÉRICO
# =============================================================================

class RULE_PARSE_NUMBER:

    REMOVE_THOUSAND_SEPARATOR = (
        "remoção de separador de milhar"
    )

    CONVERT_DECIMAL = (
        "conversão de decimal brasileiro"
    )

    HANDLE_HALF_FORMAT = (
        'tratamento de valores no formato ",5"'
    )

    HANDLE_SMALL_DECIMAL = (
        'tratamento de valores no formato ",08"'
    )

    CONVERT_FLOAT64 = (
        "conversão para float64"
    )


# =============================================================================
# DATAS
# =============================================================================

class RULE_PARSE_DATE:

    CONVERT_BRAZILIAN_DATE = (
        "conversão de datas no padrão brasileiro"
    )

    HANDLE_INVALID_DATE = (
        "tratamento de datas inválidas"
    )

    STANDARDIZE_DATETIME = (
        "padronização datetime64"
    )


# =============================================================================
# CNPJ
# =============================================================================

class RULE_CNPJ:

    REMOVE_NON_DIGITS = (
        "remoção de caracteres não numéricos"
    )

    KEEP_VALID_CNPJ = (
        "manutenção apenas de CNPJs válidos"
    )

    STANDARDIZE_14_DIGITS = (
        "padronização de documentos com 14 dígitos"
    )


# =============================================================================
# AGREGAÇÃO
# =============================================================================

class RULE_GROUPBY:

    GROUP_BY_DOCUMENT = (
        "agrupamento por documento"
    )

    GROUP_BY_ORIGIN = (
        "agregação por origem da movimentação"
    )

    COUNT_OPERATIONS = (
        "cálculo de quantidade de operações"
    )

    SUM_VALUES = (
        "cálculo de valor total movimentado"
    )


# =============================================================================
# DEDUPLICAÇÃO
# =============================================================================

class RULE_DUPLICATES:

    DROP_DUPLICATES = (
        "remoção de registros duplicados"
    )

    KEEP_DISTINCT = (
        "manutenção apenas de valores distintos"
    )


# =============================================================================
# PERSISTÊNCIA
# =============================================================================

class RULE_WRITE_PARQUET:

    COLUMNAR_STORAGE = (
        "persistência em formato parquet"
    )

    ANALYTICAL_OPTIMIZATION = (
        "otimização para leitura analítica"
    )

    COMPRESSED_STORAGE = (
        "armazenamento colunar compactado"
    )


class RULE_WRITE_CSV:

    UTF8_ENCODING = (
        "persistência em formato CSV UTF-8"
    )


# =============================================================================
# CAMADA SILVER
# =============================================================================

class RULE_SILVER_LAYER:

    STANDARDIZE_TYPES = (
        "padronização de tipos"
    )

    REMOVE_TEXT_INCONSISTENCIES = (
        "remoção de inconsistências textuais"
    )

    HANDLE_MONETARY_VALUES = (
        "tratamento de valores monetários"
    )

    OPTIMIZED_STORAGE = (
        "persistência analítica otimizada"
    )