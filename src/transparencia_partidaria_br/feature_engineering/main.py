from pathlib import Path

from transparencia_partidaria_br.feature_engineering.despesa import (
    aggregate_expense_party_year,
)

from transparencia_partidaria_br.feature_engineering.features import (
    create_financial_size_feature,
)

from transparencia_partidaria_br.feature_engineering.partido_ano import (
    create_incomplete_record_flag,
    create_party_year_percentage_features,
    create_party_year_ticket_features,
    fill_numeric_columns,
    merge_party_year_data,
    remove_invalid_party_year_records,
)

from transparencia_partidaria_br.feature_engineering.receita import (
    aggregate_revenue_party_year,
)

from transparencia_partidaria_br.utils.pipeline.logging import (
    log_pipeline_end,
    log_pipeline_start,
    success,
)

from transparencia_partidaria_br.utils.pipeline.pipeline_utils import (
    persist_dataset,
    process_dataframe,
    read_and_log_parquet,
)

# =============================================================================
# Paths
# =============================================================================

DATA_DIR = Path("data")

SILVER_DIR = DATA_DIR / "03-silver"

GOLD_DIR = DATA_DIR / "04-gold"

GOLD_DIR.mkdir(
    parents=True,
    exist_ok=True,
)

# =============================================================================
# Main
# =============================================================================


def main() -> None:
    """
    Pipeline principal feature engineering.
    """

    log_pipeline_start("FEATURE_ENGINEERING")

    # =========================================================================
    # Load silver enriquecido
    # =========================================================================

    df_receita = read_and_log_parquet(
        path=SILVER_DIR / "receita_enriquecida.parquet",
        dataframe_name="receita_enriquecida",
    )

    df_despesa = read_and_log_parquet(
        path=SILVER_DIR / "despesa_enriquecida.parquet",
        dataframe_name="despesa_enriquecida",
    )

    # =========================================================================
    # Receita agregada
    # =========================================================================

    df_partido_ano_receita = process_dataframe(
        df=df_receita,
        func=aggregate_revenue_party_year,
        dataframe_name="df_partido_ano_receita",
        operation="AGGREGATE_REVENUE_PARTY_YEAR",
    )

    persist_dataset(
        df=df_partido_ano_receita,
        path=GOLD_DIR / "partido_ano_receita.parquet",
        dataset_name="df_partido_ano_receita(partido ano receita)",
    )

    # =========================================================================
    # Despesa agregada
    # =========================================================================

    df_partido_ano_despesa = process_dataframe(
        df=df_despesa,
        func=aggregate_expense_party_year,
        dataframe_name="df_partido_ano_despesa",
        operation="AGGREGATE_EXPENSE_PARTY_YEAR",
    )

    persist_dataset(
        df=df_partido_ano_despesa,
        path=GOLD_DIR / "partido_ano_despesa.parquet",
        dataset_name="df_partido_ano_despesa(partido ano despesa)",
    )

    # =========================================================================
    # Merge partido-ano
    # =========================================================================

    df_partido_ano = merge_party_year_data(
        df_receita=df_partido_ano_receita,
        df_despesa=df_partido_ano_despesa,
    )

    # =========================================================================
    # Registros incompletos
    # =========================================================================

    df_partido_ano = process_dataframe(
        df=df_partido_ano,
        func=create_incomplete_record_flag,
        dataframe_name="df_partido_ano",
        operation="CREATE_INCOMPLETE_RECORD_FLAG",
    )

    df_partido_ano = (
        remove_invalid_party_year_records(
            df_partido_ano
        )
    )

    # =========================================================================
    # Fillna
    # =========================================================================

    df_partido_ano = process_dataframe(
        df=df_partido_ano,
        func=fill_numeric_columns,
        dataframe_name="df_partido_ano",
        operation="FILL_NUMERIC_COLUMNS",
    )

    # =========================================================================
    # Features percentuais
    # =========================================================================

    df_partido_ano = (
        create_party_year_percentage_features(
            df_partido_ano
        )
    )

    # =========================================================================
    # Features ticket médio
    # =========================================================================

    df_partido_ano = (
        create_party_year_ticket_features(
            df_partido_ano
        )
    )

    # =========================================================================
    # Porte financeiro
    # =========================================================================

    df_partido_ano = create_financial_size_feature(
        df_partido_ano
    )

    # =========================================================================
    # Persistência dataset final
    # =========================================================================

    persist_dataset(
        df=df_partido_ano,
        path=GOLD_DIR / "partido_ano.parquet",
        dataset_name="partido ano",
    )

    # =========================================================================
    # Finalização
    # =========================================================================

    success(
        "Feature engineering concluído | "
        f"receita={len(df_partido_ano_receita):,} | "
        f"despesa={len(df_partido_ano_despesa):,} | "
        f"partido_ano={len(df_partido_ano):,}"
    )

    log_pipeline_end("FEATURE_ENGINEERING")


# =============================================================================
# CLI
# =============================================================================

if __name__ == "__main__":

    main()