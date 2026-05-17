#%%
# Imports
# ============================================================================

from pathlib import Path

from transparencia_partidaria_br.utils.pipeline.logger import (
    log_step,
    success,
)

from transparencia_partidaria_br.utils.pipeline.parquet_utils import (
    export_ddl,
    export_schema,
    print_parquet_schema,
)

from transparencia_partidaria_br.utils.pipeline.pipeline_utils import (
    log_dataframe_preview,
    persist_dataframe,
    process_dataframe,
    read_and_log_csv,
)

from transparencia_partidaria_br.utils.pipeline.rules import (
    RULE_PARSE_DATE,
    RULE_PARSE_NUMBER,
    RULE_STANDARDIZE_NULLS,
    RULE_STANDARDIZE_TEXT,
)

from transparencia_partidaria_br.utils.tse.tse_parser import (
    apply_date_parser,
    apply_number_parser,
    read_tse_csv,
    standardize_nulls,
    standardize_text_columns,
)

#%%
# Configurações
# ============================================================================

BASE_DIR = Path("../")

RAW_DIR = (
    BASE_DIR / "data/01-raw/tse"
)

SILVER_DIR = (
    BASE_DIR / "data/02-silver"
)

SILVER_DIR.mkdir(
    parents=True,
    exist_ok=True,
)

# -----------------------------------------------------------------------------
# Entrada
# -----------------------------------------------------------------------------

ARQ_RECEITA = (
    RAW_DIR / "receita_anual_2025_BRASIL.csv"
)

ARQ_DESPESA = (
    RAW_DIR / "despesa_anual_2025_BRASIL.csv"
)

# -----------------------------------------------------------------------------
# Saída parquet
# -----------------------------------------------------------------------------

ARQ_RECEITA_SILVER = (
    SILVER_DIR / "01_receita_2025.parquet"
)

ARQ_DESPESA_SILVER = (
    SILVER_DIR / "01_despesa_2025.parquet"
)

# -----------------------------------------------------------------------------
# Saída CSV
# -----------------------------------------------------------------------------

ARQ_RECEITA_SILVER_CSV = (
    SILVER_DIR / "01_receita_2025.csv"
)

ARQ_DESPESA_SILVER_CSV = (
    SILVER_DIR / "01_despesa_2025.csv"
)

#%%
# Leitura dos arquivos
# ============================================================================

log_step(
    "Leitura dos arquivos TSE",
    notebook="01_ingestion_tse.py",
)

df_receita = read_and_log_csv(
    path=ARQ_RECEITA,
    dataframe_name="df_receita",
    read_func=read_tse_csv,
)

df_despesa = read_and_log_csv(
    path=ARQ_DESPESA,
    dataframe_name="df_despesa",
    read_func=read_tse_csv,
)

log_dataframe_preview(
    df=df_receita,
    title="Top 5 Receita",
)

log_dataframe_preview(
    df=df_despesa,
    title="Top 5 Despesa",
)

#%%
# Padronização de valores nulos
# ============================================================================

log_step(
    "Padronização de valores nulos",
)

df_receita = process_dataframe(
    df=df_receita,
    func=standardize_nulls,
    dataframe_name="df_receita",
    operation="STANDARDIZE_NULLS",
    rules=[
        RULE_STANDARDIZE_NULLS.REPLACE_NULO,
        RULE_STANDARDIZE_NULLS.REPLACE_EMPTY,
        RULE_STANDARDIZE_NULLS.NORMALIZE_NULLS,
    ],
)

df_despesa = process_dataframe(
    df=df_despesa,
    func=standardize_nulls,
    dataframe_name="df_despesa",
    operation="STANDARDIZE_NULLS",
    rules=[
        RULE_STANDARDIZE_NULLS.REPLACE_NULO,
        RULE_STANDARDIZE_NULLS.REPLACE_EMPTY,
        RULE_STANDARDIZE_NULLS.NORMALIZE_NULLS,
    ],
)

#%%
# Padronização textual
# ============================================================================

log_step(
    "Padronização textual",
)

df_receita = process_dataframe(
    df=df_receita,
    func=standardize_text_columns,
    dataframe_name="df_receita",
    operation="STANDARDIZE_TEXT_COLUMNS",
    rules=[
        RULE_STANDARDIZE_TEXT.TO_UPPERCASE,
        RULE_STANDARDIZE_TEXT.REMOVE_ACCENTS,
        RULE_STANDARDIZE_TEXT.REMOVE_EXTRA_SPACES,
        RULE_STANDARDIZE_TEXT.NORMALIZE_STRING,
    ],
)

