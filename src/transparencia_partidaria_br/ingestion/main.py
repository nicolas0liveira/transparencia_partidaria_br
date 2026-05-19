from transparencia_partidaria_br.ingestion.cnpj import (
    ingest_cnpj,
)

from transparencia_partidaria_br.ingestion.tse import (
    ingest_despesa,
    ingest_receita,
)

from transparencia_partidaria_br.ingestion.aux import (
    ingest_aux_classificacao_despesa,
)

from transparencia_partidaria_br.utils.pipeline.logging import (
    log_step,
    success,
)

# =============================================================================
# Pipeline ingestion
# =============================================================================


def run_ingestion() -> None:
    """
    Executa pipeline de ingestão.

    Responsável por:
    - carregar datasets externos
    - validar leitura inicial
    - disponibilizar dataframes brutos

    Não realiza:
    - preprocessing
    - enriquecimento
    - análise
    """

    log_step(
        "Início pipeline ingestion"
    )

    # -------------------------------------------------------------------------
    # TSE
    # -------------------------------------------------------------------------

    df_receita = ingest_receita()

    df_despesa = ingest_despesa()

    # -------------------------------------------------------------------------
    # Receita Federal
    # -------------------------------------------------------------------------

    df_cnpj = ingest_cnpj()

    # -------------------------------------------------------------------------
    # Auxiliares
    # -------------------------------------------------------------------------

    df_despesa_class = ingest_aux_classificacao_despesa()

    success(
        "Pipeline ingestion concluída."
    )
