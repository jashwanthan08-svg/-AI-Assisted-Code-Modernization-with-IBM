# analyze.py
# SUMMARY: The two factors that reliably separate cars that broke down from those that did not
# are km_since_service (+60.8% higher in the broke-down group) and load_factor (+18.8% higher).
# Total mileage (odometer_km) and age_years show virtually zero difference between the two groups
# and are NOT useful predictors — the obvious assumption is wrong. Follow the data, not the hunch.

import pandas as pd

df = pd.read_csv("fleet_history.csv")

# ── Step 1: compare each column between the two groups ───────────────────────
predictors = ["odometer_km", "km_since_service", "avg_daily_km", "load_factor", "age_years"]
broke = df[df["broke_down"] == 1]
ok    = df[df["broke_down"] == 0]

print("Group means — broke_down=1 vs broke_down=0")
print(f"{'Column':<20} {'broke mean':>12} {'ok mean':>12} {'difference':>12} {'diff %':>10}")
print("-" * 70)
for col in predictors:
    bm   = broke[col].mean()
    om   = ok[col].mean()
    diff = bm - om
    pct  = (diff / om * 100) if om != 0 else 0
    print(f"{col:<20} {bm:>12.2f} {om:>12.2f} {diff:>12.2f} {pct:>9.1f}%")

print()
print("Conclusion: odometer_km (+0.3%) and age_years (-0.2%) show almost no difference.")
print("km_since_service (+60.8%) and load_factor (+18.8%) are the real signals.")
print()

# ── Step 2: build a 0–100 risk score from the two separating columns ─────────
# Normalise each to [0, 1] across the full fleet, weight equally, scale to 100.
km_min = df["km_since_service"].min()
km_max = df["km_since_service"].max()
lf_min = df["load_factor"].min()
lf_max = df["load_factor"].max()

df["km_norm"] = (df["km_since_service"] - km_min) / (km_max - km_min)
df["lf_norm"] = (df["load_factor"]      - lf_min) / (lf_max - lf_min)

df["risk_score"] = ((df["km_norm"] + df["lf_norm"]) / 2 * 100).round(1)

# ── Step 3: print cars ranked by risk, highest first ─────────────────────────
ranked = df[["car_id", "km_since_service", "load_factor", "risk_score", "broke_down"]].sort_values(
    "risk_score", ascending=False
).reset_index(drop=True)

print("Cars ranked by breakdown risk (highest first)")
print(f"{'#':<4} {'car_id':<12} {'km_since_svc':>14} {'load_factor':>12} {'risk_score':>11} {'broke_down':>11}")
print("-" * 68)
for i, row in ranked.iterrows():
    print(
        f"{i+1:<4} {row['car_id']:<12} {row['km_since_service']:>14,.0f} "
        f"{row['load_factor']:>12.2f} {row['risk_score']:>11.1f} {int(row['broke_down']):>11}"
    )
