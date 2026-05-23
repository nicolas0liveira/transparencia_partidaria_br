\section{Hipóteses}

Nesta seção estabelecem-se as hipóteses do estudo. Supõe-se correlação positiva entre receita total ($X$) e despesa administrativa total ($Y$) dos partidos, de modo que o uso de amostragem estratificada e estimadores auxiliares (razão e regressão) melhore a precisão da estimativa. Definem-se hipóteses quantitativas sobre correlação (ex.: $\rho_{XY}>0$), redução de variância por estratificação (ex.: redução ≥ 20\%), eficácia da alocação de Neyman, e ganhos de eficiência dos estimadores auxiliares. Consideram-se também hipóteses sobre o impacto de eventuais problemas de qualidade dos dados. Os testes estatísticos propostos incluem correlação de Pearson, comparação de variâncias (teste~$F$), intervalo de confiança, bootstrap e simulações. Adota-se nível de significância $\alpha=0{,}05$ (ajustável pelo leitor) e critérios práticos (ex.: redução de variância ≥ 20\%, viés máximo aceitável de 5\%), explicitando valores fictícios como exemplos.

\subsection{Hipóteses Principais}
\begin{itemize}
  \item Sejam $Y = \sum_{i=1}^N Y_i$ a despesa administrativa total populacional e $X = \sum_{i=1}^N X_i$ a receita total; $N$ é o número de partidos e $n$ o tamanho da amostra. Denotam-se a variância populacional por $\Var(Y)$, o viés de um estimador $\hat{Y}$ por $\Bias(\hat{Y})=E[\hat{Y}]-Y$, e o erro quadrático médio por $\MSE(\hat{Y})=\Var(\hat{Y})+[\Bias(\hat{Y})]^2$.
  \item Presume-se $\rho_{XY}>0$ (correlação positiva) entre receita e despesa administrativa. Em termos práticos, espera-se que um partido com maior receita tenda a ter maior despesa administrativa total.
  \item Espera-se que a amostragem estratificada reduza a variância do estimador de $Y$ em relação à amostragem aleatória simples (por exemplo, redução ≥ 20\% na variância, valor ilustrativo). Adota-se hipótese operacional de que $\Var(\hat{Y}_{estrat})\le 0{,}8\,\Var(\hat{Y}_{SRS})$, ajustável conforme necessidade.
  \item A alocação ótima de Neyman deverá produzir o menor erro amostral possível para $Y$, em comparação com alocação proporcional ou igual. Em especial, supõe-se $\Var(\hat{Y}_{Neyman}) \le \Var(\hat{Y}_{prop})$.
  \item Os estimadores auxiliares (razão e regressão), baseados na variável $X$, devem apresentar MSE inferior ao estimador sem variável auxiliar. Formalmente, espera-se por exemplo $\MSE(\hat{Y}_R) \le \MSE(\hat{Y}_{AAS})$ e $\MSE(\hat{Y}_{reg}) \le \MSE(\hat{Y}_{AAS})$.
  \item Considera-se que potenciais problemas de qualidade (dados faltantes, erros de registro ou outliers) não induzirão viés significativo ao estimador de $Y$. Exemplo operacional: admite-se hipóteses de que 5\% de dados fora ou 5\% de dados faltantes sem tendência causam viés ≤ 5\% no total estimado (ajustável conforme necessidade).
\end{itemize}

\subsection{Hipóteses Estatísticas}
\begin{itemize}
  \item \textbf{Correlação:} $H_{0}$: $\rho_{XY}=0$ (nenhuma correlação) versus $H_{1}$: $\rho_{XY}>0$. Teste de correlação de Pearson a $\alpha=0{,}05$ (unilateral). Rejeitar $H_0$ se $p<\alpha$, indicando correlação positiva significativa.
  \item \textbf{Variâncias:} $H_{0}$: $\Var(\hat{Y}_{estrat}) \ge \Var(\hat{Y}_{SRS})$ versus $H_{1}$: $\Var(\hat{Y}_{estrat}) < \Var(\hat{Y}_{SRS})$. Aplicar teste $F$ para comparar variâncias das estimativas (ex.: razão das variâncias < 1 para rejeitar $H_0$). Critério prático: aceitar $H_1$ se $\Var(\hat{Y}_{estrat})/\Var(\hat{Y}_{SRS}) \le 0{,}8$.
  \item \textbf{Alocação de Neyman:} $H_{0}$: $\Var(\hat{Y}_{Neyman}) \ge \Var(\hat{Y}_{prop})$ versus $H_{1}$: $\Var(\hat{Y}_{Neyman}) < \Var(\hat{Y}_{prop})$. Pode-se usar comparação de variâncias (teste $F$) ou simulações para verificar a superioridade da alocação.
  \item \textbf{Estimadores de Razão/Regressão:} $H_{0}$: $\MSE(\hat{Y}_{aux}) \ge \MSE(\hat{Y}_{AAS})$ versus $H_{1}$: $\MSE(\hat{Y}_{aux}) < \MSE(\hat{Y}_{AAS})$. Em teste prático, usar razão de variâncias ou comparar intervalos de confiança via bootstrap. Também pode-se testar o viés médio (teste $t$) assumindo $\Bias(\hat{Y}_{aux}) \approx 0$ sob $H_0$.
  \item \textbf{Bias do estimador:} $H_{0}$: $\Bias(\hat{Y})=0$ versus $H_{1}$: $\Bias(\hat{Y})\neq 0$. Avaliar intervalos de confiança para $\hat{Y}$ e verificar se incluem o total real $Y$ (simulações amostrais podem ser usadas).
