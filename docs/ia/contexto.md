# Contexto do Projeto

## Universidade

* Universidade de Brasília (UnB)
* Disciplina: NBSA
* Semestre: 1/2026

---

# Tema da Pesquisa

## Macrotema

Estimação de indicadores financeiros partidários utilizando técnicas de amostragem e estimadores auxiliares.

## Tema

Comparação entre amostragem aleatória simples e amostragem estratificada aplicada às despesas administrativas partidárias brasileiras em 2025.

O estudo busca avaliar ganhos de precisão estatística na estimação de despesas administrativas partidárias utilizando:

* amostragem estratificada;
* alocação ótima de Neyman;
* estimadores auxiliares do tipo razão;
* estimadores por regressão.

---

# Problema de Pesquisa

Os partidos políticos brasileiros apresentam elevada heterogeneidade financeira, com forte assimetria entre partidos de pequeno, médio e grande porte.

Nesse contexto, métodos tradicionais de amostragem aleatória simples podem produzir estimativas com elevada variância e baixa precisão inferencial.

A pesquisa investiga se técnicas de:

* estratificação por porte financeiro;
* utilização de variáveis auxiliares;
* agrupamentos financeiros;

podem produzir estimativas mais eficientes das despesas administrativas partidárias.

Questões centrais da pesquisa:

* A estratificação por porte financeiro reduz a variância das estimativas populacionais?
* A utilização da receita total partidária como variável auxiliar melhora a precisão das estimativas?
* Quais estratégias amostrais apresentam melhor desempenho em cenários de elevada dispersão financeira?
* O uso de alocação ótima de Neyman produz ganhos adicionais de eficiência?
* Existe forte correlação entre arrecadação e despesas administrativas partidárias?

---

# Motivação

O projeto busca aplicar técnicas clássicas de inferência estatística em dados governamentais reais disponibilizados em formato aberto pelo Tribunal Superior Eleitoral (TSE).

Além da contribuição metodológica relacionada à teoria de amostragem, o trabalho também busca construir uma estrutura analítica reprodutível para pesquisas quantitativas aplicadas a:

* transparência pública;
* financiamento político;
* ciência de dados aplicada ao setor público;
* análise financeira partidária;
* estatística computacional.

O estudo também explora integração entre:

* estatística;
* engenharia de dados;
* análise exploratória;
* pipelines analíticos reprodutíveis;
* dados abertos governamentais.

---

# Objetivo Geral

Comparar técnicas de amostragem e estimação aplicadas às despesas administrativas partidárias, avaliando ganhos de precisão obtidos por:

* amostragem estratificada;
* alocação ótima;
* utilização de variáveis auxiliares.

---

# Objetivos Específicos

* Construir pipeline analítico reprodutível para processamento dos dados do TSE;
* Realizar ingestão, limpeza e padronização das bases financeiras partidárias;
* Integrar dados auxiliares do CNPJ e CNAE;
* Definir variável financeira principal de interesse;
* Construir estratos financeiros partidários;
* Aplicar diferentes planos amostrais;
* Comparar estimadores estatísticos;
* Avaliar variância, erro padrão e intervalos de confiança;
* Aplicar alocação ótima de Neyman;
* Explorar agrupamentos financeiros via clusterização;
* Avaliar correlação entre receita total e despesa administrativa;
* Produzir tabelas, gráficos e indicadores analíticos reprodutíveis.

---

# Hipóteses

## Hipótese principal

Partidos políticos apresentam heterogeneidade financeira suficiente para que técnicas de estratificação produzam ganhos relevantes de precisão inferencial quando comparadas à amostragem aleatória simples.

## Hipóteses secundárias

* Existe correlação positiva entre receita total e despesa administrativa;
* O estimador razão apresenta menor variância que o estimador baseado na média simples;
* A estratificação por porte financeiro reduz a dispersão intraestrato;
* Técnicas de agrupamento podem identificar perfis financeiros partidários semelhantes.

---

# População e Unidade Amostral

## População

Partidos políticos brasileiros com registros financeiros disponíveis nas bases de prestação de contas partidárias do TSE referentes ao exercício de 2025.

## Unidade amostral

Partido Político × Ano

A agregação no nível partido-ano foi adotada para:

* reduzir variabilidade transacional;
* facilitar inferência estatística;
* permitir estratificação;
* facilitar clusterização;
* consolidar indicadores financeiros analíticos.

---

# Variáveis da Pesquisa

## Variável principal

[
Y = \text{Despesa Administrativa Total}
]

Soma das despesas classificadas como administrativas para cada partido político.

Exemplos de despesas administrativas:

