#%%
# Imports
# ============================================================================

from pathlib import Path

from IPython.display import display

import pandas as pd

from transparencia_partidaria_br.utils.pipeline.logging import (
    elapsed,
    info,
    log_dataframe,
    log_file_operation,
    log_step,
    log_transformation,
    success,
    timer,
)

from transparencia_partidaria_br.utils.pipeline.rules import (
    RULE_CNPJ,
    RULE_DUPLICATES,
    RULE_GROUPBY,
    RULE_WRITE_PARQUET,
)

from transparencia_partidaria_br.utils.tse.tse_parser import (
    clean_cnpj,
)

from transparencia_partidaria_br.utils.pipeline.parquet_utils import (
    export_ddl,
    export_schema,
    print_parquet_schema,
    write_parquet,
)

#%%
# Configurações
# ============================================================================

BASE_DIR = Path("../")

SILVER_DIR = BASE_DIR / "data/02-silver"

ARQ_RECEITA = (
    SILVER_DIR / "01_receita_2025.parquet"
)

ARQ_DESPESA = (
    SILVER_DIR / "01_despesa_2025.parquet"
)

ARQ_CNPJS_AGG = (
    SILVER_DIR / "01a_cnpjs_agregados.parquet"
)

ARQ_CNPJS_DISTINTOS = (
    SILVER_DIR / "01a_cnpjs_distintos.parquet"
)


#%%
# Leitura parquet
# ============================================================================

log_step(
    "Leitura da camada silver",
    notebook="02_cnpj_extraction.py",
)

start = timer()

info("Lendo parquet de receita...")

df_receita = pd.read_parquet(
    ARQ_RECEITA,
)

success(
    f"Receita carregada em {elapsed(start)}"
)

log_dataframe(
    name="df_receita",
    df=df_receita,
    source=ARQ_RECEITA,
)

start = timer()

info("Lendo parquet de despesa...")

df_despesa = pd.read_parquet(
    ARQ_DESPESA,
)

success(
    f"Despesa carregada em {elapsed(start)}"
)

log_dataframe(
    name="df_despesa",
    df=df_despesa,
    source=ARQ_DESPESA,
)


#%%
# Extração de CNPJs da receita
# ============================================================================

log_step(
    "Extração de CNPJs da receita",
)

start = timer()

info("Extraindo CNPJs da receita...")

cnpj_receita = (
    df_receita[
        [
            "cd_cpf_cnpj_doador",
            "NM_DOADOR",
            "VR_RECEITA",
        ]
    ]
    .copy()
)

cnpj_receita["documento"] = (
    cnpj_receita["cd_cpf_cnpj_doador"]
    .apply(clean_cnpj)
)

success(
    f"CNPJs receita extraídos em {elapsed(start)}"
)

log_transformation(
    dataframe="cnpj_receita",
    operation="CLEAN_CNPJ",
    columns=["cd_cpf_cnpj_doador"],
    rules=[
        RULE_CNPJ.REMOVE_NON_DIGITS,
        RULE_CNPJ.KEEP_VALID_CNPJ,
        RULE_CNPJ.STANDARDIZE_14_DIGITS,
    ],
)

print("\nTop 5 receita:")

display(
    cnpj_receita.head()
)


#%%
# Extração de CNPJs da despesa
# ============================================================================

log_step(
    "Extração de CNPJs da despesa",
)

start = timer()

info("Extraindo CNPJs da despesa...")

cnpj_despesa = (
    df_despesa[
        [
            "NR_CPF_CNPJ_FORNECEDOR",
            "NM_FORNECEDOR",
            "VR_GASTO",
        ]
    ]
    .copy()
)

cnpj_despesa["documento"] = (
    cnpj_despesa["NR_CPF_CNPJ_FORNECEDOR"]
    .apply(clean_cnpj)
)

success(
    f"CNPJs despesa extraídos em {elapsed(start)}"
)

log_transformation(
    dataframe="cnpj_despesa",
    operation="CLEAN_CNPJ",
    columns=["NR_CPF_CNPJ_FORNECEDOR"],
    rules=[
        RULE_CNPJ.REMOVE_NON_DIGITS,
        RULE_CNPJ.KEEP_VALID_CNPJ,
        RULE_CNPJ.STANDARDIZE_14_DIGITS,
    ],
)

print("\nTop 5 despesa:")

display(
    cnpj_despesa.head()
)


#%%
# Consolidação
# ============================================================================

log_step(
    "Consolidação de CNPJs",
)

start = timer()

info("Consolidando datasets...")

df_cnpjs = pd.concat(
    [
        cnpj_receita[
            [
                "documento",
                "NM_DOADOR",
                "VR_RECEITA",
            ]
        ],
        cnpj_despesa[
            [
                "documento",
                "NM_FORNECEDOR",
                "VR_GASTO",
            ]
        ],
    ],
    ignore_index=True,
)

success(
    f"Consolidação concluída em {elapsed(start)}"
)

