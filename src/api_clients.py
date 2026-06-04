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
        messages=[          # papéis separados
            {"role": "system", "content": system}, # Instrução
            {"role": "user",   "content": user},   # Pergunta
        ],
        temperature=0, # O quanto o modelo !arrisca nas respotas (0-1)
        max_tokens=50, # Limita o tamanho da resposta
    )
    elapsed = (time.time() - t0) * 1000 # tempo DEPOIS menos ANTES = duração- A subtração dá a duração em segundos — multiplicar por 1000 converte pra milissegundos.
    text = response.choices[0].message.content.strip().lower()
    return text, round(elapsed, 1)

# ── Gemini ────────────────────────────────────────────────────────────────────
# Gemini não tem esse conceito de campos distintos (role: system) 
# Ela espera um único texto. Por isso tem que precisa juntar tudo manualmente antes de enviar
def call_gemini(system: str, user: str, model: str = "gemini-1.5-flash") -> tuple[str, float]:
    import google.generativeai as genai

    genai.configure(api_key=os.environ["GEMINI_API_KEY"])
    full_prompt = f"{system}\n\n{user}"
    gen_model = genai.GenerativeModel(model) # Primeiro instancia /cria o objeto do modelo
    t0 = time.time()
    response = gen_model.generate_content(       # Chama o método
        full_prompt,
        generation_config=genai.types.GenerationConfig(
            temperature=0,
            max_output_tokens=50,
        ),
    )
    elapsed = (time.time() - t0) * 1000
    text = response.text.strip().lower()
    return text, round(elapsed, 1)

# ── Anthropic ─────────────────────────────────────────────────────────────────


# ── Dispatcher ────────────────────────────────────────────────────────────────

PROVIDERS = {
    "openai":    call_openai,
    "gemini":    call_gemini,
    "anthropic": call_anthropic,
}