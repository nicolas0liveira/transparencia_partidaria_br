# Transformações Básicas

Essas transformações devem estar em código para serem reaproveitadas.
Toda transformação aplicada em um dataframe deve ser registrado no pipeline.log

## Padronização de Texto

- tornar todo texto Uppser case
- remover espaços (trim)

## Campo CNPJ

O campo CNPJ sempre deve ser tratado como texto e com 14 posições, complementado com 0s)

## Tratamento Null

Trate todos os campos e deixe nulo caso possua os seguintes valores:COnverta para NULL:

- NULL
- "NULL"
- " "
- ""
- #NULO#

## Tratamento de Datas

Verifique sempre as datas e  deixe-as no formato adequado apra trabalhar nos dataframes

## Tratamentos Específicos

### Tratamento númérico Arquivos TSE

Trate os valores numéricos financeiros dos arquivos do TSE, pois estão no padrão Brasileiro (pt-br) e possuem os seguintes exemplos de valores:

- ",9"
- ",99"
- "R$ ,9"
- "R$ 99,9"
- "9.999.999,99"
