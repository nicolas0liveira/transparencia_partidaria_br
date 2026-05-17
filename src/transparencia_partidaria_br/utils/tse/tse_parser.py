"""
Utilitários para leitura e tratamento dos datasets do TSE.

Objetivos:
- leitura robusta de CSVs do TSE
- tratamento de encoding latin1
- padronização textual
- padronização de valores nulos
- normalização de CNPJ/CPF
- parsing robusto de números brasileiros
- tipagem consistente para análise posterior

Exemplos de problemas tratados:
- "#NULO#"
- ""
- ",5"
- ",08"
- "1.234,56"
- CNPJ com máscara
- colunas numéricas lidas como texto
- múltiplos espaços
- diferenças de caixa
- acentuação inconsistente
"""

from __future__ import annotations

import re
import unicodedata
from pathlib import Path
from typing import Any, Callable

import numpy as np
import pandas as pd


# =============================================================================
# CONSTANTES
# =============================================================================

NULL_VALUES = {
    "",
    "#NULO#",
    "NULL",
    "null",
    "None",
    "NONE",
}


# =============================================================================
# FUNÇÕES AUXILIARES
# =============================================================================

def is_null(value: Any) -> bool:
    """
    Verifica se um valor deve ser tratado como nulo.

    Parameters
    ----------
    value : Any
        Valor a ser validado.

    Returns
    -------
    bool
        True se o valor for considerado nulo.
    """

    if pd.isna(value):
        return True

    value_str = str(value).strip()

    return value_str in NULL_VALUES


def remove_accents(value: str) -> str:
    """
    Remove acentos unicode.

    Parameters
    ----------
    value : str

    Returns
    -------
    str
    """

    return "".join(
        char
        for char in unicodedata.normalize("NFKD", value)
        if not unicodedata.combining(char)
    )


def clean_string(
    value: Any,
    *,
    upper: bool = True,
    remove_accent: bool = True,
) -> str | None:
    """
    Limpa e padroniza strings.

    Regras:
    - trim
    - remove múltiplos espaços
    - uppercase opcional
    - remoção de acentos opcional
    - tratamento de nulos

    Parameters
    ----------
    value : Any
        Valor de entrada.

    upper : bool
        Converte texto para uppercase.

    remove_accent : bool
        Remove acentos unicode.

    Returns
    -------
    str | None
        Texto padronizado.
    """

    if is_null(value):
        return None

    value_str = str(value).strip()

    # remove múltiplos espaços
    value_str = re.sub(r"\s+", " ", value_str)

    if remove_accent:
        value_str = remove_accents(value_str)

    if upper:
        value_str = value_str.upper()

    return value_str


def only_digits(value: Any) -> str:
    """
    Remove tudo que não for dígito.

    Parameters
    ----------
    value : Any
        Valor de entrada.

    Returns
    -------
    str
        Apenas dígitos.
    """

    if is_null(value):
        return ""

    return re.sub(r"\D", "", str(value))


# =============================================================================
# DOCUMENTOS
# =============================================================================

def clean_cnpj(value: Any) -> str | None:
    """
    Normaliza CNPJ.

    Remove máscara e valida tamanho.

    Parameters
    ----------
    value : Any
        CNPJ de entrada.

    Returns
    -------
    str | None
        CNPJ com 14 dígitos ou None.
    """

    digits = only_digits(value)

    if len(digits) == 14:
        return digits

    return None


def clean_cpf(value: Any) -> str | None:
    """
    Normaliza CPF.

    Parameters
    ----------
    value : Any
        CPF de entrada.

    Returns
    -------
    str | None
        CPF com 11 dígitos ou None.
    """

    digits = only_digits(value)

    if len(digits) == 11:
        return digits

    return None


def get_document_type(value: Any) -> str | None:
    """
    Identifica tipo do documento.

    Parameters
    ----------
    value : Any

    Returns
    -------
    str | None
        CPF, CNPJ ou None.
    """

    digits = only_digits(value)

    if len(digits) == 11:
        return "CPF"

    if len(digits) == 14:
        return "CNPJ"

    return None


# =============================================================================
# PARSING NUMÉRICO
# =============================================================================

