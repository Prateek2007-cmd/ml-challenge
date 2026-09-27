from collections import Counter
from pathlib import Path

root = Path(r"c:\Users\Prateek\Downloads\amazon\AmazonML-New")
v5_path = root / "output" / "v5_v3_v4_hybrid" / "matching_results.tsv"
v6_path = root / "output" / "v6_high_precision_intersection" / "matching_results.tsv"

def match_distribution(p):
    c = Counter()
    with open(p, "r", encoding="utf-8") as f:
        next(f)
        for line in f:
            parts = line.rstrip("\r\n").split("\t")
            if len(parts) > 1 and parts[1]:
                k = len(parts[1].split(","))
                c[k] += 1
            else:
                c[0] += 1
    return c

print("--- v5 Distribution ---")
c5 = match_distribution(v5_path)
for k in range(10):
    print(f"Entities with {k} matches: {c5[k]:,}")

print("\n--- v6 Distribution ---")
c6 = match_distribution(v6_path)
for k in range(10):
    print(f"Entities with {k} matches: {c6[k]:,}")
