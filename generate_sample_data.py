"""
Generates simulated data-observability metrics for demo purposes.
Produces data/dq_metrics.csv with daily scores per table across
4 dimensions: Completeness, Timeliness, Uniqueness, OverallHealth.
"""
import csv
import random
from datetime import date, timedelta

random.seed(42)

TABLES = [
    "marketing.campaign_leads",
    "marketing.email_events",
    "marketing.web_sessions",
    "marketing.crm_contacts",
    "marketing.ad_spend",
    "marketing.conversion_events",
]

START_DATE = date.today() - timedelta(days=29)
NUM_DAYS = 30

def simulate_score(base, day_index, volatility=4):
    """Random-walk a score around a base value, clipped to [0, 100]."""
    drift = random.uniform(-volatility, volatility)
    seasonal = 2 * (1 if day_index % 7 in (5, 6) else 0)  # dip on weekends
    score = base + drift - seasonal
    return max(0, min(100, round(score, 1)))

rows = []
for table in TABLES:
    base_completeness = random.uniform(88, 99)
    base_timeliness = random.uniform(85, 98)
    base_uniqueness = random.uniform(90, 100)

    for i in range(NUM_DAYS):
        d = START_DATE + timedelta(days=i)
        completeness = simulate_score(base_completeness, i)
        timeliness = simulate_score(base_timeliness, i, volatility=6)
        uniqueness = simulate_score(base_uniqueness, i, volatility=2)
        overall = round((completeness + timeliness + uniqueness) / 3, 1)

        rows.append({
            "date": d.isoformat(),
            "table_name": table,
            "completeness_score": completeness,
            "timeliness_score": timeliness,
            "uniqueness_score": uniqueness,
            "overall_health_score": overall,
            "row_count": random.randint(5000, 250000),
        })

import os
os.makedirs("data", exist_ok=True)
with open("data/dq_metrics.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=rows[0].keys())
    writer.writeheader()
    writer.writerows(rows)

print(f"Wrote {len(rows)} rows to data/dq_metrics.csv")
