# AGENTS.md

Leia prioritariamente os documentos em `docs/ia/`:

1. `docs/ia/padronizacao_codigo.md`
2. `docs/ia/convencoes_git.md`
3. `docs/ia/notebooks.md`
4. `docs/ia/contexto.md`
5. `docs/ia/arquitetura.md`

Esses documentos definem:

- padrões de código
- convenções de projeto
- organização dos notebooks
- contexto acadêmico
- arquitetura analítica
- boas práticas para agentes de IA

A documentação relacionada aos dados está em `docs/data/`.

## Documentação Geral

1. `docs/data/fontes.md`
2. `docs/data/dicionario.md`
3. `docs/data/modelagem.md`

Esses documentos descrevem:

- fontes utilizadas
- modelagem analítica
- entidades
- métricas
- granularidade
- tabelas analíticas
- variáveis derivadas

## Dicionário de Dados Brutos

Documentação detalhada dos dados brutos em:

1. `docs/data/dicionario/raw/tse.md`
2. `docs/data/dicionario/raw/cnpj.md`

Arquivos auxiliares do TSE:

- `docs/data/dicionario/raw/tse-leiame-despesas.pdf`
- `docs/data/dicionario/raw/tse-leiame-receitas.pdf`

Esses documentos auxiliam na interpretação de:

- colunas
- classificações
- layouts
- granularidade
- semântica dos dados

## Metodologia Estatística

As anotações metodológicas estão em `docs/metodologia/`.

### Métodos Estatísticos

1. `docs/metodologia/amostragem.md`
2. `docs/metodologia/estimador_razao.md`
3. `docs/metodologia/estimador_regressao.md`
4. `docs/metodologia/clusterizacao.md`
5. `docs/metodologia/imputacao.md`

Esses documentos descrevem:

- estratégias de amostragem
- estimadores
- variáveis auxiliares
- clusterização
- imputação de dados
- hipóteses estatísticas

---

### Regras de Negócio e Transformações

1. `docs/metodologia/regras_negocio/classificacao_financeira.md`
2. `docs/metodologia/regras_negocio/transformacoes.md`

Esses documentos definem:

- classificação administrativa/finalística
- regras derivadas
- padronizações analíticas
- transformações aplicadas aos dados

---

## Apoio ao Artigo

Os documentos relacionados ao artigo estão em `docs/artigo/`.

1. `docs/artigo/notas.md`
2. `docs/artigo/estrutura.md`
3. `docs/artigo/hipoteses.md`
4. `docs/artigo/referencias.md`

Esses documentos auxiliam em:

- estruturação do paper
- hipóteses de pesquisa
- revisão bibliográfica
- anotações metodológicas
- resultados esperados
- organização da escrita acadêmica

---

## Objetivo

Projeto acadêmico da disciplina NBSA (UnB 1/2026)
sobre análise de dados financeiros partidários do TSE para o ano de 2025.

Objetivo:

- análise exploratória
- amostragem
- estimadores
- clusterização
- transparência
- eficiência financeira

---

## Regras Gerais

- Priorizar simplicidade
- Evitar overengineering
- Código altamente legível
- Reprodutibilidade acima de sofisticação
- Foco em entrega acadêmica

---

## Ferramentas de IA

Usar principalmente para:

- boilerplate
- autocomplete
- manipulação de dados
- gráficos
- funções utilitárias
- revisão de código

---

## Stack

- Python 3.13
- pandas
- numpy
- scipy
- scikit-learn
- statsmodels
- pyarrow
- matplotlib
- seaborn
- jupyter
- ipykernel

## Gerenciamento

- uv

## Padronização

- ruff.toml
- pyrightconfig.json
