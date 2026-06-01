## Relatório Técnico - Benchmark de Estratégias de Prompt Engineering ##
Classificação NLP em Operações Logísticas (Supplay Chain) de peças para veículos pesados

**Projeto:** LLM-Evaluation-Prompts

**Tipo:** Pesquisa exploratória com abordagem quantitativa

**Data:** Maio de 2025

### 1. Objetivo ###

Este relatório documenta as decisões metodológicas do benchmark comparativo de estratégias de prompt engineering aplicadas à tarefa de classificação de sentimento em NLP, no domínio técnico de supply chain de peças para caminhões.

O benchmark foi projetado para avaliar modelos de linguagem em um domínio especializado composto por exemplos explícitos e casos de fronteira (*borderline cases*), nos quais a polaridade do sentimento depende da interpretação do contexto operacional e do impacto para o negócio, e não apenas da presença de palavras tradicionalmente associadas a sentimentos positivos ou negativos.

O experimento investiga a seguinte questão de pesquisa: 
> Em um domínio técnico especializado, estratégias estruturadas de prompt (few-shot e chain-of-thought) produzem ganhos de acurácia mensuráveis em relação ao baseline zero-shot, e esse comportamento varia entre provedores de LLM? 

A hipótese de trabalho, fundamentada na literatura, é que domínios técnicos com sentimento implícito e exemplos que exigem raciocínio contextual amplificam as diferenças entre estratégias de prompting, ao contrário de domínios genéricos, onde o zero-shot frequentemente apresenta desempenho elevado e os ganhos obtidos por estratégias mais sofisticadas tendem a ser marginais. 

O experimento investiga a seguinte questão de pesquisa:

> Em um domínio técnico especializado, estratégias estruturadas de prompt (few-shot e chain-of-thought) produzem ganhos de acurácia mensuráveis em relação ao baseline zero-shot, e esse comportamento varia entre provedores de LLM?

A hipótese de trabalho, fundamentada na literatura, é que domínios técnicos com sentimento **implícito amplificam as diferenças entre estratégias**, ao contrário de domínios genéricos como reviews de produtos, onde o **zero-shot** já performa bem e as estratégias adicionais produzem ganhos marginais (Wang e Luo, 2023).

### 2. Justificativa do Domínio ###

2.1 Por que supply chain de peças para caminhões

A escolha do domínio é uma decisão metodológica central.
Modelos de linguagem são treinados em corpora genéricos, bilhões de páginas web, Wikipedia, notícias e fóruns. Como consequência, tarefas de análise de sentimento em linguagem cotidiana já estão amplamente representadas nesses dados. Frases como "o atendimento foi péssimo" ou "o produto superou as expectativas" aparecem em milhares de reviews de e-commerce. O modelo aprende esses padrões durante o pré-treinamento quase sem esforço.

Se o experimento utilizasse um corpus genérico como esse, os três modelos com as três estratégias provavelmente atingiriam acurácias acima de 90% em todas as combinações. O zero-shot já seria suficiente. As diferenças entre estratégias seriam mínimas e o experimento seria metodologicamente pouco informativo.

O domínio técnico especializado resolve esse problema. No supply chain de peças para caminhões, o modelo pode encontrar terminologias que pouco aparece no corpus genérico: ruptura de estoque, first-time fill rate, VMI, homologação OEM. Mais do que vocabulário, encontra ambiguidades semânticas específicas do domínio, a palavra "atingiu", normalmente associada a conquistas no corpus genérico, pode indicar resultado negativo em "o índice de ruptura atingiu 22%".

Herrera-Poyatos et al. (2025) documentam esse fenômeno como **domain drift:** modelos treinados em datasets genéricos falham ao generalizar para aplicações especializadas como finanças, saúde e análise jurídica, pois frequentemente interpretam mal a linguagem técnica e as pistas de sentimento específicas do domínio. O mesmo princípio se aplica ao domínio logístico B2B.

Wang e Luo (2023) demonstraram empiricamente que, em domínios técnicos com sentimento implícito, o CoT produz ganhos expressivos, no dataset financeiro deles, a acurácia subiu de 69,6% com vanilla prompting (também chamado de prompt básico ou padrão) para 83,4% com CoT, uma diferença de 13,8 pontos percentuais que não se replicou nos domínios genéricos de filmes e compras.

O resultado esperado é que as diferenças entre estratégias sejam visíveis e mensuráveis, e é exatamente isso que um benchmark bem desenhado deve medir: não o teto de desempenho do modelo em tarefas triviais, mas a **contribuição marginal de cada estratégia quando o modelo enfrenta um domínio que genuinamente o desafia**.

### 3. Dataset ###

3.1 Composição

O dataset foi construído manualmente com 90 frases do domínio de supply chain de peças para caminhões, distribuídas em três classes balanceadas:

| Classe   | N | Exemplos de terminologia                                               |
|-----------|---|------------------------------------------------------------------------|
| Positivo | 30 | lead time reduzido, certificação OEM, fill rate alto                  |
| Negativo | 30 | ruptura de estoque, atraso, não conformidade, parada de frota         |
| Neutro   | 30 | pedido em processamento, contrato vigente, inventário trimestral      |


As frases foram elaboradas para refletir comunicações reais de operações de supply chain — relatórios de fornecedores, alertas de estoque, registros de recebimento, com terminologia técnica que desafia modelos treinados em corpora genéricos.

Os exemplos few-shot (3 frases, uma por classe) foram mantidos fora do dataset de avaliação para evitar data leakage — critério metodológico adotado também por Pauletti e Silva (2025), que restringiram o LeetCodeEval a problemas publicados após maio de 2023 para forçar raciocínio inédito nos modelos.

3.2 Critério amostral

O tamanho de 30 amostras por classe foi definido pelo intervalo de confiança sobre a acurácia, critério padrão para benchmarks exploratórios de NLP.

A margem de erro de uma acurácia medida sobre N amostras segue a fórmula do intervalo de confiança para proporção binomial:
```
margem = z × sqrt(p × (1 - p) / N)
```

**Por que proporção binomial:** cada frase tem exatamente dois resultados possíveis — acerto (1) ou erro (0). Isso caracteriza uma variável binária, e a distribuição estatística correta para modelar proporções de eventos binários independentes é a distribuição binomial.

**Por que z = 1.96:** é o valor crítico da distribuição normal para 95% de confiança — padrão consolidado na literatura científica. Para 90% seria 1.645; para 99% seria 2.576.

**Por que p = 0.5:** é o pior caso, quando p = 0.5, o produto p × (1-p) é máximo (0.25), gerando a maior margem de erro possível. É uma escolha conservadora: se a margem é aceitável no pior caso, é aceitável em qualquer cenário real.

**Comparativo de tamanhos amostrais:**

| Amostras por classe | Margem de erro (IC 95%) | Interpretação |
|--------------------|-------------------------|---------------|
| 15 | ±25% | Adequado apenas para identificar diferenças muito expressivas entre modelos (> 25 pontos percentuais)|
| 30 (atual) | ±18% | Compromisso entre esforço de anotação e confiabilidade estatística |
| 50 | ±14% | Maior estabilidade para comparação de estratégias de prompt |
| 97 | ±10% | Referência frequentemente utilizada em estudos experimentais e benchmarks de LLMs |

Com 30 amostras por classe, diferenças de acurácia acima de 18 pontos percentuais entre modelos e estratégias são estatisticamente interpretáveis. Diferenças menores podem ser ruído amostral.

O tamanho de 30 por classe equilibra rigor estatístico mínimo com custo operacional razoável: 810 chamadas de API com execução em aproximadamente 10–12 minutos.