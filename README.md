
<!-- markdownlint-disable MD012 -->

# Perfil Político-Partidario Brasileiro em 2025


<!--TODO: analisar os possíveis nomes pro artigo-->
## Possíveis nomes pra atanisar dps (TODO)

- Modelo Analítico para Avaliação de Eficiência, Risco e Estrutura nas Finanças Partidárias Brasileiras em 2025
- Análise das Finanças Partidárias Brasileiras em 2025, para Avaliação de Eficiência, Risco e Estrutura
- Análise de Transparência, Risco e Desigualdade em Dados Financeiros Partidários em 2025

## Programa da disciplina NBSA

- Amostragem Aleatória Simples Com e Sem Reposição
- Amostragem Estratificada
- Estimadores Tipo Razão
- Estimadores Tipo Regressão
- Amostragem Sistemática
- Amostragem por Conglomerados
- Imputação de Dados

## Distribuição das notas para avaliação

- Escolha da Conferência com Qualis: 0,5
- Título e Resumo: 0,5
- Introdução: 1,0
- Referencial Teórico: 1,0
- Trabalhos Relacionados: 1,0
- Desenvolvimento: 4,0
- Conclusões: 1,0
- Referências: 1,0

## Principais questões de negócio

### Transparência e eficiência

- Partidos gastam mais com atividade-fim ou com manutenção?
- Existe concentração de receitas em poucos doadores?
- Há padrão de ineficiência (alto gasto administrativo vs. baixa atividade política)?

### Risco e compliance

- Existem padrões suspeitos de gastos (ex: fornecedores repetidos, valores fracionados)?
- Partidos com maior receita têm maior dispersão de despesas?
- Há indícios de comportamento atípico comparado ao padrão geral?

### Estrutura e desigualdade

- Existe concentração de recursos entre partidos?
- Partidos maiores capturam mais financiamento proporcionalmente?
- Relação entre receita pública vs. privada

## Principais fontes dos dados

- TSE
- CNPJ
- CEIS
- IBGE

Mais informações em  `docs/data`

## APIs para enriquecer o dado

### Pessoas físicas e jurídicas

```sh
# para CPFs
curl -X 'GET' \
  'https://api.portaldatransparencia.gov.br/api-de-dados/pessoa-fisica?cpf=02246149592' \
  -H 'accept: */*' \
  -H 'chave-api-dados: xxxxxxxxxxx'
```

Exemplo retorno da /api-de-dados/pessoa-fisica:
Response body

```json
{
  "cpf": "***.461.495-**",
  "nome": "NICOLAS RODRIGUES DE OLIVEIRA",
  "nis": "",
  "favorecidoDespesas": true,
  "servidor": false,
  "beneficiarioDiarias": false,
  "permissionario": false,
  "contratado": false,
  "sancionadoCEIS": false,
  "sancionadoCNEP": false,
  "sancionadoCEAF": false,
  "portadorCPDC": false,
  "portadorCPGF": false,
  "favorecidoBolsaFamilia": false,
  "favorecidoPeti": false,
  "favorecidoSafra": false,
  "favorecidoSeguroDefeso": false,
  "favorecidoBpc": false,
  "favorecidoTransferencias": false,
  "favorecidoCPCC": false,
  "favorecidoCPDC": false,
  "favorecidoCPGF": false,
  "participanteLicitacao": false,
  "servidorInativo": false,
  "pensionistaOuRepresentanteLegal": false,
  "instituidorPensao": false,
  "auxilioEmergencial": false,
  "favorecidoAuxilioBrasil": false,
  "favorecidoNovoBolsaFamilia": false,
  "favorecidoAuxilioReconstrucao": false
}
```

```sh
# PAra CNPJs
curl -X 'GET' \
  'https://api.portaldatransparencia.gov.br/api-de-dados/pessoa-juridica?cnpj=60701190000104' \
  -H 'accept: */*' \
  -H 'chave-api-dados: xxxxxxxxxxx'
  ```

exemplo de retorno da /api-de-dados/pessoa-juridica:

Response body

```json
{
  "cnpj": "60701190000104",
  "razaoSocial": "ITAU UNIBANCO S.A.",
  "nomeFantasia": "ITAU UNIBANCO",
  "favorecidoDespesas": true,
  "possuiContratacao": true,
  "convenios": false,
  "favorecidoTransferencias": false,
  "sancionadoCEPIM": false,
  "sancionadoCEIS": false,
  "sancionadoCNEP": false,
  "sancionadoCEAF": false,
  "participanteLicitacao": true,
  "emitiuNFe": false,
  "beneficiadoRenunciaFiscal": true,
  "isentoImuneRenunciaFiscal": false,
  "habilitadoRenunciaFiscal": false
}
```

as consultas sao paginadas

