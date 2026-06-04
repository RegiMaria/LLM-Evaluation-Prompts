"""
03 - fazer esse 03-06-2026
Clientes unificados para OpenAI, Gemini e Anthropic.
As chaves são lidas de variáveis de ambiente.
"""

import os
import time


# ── OpenAI ────────────────────────────────────────────────────────────────────

def call_openai(system: str, user: str, model: str = "gpt-4o-mini") -> tuple[str, float]:
    from openai import OpenAI

    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    t0 = time.time() # anota o momento ANTES da chamada à API
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system},
            {"role": "user",   "content": user},
        ],
        temperature=0, # O quanto o modelo !arrisca nas respotas (0-1)
        max_tokens=50, # Limita o tamanho da resposta
    )
    elapsed = (time.time() - t0) * 1000 # tempo DEPOIS menos ANTES = duração- A subtração dá a duração em segundos — multiplicar por 1000 converte pra milissegundos.
    text = response.choices[0].message.content.strip().lower()
    return text, round(elapsed, 1)

# ── Gemini ────────────────────────────────────────────────────────────────────


# ── Anthropic ─────────────────────────────────────────────────────────────────


# ── Dispatcher ────────────────────────────────────────────────────────────────

PROVIDERS = {
    "openai":    call_openai,
    "gemini":    call_gemini,
    "anthropic": call_anthropic,
}