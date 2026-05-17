import os
from pathlib import Path

CONFIG_PATH = Path.home() / ".tpbr.json"

CKAN_BASE_URLS = {
    "tse": os.getenv("CKAN_TSE_BASE_URL", "https://dadosabertos.tse.jus.br"),
    "dados_gov": os.getenv("CKAN_DADOS_GOV_BASE_URL", "https://dados.gov.br"),
    "dados_gov_df": os.getenv("CKAN_DADOS_GOV_BSB_BASE_URL", "https://dados.df.gov.br"),
    "ana": os.getenv("CKAN_ANA_BASE_URL", "https://dados.ana.gov.br"),
    "saude": os.getenv("CKAN_SAUDE_BASE_URL", "https://dados.saude.gov.br"),
}
