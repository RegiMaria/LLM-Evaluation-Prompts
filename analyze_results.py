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
