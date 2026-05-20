# Contexto do Projeto

## Universidade

- Universidade de Brasília (UnB)
- Disciplina NBSA
- 1/2026

---

## Macrotema

Estimação de indicadores financeiros partidários utilizando técnicas de amostragem e estimadores auxiliares

## Tema

Estimativa da despesa administrativa de partidos políticos brasileiras em 2025 utilizando amostragem estratificada e estimadores do tipo razão

## Problema de pesquisa

Partidos políticos apresentam padrões financeiros heterogêneos, sendo possível melhorar a precisão das estimativas por meio de amostragem estratificada e estimadores do tipo razão.

---

## Motivação

O projeto busca aplicar técnicas de:

- amostragem
- estimação
- clusterização
- análise multivariada

em dados reais do TSE.

---

## Objetivo geral

Comparar técnicas de amostragem e estimação aplicadas aos dados financeiros partidários do TSE, avaliando ganhos de precisão obtidos por estratificação e uso de variáveis auxiliares.

## Objetivos específicos

Definir uma variável financeira principal de interesse;
Construir estratos de partidos políticos;
Aplicar diferentes planos amostrais;
Comparar estimadores:

- média simples;
- razão;
- regressão;
- Avaliar variância, erro padrão e intervalo de confiança;
- Aplicar alocação ótima de Neyman;
- Explorar agrupamentos financeiros partidários via clusterização.
- População

## Unidade amostral: Partido político

- foco em reduzir variância;
- facilitar estratificação;
- facilitar clusterização;

## Variáveis principais

`Y = Despesa Administrativa Total` - Soma das despesas classificadas como administrativas para cada partido.

`X = Receita Total do Partido`

## Estimador Razão (R=X/Y)

R = Receita Total / Despesa Administrativa

## investigar

- Quanto o partido gasta administrativamente para cada R$1 arrecadado.

## Estratificação

- Registrar os critérios utilizados para estratificação

---

## Bases Utilizadas

- TSE
- CNPJ

---

## Restrições

- prazo curto
- foco acadêmico
- evitar complexidade excessiva
- priorizar entrega funcional
