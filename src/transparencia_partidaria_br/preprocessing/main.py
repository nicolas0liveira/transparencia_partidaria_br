from pathlib import Path

import pandas as pd

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

from transparencia_partidaria_br.utils.pipeline.io import (
    read_parquet,
    write_parquet,
)

from transparencia_partidaria_br.utils.pipeline.logging import (
    info,
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

SILVER_DIR = (
    BASE_DIR / "data/03-silver"
)

SILVER_DIR.mkdir(
    parents=True,
    exist_ok=True,
)

# =============================================================================
# Arquivos bronze
# =============================================================================

ARQ_RECEITA_BRONZE = (
    BRONZE_DIR / "receita.parquet"
)

ARQ_DESPESA_BRONZE = (
    BRONZE_DIR / "despesa.parquet"
)

ARQ_CLASS_DESPESA_BRONZE = (
    BRONZE_DIR
    / "classificacao_despesa.parquet"
)

ARQ_CNPJ_BRONZE = (
    BRONZE_DIR / "cnpj.parquet"
)

# =============================================================================
# Arquivos silver
# =============================================================================

ARQ_RECEITA_SILVER = (
    SILVER_DIR / "receita.parquet"
)

ARQ_DESPESA_SILVER = (
    SILVER_DIR / "despesa.parquet"
)

ARQ_CLASS_DESPESA_SILVER = (
    SILVER_DIR
    / "classificacao_despesa.parquet"
)

ARQ_CNPJ_SILVER = (
    SILVER_DIR / "cnpj.parquet"
)




# =============================================================================
# Pipeline preprocessing
# =============================================================================


def run_preprocessing() -> None:
    """
    Executa pipeline preprocessing.

    Responsável por:
    - leitura bronze
    - limpeza
    - padronização
    - persistência silver
    """

    log_step(
        "Início preprocessing"
    )

    # =========================================================================
    # Load bronze
    # =========================================================================

    info(
        "Carregando datasets bronze..."
    )

    df_receita = read_parquet(
        ARQ_RECEITA_BRONZE
    )

    df_despesa = read_parquet(
        ARQ_DESPESA_BRONZE
    )

    df_cnpj = read_parquet(
        ARQ_CNPJ_BRONZE
    )

    df_aux = read_parquet(
        ARQ_CLASS_DESPESA_BRONZE
    )

    # =========================================================================
    # Preprocessing
    # =========================================================================

    info(
        "Preprocessando receita..."
    )

    df_receita = preprocess_receita(
        df_receita
    )

    info(
        "Salvando receita na camada silver.."
    )

    write_parquet(
        df_receita,
        ARQ_RECEITA_SILVER,
    )


    info(
        "receita processado ..."
    )

    # -------------------------------------------------------------------------

    info(
        "Preprocessando despesa..."
    )

    df_despesa = preprocess_despesa(
        df_despesa
    )

    info(
        "Salvando despesa na camada silver.."
    )

    write_parquet(
        df_despesa,
        ARQ_DESPESA_SILVER,
    )


    info(
        "despesa processado ..."
    )

    # -------------------------------------------------------------------------

    info(
        "Preprocessando CNPJ..."
    )

    df_cnpj = preprocess_cnpj(
        df_cnpj
    )

    info(
        "Salvando CNPJ na camada silver.."
    )

    write_parquet(
        df_cnpj,
        ARQ_CNPJ_SILVER,
    )

    info(
        "CNPJ processado ..."
    )

    # -------------------------------------------------------------------------

    info(
        "Preprocessando classificação despesa..."
    )

    df_aux = (
        preprocess_classificacao_despesa(
            df_aux
        )
    )

    info(
        "Salvando classificação despesa na camada silver.."
    )

    write_parquet(
        df_aux,
        ARQ_CLASS_DESPESA_SILVER,
    )

    info(
        "Classificação despesa processado ..."
    )

    # =========================================================================
    # Finalização
    # =========================================================================

    success(
        "Preprocessing concluído."
    )