from transparencia_partidaria_br.enrichment.main import (
    main as run_enrichment,
)

from transparencia_partidaria_br.enrichment.cnpj import (
    enrich_cnpj_data,
)

from transparencia_partidaria_br.enrichment.receita import (
    enrich_revenue_data,
)

from transparencia_partidaria_br.enrichment.despesa import (
    enrich_expense_data,
)

__all__ = [
    "run_enrichment",

    # CNPJ
    "enrich_cnpj_data",

    # Receita
    "enrich_revenue_data",

    # Despesa
    "enrich_expense_data",
]