def parse_number(value: Any) -> float | None:
    """
    Converte números brasileiros para float.

    Casos suportados:
    - "123"
    - "123,45"
    - ",5"
    - ",08"
    - "1.234,56"

    Parameters
    ----------
    value : Any
        Valor de entrada.

    Returns
    -------
    float | None
        Número convertido.
    """

    if is_null(value):
        return None

    value_str = str(value).strip()

    # remove separador de milhar
    value_str = value_str.replace(".", "")

    # converte decimal brasileiro
    value_str = value_str.replace(",", ".")

    # ",5" -> "0.5"
    if value_str.startswith("."):
        value_str = f"0{value_str}"

    try:
        return float(value_str)

    except (ValueError, TypeError):
        return None


# =============================================================================
# DATAS
# =============================================================================

def parse_date(
    series: pd.Series,
    fmt: str = "%d/%m/%Y",
) -> pd.Series:
    """
    Converte datas do TSE.

    Parameters
    ----------
    series : pd.Series

    fmt : str
        Formato esperado.

    Returns
    -------
    pd.Series
    """

    return pd.to_datetime(
        series,
        format=fmt,
        errors="coerce",
    )


## =============================================================================
# LEITURA CSV
# =============================================================================

def read_tse_csv(
    path: str | Path,
    *,
    sep: str = ";",
    encoding: str = "latin1",
    low_memory: bool = False,
) -> pd.DataFrame:
    """
    Lê arquivos CSV do TSE com configuração robusta.
    """

    return pd.read_csv(
        path,
        sep=sep,
        encoding=encoding,
        dtype=str,
        keep_default_na=False,
        low_memory=low_memory,
    )


def read_tse_csv_chunks(
    path: str | Path,
    *,
    chunksize: int = 100_000,
    sep: str = ";",
    encoding: str = "latin1",
):
    """
    Lê CSV do TSE em chunks.

    Ideal para arquivos grandes.

    Parameters
    ----------
    path : str | Path

    chunksize : int

    Yields
    ------
    pd.DataFrame
    """

    yield from pd.read_csv(
        path,
        sep=sep,
        encoding=encoding,
        dtype=str,
        keep_default_na=False,
        chunksize=chunksize,
    )


# =============================================================================
# PADRONIZAÇÃO DATAFRAME
# =============================================================================

def standardize_nulls(df: pd.DataFrame) -> pd.DataFrame:
    """
    Padroniza valores nulos.

    Parameters
    ----------
    df : pd.DataFrame

    Returns
    -------
    pd.DataFrame
    """

    return df.replace(list(NULL_VALUES), np.nan)


def standardize_text_columns(
    df: pd.DataFrame,
    *,
    exclude: list[str] | None = None,
    upper: bool = True,
    remove_accent: bool = True,
) -> pd.DataFrame:
    """
    Padroniza colunas textuais.

    Regras:
    - trim
    - uppercase
    - remove acentos
    - remove múltiplos espaços

    Parameters
    ----------
    df : pd.DataFrame

    exclude : list[str] | None
        Colunas ignoradas.

    upper : bool

    remove_accent : bool

    Returns
    -------
    pd.DataFrame
    """

    exclude = exclude or []

    object_cols = df.select_dtypes(include=["object"]).columns

    for col in object_cols:

        if col in exclude:
            continue

        df[col] = df[col].apply(
            lambda value: clean_string(
                value,
                upper=upper,
                remove_accent=remove_accent,
            )
        )

    return df


def apply_number_parser(
    df: pd.DataFrame,
    columns: list[str],
) -> pd.DataFrame:
    """
    Aplica parse_number em múltiplas colunas.

    Parameters
    ----------
    df : pd.DataFrame

    columns : list[str]

    Returns
    -------
    pd.DataFrame
    """

    for col in columns:

        if col in df.columns:
            df[col] = df[col].apply(parse_number)

    return df


def apply_date_parser(
    df: pd.DataFrame,
    columns: list[str],
) -> pd.DataFrame:
    """
    Aplica parser de datas em múltiplas colunas.

    Parameters
    ----------
    df : pd.DataFrame

    columns : list[str]

    Returns
    -------
    pd.DataFrame
    """

    for col in columns:

        if col in df.columns:
            df[col] = parse_date(df[col])

    return df