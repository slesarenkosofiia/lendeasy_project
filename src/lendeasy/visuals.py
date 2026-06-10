
import os
import numpy as np
import matplotlib.pyplot as plt

def ensure_dir(path: str):
    os.makedirs(path, exist_ok=True)

def plot_cashflow(years, cash_flows, discounted_cash_flows, output_path="figures/cashflow.png"):
    ensure_dir(os.path.dirname(output_path))
    cumulative_discounted = np.cumsum(discounted_cash_flows)

    plt.figure(figsize=(10, 6))
    plt.plot(years, cash_flows, marker="o", label="Обычный денежный поток")
    plt.plot(years, discounted_cash_flows, marker="o", label="Дисконтированный поток")
    plt.plot(years, cumulative_discounted, marker="o", label="Кумулятивный дисконтированный поток")
    plt.axhline(0, linestyle="--", linewidth=1)
    plt.title("Денежные потоки проекта LendEasy")
    plt.xlabel("Год")
    plt.ylabel("тыс. руб.")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_path, dpi=160)
    plt.close()

def plot_tornado(base_npv, low_high_by_factor, output_path="figures/tornado.png"):
    ensure_dir(os.path.dirname(output_path))
    labels = list(low_high_by_factor.keys())
    lows = [low_high_by_factor[k][0] for k in labels]
    highs = [low_high_by_factor[k][1] for k in labels]

    widths_low = [base_npv - low for low in lows]
    widths_high = [high - base_npv for high in highs]

    plt.figure(figsize=(10, 5))
    y_pos = np.arange(len(labels))
    plt.barh(y_pos, widths_low, left=lows, label="-30%")
    plt.barh(y_pos, widths_high, left=base_npv, label="+30%")
    plt.axvline(base_npv, linestyle="--", linewidth=1, label=f"Базовый NPV = {base_npv:,.0f}")
    plt.yticks(y_pos, labels)
    plt.xlabel("NPV, тыс. руб.")
    plt.title("Торнадо-диаграмма чувствительности NPV")
    plt.legend()
    plt.grid(True, axis="x", alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_path, dpi=160)
    plt.close()

def plot_monte_carlo(npv_results, threshold=500, output_path="figures/monte_carlo.png"):
    ensure_dir(os.path.dirname(output_path))
    plt.figure(figsize=(10, 6))
    plt.hist(npv_results, bins=50)
    plt.axvline(threshold, linestyle="--", linewidth=2, label=f"Порог NPV = {threshold} тыс. руб.")
    plt.axvline(np.mean(npv_results), linestyle=":", linewidth=2, label=f"Среднее = {np.mean(npv_results):,.0f}")
    plt.title("Монте-Карло: распределение NPV")
    plt.xlabel("NPV, тыс. руб.")
    plt.ylabel("Количество симуляций")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_path, dpi=160)
    plt.close()
