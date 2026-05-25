import pandas as pd

from transparencia_partidaria_br.feature_engineering.features import (
    create_financial_size_feature,
)

from transparencia_partidaria_br.utils.pipeline.logging import (
    info,
)


def merge_party_year_data(
    df_receita: pd.DataFrame,
    df_despesa: pd.DataFrame,
) -> pd.DataFrame:
    """
    Realiza merge entre datasets agregados de receita e despesa.
    """

    merge_keys = [
        "sg_partido",
        "aa_exercicio",
    ]

    return df_receita.merge(
        df_despesa,
        on=merge_keys,
        how="outer",
    )


def create_incomplete_record_flag(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Cria flag para registros inválidos para inferência.
    """

    df["in_registro_incompleto"] = (
        df["vl_receita_total"].isna()
        | df["vl_despesa_total"].isna()
        | (df["vl_receita_total"] <= 0)
        | (df["vl_despesa_total"] <= 0)
    )

    return df


def remove_invalid_party_year_records(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Remove registros sem receita ou despesa válida.
    """

    df_invalidos = df[
        df["in_registro_incompleto"]
    ]

    qtd_registros_incompletos = len(df_invalidos)

    max_log_rows = 20

    ds_registros_incompletos = "\n".join(
        (
            f"{row.sg_partido} | "
            f"{row.aa_exercicio} | "
            f"receita={row.vl_receita_total} | "
            f"despesa={row.vl_despesa_total}"
        )
        for row in (
            df_invalidos
            .head(max_log_rows)
            .itertuples()
        )
    )

    info(
        f"Removidos {qtd_registros_incompletos} "
        "registros partido-ano sem receita "
        "ou despesa válida.\n"
        f"{ds_registros_incompletos}"
    )

    return (
        df[
            ~df["in_registro_incompleto"]
        ]
        .copy()
    )


def fill_numeric_columns(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Preenche colunas numéricas nulas.
    """

    numeric_columns = [
        "vl_receita_total",
        "vl_despesa_total",
        "vl_despesa_administrativa",
        "vl_despesa_finalistica",
        "vl_despesa_indefinida",
        "vl_receita_publica",
        "vl_receita_privada",
        "vl_receita_partidaria",
        "qtd_receitas",
        "qtd_despesas",
        "qtd_fornecedores",
    ]

    existing_numeric_columns = [
        column
        for column in numeric_columns
        if column in df.columns
    ]

    df[existing_numeric_columns] = (
        df[existing_numeric_columns]
        .fillna(0)
    )

    return df


def create_party_year_percentage_features(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Cria variáveis percentuais financeiras.
    """

    df["pct_despesa_administrativa"] = (
        df["vl_despesa_administrativa"]
        / df["vl_despesa_total"]
    )

    df["pct_despesa_finalistica"] = (
        df["vl_despesa_finalistica"]
        / df["vl_despesa_total"]
    )

    df["pct_despesa_indefinida"] = (
        df["vl_despesa_indefinida"]
        / df["vl_despesa_total"]
    )

    df["pct_receita_publica"] = (
        df["vl_receita_publica"]
        / df["vl_receita_total"]
    )

    df["pct_receita_privada"] = (
        df["vl_receita_privada"]
        / df["vl_receita_total"]
    )

    df["pct_receita_partidaria"] = (
        df["vl_receita_partidaria"]
        / df["vl_receita_total"]
    )

    return df


def create_party_year_ticket_features(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Cria métricas de ticket médio.
    """

    df["ticket_medio_despesa"] = (
        df["vl_despesa_total"]
        / df["qtd_despesas"]
    )

    return df
