from pathlib import Path

from transparencia_partidaria_br.feature_engineering.partido_ano import (
    build_party_year_dataset,
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

    log_pipeline_start(
        "FEATURE_ENGINEERING"
    )

    # =========================================================================
    # Load gold
    # =========================================================================

    df_partido_ano_receita = (
        read_and_log_parquet(
            path=(
                GOLD_DIR
                / "partido_ano_receita.parquet"
            ),
            dataframe_name=(
                "partido_ano_receita"
            ),
        )
    )

    df_partido_ano_despesa = (
        read_and_log_parquet(
            path=(
                GOLD_DIR
                / "partido_ano_despesa.parquet"
            ),
            dataframe_name=(
                "partido_ano_despesa"
            ),
        )
    )

    # =========================================================================
    # PARTIDO ANO
    # =========================================================================

    df_partido_ano = (
        process_dataframe(
            df=df_partido_ano_receita,
            func=build_party_year_dataset,
            dataframe_name="partido_ano",
            operation=(
                "BUILD_PARTY_YEAR_DATASET"
            ),
            df_despesa=(
                df_partido_ano_despesa
            ),
        )
    )

    persist_dataset(
        df=df_partido_ano,
        path=(
            GOLD_DIR
            / "partido_ano.parquet"
        ),
        dataset_name=(
            "partido ano"
        ),
    )

    # =========================================================================
    # Finalização
    # =========================================================================

    success(
        (
            "Feature engineering concluído | "
            f"partido_ano={len(df_partido_ano):,}"
        )
    )

    log_pipeline_end(
        "FEATURE_ENGINEERING"
    )


# =============================================================================
# CLI
# =============================================================================

if __name__ == "__main__":

    main()