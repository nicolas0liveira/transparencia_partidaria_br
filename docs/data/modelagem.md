# Modelagem de Dados

## Entidades Principais Básicas

- receita_tse: cada linha representa uma receita declarada
- despesa_tse: cada linha representa uma despesa declarada
- cnpj: representa um estabelecimento

## Relacionamentos

- Receita -> CNPJ: `cd_cpf_cnpj_fornecedor_cpf_doador = cd_cnpj`
- Despesa -> CNPJ: `cd_cpf_cnpj_fornecedor_cpf_fornecedor = cd_cnpj`

---

## Atributos Relevantes

### Dimensão Partidária

- sg_partido
- nr_ano
- sg_uf
- nm_municipio

---

### Dimensão Fornecedor

- nm_fornecedor_cnae_secao1
- nm_fornecedor_porte
- nm_fornecedor_nat_jur
- sg_fornecedor_uf
- nr_fornecedor_idade_anos
- nm_fornecedor_faixa_idade_anos

---

### Dimensão Doador

- nm_doador_cnae_secao1
- nm_doador_porte
- nm_doador_nat_jur
- sg_doador_uf
- nr_doador_idade_anos
- nm_doador_faixa_idade_anos

---

## Métricas Padronizadas

### Receita

- vl_receita_total
- vl_receita_publica
- vl_receita_privada
- pct_receita_publica
- pct_receita_privada

### Despesas

- vl_despesa_total
- vl_despesa_administrativa
- vl_despesa_finalistica
- pct_despesa_administrativa = (vl_despesa_administrativa / vl_despesa_total) * 100
- pct_despesa_finalistica = (vl_despesa_finalistica / vl_despesa_total) * 100

### Quantidades

- qtd_fornecedores
- qtd_doadores
- qtd_receitas
- qtd_despesas

### Indices

- idx_eficiencia_politica = (vl_despesa_finalistica / vl_despesa_administrativa ) * 100

### Ticket médios

- ticket_medio_receita = (vl_receita_total / qtd_receitas)
- ticket_medio_despesa = (vl_despesa_total / qtd_despesas)

---

## Tabelas Analíticas

### partido_ano_uf_municipio

Uma linha representa:  Partido x Ano x UF x Municipio
Utiliza:

- atributos partidários
- métricas padronizadas

### partido_ano_uf

Uma linha representa: Partido x Ano x UF
Utiliza:

- atributos partidários
- métricas padronizadas

### partido_ano

Uma linha representa: Partido x Ano
Utiliza:

- atributos partidários
- métricas padronizadas

### fornecedor_partido_ano

Uma linha representa: fornecedor x partido x ano
Utiliza:

- atributos de fornecedor
- métricas padronizadas de despesa

### doador_partido_ano

Uma linha representa: doador x partido x ano
Utiliza:

- atributos de doador
- métricas padronizadas de receita

---

## Observações

As métricas padronizadas podem ser reutilizadas em diferentes granularidades analíticas.

## Variáveis para Estimador Razão

Y:

- vl_despesa_administrativa

X:

- vl_receita_total

---

## Variáveis para Clusterização

- pct_receita_publica
- pct_despesa_administrativa
- pct_despesa_finalistica
- idx_eficiencia_politica
- qtd_fornecedores
- qtd_doadores
- ticket_medio_receita
- ticket_medio_despesa
