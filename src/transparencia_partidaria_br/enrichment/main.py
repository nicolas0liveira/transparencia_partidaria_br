from pathlib import Path

from transparencia_partidaria_br.enrichment.despesa import (
    aggregate_expense_party_year,
    enrich_expense_data,
)

from transparencia_partidaria_br.enrichment.receita import (
    aggregate_revenue_party_year,
    enrich_revenue_data,
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
    Pipeline principal enrichment.
    """

    log_pipeline_start(
        "ENRICHMENT"
    )

    # =========================================================================
    # Load silver
    # =========================================================================

    df_receita = read_and_log_parquet(
        path=(
            SILVER_DIR
            / "receita.parquet"
        ),
        dataframe_name="receita",
    )

    df_despesa = read_and_log_parquet(
        path=(
            SILVER_DIR
            / "despesa.parquet"
        ),
        dataframe_name="despesa",
    )

    df_cnpj = read_and_log_parquet(
        path=(
            SILVER_DIR
            / "cnpj.parquet"
        ),
        dataframe_name="cnpj",
    )

    df_classificacao = (
        read_and_log_parquet(
            path=(
                SILVER_DIR
                / "classificacao_despesa.parquet"
            ),
            dataframe_name=(
                "classificacao_despesa"
            ),
        )
    )

    # =========================================================================
    # RECEITA
    # =========================================================================

    df_receita_enriquecida = (
        process_dataframe(
            df=df_receita,
            func=enrich_revenue_data,
            dataframe_name="receita",
            operation="ENRICH_REVENUE",
            df_cnpj=df_cnpj,
        )
    )

    persist_dataset(
        df=df_receita_enriquecida,
        path=(
            SILVER_DIR
            / "receita_enriquecida.parquet"
        ),
        dataset_name=(
            "receita enriquecida"
        ),
    )

    df_partido_ano_receita = (
        process_dataframe(
            df=df_receita_enriquecida,
            func=aggregate_revenue_party_year,
            dataframe_name="receita",
            operation=(
                "AGGREGATE_REVENUE_PARTY_YEAR"
            ),
        )
    )

    persist_dataset(
        df=df_partido_ano_receita,
        path=(
            GOLD_DIR
            / "partido_ano_receita.parquet"
        ),
        dataset_name=(
            "partido ano receita"
        ),
    )

    # =========================================================================
    # DESPESA
    # =========================================================================

    df_despesa_enriquecida = (
        process_dataframe(
            df=df_despesa,
            func=enrich_expense_data,
            dataframe_name="despesa",
            operation="ENRICH_EXPENSE",
            df_cnpj=df_cnpj,
            df_classificacao=df_classificacao,
        )
    )

    persist_dataset(
        df=df_despesa_enriquecida,
        path=(
            SILVER_DIR
            / "despesa_enriquecida.parquet"
        ),
        dataset_name=(
            "despesa enriquecida"
        ),
    )

    df_partido_ano_despesa = (
        process_dataframe(
            df=df_despesa_enriquecida,
            func=aggregate_expense_party_year,
            dataframe_name="despesa",
            operation=(
                "AGGREGATE_EXPENSE_PARTY_YEAR"
            ),
        )
    )

    persist_dataset(
        df=df_partido_ano_despesa,
        path=(
            GOLD_DIR
            / "partido_ano_despesa.parquet"
        ),
        dataset_name=(
            "partido ano despesa"
        ),
    )

    # =========================================================================
    # Finalização
    # =========================================================================

    success(
        (
            "Enrichment concluído | "
            f"receita={len(df_receita_enriquecida):,} | "
            f"despesa={len(df_despesa_enriquecida):,}"
        )
    )

    log_pipeline_end(
        "ENRICHMENT"
    )


# =============================================================================
# CLI
# =============================================================================

if __name__ == "__main__":

    main()