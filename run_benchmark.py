"""
03 - Benchmark de Prompt Engineering — LLM-Evaluation-Prompts
Compara 3 estratégias (zero-shot, few-shot, CoT) × 3 provedores (OpenAI, Gemini, Anthropic)
na tarefa de classificação de sentimento em supply chain de peças para caminhões.

Uso:
    export OPENAI_API_KEY=...
    export GEMINI_API_KEY=...
    export ANTHROPIC_API_KEY=...
    python run_benchmark.py
"""

import csv
import os
import sys
import time
from datetime import datetime
from pathlib import Path

# Apontando onde está - imports relativos sem instalar como pacote
ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT))

from data.dataset import DATASET
from src.prompts import STRATEGIES
from src.api_clients import PROVIDERS

# ── Configuração ──────────────────────────────────────────────────────────────

VALID_LABELS = {"positivo", "negativo", "neutro"}

# Para CoT o modelo pode escrever mais antes da resposta final 
# extraímos apenas a última palavra válida da resposta.
def extract_label(raw: str) -> str:
    """Extrai o label de sentimento do texto, mesmo que o modelo escreva mais."""
    raw = raw.strip().lower()
    # Procura a última ocorrência de um label válido
    for word in reversed(raw.replace("\n", " ").split()):
        word_clean = word.strip(".,;:!?\"'()")
        if word_clean in VALID_LABELS:
            return word_clean
    # Fallback: verifica se algum label aparece em qualquer ponto
    for label in VALID_LABELS:
        if label in raw:
            return label
    return "inválido"


# ── Pipeline principal ────────────────────────────────────────────────────────

def run_benchmark(
    providers: list[str] = list(PROVIDERS.keys()),
    strategies: list[str] = list(STRATEGIES.keys()),
    output_dir: str = "results",
    delay_between_calls: float = 0.5,   # segundos entre chamadas (isso evita rate limit) pode ser preciso ajustar
):
    results = []
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = Path(output_dir) / f"benchmark_{timestamp}.csv"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    total = len(providers) * len(strategies) * len(DATASET)
    done  = 0

    print(f"\n{'='*60}")
    print(f"Benchmark iniciado: {timestamp}")
    print(f"Provedores  : {providers}")
    print(f"Estratégias : {strategies}")
    print(f"Amostras    : {len(DATASET)}")
    print(f"Total calls : {total}")
    print(f"{'='*60}\n")

    for provider_name in providers:
        call_fn = PROVIDERS[provider_name]

        for strategy_name in strategies:
            build_prompt = STRATEGIES[strategy_name]

            correct = 0
            errors  = 0
            times   = []

            for item in DATASET:
                done += 1
                text       = item["text"]
                true_label = item["label"]

                try:
                    system, user = build_prompt(text)
                    raw_response, elapsed_ms = call_fn(system, user)
                    pred_label = extract_label(raw_response)
                    is_correct = (pred_label == true_label)
                    if is_correct:
                        correct += 1

                    times.append(elapsed_ms)
                    status = "✓" if is_correct else "✗"
                    print(
                        f"[{done:3d}/{total}] {provider_name:10s} | {strategy_name:18s} | "
                        f"id={item['id']:2d} | esperado={true_label:8s} | "
                        f"obtido={pred_label:8s} | {elapsed_ms:6.0f}ms {status}"
                    )

                    results.append({
                        "provider":       provider_name,
                        "strategy":       strategy_name,
                        "sample_id":      item["id"],
                        "text":           text,
                        "true_label":     true_label,
                        "pred_label":     pred_label,
                        "correct":        int(is_correct),
                        "elapsed_ms":     elapsed_ms,
                        "raw_response":   raw_response[:200],   # trunca para o CSV
                    })

                except Exception as exc:
                    errors += 1
                    print(f"[{done:3d}/{total}] ERRO em {provider_name}/{strategy_name}/id={item['id']}: {exc}")
                    results.append({
                        "provider":       provider_name,
                        "strategy":       strategy_name,
                        "sample_id":      item["id"],
                        "text":           text,
                        "true_label":     true_label,
                        "pred_label":     "erro",
                        "correct":        0,
                        "elapsed_ms":     0,
                        "raw_response":   str(exc)[:200],
                    })

                time.sleep(delay_between_calls)

            # Sumário do bloco atual
            avg_time  = sum(times) / len(times) if times else 0
            accuracy  = correct / len(DATASET) * 100
            print(
                f"\n  ▶ {provider_name} / {strategy_name}: "
                f"acurácia={accuracy:.1f}% | tempo médio={avg_time:.0f}ms | erros={errors}\n"
            )

# ── Salva CSV completo ────────────────────────────────────────────────────
# pega todos os resultados que ficaram na memória durante o benchmark e salva num arquivo CSV
   
    fieldnames = [
        "provider", "strategy", "sample_id", "text",
        "true_label", "pred_label", "correct", "elapsed_ms", "raw_response",
    ]
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames) # Cada linha do results é um dict
        writer.writeheader()
        writer.writerows(results)

    print(f"\nCSV salvo em: {output_path}")