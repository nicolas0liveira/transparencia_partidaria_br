from pathlib import Path

from transparencia_partidaria_br.ingestion.aux import (
    ingest_aux_classificacao_despesa,
)

from transparencia_partidaria_br.ingestion.cnpj import (
    ingest_cnpj,
)

from transparencia_partidaria_br.ingestion.tse import (
    ingest_despesa,
    ingest_receita,
)

from transparencia_partidaria_br.utils.pipeline.logging import (
    log_step,
    success,
)

from transparencia_partidaria_br.utils.pipeline.pipeline_utils import (
    persist_dataset,
)

# =============================================================================
# Paths
# =============================================================================

DATA_DIR = Path("data")

BRONZE_DIR = DATA_DIR / "02-bronze"

BRONZE_DIR.mkdir(
    parents=True,
    exist_ok=True,
)

# =============================================================================
# Pipeline ingestion
# =============================================================================


def run_ingestion() -> None:
    """
    Executa pipeline de ingestão.
    """

    log_step(
        "Início pipeline ingestion"
    )

    datasets = [
        (
            ingest_receita,
            "receita.parquet",
            "receita bronze",
        ),
        (
            ingest_despesa,
            "despesa.parquet",
            "despesa bronze",
        ),
        (
            ingest_cnpj,
            "cnpj.parquet",
            "cnpj bronze",
        ),
        (
            ingest_aux_classificacao_despesa,
            "classificacao_despesa.parquet",
            "classificacao despesa bronze",
        ),
    ]

    for ingest_func, filename, dataset_name in datasets:

        df = ingest_func()

        persist_dataset(
            df=df,
            path=BRONZE_DIR / filename,
            dataset_name=dataset_name,
        )

        del df

    success(
        "Pipeline ingestion concluída."
    )