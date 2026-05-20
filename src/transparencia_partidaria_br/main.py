from transparencia_partidaria_br.enrichment import (
    run_enrichment,
)

from transparencia_partidaria_br.ingestion import (
    run_ingestion,
)

from transparencia_partidaria_br.preprocessing import (
    run_preprocessing,
)

from transparencia_partidaria_br.utils.pipeline.logging import (
    exception,
    log_pipeline_end,
    log_pipeline_start,
    log_step,
    success,
)

# =============================================================================
# Pipeline principal
# =============================================================================


def main() -> None:
    """
    Executa pipeline principal do projeto.
    """

    pipeline_name = (
        "transparencia_partidaria_br"
    )

    log_pipeline_start(
        pipeline_name
    )

    try:

        # ---------------------------------------------------------------------
        # Ingestion
        # ---------------------------------------------------------------------

        log_step(
            "INGESTION"
        )

        run_ingestion()

        success(
            "Ingestion finalizada."
        )

        # ---------------------------------------------------------------------
        # Preprocessing
        # ---------------------------------------------------------------------

        log_step(
            "PREPROCESSING"
        )

        run_preprocessing()

        success(
            "Preprocessing finalizado."
        )

        # # ---------------------------------------------------------------------
        # # Enrichment
        # # ---------------------------------------------------------------------

        # log_step(
        #     "ENRICHMENT"
        # )

        # run_enrichment()

        # success(
        #     "Enrichment finalizado."
        # )

        # ---------------------------------------------------------------------
        # Pipeline end
        # ---------------------------------------------------------------------

        log_pipeline_end(
            pipeline_name
        )

    except Exception as exc:

        exception(
            "Erro pipeline principal",
            error=exc,
        )

        raise


# =============================================================================
# Entrypoint
# =============================================================================

if __name__ == "__main__":

    main()