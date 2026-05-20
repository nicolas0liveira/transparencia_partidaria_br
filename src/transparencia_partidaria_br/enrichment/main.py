from pathlib import Path

import pandas as pd

from transparencia_partidaria_br.enrichment.receita import (
    aggregate_revenue_party_year,
    enrich_revenue_data,
)

from transparencia_partidaria_br.enrichment.despesa import (
    aggregate_expense_party_year,
    enrich_expense_data,
)

from transparencia_partidaria_br.utils.pipeline.logging import (
    info,
    log_pipeline_end,
    log_pipeline_start,
    success,
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
    Pipeline principal enrichment.
    """

    log_pipeline_start(
        "ENRICHMENT"
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

    df_cnpj = pd.read_parquet(
        BRONZE_DIR / "cnpj.parquet"
    )

    df_receita = pd.read_parquet(
        BRONZE_DIR / "receita.parquet"
    )

    df_despesa = pd.read_parquet(
        BRONZE_DIR / "despesa.parquet"
    )

    df_classificacao_despesa = pd.read_parquet(
        BRONZE_DIR / "classificacao_despesa.parquet"
    )

    # -------------------------------------------------------------------------
    # Info bronze datasets
    # -------------------------------------------------------------------------

    info(
        f"CNPJ shape: "
        f"{df_cnpj.shape}"
    )

    info(
        f"Receita shape: "
        f"{df_receita.shape}"
    )

    info(
        f"Despesa shape: "
        f"{df_despesa.shape}"
    )

    info(
        f"Classificação Despesa shape: "
        f"{df_classificacao_despesa.shape}"
    )

    # =========================================================================
    # RECEITA
    # =========================================================================

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
    # Save silver receita
    # -------------------------------------------------------------------------

    receita_silver_path = (
        SILVER_DIR
        / "receita_enriquecida.parquet"
    )

    df_receita_enriquecida.to_parquet(
        receita_silver_path,
        index=False,
    )

    success(
        (
            "Receita enriquecida salva em:\n"
            f"{receita_silver_path}"
        )
    )

    # -------------------------------------------------------------------------
    # Receita gold
    # -------------------------------------------------------------------------

    info(
        "Gerando dataset receita partido_ano..."
    )

    df_partido_ano_receita = (
        aggregate_revenue_party_year(
            df_receita_enriquecida
        )
    )

    # -------------------------------------------------------------------------
    # Save gold receita
    # -------------------------------------------------------------------------

    receita_gold_path = (
        GOLD_DIR
        / "partido_ano_receita.parquet"
    )

    df_partido_ano_receita.to_parquet(
        receita_gold_path,
        index=False,
    )

    success(
        (
            "Dataset receita salvo em:\n"
            f"{receita_gold_path}"
        )
    )

    # =========================================================================
    # DESPESA
    # =========================================================================

    info(
        "Enriquecendo despesas..."
    )

    df_despesa_enriquecida = (
        enrich_expense_data(
            df_despesa=df_despesa,
            df_cnpj=df_cnpj,
            df_classificacao=df_classificacao_despesa,
        )
    )

    # -------------------------------------------------------------------------
    # Save silver despesa
    # -------------------------------------------------------------------------

    despesa_silver_path = (
        SILVER_DIR
        / "despesa_enriquecida.parquet"
    )

    df_despesa_enriquecida.to_parquet(
        despesa_silver_path,
        index=False,
    )

    success(
        (
            "Despesa enriquecida salva em:\n"
            f"{despesa_silver_path}"
        )
    )

    # -------------------------------------------------------------------------
    # Despesa gold
    # -------------------------------------------------------------------------

    info(
        "Gerando dataset despesa partido_ano..."
    )

    df_partido_ano_despesa = (
        aggregate_expense_party_year(
            df_despesa_enriquecida
        )
    )

    # -------------------------------------------------------------------------
    # Save gold despesa
    # -------------------------------------------------------------------------

    despesa_gold_path = (
        GOLD_DIR
        / "partido_ano_despesa.parquet"
    )

    df_partido_ano_despesa.to_parquet(
        despesa_gold_path,
        index=False,
    )

    success(
        (
            "Dataset despesa salvo em:\n"
            f"{despesa_gold_path}"
        )
    )

    # =========================================================================
    # Métricas finais
    # =========================================================================

    info(
        (
            f"Receitas enriquecidas: "
            f"{len(df_receita_enriquecida):,}"
        )
    )

    info(
        (
            f"Despesas enriquecidas: "
            f"{len(df_despesa_enriquecida):,}"
        )
    )

    info(
        (
            f"Partidos agregados receita: "
            f"{len(df_partido_ano_receita):,}"
        )
    )

    info(
        (
            f"Partidos agregados despesa: "
            f"{len(df_partido_ano_despesa):,}"
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