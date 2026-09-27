import os
import sys
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')

root = Path(r"AmazonML-New")
out_dir = root / "output"

def load_file(p):
    rows = []
    with open(p, "r", encoding="utf-8") as f:
        header = next(f)
        for line in f:
            parts = line.rstrip("\r\n").split("\t")
            rows.append((parts[0], parts[1] if len(parts) > 1 else ""))
    return header, rows

print("Loading Base, v4_90, v4_80, v3...")
header, r_base = load_file(out_dir / "matching_results.tsv")
_, r_v4_90 = load_file(out_dir / "v4_c4fr_frp_t90" / "matching_results.tsv")
_, r_v4_80 = load_file(out_dir / "v4_c4fr_t80" / "matching_results.tsv")
_, r_v3 = load_file(out_dir / "v3_roles" / "matching_results.tsv")

# Definite France entities: any entity where Base differs from either v4 variant
definite_france = set([i for i in range(len(r_base)) if r_base[i][1] != r_v4_90[i][1] or r_base[i][1] != r_v4_80[i][1]])
print(f"Definite France entities identified: {len(definite_france):,}")

strategies = [
    ("v8_recall_boost", "France: Union of v4_90 | v4_80; US/IN: v3_roles (Maximum Recall recovery on France)"),
    ("v8_balanced_hybrid", "France: v4_90 with v4_80 fallback on empty; US/IN: v3_roles"),
    ("v8_pure_france_fix", "France: v4_90 on all 50,530 FR entities; US/IN: v3_roles")
]

for name, desc in strategies:
    dest_folder = out_dir / name
    dest_folder.mkdir(parents=True, exist_ok=True)
    dest_file = dest_folder / "matching_results.tsv"
    
    total_matches = 0
    empty_singletons = 0
    
    with open(dest_file, "w", encoding="utf-8") as f_out:
        f_out.write(header)
        for i in range(len(r_base)):
            s1 = r_base[i][0]
            m3 = set(r_v3[i][1].split(",")) if r_v3[i][1] else set()
            m90 = set(r_v4_90[i][1].split(",")) if r_v4_90[i][1] else set()
            m80 = set(r_v4_80[i][1].split(",")) if r_v4_80[i][1] else set()
            
            if i in definite_france:
                if name == "v8_recall_boost":
                    # Union of self-trained discoveries and t=0.80 threshold
                    m = sorted(list(m90 | m80))
                elif name == "v8_balanced_hybrid":
                    # Agreement or fallback to avoid empty score 0.0
                    inter = m90 & m80
                    m = sorted(list(inter if inter else (m90 if m90 else m80)))
                elif name == "v8_pure_france_fix":
                    m = sorted(list(m90))
            else:
                # US and India: pure v3_roles
                m = sorted(list(m3))
                
            if m:
                f_out.write(f"{s1}\t{','.join(m)}\n")
                total_matches += len(m)
            else:
                f_out.write(f"{s1}\t\n")
                empty_singletons += 1
                
    size = dest_file.stat().st_size
    print(f"\nGenerated {name}:")
    print(f"  Description:      {desc}")
    print(f"  Total Matches:    {total_matches:,}")
    print(f"  Singletons:       {empty_singletons:,}")
    print(f"  File Size:        {size / 1_000_000:.2f} MB ({size:,} bytes)")
