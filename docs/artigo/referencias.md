# Referências

## Financiamento Partidário e Tipologias

### *O perfil do financiamento dos partidos brasileiros (2006-2012): autores, objetivos, êxito e fracasso (1988-2010)*  
Link: [Repositório UnB](http://repositorio.unb.br/handle/10482/29679)  
```bibtex
@article{bolognesi2018perfil,
  title     = {O perfil do financiamento dos partidos brasileiros (2006-2012): autores, objetivos, êxito e fracasso},
  author    = {Bolognesi, Bruno and Cervi, Emerson Urizzi},
  journal   = {Revista Brasileira de Ci\^encia Pol\'itica},
  year      = {2018},
  number    = {23},
  pages     = {71--96},
  publisher = {Instituto de Ci\^encia Pol\'itica da Universidade de Bras\'ilia},
  url       = {http://repositorio.unb.br/handle/10482/29679}
}
```  
**Sugestão de uso:** Explora a origem dos recursos partidários e discute tipologias (cartel vs. partido de quadros) no contexto brasileiro. Útil para fundamentar a dependência dos partidos em verbas públicas (por exemplo *pct_receita_publica*) versus privadas (*pct_receita_privada*), e para justificar análises de clusterização de partidos conforme seu perfil de financiamento. Por exemplo: *“A estrutura de financiamento partidário pode refletir padrões organizacionais distintos entre legendas políticas.”*

Você pode usar esse artigo para justificar algo como:

“A estrutura de financiamento partidário pode refletir padrões organizacionais distintos entre legendas políticas.”

### *O financiamento político e a corrupção no Brasil* (Bruno Wilhelm Speck, 2012)  
Link: [Academia.edu (PDF)](https://www.academia.edu/3556070/Bruno_Wilhelm_Speck_O_financiamento_pol%C3%ADtico_e_a_corrup%C3%A7%C3%A3o_no_Brasil)  
```bibtex
@incollection{speck2012corrupcao,
  author    = {Speck, Bruno Wilhelm},
  title     = {O financiamento pol\'itico e a corrup\c{c}\~ao no Brasil},
  booktitle = {Temas de corrup\c{c}\~ao pol\'itica no Brasil},
  editor    = {Biason, Rita de C\'assia},
  publisher = {Bal\~ao Editorial},
  address   = {S\~ao Paulo},
  year      = {2012},
  pages     = {49--97},
  url       = {https://www.academia.edu/3556070/Bruno_Wilhelm_Speck_O_financiamento_pol%C3%ADtico_e_a_corrup%C3%A7%C3%A3o_no_Brasil},
  note      = {Acesso via Academia.edu}
}
```  
**Sugestão de uso:** Trata da relação histórica entre fontes de financiamento de campanha (empresas, pessoas físicas e fundos públicos) e casos de corrupção, incluindo o escândalo Collor. Pode servir para discutir como doações privadas influenciam comportamentos políticos. Use este capítulo para contextualizar a discussão sobre influência de doadores na política brasileira e justificar variáveis ou indicadores ligados à corrupção/financiamento. Por exemplo: *“…esquemas de corrupção envolvendo financiamento de campanhas por empresas se repetem, sugerindo a necessidade de reforma no sistema de captação de recursos eleitorais.”*


### *Partidos políticos no Brasil: organização partidária, competição eleitoral e financiamento público* (Braga & Bourdoukan, 2009)  
Link: [Perspectivas (FCLAR/Unesp)](https://periodicos.fclar.unesp.br/perspectivas/article/view/2290/1858)  
```bibtex
@article{braga2009partidos,
  author    = {Braga, Maria do Socorro Sousa and Bourdoukan, Adla},
  title     = {Partidos pol\'iticos no Brasil: organiza\c{c}\~ao partid\'aria, competi\c{c}\~ao eleitoral e financiamento p\'ublico},
  journal   = {Perspectivas},
  volume    = {35},
  pages     = {117--148},
  year      = {2009},
  address   = {S\~ao Paulo},
  url       = {https://periodicos.fclar.unesp.br/perspectivas/article/view/2290/1858},
  note      = {Artigo dispon\'ivel em PDF no portal da UNESP}
}
```  
**Sugestão de uso:** Analisa em detalhe como o Fundo Partidário é distribuído entre partidos e suas instâncias (nacional, estadual, municipal) e examina implicações para organização interna e competição política. Use este artigo para fundamentar argumentos sobre concentração ou dispersão de verbas públicas partidárias e seus efeitos, além de ilustrar diferenças entre partidos de massa e de quadros no Brasil. Exemplo de uso: *“Os padrões históricos de distribuição do fundo partidário revelam dinâmicas internas que favorecem a concentração de poder nas lideranças.”*



## Metodologia e estatistica

### CRISP DM
@misc{chapman2000crisp,
  author      = {Chapman, Pete and Clinton, Julian and Kerber, Randy and Khabaza, Thomas and Reinartz, Thomas and Shearer, Colin and Wirth, Rudiger},
  title       = {CRISP-DM 1.0: Step-by-step Data Mining Guide},
  year        = {2000},
  institution = {SPSS}
}

### Lakehouse: A New Generation of Open Platforms that Unify Data Warehousing and Advanced Analytic (Medallion Architecture (Databricks))

@inproceedings{armbrust2021lakehouse,
  author    = {Armbrust, Michael and Ghodsi, Ali and Xin, Reynold and Zaharia, Matei},
  title     = {Lakehouse: A New Generation of Open Platforms that Unify Data Warehousing and Advanced Analytics},
  booktitle = {CIDR '21: Conference on Innovative Data Systems Research},
  year      = {2021},
  url       = {https://www.cidrdb.org/cidr2021/papers/cidr2021_paper17.pdf}
}
**Sugestão de uso no artigo:**

Você pode usar na seção de arquitetura/pipeline de dados.

Exemplo de texto:

A organização dos dados seguiu uma arquitetura em múltiplas camadas inspirada no modelo Medallion Architecture, amplamente utilizado em pipelines analíticos modernos. Nesse modelo, os dados evoluem progressivamente de camadas brutas para estruturas refinadas e analíticas, tradicionalmente denominadas Bronze, Silver e Gold.

Ou:

A camada Bronze concentrou os dados padronizados e minimamente tratados; a Silver incorporou enriquecimentos, validações e regras de negócio; enquanto a Gold armazenou agregações analíticas finais utilizadas nas análises estatísticas e na clusterização.

| Sua Estrutura | Medallion      |
| ------------- | -------------- |
| 00-download   | ingestão/raw   |
| 01-raw        | raw zone       |
| 02-bronze     | bronze         |
| 03-silver     | silver         |
| 04-gold       | gold           |
| 05-output     | serving/output |