### Sancoes

- <https://api.portaldatransparencia.gov.br/api-de-dados/cnep?codigoSancionado={CPF|CNPJ}&pagina=1>

```
[
  {
    "id": 0,
    "dataReferencia": "string",
    "dataInicioSancao": "string",
    "dataFimSancao": "string",
    "dataPublicacaoSancao": "string",
    "dataTransitadoJulgado": "string",
    "dataOrigemInformacao": "string",
    "tipoSancao": {
      "descricaoResumida": "string",
      "descricaoPortal": "string"
    },
    "fonteSancao": {
      "nomeExibicao": "string",
      "telefoneContato": "string",
      "enderecoContato": "string"
    },
    "fundamentacao": [
      {
        "codigo": "string",
        "descricao": "string"
      }
    ],
    "orgaoSancionador": {
      "nome": "string",
      "siglaUf": "string",
      "poder": "string",
      "esfera": "string"
    },
    "sancionado": {
      "nome": "string",
      "codigoFormatado": "string"
    },
    "valorMulta": "string",
    "pessoa": {
      "id": 0,
      "cpfFormatado": "string",
      "cnpjFormatado": "string",
      "numeroInscricaoSocial": "string",
      "nome": "string",
      "razaoSocialReceita": "string",
      "nomeFantasiaReceita": "string",
      "tipo": "string"
    },
    "textoPublicacao": "string",
    "linkPublicacao": "string",
    "detalhamentoPublicacao": "string",
    "numeroProcesso": "string",
    "abrangenciaDefinidaDecisaoJudicial": "string",
    "informacoesAdicionaisDoOrgaoSancionador": "string"
  }
]
```


https://api.portaldatransparencia.gov.br/api-de-dados/cepim?cnpjSancionado={CPF|CNPJ}&pagina=1

```
[
  {
    "id": 0,
    "dataReferencia": "string",
    "motivo": "string",
    "orgaoSuperior": {
      "nome": "string",
      "codigoSIAFI": "string",
      "cnpj": "string",
      "sigla": "string",
      "descricaoPoder": "string",
      "orgaoMaximo": {
        "codigo": "string",
        "sigla": "string",
        "nome": "string"
      }
    },
    "pessoaJuridica": {
      "id": 0,
      "cpfFormatado": "string",
      "cnpjFormatado": "string",
      "numeroInscricaoSocial": "string",
      "nome": "string",
      "razaoSocialReceita": "string",
      "nomeFantasiaReceita": "string",
      "tipo": "string"
    },
    "convenio": {
      "codigo": "string",
      "objeto": "string",
      "numero": "string"
    }
  }
]
```

'https://api.portaldatransparencia.gov.br/api-de-dados/ceaf?cpfSancionado=02246149592&pagina=1'
[
  {
    "id": 0,
    "dataReferencia": "string",
    "dataInicioSancao": "string",
    "dataFimSancao": "string",
    "dataPublicacaoSancao": "string",
    "dataTransitadoJulgado": "string",
    "dataOrigemInformacao": "string",
    "tipoSancao": {
      "descricaoResumida": "string",
      "descricaoPortal": "string"
    },
    "fonteSancao": {
      "nomeExibicao": "string",
      "telefoneContato": "string",
      "enderecoContato": "string"
    },
    "fundamentacao": [
      {
        "codigo": "string",
        "descricao": "string"
      }
    ],
    "orgaoSancionador": {
      "nome": "string",
      "siglaUf": "string",
      "poder": "string",
      "esfera": "string"
    },
    "sancionado": {
      "nome": "string",
      "codigoFormatado": "string"
    },
    "pessoa": {
      "id": 0,
      "cpfFormatado": "string",
      "cnpjFormatado": "string",
      "numeroInscricaoSocial": "string",
      "nome": "string",
      "razaoSocialReceita": "string",
      "nomeFantasiaReceita": "string",
      "tipo": "string"
    },
    "textoPublicacao": "string",
    "linkPublicacao": "string",
    "detalhamentoPublicacao": "string",
    "numeroProcesso": "string",
    "abrangenciaDefinidaDecisaoJudicial": "string",
    "informacoesAdicionaisDoOrgaoSancionador": "string"
  }
]
```

## APIs gratuitas de CNPJ

- ttps://brasilapi.com.br/api/cnpj/v1/00000000000191
- https://www.receitaws.com.br/v1/cnpj/00000000000191
- https://open.cnpja.com/office/00000000000191


## Artigos relevantes

- <https://repositorio.unb.br/simple-search?query=sele%C3%A7%C3%A3o+amostras>
- <https://repositorio.unb.br/handle/10482/29679>


## Perguntas

- Qual os estimadores e porque?
- 

- quanto maior a diferença dos conglomerados