* pessoal;
* contabilidade;
* assessoria jurídica;
* infraestrutura;
* manutenção operacional;
* serviços recorrentes.

## Variável auxiliar

[
X = \text{Receita Total do Partido}
]

Soma das receitas arrecadadas por cada partido político.

## Estimador Razão

\hat{Y}_R = X\frac{\bar{y}}{\bar{x}}

Objetivo:

* investigar quanto o partido gasta administrativamente para cada R$1 arrecadado;
* reduzir variância das estimativas;
* melhorar eficiência inferencial.

---

# Estratégias Metodológicas

## Planos amostrais avaliados

* Amostragem Aleatória Simples (AAS);
* Amostragem Estratificada Proporcional;
* Alocação Ótima de Neyman.

## Estimadores avaliados

* Média simples;
* Estimador razão;
* Estimador regressão.

## Técnicas complementares

* análise exploratória;
* análise de dispersão;
* análise de correlação;
* clusterização;
* construção de indicadores financeiros;
* estratificação por porte financeiro.

---

# Estratificação

A estratificação será baseada em características financeiras dos partidos, incluindo:

* receita total;
* magnitude das despesas;
* porte financeiro;
* possíveis agrupamentos obtidos via clustering.

Objetivos da estratificação:

* reduzir variabilidade intraestrato;
* melhorar precisão inferencial;
* produzir grupos financeiramente homogêneos.

---

# Pipeline Analítico

O pipeline analítico foi desenvolvido em Python utilizando tecnologias open source.

Etapas principais:

1. ingestão de dados;
2. pré-processamento;
3. enriquecimento;
4. modelagem analítica;
5. análise estatística;
6. geração de visualizações e indicadores.

## Principais etapas de tratamento

* padronização textual;
* normalização monetária;
* tratamento de nulos;
* parsing de datas;
* normalização de CNPJ;
* integração CNAE;
* classificação financeira;
* criação de variáveis derivadas.

---

# Arquitetura de Dados

O projeto utiliza arquitetura Medallion com persistência em:

* CSV;
* Parquet;
* DuckDB.

Camadas analíticas:

* RAW;
* BRONZE;
* SILVER;
* GOLD.

Estrutura de armazenamento: 

---

# Tecnologias Utilizadas

## Linguagem e bibliotecas

* Python 3.13;
* pandas;
* pyarrow;
* matplotlib;
* duckdb;
* typer;
* rich.

Configuração do projeto: 

## Ferramentas estatísticas

* Jamovi;
* Python;
* notebooks Jupyter.

## Qualidade de código

* ruff;
* pyright;
* mypy;
* pytest.

Padronização do projeto: 

---

# Fontes de Dados

## Tribunal Superior Eleitoral (TSE)

Bases utilizadas:

* receitas anuais partidárias;
* despesas anuais partidárias.

Os dados possuem granularidade transacional e incluem:

* arrecadações;
* pagamentos;
* fornecedores;
* documentos fiscais;
* classificações financeiras.

Documentação TSE:  

## Receita Federal

### Base CNPJ

Utilizada para:

* enriquecimento cadastral;
* identificação de fornecedores;
* integração CNAE;
* análise exploratória econômica.

Fonte cadastrada: 

---

# Características dos Dados

As bases do TSE apresentam:

* elevada heterogeneidade financeira;
* forte assimetria;
* alta dispersão;
* granularidade transacional;
* registros de receitas e despesas individualizados.

Observações importantes do TSE:

* arquivos em Latin-1;
* separador `;`;
* campos `#NULO` e `#NE`;
* atualização contínua das bases.  

---

# Estratégia Analítica

O estudo prioriza:

* simplicidade metodológica;
* clareza estatística;
* reprodutibilidade;
* pipeline funcional;
* documentação acadêmica incremental.

O projeto evita:

* overengineering;
* abstrações desnecessárias;
* complexidade excessiva;
* dependência de infraestrutura pesada.

---

# Organização Analítica

## Notebooks

Utilizados para:

* exploração;
* validação estatística;
* visualização;
* prototipação.

Regras dos notebooks: 

## Código fonte

Responsável por:

* regras de negócio;
* transformações;
* pipelines;
* funções reutilizáveis.

---

# Resultados Esperados

Espera-se observar:

* redução de variância em métodos estratificados;
* melhoria de precisão inferencial;
* correlação positiva entre receita e despesa;
* melhor desempenho de estimadores auxiliares;
* identificação de perfis financeiros partidários.

O projeto também busca entregar:

* pipeline reproduzível;
* estrutura analítica reutilizável;
* documentação acadêmica consistente;
* contribuição metodológica aplicada a dados eleitorais abertos.
