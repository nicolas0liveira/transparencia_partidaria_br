# Arquitetura do Projeto

## Filosofia

O projeto possui foco acadêmico e analítico, priorizando simplicidade, reprodutibilidade e clareza estatística.

A arquitetura foi planejada para:

* facilitar exploração analítica;
* permitir reprocessamento dos dados;
* manter rastreabilidade das transformações;
* reduzir complexidade desnecessária;
* favorecer manutenção incremental;
* suportar experimentação estatística e inferencial.

O projeto NÃO deve ser tratado como sistema enterprise.

Priorizar:

* simplicidade;
* reprodutibilidade;
* clareza;
* pipelines explícitos;
* velocidade analítica;
* baixo acoplamento;
* transparência das transformações.

Evitar:

* overengineering;
* abstrações excessivas;
* orientação a objetos desnecessária;
* frameworks complexos;
* pipelines “mágicos”.

---

# Arquitetura Analítica

A arquitetura do projeto foi inspirada em conceitos de:

* Medallion Architecture;
* Lakehouse;
* pipelines analíticos reprodutíveis;
* CRISP-DM;
* processamento incremental em camadas.

Os dados evoluem progressivamente entre camadas analíticas:

```text
download -> raw -> bronze -> silver -> gold -> output
```

---

# Estrutura do Código

```text
src/transparencia_partidaria_br/
│
├── ingestion/
├── preprocessing/
├── enrichment/
├── analysis/
│   ├── eda.py
│   ├── estimators.py
│   ├── sampling.py
│   ├── clustering.py
│   ├── plots.py
│   └── __init__.py
├── __init__.py
├── utils/
├── config/
│
├── main.py
└── __init__.py
```

---

# Responsabilidade dos Módulos

## ingestion/

Responsável por:

* download das bases;
* extração de arquivos;
* organização inicial;
* persistência em `00-download` e `01-raw`.

Exemplos:

* download TSE;
* download CNPJ;
* leitura de ZIPs;
* validação de arquivos.

---

## preprocessing/

Responsável pelo pré-processamento inicial dos dados.

Transformações típicas:

* normalização de colunas;
* parsing monetário;
* parsing de datas;
* tratamento de nulos;
* casting de tipos;
* normalização textual;
* padronização de CNPJ;
* validações básicas.

Saída esperada:

* datasets padronizados em bronze.

---

## enrichment/

Responsável pelo enriquecimento analítico dos dados.

Transformações típicas:

* joins;
* integração CNPJ;
* integração CNAE;
* regras de negócio;
* imputações;
* consolidação de atributos auxiliares.

Saída esperada:

* datasets enriquecidos em silver.

---

## classification/

Responsável pelas regras de classificação financeira.

Exemplos:

* classificação de despesas administrativas;
* categorização de gastos;
* regras heurísticas;
* taxonomias analíticas.

Objetivo:

* transformar descrições textuais em variáveis analíticas estruturadas.

---

## feature_engineering/

Responsável pela construção de variáveis derivadas e métricas analíticas.

Exemplos:

* percentual de despesa administrativa;
* indicadores financeiros;
* porte financeiro;
* métricas agregadas;
* razões financeiras;
* métricas de dispersão.

Saída esperada:

* tabelas analíticas utilizadas na inferência estatística.

---

## sampling/

Responsável pelos planos amostrais.

Exemplos:

* amostragem aleatória simples;
* amostragem estratificada;
* alocação ótima de Neyman;
* cálculo de tamanhos amostrais;
* avaliação de variância.

---

## estimators/

Responsável pelos estimadores inferenciais.

Exemplos:

* média simples;
* estimador razão;
* estimador regressão;
* intervalos de confiança;
* erro padrão;
* coeficiente de variação.

---

## clustering/

Responsável pelas análises exploratórias de agrupamento.

Exemplos:

* clustering financeiro;
* agrupamento por porte;
* análise exploratória multivariada;
* identificação de perfis partidários.

Objetivo:

* apoiar estratificação e análise exploratória.

---

## visualization/

Responsável pela geração de artefatos visuais.

Exemplos:

* histogramas;
* boxplots;
* scatter plots;
* heatmaps;
* gráficos estatísticos;
* imagens utilizadas no artigo.

Saída esperada:

* arquivos em `05-output/images`.

---

## utils/

Responsável por componentes reutilizáveis.

Exemplos:

* logging;
* persistência parquet;
* persistência duckdb;
* helpers;
* utilitários de dataframe;
* funções de IO;
* métricas auxiliares.

