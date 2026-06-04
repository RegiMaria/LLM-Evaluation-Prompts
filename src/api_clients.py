"""
03 - fazer esse 03-06-2026
Clientes unificados para OpenAI, Gemini e Anthropic.
As chaves são lidas de variáveis de ambiente.
"""

import os
import time


# ── Dispatcher ────────────────────────────────────────────────────────────────

PROVIDERS = {
    "openai":    call_openai,
    "gemini":    call_gemini,
    "anthropic": call_anthropic,
}