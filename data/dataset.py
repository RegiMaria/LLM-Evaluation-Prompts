"""
Dataset fixo: 90 frases do domínio (supply chain de peças para caminhões).
Cada entrada tem texto + label correto (positivo / negativo / neutro).

Critério amostral: 30 por classe → margem de erro ±18% (IC 95%, proporção binomial).
Para entender melhor consultar REPORT.md.

ADR-004 (01-06-2026): 21 das 90 amostras substituídas por borderline cases. Exemplos de maior ambiguidade
semântica para avaliar raciocínio contextual
em vez de reconhecimento de palavras-chave. Ver architecture-decisions.md para justificativa.
"""

DATASET = [
    # POSITIVO (ids 1–30)
    {"id": 1,  "text": "O lote de filtros de óleo chegou dois dias antes do prazo acordado.", "label": "positivo"},
    {"id": 2,  "text": "O fornecedor substituiu as pastilhas de freio com defeito sem custo adicional.", "label": "positivo"},
    {"id": 3,  "text": "As correias dentadas vieram devidamente embaladas e sem avarias.", "label": "positivo"},
    {"id": 4,  "text": "Conseguimos reduzir o estoque de sobressalentes em 18% sem aumentar as paradas.", "label": "positivo"},
    {"id": 5,  "text": "O estoque de segurança dos filtros de óleo foi ampliado para 45 dias de cobertura.", "label": "positivo"},
    {"id": 6,  "text": "A acurácia do inventário subiu para 98% após a implementação do WMS.", "label": "positivo"},
    {"id": 7,  "text": "A cobertura dos rolamentos passou a absorver integralmente as oscilações sazonais de demanda.", "label": "positivo"},
    {"id": 8,  "text": "A parceria com a nova transportadora reduziu o lead time de 7 para 3 dias.", "label": "positivo"},
    {"id": 9,  "text": "Os kits de embreagem estão chegando dentro do prazo e dentro do orçamento.", "label": "positivo"},
    {"id": 10, "text": "O nível de serviço dos kits de embreagem permaneceu acima da meta durante todo o trimestre.", "label": "positivo"},
    {"id": 11, "text": "O novo fornecedor de tensores de correia concluiu o processo de homologação sem ressalvas.", "label": "positivo"},
    {"id": 12, "text": "A qualidade das juntas de culatra importadas superou os testes de bancada.", "label": "positivo"},
    {"id": 13, "text": "Reduzimos o índice de devoluções de peças em 30% com o novo processo de inspeção.", "label": "positivo"},
    {"id": 14, "text": "O tempo médio de atendimento de pedidos de peças caiu de 4h para 1h.", "label": "positivo"},
    {"id": 15, "text": "A revisão dos parâmetros de reposição eliminou a necessidade de compras emergenciais.", "label": "positivo"},
    {"id": 46, "text": "O fornecedor de velas de ignição obteve certificação ISO 9001 e passou na auditoria de qualidade.", "label": "positivo"},
    {"id": 47, "text": "A negociação com o importador reduziu o custo unitário dos bicos injetores em 12%.", "label": "positivo"},
    {"id": 48, "text": "O novo sistema de kanban eliminou as rupturas de estoque de filtros de ar nos últimos 60 dias.", "label": "positivo"},
    {"id": 49, "text": "O fornecedor entregou os amortecedores com laudo técnico e certificado de conformidade.", "label": "positivo"},
    {"id": 50, "text": "A operação manteve o abastecimento das peças críticas mesmo durante a parada programada do fornecedor.", "label": "positivo"},
    {"id": 51, "text": "Os kits de vedação importados passaram em todos os testes de pressão conforme especificação.", "label": "positivo"},
    {"id": 52, "text": "O novo contrato de SLA garante reposição de peças críticas em até 4 horas.", "label": "positivo"},
    {"id": 53, "text": "A taxa de conformidade dos rolamentos recebidos atingiu 99,5% no último trimestre.", "label": "positivo"},
    {"id": 54, "text": "O fornecedor assumiu o frete e entregou o lote de turbinas dentro do prazo revisado.", "label": "positivo"},
    {"id": 55, "text": "O giro de estoque de peças A melhorou de 4x para 7x ao ano após a revisão dos parâmetros.", "label": "positivo"},
    {"id": 56, "text": "A homologação do novo fornecedor de discos de freio foi concluída antes do prazo previsto.", "label": "positivo"},
    {"id": 57, "text": "A disponibilidade de componentes críticos permaneceu estável durante o período de pico operacional.", "label": "positivo"},
    {"id": 58, "text": "A rastreabilidade por QR code reduziu o tempo de localização de peças no almoxarifado em 70%.", "label": "positivo"},
    {"id": 59, "text": "O fornecedor de bombas hidráulicas ampliou a garantia de 12 para 24 meses sem aumento de custo.", "label": "positivo"},
    {"id": 60, "text": "O processo de desembaraço aduaneiro dos eixos cardan foi concluído dois dias antes do previsto.", "label": "positivo"},

    # NEGATIVO (ids 16–30 + 61–75)
    {"id": 16, "text": "O fornecedor entregou amortecedores fora da especificação técnica novamente.", "label": "negativo"},
    {"id": 17, "text": "Faltam bicos injetores no estoque e a frota está parada há três dias.", "label": "negativo"},
    {"id": 18, "text": "O lead time dos eixos cardan passou de 9 para 16 dias após a mudança de operador logístico.", "label": "negativo"},
    {"id": 19, "text": "Recebemos um lote de velas de ignição falsificadas que danificou dois motores.", "label": "negativo"},
    {"id": 20, "text": "O fornecedor revisou novamente a previsão de entrega dos retentores.", "label": "negativo"},
    {"id": 21, "text": "A distribuidora cobrou frete acima do contrato sem aviso prévio.", "label": "negativo"},
    {"id": 22, "text": "Dezesseis turbinas foram reprovadas na inspeção de entrada por corrosão.", "label": "negativo"},
    {"id": 23, "text": "O estoque disponível de peças A ficou abaixo da cobertura mínima definida na política corporativa.", "label": "negativo"},
    {"id": 24, "text": "O fornecedor informou restrição temporária de capacidade para os filtros de ar.", "label": "negativo"},
    {"id": 25, "text": "Três caminhões estão parados por falta de kits de vedação que não chegaram.", "label": "negativo"},
    {"id": 26, "text": "A embalagem inadequada causou danos em 40% dos compressores recebidos.", "label": "negativo"},
    {"id": 27, "text": "O fornecedor não respondeu ao chamado de garantia dos discos de freio com defeito.", "label": "negativo"},
    {"id": 28, "text": "O custo de peças de reposição subiu 35% por conta da variação cambial sem repasse negociado.", "label": "negativo"},
    {"id": 29, "text": "O sistema de pedidos do fornecedor ficou offline por dois dias, travando os reabastecimentos.", "label": "negativo"},
    {"id": 30, "text": "A garantia das buchas de bandeja foi negada por alegação de instalação incorreta.", "label": "negativo"},
    {"id": 61, "text": "O lote de correias dentadas veio com medidas fora de tolerância e precisou ser devolvido integralmente.", "label": "negativo"},
    {"id": 62, "text": "O fornecedor comunicou desabastecimento de pastilhas de freio sem prazo de normalização.", "label": "negativo"},
    {"id": 63, "text": "A transportadora extraviou 30 unidades de rolamentos e não aceitou responsabilidade pelo sinistro.", "label": "negativo"},
    {"id": 64, "text": "O tempo médio de reposição dos filtros de transmissão aumentou após a troca de fornecedor.", "label": "negativo"},
    {"id": 65, "text": "Quatro kits de embreagem instalados apresentaram falha prematura dentro do período de garantia.", "label": "negativo"},
    {"id": 66, "text": "O fornecedor entregou tensores de correia sem o certificado de origem exigido em contrato.", "label": "negativo"},
    {"id": 67, "text": "As bombas de combustível permaneceram indisponíveis durante parte do ciclo de manutenção.", "label": "negativo"},
    {"id": 68, "text": "O índice de peças não conformes recebidas ultrapassou 15% no último lote de juntas.", "label": "negativo"},
    {"id": 69, "text": "O fornecedor repassou reajuste de 28% sem negociação prévia, violando a cláusula contratual.", "label": "negativo"},
    {"id": 70, "text": "Os compressores de ar chegaram sem lacre e com sinais de violação na embalagem.", "label": "negativo"},
    {"id": 71, "text": "O atraso no desembaraço aduaneiro dos retentores gerou multa por inatividade de frota.", "label": "negativo"},
    {"id": 72, "text": "O fornecedor substituiu o material dos retentores sem comunicar a alteração de especificação.", "label": "negativo"},
    {"id": 73, "text": "A auditoria identificou divergência de 18% entre o estoque físico e o sistema, indicando falha de controle.", "label": "negativo"},
    {"id": 74, "text": "O distribuidor entregou amortecedores de linha leve no lugar dos de linha pesada solicitados.", "label": "negativo"},
    {"id": 75, "text": "O prazo revisado para fornecimento das buchas de bandeja ultrapassa a cobertura atual de estoque.", "label": "negativo"},

    # NEUTRO (ids 31–45 + 76–90)
    {"id": 31, "text": "O pedido de 200 filtros de combustível está em processamento.", "label": "neutro"},
    {"id": 32, "text": "O contrato com o fornecedor de pneus vence em dezembro.", "label": "neutro"},
    {"id": 33, "text": "A próxima auditoria de fornecedores está agendada para março.", "label": "neutro"},
    {"id": 34, "text": "O estoque atual de correias poly-V é de 340 unidades.", "label": "neutro"},
    {"id": 35, "text": "O lead time registrado para as juntas permaneceu em 10 dias úteis.", "label": "neutro"},
    {"id": 36, "text": "O catálogo de peças foi atualizado para incluir os modelos 2025.", "label": "neutro"},
    {"id": 37, "text": "A reunião de S&OP com os fornecedores estratégicos ocorre mensalmente.", "label": "neutro"},
    {"id": 38, "text": "O modal de transporte utilizado para peças importadas é aéreo.", "label": "neutro"},
    {"id": 39, "text": "O processo de homologação do novo fornecedor encontra-se na etapa documental.", "label": "neutro"},
    {"id": 40, "text": "O inventário rotativo das peças classe A será executado na próxima semana.", "label": "neutro"},
    {"id": 41, "text": "O departamento de compras recebeu o relatório de consumo de peças do trimestre.", "label": "neutro"},
    {"id": 42, "text": "A previsão de demanda dos amortecedores foi recalculada utilizando dados do último trimestre.", "label": "neutro"},
    {"id": 43, "text": "O processo de importação dos rolamentos permanece sob análise dos órgãos competentes.", "label": "neutro"},
    {"id": 44, "text": "O mínimo de pedido para bombas hidráulicas é de 10 unidades.", "label": "neutro"},
    {"id": 45, "text": "O fornecedor informou mudança de código de peça para os filtros de transmissão.", "label": "neutro"},
    {"id": 76, "text": "O contrato de fornecimento de discos de freio está em fase de renovação.", "label": "neutro"},
    {"id": 77, "text": "O almoxarifado central armazena atualmente 1.240 SKUs de peças para caminhões.", "label": "neutro"},
    {"id": 78, "text": "A política de segurança de estoque define cobertura mínima de 15 dias para peças A.", "label": "neutro"},
    {"id": 79, "text": "O fornecedor de velas de ignição opera com capacidade produtiva de 50.000 unidades por mês.", "label": "neutro"},
    {"id": 80, "text": "A cotação para o lote de tensores de correia foi solicitada a três fornecedores.", "label": "neutro"},
    {"id": 81, "text": "O relatório de spend analysis será utilizado na reunião mensal de suprimentos.", "label": "neutro"},
    {"id": 82, "text": "O fornecedor de retentores está cadastrado na base desde 2019.", "label": "neutro"},
    {"id": 83, "text": "A classificação ABC do estoque de peças é revisada semestralmente.", "label": "neutro"},
    {"id": 84, "text": "O prazo de pagamento negociado com o distribuidor de filtros é de 45 dias.", "label": "neutro"},
    {"id": 85, "text": "O volume de compras de peças de reposição no último exercício foi de R$ 4,2 milhões.", "label": "neutro"},
    {"id": 86, "text": "A especificação técnica dos amortecedores está disponível no portal do fornecedor.", "label": "neutro"},
    {"id": 87, "text": "O processo de recebimento fiscal de peças importadas envolve três etapas de conferência.", "label": "neutro"},
    {"id": 88, "text": "O fornecedor de bombas hidráulicas possui unidade fabril em São Paulo e filial em Curitiba.", "label": "neutro"},
    {"id": 89, "text": "A solicitação de compra dos kits de vedação foi aprovada pelo gestor de manutenção.", "label": "neutro"},
    {"id": 90, "text": "O indicador de cobertura de estoque das correias dentadas passou a ser acompanhado semanalmente.", "label": "neutro"},
]

# Exemplos few-shot (fora do dataset de avaliação)
FEW_SHOT_EXAMPLES = [
    {"text": "O lote de anéis de pistão chegou com documentação completa e dentro do prazo.", "label": "positivo"},
    {"text": "O fornecedor atrasou a entrega das válvulas termostáticas em duas semanas.", "label": "negativo"},
    {"text": "O pedido de retentores está em análise pelo setor de compras.", "label": "neutro"},
]