\end{itemize}

\subsection{Hipóteses sobre Estratificação e Alocação}
\begin{itemize}
  \item A estratificação por porte ou receita dos partidos deve produzir estratos mais homogêneos. Hipótese: variância dentro de cada estrato é reduzida, o que leva a ganho geral de precisão. Testar comparando $\Var_h(Y)$ antes e depois da estratificação.
  \item Espera-se redução percentual $\Delta_{var} = 1 - \Var(\hat{Y}_{estrat})/\Var(\hat{Y}_{SRS})$ significativa (ex.: $\Delta_{var}\ge 20\%$). Critério: aceitar estratificação eficaz se $\Delta_{var}\ge$ valor de corte (por exemplo, 0,2).
  \item A alocação de Neyman é assumida ótima: formalmente, $n_h \propto N_h\sigma_h$, onde $\sigma_h^2$ é a variância no estrato $h$. Hipótese: nenhuma outra alocação proporcional (ou arbitrária) supera a alocação de Neyman em termos de MSE total.
  \item Usar simulações amostrais (ou fórmula de variância) para comparar $ \Var(\hat{Y})$ sob alocação de Neyman e proporcional. Adotar $H_0$ como equivalência (nenhuma vantagem) e rejeitar se $\Var_{Neyman}$ é pelo menos 20\% menor que $\Var_{prop}$.
\end{itemize}

\subsection{Hipóteses sobre Estimadores Auxiliares}
\begin{itemize}
  \item A variável auxiliar $X$ tem correlação significativa com $Y$ ($\rho_{XY}>0$), justificando seu uso. Teste de correlação confirma esta hipótese.
  \item O estimador de razão ($\hat{Y}_R = X\,\bar{y}/\bar{x}$) e o de regressão ($\hat{Y}_{reg} = \bar{y} + b\,(X-\bar{x})$) são esperados sem viés ou com viés pequeno. Critério: verificar se $\Bias(\hat{Y}_{R}),\Bias(\hat{Y}_{reg})$ são aproximadamente zero (p.ex. $|\Bias|/Y < 5\%$) via simulações bootstrap.
  \item Esses estimadores devem melhorar a precisão: testar $H_0: \Var(\hat{Y}_{aux}) \ge \Var(\hat{Y}_{AAS})$ versus $H_1: <$. Em nível prático, adotar redução de MSE ≥ 20\% como indicação de ganho.
  \item Aplicar teste $t$ para diferença de médias ajustadas ou usar razão de variâncias dos estimadores para avaliação. Comparar intervalos de confiança dos estimadores com e sem auxilar.
\end{itemize}

\subsection{Hipóteses sobre Qualidade dos Dados e Robustez}
\begin{itemize}
  \item Supõe-se ausência de viés sistemático em dados faltantes ou outliers. $H_0$: dados inconsistentes não afetam significativamente $\hat{Y}$; $H_1$: afetam. Utilizar simulações ou análise de robustez (ex.: estimativa com e sem casos extremos).
  \item Hipótese operacional: até 5\% de erros aleatórios (outliers ou dados omitidos) altera $\hat{Y}$ em menos de 5\%. Testar por bootstrap adicionando ruído simulado e checando o intervalo de confiança resultante de $\hat{Y}$.
  \item Comparar estimativas obtidas com processamento diferente (p.ex. limpeza mais ou menos agressiva) para avaliar sensibilidade. Se as diferenças permanecerem dentro do limite de erro (ex.: $|\Delta|/Y < 5\%$), considerar hipótese de robustez aprovada.
\end{itemize}
