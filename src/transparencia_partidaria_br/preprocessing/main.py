from pathlib import Path

from transparencia_partidaria_br.preprocessing.aux import (
    preprocess_classificacao_despesa,
)

from transparencia_partidaria_br.preprocessing.cnpj import (
    preprocess_cnpj,
)

from transparencia_partidaria_br.preprocessing.despesa import (
    preprocess_despesa,
)

from transparencia_partidaria_br.preprocessing.receita import (
    preprocess_receita,
)

from transparencia_partidaria_br.utils.pipeline.logging import (
    log_step,
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

BRONZE_DIR = DATA_DIR / "02-bronze"

SILVER_DIR = DATA_DIR / "03-silver"

SILVER_DIR.mkdir(
    parents=True,
    exist_ok=True,
)

# =============================================================================
# Pipeline preprocessing
# =============================================================================


def run_preprocessing() -> None:
    """
    Executa pipeline preprocessing.
    """

    log_step(
        "Início preprocessing"
    )

    datasets = [
        (
            "receita",
            preprocess_receita,
        ),
        (
            "despesa",
            preprocess_despesa,
        ),
        (
            "cnpj",
            preprocess_cnpj,
        ),
        (
            "classificacao_despesa",
            preprocess_classificacao_despesa,
        ),
    ]

    for dataset_name, preprocess_func in datasets:

        df = read_and_log_parquet(
            path=(
                BRONZE_DIR
                / f"{dataset_name}.parquet"
            ),
            dataframe_name=(
                f"{dataset_name}_bronze"
            ),
        )

        df = process_dataframe(
            df=df,
            func=preprocess_func,
            dataframe_name=dataset_name,
            operation=(
                f"PREPROCESS_{dataset_name.upper()}"
            ),
        )

        persist_dataset(
            df=df,
            path=(
                SILVER_DIR
                / f"{dataset_name}.parquet"
            ),
            dataset_name=(
                f"{dataset_name} silver"
            ),
        )

        del df

    success(
        "Preprocessing concluído."
    )