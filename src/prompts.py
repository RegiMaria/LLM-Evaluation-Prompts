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

