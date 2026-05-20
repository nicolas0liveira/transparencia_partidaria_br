from transparencia_partidaria_br.enrichment.main import (
    main as run_enrichment,
)

from transparencia_partidaria_br.enrichment.cnpj import (
    enrich_cnpj_data,
)

from transparencia_partidaria_br.enrichment.receita import (
    aggregate_revenue_party_year,
    enrich_revenue_data,
)

from transparencia_partidaria_br.enrichment.despesa import (
    aggregate_expense_party_year,
    enrich_expense_data,
)

__all__ = [
    "run_enrichment",

    # CNPJ
    "enrich_cnpj_data",

    # Receita
    "aggregate_revenue_party_year",
    "enrich_revenue_data",

    # Despesa
    "aggregate_expense_party_year",
    "enrich_expense_data",
]