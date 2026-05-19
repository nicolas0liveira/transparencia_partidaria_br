# Padronização de Código

## Objetivos

O código deste projeto deve priorizar:

- simplicidade
- legibilidade
- reprodutibilidade
- facilidade de manutenção
- clareza estatística

Evitar:

- overengineering
- abstrações desnecessárias
- orientação a objetos excessiva
- pipelines mágicos

---

## Convenções Gerais

### Linguagem

- Python 3.13

### Formatação

- ruff
- PEP8

### Tipagem

Utilizar:

- type hints
- pandas typing quando possível

---

## Nomeação

### Utilizar

- snake_case
- nomes explícitos
- nomes em português para regras de negócio
- nomes em inglês para componentes técnicos reutilizáveis

---

## DataFrames

Sempre:

- normalizar nomes de colunas
- remover acentos
- converter para snake_case
- evitar espaços

Exemplo:

NM_PARTIDO -> nm_partido

| Tipo               | Prefixo |
| ------------------ | ------- |
| percentual         | `pct_*` |
| valor monetário    | `vl_*`  |
| quantidade         | `qtd_*` |
| indicador booleano | `in_*`  |
| índice             | `idx_*` |
| código             | `cd_*`  |
| sigla              | `sg_*`  |
| nome textual       | `nm_*`  |
| número             | `nr_*`  |
| data               | `dt_*`  |

Observar:

```text
nr_* = quantitativo numérico
cd_* = identificador/código

logo cpnj deve ser tratado como cd_cnpj, por exemplo
```

---

## Persistência

Preferir:

- parquet
- CSV

---

## Funções

Priorizar:

- funções pequenas
- funções puras
- responsabilidades únicas
- funcao para logging das transofrmações
- funções para reaproveitamento da geração de imagens e tabelas

Evitar:

- funções acima de ~80 linhas
- funções com múltiplas responsabilidades

---

## Logging

Transformações importantes devem possuir logging.
Salve todas as transformações aplicadas em log/pipeline.log

Exemplo:

```python
log_dataframe(
    name="despesas_refined",
    df=df,
    source="trusted",
    transformation="classificacao_financeira"
)
```

## Notebooks

Notebooks devem:

- ser objetivos
- possuir hipóteses claras
- evitar código duplicado

Mover para src/:

- lógica reutilizável
- regras de negócio
- transformações complexas
