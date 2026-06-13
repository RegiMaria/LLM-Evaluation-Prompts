"""
04 - Análise dos resultados do benchmark.
Lê o CSV gerado por run_benchmark.py e produz:
  - Tabela de acurácia por classe (positivo/negativo/neutro)
  - Tabela de consistência (desvio padrão do tempo)
  - Gráficos de barra (se matplotlib disponível -  ainda vamos decidir)

Uso:
    python analyze_results.py results/benchmark_YYYYMMDD_HHMMSS.csv
"""

import csv
import sys
import statistics
from collections import defaultdict
from pathlib import Path


def load_csv(path: str) -> list[dict]:
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def accuracy_table(rows: list[dict]) -> None:
    """Acurácia geral e por classe para cada (provider, strategy)."""
    combos = sorted({(r["provider"], r["strategy"]) for r in rows})
    labels = ["positivo", "negativo", "neutro"]

    print(f"\n{'='*80}")
    print(f"{'ACURÁCIA POR CLASSE':^80}")
    print(f"{'='*80}")
    print(f"{'Provedor':12} {'Estratégia':20} {'Geral':>7}", end="")
    for lbl in labels:
        print(f" {lbl:>10}", end="")
    print()
    print("-" * 80)

    for prov, strat in combos:
        subset = [r for r in rows if r["provider"] == prov and r["strategy"] == strat]
        geral  = sum(int(r["correct"]) for r in subset) / len(subset) * 100
        print(f"{prov:12} {strat:20} {geral:6.1f}%", end="")
        for lbl in labels:
            sub_lbl = [r for r in subset if r["true_label"] == lbl]
            if sub_lbl:
                acc = sum(int(r["correct"]) for r in sub_lbl) / len(sub_lbl) * 100
                print(f" {acc:9.1f}%", end="")
            else:
                print(f" {'N/A':>9}", end="")
        print()
    print("=" * 80)

""" 
Acurácia geral: quantas classificações o modelo acertou no total, independente da classe.
Acurácia por classe: quantas frases positivo ele acertou, quantas negativo, quantas neutro. 
Isso é importante porque um modelo pode ter 80% geral mas errar sistematicamente todas as frases neutro. 
A a acurácia geral esconde esse problema.

Por que isso importa noeexperimento
Fizemos borderline cases no dataset (ADR-003, ADR-004), que são frases de fronteira que tendem a ser mais difíceis.
A coluna por classe vai revelar se o CoT realmente ajudou nesses casos ou se o modelo ainda erra sistematicamente as frases neutro,
que costumam ser as mais ambíguas.
"""
def consistency_table(rows: list[dict]) -> None:
    """Tempo médio e desvio padrão por (provider, strategy)."""
    combos = sorted({(r["provider"], r["strategy"]) for r in rows})

    print(f"\n{'='*65}")
    print(f"{'CONSISTÊNCIA (TEMPO DE RESPOSTA)':^65}")
    print(f"{'='*65}")
    print(f"{'Provedor':12} {'Estratégia':20} {'Média (ms)':>12} {'σ (ms)':>10} {'Min':>8} {'Max':>8}")
    print("-" * 65)

    for prov, strat in combos:
        times = [
            float(r["elapsed_ms"])
            for r in rows
            if r["provider"] == prov and r["strategy"] == strat and float(r["elapsed_ms"]) > 0
        ]
        if not times:
            continue
        avg = statistics.mean(times)
        std = statistics.stdev(times) if len(times) > 1 else 0
        print(f"{prov:12} {strat:20} {avg:11.0f} {std:9.0f} {min(times):7.0f} {max(times):7.0f}")
    print("=" * 65)
    print("\nσ menor = modelo mais previsível e consistente")


"""
Mede a consistência de cada modelo, o quanto o tempo de resposta varia entre chamadas.
O desvio padrão (σ) diz: se a média é 800ms mas o σ é 600ms, o modelo é imprevisível, às vezes responde em 200ms, às vezes em 1400ms.
Se o σ é 50ms, ele é consistente.
Isso e importnte pro experimento porque tempo instável pode indicar sobrecarga do servidor do provedor, throttling, 
ou comportamento diferente pra prompts longos (como CoT) vs curtos (zero-shot).
"""

def confusion_summary(rows: list[dict]) -> None:
    """Erros mais comuns: onde cada modelo/estratégia erra. mostra onde cada modelo erra, não só quanto"""
    combos = sorted({(r["provider"], r["strategy"]) for r in rows})
    labels = ["positivo", "negativo", "neutro"]

    print(f"\n{'='*65}")
    print(f"{'ERROS POR CLASSE (falsos negativos por categoria)':^65}")
    print(f"{'='*65}")

    for prov, strat in combos:
        subset = [r for r in rows if r["provider"] == prov and r["strategy"] == strat
                  and int(r["correct"]) == 0 and r["pred_label"] != "erro"]
        if not subset:
            print(f"{prov}/{strat}: nenhum erro!")
            continue
        print(f"\n{prov} / {strat} — {len(subset)} erros:")
        for lbl in labels:
            wrong = [r for r in subset if r["true_label"] == lbl]
            if wrong:
                pred_counts = defaultdict(int)
                for r in wrong:
                    pred_counts[r["pred_label"]] += 1
                detail = ", ".join(f"{k}→{v}x" for k, v in pred_counts.items())
                print(f"  {lbl:10}: {len(wrong)} erros ({detail})")

"""
Para cada combinação provedor + estratégia, lista os erros agrupados por classe verdadeira e
mostra pra qual classe o modelo errou. muito mais útil pra entender o comportamento do modelo.
No contexto de borderline cases, verificar se os erros se concentram em neutro, frases onde o modelo
"chuta" positivo ou negativo quando o correto era neutro. Voltar e olhar pra hipótese do ADR-004.
"""