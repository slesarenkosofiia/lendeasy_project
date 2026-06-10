
import os
import sys
import numpy as np

sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from lendeasy.calculations import (
    DISCOUNT_RATE,
    YEARS,
    load_data,
    prepare_arrays,
    discount_factors,
    npv,
    profitability_index,
    irr_bisection,
    tco,
    support_share,
    calculate_with_changes,
    sensitivity_table,
    monte_carlo,
)
from lendeasy.visuals import plot_cashflow, plot_tornado, plot_monte_carlo
from lendeasy.report import make_report

def main():
    os.makedirs("figures", exist_ok=True)
    os.makedirs("reports", exist_ok=True)

    df = load_data("data/variant3_data.csv")
    costs, benefits, total_costs, total_benefits, cash_flows = prepare_arrays(df)

    dfactors = discount_factors(DISCOUNT_RATE)
    discounted_cash_flows = cash_flows * dfactors

    base_npv = npv(cash_flows, DISCOUNT_RATE)
    pi = profitability_index(total_benefits, total_costs, DISCOUNT_RATE)
    irr = irr_bisection(cash_flows)
    total_tco = tco(total_costs)
    support_percent = support_share(costs, total_costs)

    sens = sensitivity_table(df)

    low_high_by_factor = {
        "Юридические затраты": (
            calculate_with_changes(df, legal_change=-0.30),
            calculate_with_changes(df, legal_change=0.30),
        ),
        "Комиссионный доход": (
            calculate_with_changes(df, commission_change=-0.30),
            calculate_with_changes(df, commission_change=0.30),
        ),
    }

    npv_results, probability_above_500 = monte_carlo(df, iterations=10000, seed=42)

    plot_cashflow(YEARS, cash_flows, discounted_cash_flows, "figures/cashflow.png")
    plot_tornado(base_npv, low_high_by_factor, "figures/tornado.png")
    plot_monte_carlo(npv_results, threshold=500, output_path="figures/monte_carlo.png")

    metrics = {
        "npv": base_npv,
        "pi": pi,
        "irr": irr,
        "tco": total_tco,
        "support_share": support_percent,
        "probability_above_500": probability_above_500,
    }

    sensitivity_html = sens.copy()
    sensitivity_html["change"] = (sensitivity_html["change"] * 100).round(0).astype(int).astype(str) + "%"
    sensitivity_html["npv"] = sensitivity_html["npv"].round(2)
    sensitivity_html = sensitivity_html.rename(columns={
        "factor": "Фактор",
        "change": "Изменение",
        "npv": "NPV, тыс. руб."
    }).to_html(index=False)

    make_report(metrics, sensitivity_html, "reports/lendeasy_report.html")

    print("Готово!")
    print(f"NPV: {base_npv:,.2f} тыс. руб.")
    print(f"PI: {pi:.3f}")
    print(f"IRR: {irr * 100:.2f}%")
    print(f"TCO: {total_tco:,.0f} тыс. руб.")
    print(f"Доля поддержки в TCO: {support_percent:.2f}%")
    print(f"Вероятность NPV > 500 тыс. руб.: {probability_above_500:.2f}%")
    print("Созданы файлы:")
    print(" - figures/cashflow.png")
    print(" - figures/tornado.png")
    print(" - figures/monte_carlo.png")
    print(" - reports/lendeasy_report.html")

if __name__ == "__main__":
    main()
