## Architecture Decisions

### ADR-001: Escolha do domínio

**Contexto**

A maioria dos benchmarks de análise de sentimento utiliza reviews de produtos, filmes ou redes sociais.

Esses domínios possuem forte presença nos dados de treinamento dos modelos e normalmente apresentam palavras explicitamente positivas ou negativas.

**Decisão**

Utilizar o domínio de supply chain de peças para caminhões.

**Justificativa**

O domínio apresenta:

Terminologia técnica especializada
Linguagem B2B
Indicadores operacionais
Menor presença em datasets públicos

Exemplos:

lead time
fill rate
homologação de fornecedor
ruptura de estoque
desembaraço aduaneiro
cobertura de estoque
Consequências

A tarefa exige compreensão do contexto operacional além do reconhecimento de palavras emocionalmente carregadas.


### ADR-002: Tamanho do dataset

Contexto

Benchmarks maiores aumentam a confiabilidade estatística, mas também elevam o custo de execução.

Decisão

Utilizar 90 amostras:

30 positivas
30 negativas
30 neutras
Justificativa

Para N = 30 por classe:

intervalo de confiança de aproximadamente ±18%
custo operacional compatível com execução em APIs comerciais
810 chamadas por execução completa
Consequências

O benchmark é adequado para identificar tendências entre modelos e estratégias.

Não deve ser interpretado como evidência definitiva de superioridade entre modelos.

## ADR-003: Introdução de exemplos de fronteira (Borderline Cases)

**Contexto**

A primeira versão do dataset contém predominantemente exemplos com polaridade explícita.

Exemplos:

Positivo:

"reduziu o custo"
"atingiu 99,5%"
"entregou antes do prazo"

Negativo:

"frota parada"
"falha prematura"
"ruptura de estoque"

Esses exemplos são facilmente classificados por modelos modernos.

Decisão

Substituir aproximadamente **7 amostras** por exemplos de polaridade implícita, por classe.

Objetivo

Avaliar a capacidade dos modelos de inferir sentimento operacional a partir do contexto de supply chain.

Exemplos

Positivo:

"O estoque de segurança dos filtros de óleo foi ampliado para 45 dias de cobertura."

Negativo:

"O prazo revisado para fornecimento das buchas de bandeja ultrapassa a cobertura atual de estoque."

Neutro:

"O indicador de cobertura de estoque das correias dentadas passou a ser acompanhado semanalmente."

Consequências

O benchmark deixa de medir apenas detecção de palavras positivas e negativas.

Passa a avaliar:

compreensão contextual
conhecimento operacional implícito
robustez das estratégias de prompt
capacidade de raciocínio em domínio especializado
Impacto esperado

Maior separação de desempenho entre:

Zero-shot
Few-shot
Chain-of-Thought

Aumentando o valor analítico dos resultados.

## ADR-004: Designe decisions -Introdução de exemplos de fronteira (borderline cases)

**Data: 01-06-2026**

Durante a revisão do dataset, 21 das 90 amostras (23%) foram substituídas por exemplos de maior ambiguidade semântica.

Objetivo:
- Reduzir dependência de palavras explicitamente positivas ou negativas.
- Avaliar a capacidade dos modelos de interpretar contexto operacional de supply chain.
- Aumentar a sensibilidade do benchmark para diferenças entre estratégias de prompt engineering.

Exemplos removidos:
- "reduziu o lead time de 7 para 3 dias"
- "atraso na importação"
- "pedido em processamento"

Exemplos adicionados:
- "A disponibilidade de componentes críticos permaneceu estável durante o período de pico operacional."
- "O estoque disponível de peças A ficou abaixo da cobertura mínima definida na política corporativa."
- "O processo de homologação do novo fornecedor encontra-se na etapa documental."

Resultado:
O benchmark deixa de avaliar apenas reconhecimento de palavras-chave e passa a avaliar interpretação de conceitos de supply chain, planejamento de estoque, capacidade operacional, reposição, homologação e nível de serviço.

 ## ADR-005: Evolução futura

 Evolução futura do benchmark

A versão atual do dataset incorpora aproximadamente 23% de exemplos de maior complexidade semântica, distribuídos entre as três classes de sentimento.

Esses exemplos foram projetados para reduzir a dependência de pistas lexicais explícitas e exigir interpretação de conceitos operacionais de supply chain, como nível de serviço, cobertura de estoque, capacidade produtiva, trade-offs de custo e desempenho logístico.

Como evolução futura, pretende-se introduzir uma *estratificação formal de dificuldade*, classificando cada amostra como:

Standard
Borderline

Essa estrutura permitirá medir separadamente o desempenho dos modelos em exemplos convencionais e em casos de fronteira, possibilitando análises de robustez semântica e comparação da contribuição marginal de estratégias como Few-Shot e Chain-of-Thought em cenários de maior complexidade interpretativa.