import csv
from collections import Counter

reasons = Counter()
country_reasons = Counter()
scores = []

with open("reports/false_positive_analysis.tsv", "r", encoding="utf-8") as f:
    reader = csv.DictReader(f, delimiter="\t")
    for row in reader:
        reasons[row["reason"]] += 1
        country_reasons[(row["country"], row["reason"])] += 1
        try:
            scores.append(float(row["model_score"]))
        except ValueError:
            pass

print("--- Top False Positive Reasons ---")
for r, count in reasons.most_common(15):
    print(f"{r:<30}: {count:>6} ({count/len(scores)*100:.1f}%)")

print("\n--- By Country and Reason ---")
for (c, r), count in country_reasons.most_common(12):
    print(f"{c:<8} {r:<25}: {count:>6}")

scores.sort()
print(f"\nTotal FPs in analysis: {len(scores):,}")
print(f"Min score: {scores[0]:.4f}")
print(f"25th percentile: {scores[len(scores)//4]:.4f}")
print(f"50th percentile (median): {scores[len(scores)//2]:.4f}")
print(f"75th percentile: {scores[3*len(scores)//4]:.4f}")
print(f"Max score: {scores[-1]:.4f}")
