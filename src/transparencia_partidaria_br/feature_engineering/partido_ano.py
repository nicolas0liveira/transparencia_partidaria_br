import pandas as pd

from transparencia_partidaria_br.feature_engineering.features import (
    create_financial_features,
    create_financial_size_feature,
)


def build_party_year_dataset(
    df_receita: pd.DataFrame,
    df_despesa: pd.DataFrame,
) -> pd.DataFrame:
    """
    Constrói dataset analítico partido-ano.
    """

    merge_keys = [
        "sg_partido",
        "aa_exercicio",
    ]

    df_partido_ano = df_receita.merge(
        df_despesa,
        on=merge_keys,
        how="outer",
    )

    # =========================================================================
    # Tratar colunas nulas
    # =========================================================================

    numeric_columns = [
        "vl_receita_total",
        "vl_despesa_total",
        "vl_despesa_administrativa",
        "qtd_receitas",
        "qtd_despesas",
    ]

    df_partido_ano[numeric_columns] = (
        df_partido_ano[numeric_columns]
        .fillna(0)
    )

    df_partido_ano["pct_despesa_administrativa"] = (
        df_partido_ano["vl_despesa_administrativa"]
        / df_partido_ano["vl_despesa_total"].replace(0, pd.NA)
    )

    df_partido_ano["ticket_medio_despesa"] = (
        df_partido_ano["vl_despesa_total"]
        / df_partido_ano["qtd_despesas"].replace(0, pd.NA)
    )

    # =========================================================================
    # Features financeiras
    # =========================================================================

    df_partido_ano = (
        create_financial_features(
            df_partido_ano
        )
    )

    # =========================================================================
    # Porte financeiro
    # =========================================================================

    df_partido_ano = (
        create_financial_size_feature(
            df_partido_ano
        )
    )

    return df_partido_ano