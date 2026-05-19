from pathlib import Path

import pandas as pd

from transparencia_partidaria_br.enrichment.receita import (
    aggregate_revenue_party_year,
    enrich_revenue_data,
)

from transparencia_partidaria_br.utils.pipeline.logging import (
    info,
    success,
    log_pipeline_start,
    log_pipeline_end,
)

# =============================================================================
# Paths
# =============================================================================

DATA_DIR = Path("data")

BRONZE_DIR = (
    DATA_DIR / "02-bronze"
)

SILVER_DIR = (
    DATA_DIR / "03-silver"
)

GOLD_DIR = (
    DATA_DIR / "04-gold"
)

# =============================================================================
# Main
# =============================================================================


def main() -> None:
    """
    Pipeline principal de enrichment.
    """

    log_pipeline_start(
        "ENRICHMENT_RECEITA"
    )

    # -------------------------------------------------------------------------
    # Criação diretórios
    # -------------------------------------------------------------------------

    SILVER_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    GOLD_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    # -------------------------------------------------------------------------
    # Load bronze
    # -------------------------------------------------------------------------

    info(
        "Carregando datasets bronze..."
    )

    df_receita = pd.read_parquet(
        BRONZE_DIR / "receita.parquet"
    )

    df_cnpj = pd.read_parquet(
        BRONZE_DIR / "cnpj.parquet"
    )

    # -------------------------------------------------------------------------
    # Info bronze datasets
    # -------------------------------------------------------------------------
    info(
        f"Receita shape: {df_receita.shape}"
    )

    info(
        f"CNPJ shape: {df_cnpj.shape}"
    )


    # -------------------------------------------------------------------------
    # Receita enriquecida
    # -------------------------------------------------------------------------

    info(
        "Enriquecendo receitas..."
    )

    df_receita_enriquecida = (
        enrich_revenue_data(
            df_receita=df_receita,
            df_cnpj=df_cnpj,
        )
    )

    # -------------------------------------------------------------------------
    # Save silver
    # -------------------------------------------------------------------------

    silver_path = (
        SILVER_DIR
        / "receita_enriquecida.parquet"
    )

    df_receita_enriquecida.to_parquet(
        silver_path,
        index=False,
    )

    success(
        (
            "Receita enriquecida salva em:\n"
            f"{silver_path}"
        )
    )

    # -------------------------------------------------------------------------
    # Agregação gold
    # -------------------------------------------------------------------------

    info(
        "Gerando dataset partido_ano..."
    )

    df_partido_ano = (
        aggregate_revenue_party_year(
            df_receita_enriquecida
        )
    )

    # -------------------------------------------------------------------------
    # Save gold
    # -------------------------------------------------------------------------

    gold_path = (
        GOLD_DIR
        / "partido_ano_receita.parquet"
    )

    df_partido_ano.to_parquet(
        gold_path,
        index=False,
    )

    success(
        (
            "Dataset analítico salvo em:\n"
            f"{gold_path}"
        )
    )

    # -------------------------------------------------------------------------
    # Métricas
    # -------------------------------------------------------------------------

    info(
        (
            f"Receitas enriquecidas: "
            f"{len(df_receita_enriquecida):,}"
        )
    )

    info(
        (
            f"Partidos agregados: "
            f"{len(df_partido_ano):,}"
        )
    )

    log_pipeline_end(
        "ENRICHMENT_RECEITA"
    )


# =============================================================================
# CLI
# =============================================================================

if __name__ == "__main__":
    main()