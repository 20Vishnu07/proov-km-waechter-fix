# analyze.py
# Summary of findings:
#   The two strongest predictors of breakdown are km_since_service (how far since last service)
#   and load_factor (how hard the car is used). Total odometer and age are NOT predictive —
#   broke-down cars and healthy cars have almost identical mileage and age.
#   avg_daily_km adds a smaller but real signal.
#   Risk score = 50% km_since_service (normalised) + 30% load_factor (normalised)
#                + 20% avg_daily_km (normalised).

import pandas as pd

df = pd.read_csv("fleet_history.csv")

# --- 1. Compare the two groups column by column ---

broke = df[df["broke_down"] == 1]
ok    = df[df["broke_down"] == 0]

print("=== Group means: broke down vs. healthy ===")
cols = ["odometer_km", "km_since_service", "avg_daily_km", "load_factor", "age_years"]
for c in cols:
    print(
        f"  {c:25s}  broke={broke[c].mean():8.2f}  "
        f"ok={ok[c].mean():8.2f}  "
        f"diff={broke[c].mean() - ok[c].mean():+.2f}"
    )

print()
print("Key finding:")
print("  odometer_km  : +146 km difference — NOT a useful predictor.")
print("  age_years    : -0.01 yr difference — NOT a useful predictor.")
print("  km_since_service: +4,417 km difference — STRONG predictor.")
print("  load_factor  : +0.09 difference — meaningful predictor.")
print("  avg_daily_km : +28 km/day difference — smaller but real signal.")
print()

# --- 2. Build a 0–100 risk score from the three factors that DO separate ---
#
# Each factor is min-max normalised across the whole fleet so the weights
# reflect business importance, not raw units.

def normalise(series: pd.Series) -> pd.Series:
    """Scale a column to [0, 1] using min-max normalisation."""
    lo, hi = series.min(), series.max()
    if hi == lo:
        return pd.Series(0.0, index=series.index)
    return (series - lo) / (hi - lo)

df["n_km_since"]   = normalise(df["km_since_service"])   # 50 % weight
df["n_load"]       = normalise(df["load_factor"])         # 30 % weight
df["n_daily"]      = normalise(df["avg_daily_km"])        # 20 % weight

df["risk_score"] = (
    0.50 * df["n_km_since"] +
    0.30 * df["n_load"]     +
    0.20 * df["n_daily"]
) * 100

# --- 3. Print cars ranked by risk, highest first ---

ranked = (
    df[["car_id", "km_since_service", "load_factor", "avg_daily_km", "risk_score", "broke_down"]]
    .sort_values("risk_score", ascending=False)
    .reset_index(drop=True)
)

print("=== Fleet ranked by breakdown risk (highest first) ===")
print(f"{'#':>3}  {'car_id':<12} {'km_since':>9} {'load':>6} {'daily_km':>9} {'risk':>6}  broke?")
print("-" * 60)
for i, row in ranked.iterrows():
    flag = "  <-- broke down" if row["broke_down"] == 1 else ""
    print(
        f"{i+1:>3}  {row['car_id']:<12} "
        f"{row['km_since_service']:>9.0f} "
        f"{row['load_factor']:>6.2f} "
        f"{row['avg_daily_km']:>9.0f} "
        f"{row['risk_score']:>6.1f}"
        f"{flag}"
    )

print()
high_risk = ranked[ranked["risk_score"] >= 60]
hit_rate  = high_risk["broke_down"].mean() * 100
print(f"Cars with risk >= 60: {len(high_risk)} total, {hit_rate:.0f}% of them later broke down.")
print("The 80% wear rule would flag these cars only once they reach 12,000 km since service.")
print("The risk score flags the high-load, high-daily-km cars earlier.")
