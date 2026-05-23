# Tratamentos, Imputações e transformações para colocar no artigo.

Foi observado varios dados inconsistentes nas fontes de dados o que dificulta a analise

## Tratamentos

Quando DT_RECEITA pode vir nula

- Dados incompletos da prestação

- Alguns diretórios partidários simplesmente não preenchem corretamente a informação no SPCA/TSE.

Isso acontece bastante em:

- diretórios municipais;
- prestações antigas;
- registros retificados;
- receitas lançadas manualmente.

Apesar do foco nao ser temporal criei o indicador in_dt_receita_nula e pretendo remover os dados sem data de receita

df = df[df["dt_receita"].notna()]