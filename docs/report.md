## Relatório Técnico — Benchmark de Estratégias de Prompt Engineering ##
Classificação NLP em Operações Logísticas (Supplay Chain) de peças para veículos pesados

**Projeto:** LLM-Evaluation-Prompts
**Tipo:** Pesquisa exploratória com abordagem quantitativa
**Data:** Maio de 2025

### 1. Objetivo ###

Este relatório documenta as decisões metodológicas do benchmark comparativo de estratégias de prompt engineering aplicadas à tarefa de classificação de NLP, no domínio técnico de supply chain de peças para caminhões.

O experimento investiga a seguinte questão de pesquisa:

> Em um domínio técnico especializado, estratégias estruturadas de prompt (few-shot e chain-of-thought) produzem ganhos de acurácia mensuráveis em relação ao baseline zero-shot, e esse comportamento varia entre provedores de LLM?

A hipótese de trabalho, fundamentada na literatura, é que domínios técnicos com sentimento **implícito** amplificam as diferenças entre estratégias, ao contrário de domínios genéricos como reviews de produtos, onde o **zero-shot** já performa bem e as estratégias adicionais produzem ganhos marginais (Wang e Luo, 2023).

### 2. Justificativa do Domínio ###

2.1 Por que supply chain de peças para caminhões

A escolha do domínio é uma decisão metodológica central.
Modelos de linguagem são treinados em corpora genéricos, bilhões de páginas web, Wikipedia, notícias e fóruns. Como consequência, tarefas de análise de sentimento em linguagem cotidiana já estão amplamente representadas nesses dados. Frases como "o atendimento foi péssimo" ou "o produto superou as expectativas" aparecem em milhares de reviews de e-commerce. O modelo aprende esses padrões durante o pré-treinamento quase sem esforço.

Se o experimento utilizasse um corpus genérico como esse, os três modelos com as três estratégias provavelmente atingiriam acurácias acima de 90% em todas as combinações. O zero-shot já seria suficiente. As diferenças entre estratégias seriam mínimas e o experimento seria metodologicamente pouco informativo.

O domínio técnico especializado resolve esse problema. No supply chain de peças para caminhões, o modelo encontra terminologia que raramente aparece no corpus genérico: ruptura de estoque, first-time fill rate, VMI, desembaraço aduaneiro, homologação OEM. Mais do que vocabulário, encontra ambiguidades semânticas específicas do domínio, a palavra "atingiu", normalmente associada a conquistas no corpus genérico, pode indicar resultado negativo em "o índice de ruptura atingiu 22%".

Herrera-Poyatos et al. (2025) documentam esse fenômeno como **domain drift:** modelos treinados em datasets genéricos falham ao generalizar para aplicações especializadas como finanças, saúde e análise jurídica, pois frequentemente interpretam mal a linguagem técnica e as pistas de sentimento específicas do domínio. O mesmo princípio se aplica ao domínio logístico B2B.

Wang e Luo (2023) demonstraram empiricamente que, em domínios técnicos com sentimento implícito, o CoT produz ganhos expressivos, no dataset financeiro deles, a acurácia subiu de 69,6% com vanilla prompting para 83,4% com CoT, uma diferença de 13,8 pontos percentuais que não se replicou nos domínios genéricos de filmes e compras.

O resultado esperado é que as diferenças entre estratégias sejam visíveis e mensuráveis, e é exatamente isso que um benchmark bem desenhado deve medir: não o teto de desempenho do modelo em tarefas triviais, mas a **contribuição marginal de cada estratégia quando o modelo enfrenta um domínio que genuinamente o desafia**.

### 3. Dataset ###

3.1 Composição

O dataset foi construído manualmente com 90 frases do domínio de supply chain de peças para caminhões, distribuídas em três classes balanceadas:




