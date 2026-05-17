"""
Utilitários para arquivos parquet.

Objetivos:
- inspeção de schema parquet
- geração de DDL Hive/Impala
- documentação automática
- leitura do schema físico parquet
"""

from __future__ import annotations

from pathlib import Path

import pyarrow.parquet as pq


# =============================================================================
# MAPEAMENTO PYARROW -> SQL
# =============================================================================

PYARROW_TO_SQL = {
    "string": "STRING",
    "int64": "BIGINT",
    "int32": "INT",
    "double": "DOUBLE",
    "float": "FLOAT",
    "bool": "BOOLEAN",
    "timestamp[ns]": "TIMESTAMP",
    "binary": "STRING",
}


# =============================================================================
# HELPERS
# =============================================================================

def normalize_type(
    type_name: str,
) -> str:

    return str(type_name).lower()


def map_parquet_type(
    parquet_type: str,
) -> str:

    parquet_type = normalize_type(
        parquet_type,
    )

    return PYARROW_TO_SQL.get(
        parquet_type,
        "STRING",
    )


# =============================================================================
# LEITURA SCHEMA
# =============================================================================

def read_parquet_schema(
    parquet_path: str | Path,
):
    """
    Lê schema físico do parquet.
    """

    parquet_file = pq.ParquetFile(
        parquet_path,
    )

    return parquet_file.schema_arrow


def parquet_schema_to_list(
    parquet_path: str | Path,
) -> list[tuple[str, str]]:
    """
    Extrai schema parquet para lista.
    """

    schema = read_parquet_schema(
        parquet_path,
    )

    fields = []

    for field in schema:

        fields.append(
            (
                field.name,
                str(field.type),
            )
        )

    return fields


# =============================================================================
# PRINT
# =============================================================================

def print_parquet_schema(
    parquet_path: str | Path,
    *,
    title: str | None = None,
) -> None:
    """
    Exibe schema parquet.
    """

    schema = parquet_schema_to_list(
        parquet_path,
    )

    print("\n" + "=" * 100)

    if title:

        print(title.upper())

    else:

        print("PARQUET SCHEMA")

    print("=" * 100)

    for col, dtype in schema:

        print(
            f"{col:<45} {dtype}"
        )


# =============================================================================
# DDL
# =============================================================================

def generate_parquet_ddl(
    *,
    parquet_path: str | Path,
    table_name: str,
    schema: str = "default",
) -> str:
    """
    Gera DDL Hive/Impala baseada no parquet físico.
    """

    fields = parquet_schema_to_list(
        parquet_path,
    )

    columns = []

    for col, dtype in fields:

        sql_type = map_parquet_type(
            dtype,
        )

        columns.append(
            f"    {col} {sql_type}"
        )

    columns_sql = ",\n".join(columns)

    ddl = f"""
CREATE EXTERNAL TABLE IF NOT EXISTS {schema}.{table_name} (
{columns_sql}
)
STORED AS PARQUET
LOCATION '{parquet_path}'
TBLPROPERTIES (
    'parquet.compression'='SNAPPY',
    'serialization.encoding'='UTF-8'
);
""".strip()

    return ddl


# =============================================================================
# EXPORTAÇÃO
# =============================================================================

def export_schema(
    *,
    parquet_path: str | Path,
    output_path: str | Path,
) -> None:
    """
    Exporta schema parquet.
    """

    schema = parquet_schema_to_list(
        parquet_path,
    )

    with open(
        output_path,
        "w",
        encoding="utf-8",
    ) as f:

        for col, dtype in schema:

            f.write(
                f"{col:<45} {dtype}\n"
            )


def export_ddl(
    *,
    parquet_path: str | Path,
    output_path: str | Path,
    table_name: str,
    schema: str = "default",
) -> None:
    """
    Exporta DDL parquet.
    """

    ddl = generate_parquet_ddl(
        parquet_path=parquet_path,
        table_name=table_name,
        schema=schema,
    )

    with open(
        output_path,
        "w",
        encoding="utf-8",
    ) as f:

        f.write(ddl)

def write_parquet(
    df,
    output_path,
) -> None:
    """
    Escreve parquet compatível com Hive/Impala legados.
    """

    df.to_parquet(
        output_path,
        index=False,
        engine="pyarrow",
        compression="snappy",
        version="1.0",
    )