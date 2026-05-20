#%%
# Imports
# ============================================================================

from pathlib import Path

import pandas as pd

from IPython.display import display

from transparencia_partidaria_br.utils.tse.tse_parser import (
    apply_date_parser,
    apply_number_parser,
    clean_cnpj,
    get_document_type,
    read_tse_csv,
    standardize_nulls,
    standardize_text_columns,
)


#%%
# Configurações
# ============================================================================

BASE_DIR = Path("../")

DATA_DIR = BASE_DIR / "data/01-raw/tse"

ARQ_RECEITA = DATA_DIR / "receita_anual_2025_BRASIL.csv"
ARQ_DESPESA = DATA_DIR / "despesa_anual_2025_BRASIL.csv"

OUTPUT_DIR = BASE_DIR / "data/02-silver"

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True,
)


#%%
# Leitura dos dados
# ============================================================================

print("=" * 80)
print("LEITURA DOS DADOS")
print("=" * 80)

print("\nLendo receita...")
df_receita = read_tse_csv(ARQ_RECEITA)

print("Lendo despesa...")
df_despesa = read_tse_csv(ARQ_DESPESA)

print("\nLeitura concluída.")


#%%
# Padronização inicial
# ============================================================================

print("=" * 80)
print("PADRONIZAÇÃO INICIAL")
print("=" * 80)

df_receita = standardize_nulls(df_receita)
df_despesa = standardize_nulls(df_despesa)

df_receita = standardize_text_columns(df_receita)
df_despesa = standardize_text_columns(df_despesa)

print("\nPadronização concluída.")


#%%
# Conversão de datas
# ============================================================================

print("=" * 80)
print("CONVERSÃO DE DATAS")
print("=" * 80)

df_receita = apply_date_parser(
    df_receita,
    columns=[
        "DT_RECEITA",
    ],
)

df_despesa = apply_date_parser(
    df_despesa,
    columns=[
        "DT_PAGAMENTO",
    ],
)

print("\nConversão de datas concluída.")


#%%
# Conversão monetária
# ============================================================================

print("=" * 80)
print("CONVERSÃO MONETÁRIA")
print("=" * 80)

df_receita = apply_number_parser(
    df_receita,
    columns=[
        "VR_RECEITA",
    ],
)

df_despesa = apply_number_parser(
    df_despesa,
    columns=[
        "VR_GASTO",
        "VR_PAGAMENTO",
        "VR_DOCUMENTO",
    ],
)

print("\nConversão monetária concluída.")


#%%
# Informações gerais
# ============================================================================

print("=" * 80)
print("INFORMAÇÕES GERAIS")
print("=" * 80)

print("\nRECEITA")
print("-" * 80)

print(f"Linhas : {len(df_receita):,}")
print(f"Colunas: {len(df_receita.columns):,}")

print("\nDESPESA")
print("-" * 80)

print(f"Linhas : {len(df_despesa):,}")
print(f"Colunas: {len(df_despesa.columns):,}")


#%%
# Amostras dos datasets
# ============================================================================

print("=" * 80)
print("AMOSTRAS DOS DATASETS")
print("=" * 80)

print("\nRECEITA")
print("-" * 80)

display(
    df_receita.head(5)
)

print("\nDESPESA")
print("-" * 80)

display(
    df_despesa.head(5)
)


#%%
# Extração de CNPJs - Receita
# ============================================================================

print("=" * 80)
print("EXTRAÇÃO DE CNPJs - RECEITA")
print("=" * 80)

cnpj_receita = (
    df_receita[
        [
            "SG_PARTIDO",
            "NM_PARTIDO",
            "cd_cpf_cnpj_doador",
            "NM_DOADOR",
            "VR_RECEITA",
            "DS_RECEITA",
        ]
    ]
    .copy()
)

cnpj_receita["documento"] = (
    cnpj_receita["cd_cpf_cnpj_doador"]
    .apply(clean_cnpj)
)

cnpj_receita["tipo_documento"] = (
    cnpj_receita["cd_cpf_cnpj_doador"]
    .apply(get_document_type)
)

cnpj_receita = cnpj_receita[
    cnpj_receita["tipo_documento"] == "CNPJ"
]

cnpj_receita["origem"] = "RECEITA"

cnpj_receita = cnpj_receita.rename(
    columns={
        "NM_DOADOR": "nome",
        "VR_RECEITA": "valor",
        "DS_RECEITA": "descricao",
    }
)

print(f"\nCNPJs receita: {len(cnpj_receita):,}")


#%%
# Extração de CNPJs - Despesa
# ============================================================================

print("=" * 80)
print("EXTRAÇÃO DE CNPJs - DESPESA")
print("=" * 80)

cnpj_despesa = (
    df_despesa[
        [
            "SG_PARTIDO",
            "NM_PARTIDO",
            "NR_CPF_CNPJ_FORNECEDOR",
            "NM_FORNECEDOR",
            "VR_GASTO",
            "DS_GASTO",
        ]
    ]
    .copy()
)

cnpj_despesa["documento"] = (
    cnpj_despesa["NR_CPF_CNPJ_FORNECEDOR"]
    .apply(clean_cnpj)
)

cnpj_despesa["tipo_documento"] = (
    cnpj_despesa["NR_CPF_CNPJ_FORNECEDOR"]
    .apply(get_document_type)
)

cnpj_despesa = cnpj_despesa[
    cnpj_despesa["tipo_documento"] == "CNPJ"
]

