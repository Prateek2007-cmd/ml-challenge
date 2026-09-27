import os
from pathlib import Path

root = Path(r"c:\Users\Prateek\Downloads\amazon\AmazonML-New")
base_tsv = root / "output" / "matching_results.tsv"
v4_tsv = root / "output" / "v4_c4fr_frp_t90" / "matching_results.tsv"
v3_tsv = root / "output" / "v3_roles" / "matching_results.tsv"

def count_lines_and_matches(p):
    lines = 0
    empty = 0
    non_empty = 0
    matches_count = 0
    with open(p, "r", encoding="utf-8") as f:
        header = next(f)
        for line in f:
            lines += 1
            parts = line.rstrip("\r\n").split("\t")
            if len(parts) > 1 and parts[1]:
                non_empty += 1
                matches_count += len(parts[1].split(","))
            else:
                empty += 1
    return lines, non_empty, empty, matches_count

for name, path in [("C4 Baseline (LB 0.970441)", base_tsv), 
                   ("v4_c4fr_frp_t90", v4_tsv), 
                   ("v3_roles", v3_tsv)]:
    if path.exists():
        l, ne, e, mc = count_lines_and_matches(path)
        print(f"{name}:")
        print(f"  Total S1 rows: {l:,}")
        print(f"  S1 with matches: {ne:,} | Singletons (no matches): {e:,}")
        print(f"  Total matched S2/S3 records: {mc:,}")