df_despesa = process_dataframe(
    df=df_despesa,
    func=standardize_text_columns,
    dataframe_name="df_despesa",
    operation="STANDARDIZE_TEXT_COLUMNS",
    rules=[
        RULE_STANDARDIZE_TEXT.TO_UPPERCASE,
        RULE_STANDARDIZE_TEXT.REMOVE_ACCENTS,
        RULE_STANDARDIZE_TEXT.REMOVE_EXTRA_SPACES,
        RULE_STANDARDIZE_TEXT.NORMALIZE_STRING,
    ],
)

#%%
# Conversão de datas
# ============================================================================

log_step(
    "Conversão de datas",
)

df_receita = process_dataframe(
    df=df_receita,
    func=apply_date_parser,
    dataframe_name="df_receita",
    operation="APPLY_DATE_PARSER",
    rules=[
        RULE_PARSE_DATE.CONVERT_BRAZILIAN_DATE,
        RULE_PARSE_DATE.HANDLE_INVALID_DATE,
        RULE_PARSE_DATE.STANDARDIZE_DATETIME,
    ],
    columns=[
        "DT_RECEITA",
    ],
)

df_despesa = process_dataframe(
    df=df_despesa,
    func=apply_date_parser,
    dataframe_name="df_despesa",
    operation="APPLY_DATE_PARSER",
    rules=[
        RULE_PARSE_DATE.CONVERT_BRAZILIAN_DATE,
        RULE_PARSE_DATE.HANDLE_INVALID_DATE,
        RULE_PARSE_DATE.STANDARDIZE_DATETIME,
    ],
    columns=[
        "DT_PAGAMENTO",
    ],
)

#%%
# Conversão monetária
# ============================================================================

log_step(
    "Conversão monetária",
)

df_receita = process_dataframe(
    df=df_receita,
    func=apply_number_parser,
    dataframe_name="df_receita",
    operation="APPLY_NUMBER_PARSER",
    rules=[
        RULE_PARSE_NUMBER.REMOVE_THOUSAND_SEPARATOR,
        RULE_PARSE_NUMBER.CONVERT_DECIMAL,
        RULE_PARSE_NUMBER.CONVERT_FLOAT64,
    ],
    columns=[
        "VR_RECEITA",
    ],
)

df_despesa = process_dataframe(
    df=df_despesa,
    func=apply_number_parser,
    dataframe_name="df_despesa",
    operation="APPLY_NUMBER_PARSER",
    rules=[
        RULE_PARSE_NUMBER.REMOVE_THOUSAND_SEPARATOR,
        RULE_PARSE_NUMBER.CONVERT_DECIMAL,
        RULE_PARSE_NUMBER.CONVERT_FLOAT64,
    ],
    columns=[
        "VR_GASTO",
        "VR_PAGAMENTO",
        "VR_DOCUMENTO",
    ],
)

#%%
# Persistência silver
# ============================================================================

log_step(
    "Persistência silver",
)

persist_dataframe(
    df=df_receita,
    parquet_path=ARQ_RECEITA_SILVER,
    csv_path=ARQ_RECEITA_SILVER_CSV,
    dataframe_name="df_receita",
)

persist_dataframe(
    df=df_despesa,
    parquet_path=ARQ_DESPESA_SILVER,
    csv_path=ARQ_DESPESA_SILVER_CSV,
    dataframe_name="df_despesa",
)

#%%
# Schema parquet
# ============================================================================

log_step(
    "Schema parquet",
)

print_parquet_schema(
    ARQ_RECEITA_SILVER,
    title="Schema Receita",
)

print_parquet_schema(
    ARQ_DESPESA_SILVER,
    title="Schema Despesa",
)

#%%
# Exportação schemas e DDLs
# ============================================================================

log_step(
    "Exportação schemas e DDLs",
)

# -----------------------------------------------------------------------------
# Receita
# -----------------------------------------------------------------------------

export_schema(
    parquet_path=ARQ_RECEITA_SILVER,
    output_path=(
        SILVER_DIR / "receita_2025.schema.txt"
    ),
)

export_ddl(
    parquet_path=ARQ_RECEITA_SILVER,
    output_path=(
        SILVER_DIR / "receita_2025.ddl.parquet.sql"
    ),
    table_name="receita_2025",
)

# -----------------------------------------------------------------------------
# Despesa
# -----------------------------------------------------------------------------

export_schema(
    parquet_path=ARQ_DESPESA_SILVER,
    output_path=(
        SILVER_DIR / "despesa_2025.schema.txt"
    ),
)

export_ddl(
    parquet_path=ARQ_DESPESA_SILVER,
    output_path=(
        SILVER_DIR / "despesa_2025.ddl.parquet.sql"
    ),
    table_name="despesa_2025",
)

success(
    "Schemas e DDLs exportados."
)

#%%
# Finalização
# ============================================================================

log_step(
    "Pipeline finalizada",
)

success(
    "Pipeline executada com sucesso."
)

#%%