log_dataframe(
    name="df_cnpjs",
    df=df_cnpjs,
    transformation="CNPJ_CONSOLIDATION",
)


#%%
# Remoção de inválidos
# ============================================================================

log_step(
    "Remoção de documentos inválidos",
)

rows_before = len(df_cnpjs)

df_cnpjs = df_cnpjs.dropna(
    subset=["documento"],
)

rows_after = len(df_cnpjs)

log_transformation(
    dataframe="df_cnpjs",
    operation="DROP_NULL_DOCUMENTS",
    columns=["documento"],
    rows_before=rows_before,
    rows_after=rows_after,
    rules=[
        RULE_CNPJ.KEEP_VALID_CNPJ,
    ],
)

success(
    f"Removidos {rows_before - rows_after:,} registros inválidos"
)


#%%
# Agregação
# ============================================================================

log_step(
    "Agregação de CNPJs",
)

start = timer()

info("Realizando agregação...")

df_cnpjs_agg = (
    df_cnpjs
    .groupby(
        ["documento"],
        as_index=False,
    )
    .size()
)

success(
    f"Agregação concluída em {elapsed(start)}"
)

log_transformation(
    dataframe="df_cnpjs_agg",
    operation="GROUPBY_AGGREGATION",
    columns=["documento"],
    rules=[
        RULE_GROUPBY.GROUP_BY_DOCUMENT,
        RULE_GROUPBY.COUNT_OPERATIONS,
    ],
)

display(
    df_cnpjs_agg.head()
)


#%%
# Lista distinta
# ============================================================================

log_step(
    "Lista distinta de CNPJs",
)

df_cnpjs_distintos = (
    df_cnpjs_agg[
        ["documento"]
    ]
    .drop_duplicates()
)

log_transformation(
    dataframe="df_cnpjs_distintos",
    operation="DROP_DUPLICATES",
    columns=["documento"],
    rules=[
        RULE_DUPLICATES.DROP_DUPLICATES,
        RULE_DUPLICATES.KEEP_DISTINCT,
    ],
)

print(
    f"\nCNPJs distintos: {len(df_cnpjs_distintos):,}"
)


#%%
# Persistência
# ============================================================================

log_step(
    "Persistência da camada de CNPJs",
)

start = timer()

info("Persistindo parquet...")

write_parquet(
    df_cnpjs_agg,
    ARQ_CNPJS_AGG
)

write_parquet(
    df_cnpjs_distintos,
    ARQ_CNPJS_DISTINTOS
)

success(
    f"Persistência concluída em {elapsed(start)}"
)

log_file_operation(
    operation="WRITE_PARQUET",
    target=ARQ_CNPJS_AGG,
)

log_file_operation(
    operation="WRITE_PARQUET",
    target=ARQ_CNPJS_DISTINTOS,
)

log_transformation(
    dataframe="df_cnpjs",
    operation="WRITE_PARQUET",
    rules=[
        RULE_WRITE_PARQUET.COLUMNAR_STORAGE,
        RULE_WRITE_PARQUET.ANALYTICAL_OPTIMIZATION,
    ],
)

success(
    "Pipeline de CNPJs finalizada com sucesso."
)

#%%
# Schema parquet
# ============================================================================

log_step(
    "Schema parquet de CNPJs",
)

print_parquet_schema(
    ARQ_CNPJS_AGG,
    title="Schema CNPJs Agregados",
)

print_parquet_schema(
    ARQ_CNPJS_DISTINTOS,
    title="Schema CNPJs Distintos",
)

#%%
# Exportação de schemas e DDLs
# ============================================================================

log_step(
    "Exportação de schemas e DDLs",
)

# -----------------------------------------------------------------------------
# CNPJs agregados
# -----------------------------------------------------------------------------

info(
    "Exportando schema de CNPJs agregados..."
)

export_schema(
    parquet_path=ARQ_CNPJS_AGG,
    output_path=(
        SILVER_DIR
        / "cnpjs_agregados.schema.txt"
    ),
)

info(
    "Exportando DDL de CNPJs agregados..."
)

export_ddl(
    parquet_path=ARQ_CNPJS_AGG,
    output_path=(
        SILVER_DIR
        / "cnpjs_agregados.ddl.parquet.sql"
    ),
    table_name="cnpjs_agregados",
)

# -----------------------------------------------------------------------------
# CNPJs distintos
# -----------------------------------------------------------------------------

info(
    "Exportando schema de CNPJs distintos..."
)

export_schema(
    parquet_path=ARQ_CNPJS_DISTINTOS,
    output_path=(
        SILVER_DIR
        / "cnpjs_distintos.schema.txt"
    ),
)

info(
    "Exportando DDL de CNPJs distintos..."
)

export_ddl(
    parquet_path=ARQ_CNPJS_DISTINTOS,
    output_path=(
        SILVER_DIR
        / "cnpjs_distintos.ddl.parquet.sql"
    ),
    table_name="cnpjs_distintos",
)

success(
    "Schemas e DDLs exportados com sucesso."
)