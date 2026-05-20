# Arquitetura do Projeto

## Filosofia

O projeto NÃO deve ser tratado como sistema enterprise.

Priorizar:

- simplicidade
- reprodutibilidade
- clareza
- velocidade analítica

---

## Estrutura

```text
src/
├── ingestion/
├── preprocessing/
├── enrichment/
├── classification/
├── sampling/
├── estimators/
├── clustering/
├── visualization/
└── utils/
```

Organização dos Dados

```text
data/
├── 00-download/
├── 01-raw/
├── 02-bronze/
├── 03-silver/
├── 04-gold/
└── 05-output/
```

## Fluxo Esperado

download -> raw -> bronze -> silver -> gold -> output

### 00-downloads

Arquivos originais exatamente como disponibilizados pelas fontes externas.

Objetivo:

- rastreabilidade
- reprocessamento
- auditoria

Nenhuma transformação deve ocorrer nesta camada.

---

### 01-raw

Arquivos extraídos e organizados para leitura computacional.

Pode conter:

- descompressão
- reorganização estrutural
- separação por domínio

Ainda não possui padronização analítica.

---

### 02-bronze

Primeira camada analítica padronizada.

Transformações permitidas:

- normalização de colunas
- casting de tipos
- tratamento NULL
- parsing monetário
- parsing de datas
- padronização textual

Sem enriquecimento ou agregação analítica.

---

### 03-silver

Camada enriquecida e validada.

Transformações permitidas:

- joins
- enriquecimento CNPJ
- classificação financeira
- imputações
- regras de negócio
- validações

Os dados devem estar prontos para modelagem analítica.

---

### 04-gold

Camada analítica final.

Contém:

- tabelas agregadas
- métricas
- indicadores
- datasets para estimação
- datasets para clusterização
- bases para visualização

Granularidades analíticas devem ser explicitamente documentadas.

---

### 05-output

Artefatos finais do projeto.

Exemplos:

- gráficos
- tabelas
- relatórios
- exports
- imagens
- arquivos do artigo