---

# Organização dos Dados

```text
data/
│
├── 00-download/
├── 01-raw/
├── 02-bronze/
├── 03-silver/
├── 04-gold/
└── 05-output/
```

---

# Camadas Analíticas

## 00-download

Arquivos originais exatamente como disponibilizados pelas fontes externas.

Objetivos:

* rastreabilidade;
* auditoria;
* reprocessamento;
* preservação da origem.

Características:

* arquivos ZIP;
* CSV originais;
* nenhum tratamento;
* somente armazenamento bruto.

Nenhuma transformação deve ocorrer nesta camada.

---

## 01-raw

Arquivos extraídos e reorganizados para leitura computacional.

Transformações permitidas:

* descompressão;
* reorganização estrutural;
* separação por domínio;
* renomeação técnica de arquivos.

Ainda não possui padronização analítica.

Objetivo:

* facilitar ingestão;
* preservar granularidade original.

---

## 02-bronze

Primeira camada analítica padronizada.

Transformações permitidas:

* normalização de colunas;
* casting de tipos;
* tratamento de NULL;
* parsing monetário;
* parsing de datas;
* padronização textual;
* normalização de CNPJ;
* remoção de inconsistências simples.

Características:

* granularidade transacional preservada;
* sem agregações;
* sem enriquecimento analítico.

Persistência preferencial:

* parquet.

---

## 03-silver

Camada enriquecida e validada.

Transformações permitidas:

* joins;
* integração CNPJ;
* integração CNAE;
* classificação financeira;
* imputações;
* validações;
* regras de negócio;
* construção de atributos auxiliares.

Os dados devem estar:

* limpos;
* consistentes;
* enriquecidos;
* prontos para modelagem analítica.

Persistência:

* parquet;
* duckdb analítico.

---

## 04-gold

Camada analítica final.

Contém:

* tabelas agregadas;
* métricas;
* indicadores;
* datasets para estimação;
* datasets para clusterização;
* datasets para visualização;
* tabelas estatísticas finais.

Granularidades devem ser explicitamente documentadas.

Exemplos:

```text
partido_ano.parquet
indicadores_financeiros.parquet
base_estimacao.parquet
base_clusterizacao.parquet
```

---

## 05-output

Artefatos finais do projeto.

Exemplos:

* gráficos;
* tabelas;
* imagens;
* relatórios;
* exports CSV;
* arquivos do artigo;
* visualizações;
* figuras LaTeX;
* resultados estatísticos.

Estrutura sugerida:

```text
05-output/
│
├── images/
├── tables/
├── reports/
├── article/
└── exports/
```

---

# Persistência

## Formatos Preferenciais

### CSV

Utilizado para:

* interoperabilidade;
* exportações;
* rastreabilidade;
* arquivos intermediários simples.

### Parquet

Formato principal do pipeline analítico.

Vantagens:

* compressão;
* tipagem;
* performance;
* integração com pandas e DuckDB.

### DuckDB

Utilizado como camada analítica local.

Objetivos:

* consultas SQL analíticas;
* exploração rápida;
* agregações;
* prototipação estatística.

Evita necessidade de infraestrutura pesada.

---

# Estratégia de Processamento

## Abordagem

O pipeline segue estratégia batch e incremental.

Características:

* processamento explícito;
* etapas independentes;
* persistência entre camadas;
* reprocessamento parcial;
* rastreabilidade analítica.

---

# Logging e Observabilidade

Todas as transformações relevantes devem possuir logging.

Objetivos:

* auditoria;
* rastreabilidade;
* depuração;
* reprodutibilidade.

Exemplos de eventos logados:

* leitura de datasets;
* quantidade de registros;
* transformações aplicadas;
* joins;
* validações;
* persistência de arquivos.

---

# Estratégia Estatística

A arquitetura foi desenhada para suportar:

* inferência estatística;
* experimentação analítica;
* comparação entre métodos;
* reprodutibilidade científica.

Os datasets finais devem facilitar:

* cálculo de variância;
* comparação de estimadores;
* análise inferencial;
* clusterização;
* análise exploratória;
* geração de tabelas do artigo.

---

# Uso de Inteligência Artificial

Ferramentas de IA generativa foram utilizadas como apoio complementar durante:

* codificação em Python;
* refinamento estrutural;
* documentação;
* geração inicial de diagramas e imagens;
* revisão textual.

Todo conteúdo gerado foi:

* supervisionado;
* revisado manualmente;
* validado analiticamente antes da utilização no projeto.