cnpj_despesa["origem"] = "DESPESA"

cnpj_despesa = cnpj_despesa.rename(
    columns={
        "NM_FORNECEDOR": "nome",
        "VR_GASTO": "valor",
        "DS_GASTO": "descricao",
    }
)

print(f"\nCNPJs despesa: {len(cnpj_despesa):,}")


#%%
# Consolidação dos CNPJs
# ============================================================================

print("=" * 80)
print("CONSOLIDAÇÃO DOS CNPJs")
print("=" * 80)

df_cnpjs = pd.concat(
    [
        cnpj_receita[
            [
                "documento",
                "nome",
                "origem",
                "valor",
                "SG_PARTIDO",
                "NM_PARTIDO",
                "descricao",
            ]
        ],
        cnpj_despesa[
            [
                "documento",
                "nome",
                "origem",
                "valor",
                "SG_PARTIDO",
                "NM_PARTIDO",
                "descricao",
            ]
        ],
    ],
    ignore_index=True,
)

print(f"\nTotal consolidado: {len(df_cnpjs):,}")


#%%
# Remoção de inválidos
# ============================================================================

print("=" * 80)
print("REMOÇÃO DE INVÁLIDOS")
print("=" * 80)

linhas_antes = len(df_cnpjs)

df_cnpjs = df_cnpjs.dropna(
    subset=["documento"]
)

linhas_depois = len(df_cnpjs)

print(f"\nAntes : {linhas_antes:,}")
print(f"Depois: {linhas_depois:,}")
print(f"Removidos: {linhas_antes - linhas_depois:,}")


#%%
# Agregação
# ============================================================================

print("=" * 80)
print("AGREGAÇÃO")
print("=" * 80)

df_cnpjs_agg = (
    df_cnpjs
    .groupby(
        [
            "documento",
            "nome",
            "origem",
        ],
        as_index=False,
    )
    .agg(
        qtd_operacoes=("documento", "count"),
        valor_total=("valor", "sum"),
        qtd_partidos=("SG_PARTIDO", "nunique"),
    )
)

print(f"\nRegistros agregados: {len(df_cnpjs_agg):,}")


#%%
# Ordenação
# ============================================================================

print("=" * 80)
print("ORDENAÇÃO")
print("=" * 80)

df_cnpjs_agg = df_cnpjs_agg.sort_values(
    by="valor_total",
    ascending=False,
)

print("\nOrdenação concluída.")


#%%
# Lista distinta de CNPJs
# ============================================================================

print("=" * 80)
print("LISTA DISTINTA DE CNPJs")
print("=" * 80)

df_cnpjs_distintos = (
    df_cnpjs_agg[
        ["documento"]
    ]
    .drop_duplicates()
    .rename(
        columns={
            "documento": "cnpj",
        }
    )
)

print(f"\nCNPJs distintos: {len(df_cnpjs_distintos):,}")


#%%
# Estatísticas
# ============================================================================

print("=" * 80)
print("ESTATÍSTICAS")
print("=" * 80)

print(f"\nCNPJs distintos: {len(df_cnpjs_distintos):,}")

print("\nTOP 10 CNPJs POR VALOR MOVIMENTADO")
print("-" * 80)

display(
    df_cnpjs_agg.head(10)
)


#%%
# Salvando outputs
# ============================================================================

print("=" * 80)
print("SALVANDO OUTPUTS")
print("=" * 80)

ARQ_CNPJS_AGG = OUTPUT_DIR / "cnpjs_agregados.parquet"

ARQ_CNPJS_DISTINTOS = OUTPUT_DIR / "cnpjs_distintos.csv"

ARQ_RECEITA_SILVER = OUTPUT_DIR / "receita_2025.parquet"

ARQ_DESPESA_SILVER = OUTPUT_DIR / "despesa_2025.parquet"

# ----------------------------------------------------------------------------
# CNPJs agregados
# ----------------------------------------------------------------------------

df_cnpjs_agg.to_parquet(
    ARQ_CNPJS_AGG,
    index=False,
)

print(f"\n[OK] {ARQ_CNPJS_AGG}")

# ----------------------------------------------------------------------------
# Lista distinta de CNPJs
# ----------------------------------------------------------------------------

df_cnpjs_distintos.to_csv(
    ARQ_CNPJS_DISTINTOS,
    index=False,
    encoding="utf-8",
)

print(f"[OK] {ARQ_CNPJS_DISTINTOS}")

# ----------------------------------------------------------------------------
# Silver layer
# ----------------------------------------------------------------------------

df_receita.to_parquet(
    ARQ_RECEITA_SILVER,
    index=False,
)

print(f"[OK] {ARQ_RECEITA_SILVER}")

df_despesa.to_parquet(
    ARQ_DESPESA_SILVER,
    index=False,
)

print(f"[OK] {ARQ_DESPESA_SILVER}")


#%%
# Finalização
# ============================================================================

print("=" * 80)
print("PROCESSAMENTO FINALIZADO")
print("=" * 80)

print("\nArquivos gerados com sucesso.")

print("\nRECEITA SILVER")
print("-" * 80)
print(ARQ_RECEITA_SILVER)

print("\nDESPESA SILVER")
print("-" * 80)
print(ARQ_DESPESA_SILVER)

print("\nCNPJs AGREGADOS")
print("-" * 80)
print(ARQ_CNPJS_AGG)

print("\nCNPJs DISTINTOS")
print("-" * 80)
print(ARQ_CNPJS_DISTINTOS)