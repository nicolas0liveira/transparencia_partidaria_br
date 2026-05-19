from pathlib import Path

from transparencia_partidaria_br.ingestion import (
    ingest_cnpj,
    ingest_despesa,
    ingest_receita,
)

from transparencia_partidaria_br.preprocessing.aux import preprocess_classificacao_despesa
from transparencia_partidaria_br.preprocessing.cnpj import (
    preprocess_cnpj,
)

from transparencia_partidaria_br.preprocessing.despesa import (
    preprocess_despesa,
)

from transparencia_partidaria_br.preprocessing.receita import (
    preprocess_receita,
)

from transparencia_partidaria_br.utils.pipeline.io import (
    write_parquet,
)

from transparencia_partidaria_br.utils.pipeline.logging import (
    log_file_operation,
    log_step,
    success,
)

# =============================================================================
# Diretórios
# =============================================================================

BASE_DIR = Path(".")

BRONZE_DIR = (
    BASE_DIR / "data/02-bronze"
)

BRONZE_DIR.mkdir(
    parents=True,
    exist_ok=True,
)

# =============================================================================
# Arquivos
# =============================================================================

ARQ_RECEITA_BRONZE = (
    BRONZE_DIR / "receita.parquet"
)

ARQ_DESPESA_BRONZE = (
    BRONZE_DIR / "despesa.parquet"
)

ARQ_CLASS_DESPESA_BRONZE = (
    BRONZE_DIR / "classificacao_despesa.parquet"
)

ARQ_CNPJ_BRONZE = (
    BRONZE_DIR / "cnpj.parquet"
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

    # -------------------------------------------------------------------------
    # Ingestion
    # -------------------------------------------------------------------------

    df_receita = ingest_receita()

    df_despesa = ingest_despesa()

    df_cnpj = ingest_cnpj()

    # -------------------------------------------------------------------------
    # Preprocessing
    # -------------------------------------------------------------------------

    df_receita = preprocess_receita(
        df_receita
    )

    df_despesa = preprocess_despesa(
        df_despesa
    )

    df_cnpj = preprocess_cnpj(
        df_cnpj
    )

    df_aux = preprocess_classificacao_despesa(
        df_despesa
    )


    # -------------------------------------------------------------------------
    # Persistência bronze
    # -------------------------------------------------------------------------

    write_parquet(
        df_receita,
        ARQ_RECEITA_BRONZE,
    )

    log_file_operation(
        operation="WRITE_PARQUET",
        source="df_receita",
        target=ARQ_RECEITA_BRONZE,
    )

    write_parquet(
        df_despesa,
        ARQ_DESPESA_BRONZE,
    )

    log_file_operation(
        operation="WRITE_PARQUET",
        source="df_despesa",
        target=ARQ_DESPESA_BRONZE,
    )

    write_parquet(
        df_cnpj,
        ARQ_CNPJ_BRONZE,
    )

    log_file_operation(
        operation="WRITE_PARQUET",
        source="df_cnpj",
        target=ARQ_CNPJ_BRONZE,
    )

    write_parquet(
        df_aux,
        ARQ_CLASS_DESPESA_BRONZE,
    )

    log_file_operation(
        operation="WRITE_PARQUET",
        source="df_aux",
        target=ARQ_CLASS_DESPESA_BRONZE,
    )

    success(
        "Preprocessing concluído."
    )