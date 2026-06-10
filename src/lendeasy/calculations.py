
import numpy as np
import pandas as pd

DISCOUNT_RATE = 0.11
YEARS = np.array([0, 1, 2, 3], dtype=float)

def load_data(path: str = "data/variant3_data.csv") -> pd.DataFrame:
    return pd.read_csv(path)

def prepare_arrays(df: pd.DataFrame):
    year_cols = ["year0", "year1", "year2", "year3"]
    costs = df[df["category"] == "cost"].set_index("item")[year_cols].astype(float)
    benefits = df[df["category"] == "benefit"].set_index("item")[year_cols].astype(float)
    total_costs = costs.sum(axis=0).to_numpy()
    total_benefits = benefits.sum(axis=0).to_numpy()
    cash_flows = total_benefits - total_costs
    return costs, benefits, total_costs, total_benefits, cash_flows

def discount_factors(rate: float = DISCOUNT_RATE) -> np.ndarray:
    return 1 / (1 + rate) ** YEARS

def npv(cash_flows: np.ndarray, rate: float = DISCOUNT_RATE) -> float:
    return float(np.sum(cash_flows * discount_factors(rate)))

def profitability_index(total_benefits: np.ndarray, total_costs: np.ndarray, rate: float = DISCOUNT_RATE) -> float:
    df = discount_factors(rate)
    pv_benefits = float(np.sum(total_benefits * df))
    pv_costs = float(np.sum(total_costs * df))
    return pv_benefits / pv_costs

def irr_bisection(cash_flows: np.ndarray, low: float = -0.99, high: float = 2.0, iterations: int = 200) -> float:
    """IRR без внешних финансовых библиотек. Возвращает ставку, при которой NPV приблизительно равен 0."""
    def f(rate):
        return npv(cash_flows, rate)

    f_low, f_high = f(low), f(high)
    if f_low * f_high > 0:
        return float("nan")

    for _ in range(iterations):
        mid = (low + high) / 2
        f_mid = f(mid)
        if f_low * f_mid <= 0:
            high = mid
            f_high = f_mid
        else:
            low = mid
            f_low = f_mid
    return (low + high) / 2

def tco(total_costs: np.ndarray) -> float:
    return float(np.sum(total_costs))

def support_share(costs: pd.DataFrame, total_costs: np.ndarray) -> float:
    support_total = float(costs.loc["Служба поддержки"].sum())
    return support_total / tco(total_costs) * 100

def calculate_with_changes(df: pd.DataFrame, legal_change: float = 0.0, commission_change: float = 0.0, rate: float = DISCOUNT_RATE):
    costs, benefits, total_costs, total_benefits, cash_flows = prepare_arrays(df)

    legal_base = costs.loc["Юридическое сопровождение"].to_numpy()
    commission_base = benefits.loc["Комиссия"].to_numpy()

    adjusted_costs = total_costs - legal_base + legal_base * (1 + legal_change)
    adjusted_benefits = total_benefits - commission_base + commission_base * (1 + commission_change)
    adjusted_cash_flows = adjusted_benefits - adjusted_costs

    return npv(adjusted_cash_flows, rate)

def sensitivity_table(df: pd.DataFrame):
    changes = [-0.30, -0.15, 0.0, 0.15, 0.30]
    rows = []
    for change in changes:
        rows.append({
            "factor": "Юридические затраты",
            "change": change,
            "npv": calculate_with_changes(df, legal_change=change)
        })
        rows.append({
            "factor": "Комиссионный доход",
            "change": change,
            "npv": calculate_with_changes(df, commission_change=change)
        })
    return pd.DataFrame(rows)

def monte_carlo(df: pd.DataFrame, iterations: int = 10000, seed: int = 42):
    rng = np.random.default_rng(seed)
    results = []
    for _ in range(iterations):
        legal_change = rng.uniform(-0.40, 0.20)
        commission_change = rng.uniform(-0.50, 0.30)
        results.append(calculate_with_changes(df, legal_change=legal_change, commission_change=commission_change))
    results = np.array(results)
    probability_above_500 = float(np.mean(results > 500) * 100)
    return results, probability_above_500
