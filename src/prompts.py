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