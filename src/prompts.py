"""
02 - Módulo de estratégias de prompt engineering.

ADR-006 (01-06-2026): CoT atualizado com passo de raciocínio sobre trade-offs
operacionais, alinhando o prompt à presença de borderline cases no dataset
(ADR-003, ADR-004). Ver architecture-decisions.md para justificativa.

"""

from data.dataset import FEW_SHOT_EXAMPLES


TASK_INSTRUCTION = (
    "Você é um especialista em análise de supply chain de peças para caminhões. "
    "Classifique o SENTIMENTO da frase abaixo como exatamente uma dessas opções: "
    "positivo, negativo ou neutro. "
    "Responda SOMENTE com uma das três palavras, sem pontuação nem explicação."
)

def zero_shot(text: str) -> tuple[str, str]:
    """
    Tuple - quem recebe não deve modificar
    Zero-shot: instrução direta, sem exemplos.Sem demonstrações de como responder.
    O modelo precisa inferir sozinho o que fazer.
    Serve como baseline - se few-shot e CoT não superarem o zero-shot
    de forma significativa (>18 pp), o modelo já generaliza bem para
    o domínio sem auxílio.
    Isto é, Se as técnicas avançadas não melhoram muito, a conclusão é:
    o modelo já entende supply chain de caminhões por conta própria, sem precisar de exemplos ou raciocínio guiado
    """
    system = TASK_INSTRUCTION
    user = f"Frase: {text}\nSentimento:"
    return system, user

def few_shot(text: str) -> tuple[str, str]:
    """
    Few-shot: 3 exemplos demonstrativos no prompt antes da frase alvo.
    Os exemplos ancoram o modelo na terminologia e no estilo do domínio.
    Baseado na Figura 1 do trabalho de Pauletti & Silva(2025) e em Wang e Luo (2023),
    que demonstraram ganhos expressivos de few-shot em domínios especializados.

    Os exemplos few-shot são mantidos fora do dataset de avaliação
    para evitar data leakage.
    """
    system = TASK_INSTRUCTION
    examples = "\n".join(
        f"Frase: {ex['text']}\nSentimento: {ex['label']}"
        for ex in FEW_SHOT_EXAMPLES
    )
    user = f"{examples}\n\nFrase: {text}\nSentimento:"
    return system, user

def chain_of_thought(text: str) -> tuple[str, str]:
    """
    Chain-of-thought: decomposição passo a passo antes da resposta final.
    Baseado na Figura 2 do trabalho de Pauletti & Silva (2025) e em Wei et al. (2022).

    ADR-006: o passo 3 foi adicionado para cobrir borderline cases (ADR-003,
    ADR-004),frases onde a polaridade depende de trade-offs operacionais
    e não pode ser inferida apenas por palavras-chave. 
    Exemplo:
    "A ruptura foi evitada mediante compra emergencial com custo 40% maior."
    Sem o passo de trade-off, o modelo tende a classificar como positivo
    (ruptura evitada) ignorando o custo adicional de 40%.

    A resposta FINAL deve ser apenas a palavra do sentimento.
    """
    system = (
        "Você é um especialista em análise de supply chain de peças para caminhões. "
        "Para classificar o sentimento de uma frase, siga EXATAMENTE estes passos:\n"
        "1. Identifique as palavras-chave que indicam ocorrências positivas, "
        "negativas ou neutras.\n"
        "2. Avalie se há impacto operacional direto (atrasos, falhas, "
        "economias, melhorias, rupturas, conformidade).\n"
        "3. Considere se existe um trade-off: um resultado aparentemente "
        "positivo pode ter consequência negativa para a operação, e vice-versa. "
        "Avalie o impacto líquido para o negócio.\n"
        "4. Decida o sentimento predominante considerando o contexto "
        "operacional completo, não apenas palavras isoladas.\n"
        "5. Escreva na última linha SOMENTE a palavra final: "
        "positivo, negativo ou neutro."
    )
    user = (
        f"Frase: {text}\n\n"
        "Pense passo a passo e escreva sua análise. "
        "Na última linha, escreva apenas a palavra do sentimento."
    )
    return system, user


STRATEGIES = {
    "zero_shot": zero_shot,
    "few_shot": few_shot,
    "chain_of_thought": chain_of_thought,
}