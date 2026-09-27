from pathlib import Path
from collections import defaultdict

root = Path(r"c:\Users\Prateek\Downloads\amazon\AmazonML-New")
base_tsv = root / "output" / "matching_results.tsv"
v4_tsv = root / "output" / "v4_c4fr_frp_t90" / "matching_results.tsv"
v3_tsv = root / "output" / "v3_roles" / "matching_results.tsv"
v4_t80_tsv = root / "output" / "v4_c4fr_t80" / "matching_results.tsv"

def load_pairs(path):
    pairs = set()
    with open(path, "r", encoding="utf-8") as f:
        next(f)
        for line in f:
            parts = line.rstrip("\r\n").split("\t")
            if len(parts) > 1 and parts[1]:
                s1 = parts[0]
                for q in parts[1].split(","):
                    pairs.add((s1, q))
    return pairs

print("Loading pairs from all models...")
p_base = load_pairs(base_tsv)
print(f"Base pairs: {len(p_base):,}")
p_v4 = load_pairs(v4_tsv)
print(f"v4_c4fr_frp_t90 pairs: {len(p_v4):,}")
p_v3 = load_pairs(v3_tsv)
print(f"v3_roles pairs: {len(p_v3):,}")

inter_v4_v3 = p_v4 & p_v3
print(f"Intersection (v4 & v3): {len(inter_v4_v3):,}")
print(f"v4 only (not in v3): {len(p_v4 - p_v3):,}")
print(f"v3 only (not in v4): {len(p_v3 - p_v4):,}")

inter_all = p_base & p_v4 & p_v3
print(f"Agreed by all 3 models: {len(inter_all):,}")
