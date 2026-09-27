import os
from pathlib import Path

root = Path(r"c:\Users\Prateek\Downloads\amazon\AmazonML-New")

files = [
    "output/matching_results.tsv",
    "output/v4_c4fr_frp_t90/matching_results.tsv",
    "output/v5_v3_v4_hybrid/matching_results.tsv",
    "output/v6_high_precision_intersection/matching_results.tsv"
]

for rel in files:
    p = root / rel
    size = p.stat().st_size
    with open(p, "r", encoding="utf-8") as f:
        lines = sum(1 for _ in f)
    print(f"{rel}:")
    print(f"  Exact Lines: {lines:,}")
    print(f"  Raw Bytes:   {size:,} bytes")
    print(f"  Decimal MB:  {size / 1_000_000:.2f} MB")
    print(f"  Windows MiB: {size / (1024 * 1024):.2f} MB")
