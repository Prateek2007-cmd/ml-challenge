from pathlib import Path
from collections import Counter

root = Path(r"c:\Users\Prateek\Downloads\amazon\AmazonML-New")
base_tsv = root / "output" / "matching_results.tsv"
v4_tsv = root / "output" / "v4_c4fr_frp_t90" / "matching_results.tsv"
v3_tsv = root / "output" / "v3_roles" / "matching_results.tsv"
v5_tsv = root / "output" / "v5_v3_v4_hybrid" / "matching_results.tsv"
v6_tsv = root / "output" / "v6_high_precision_intersection" / "matching_results.tsv"

def load_data(path):
    d = {}
    with open(path, "r", encoding="utf-8") as f:
        next(f)
        for line in f:
            parts = line.rstrip("\r\n").split("\t")
            s1 = parts[0]
            m = set(parts[1].split(",")) if len(parts) > 1 and parts[1] else set()
            d[s1] = m
    return d

print("Loading all files...")
d_base = load_data(base_tsv)
d_v4 = load_data(v4_tsv)
d_v3 = load_data(v3_tsv)
d_v5 = load_data(v5_tsv)
d_v6 = load_data(v6_tsv)

total = len(d_base)
print(f"Total S1 entities: {total:,}")

# How many S1 entities differ between v5 (which scored 0.973) and v6?
diff_v5_v6 = sum(1 for s1 in d_base if d_v5[s1] != d_v6[s1])
print(f"Entities where v5 != v6: {diff_v5_v6:,}")

# In those diffs, what happened?
# In v6, matches are ONLY subsets of v5 (since v6 is intersection of v3 and v4, and v5 took v4 for FR and v3 for US/IN)
pruned_matches = 0
dropped_to_empty = 0
for s1 in d_base:
    if d_v5[s1] != d_v6[s1]:
        diff_set = d_v5[s1] - d_v6[s1]
        pruned_matches += len(diff_set)
        if len(d_v5[s1]) > 0 and len(d_v6[s1]) == 0:
            dropped_to_empty += 1

print(f"Total doubtful matches pruned in v6 vs v5: {pruned_matches:,}")
print(f"Entities that became empty (singletons) in v6 vs v5: {dropped_to_empty:,}")
