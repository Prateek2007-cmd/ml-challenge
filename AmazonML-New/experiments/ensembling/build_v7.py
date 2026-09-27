import os
from pathlib import Path

root = Path(r"c:\Users\Prateek\Downloads\amazon\AmazonML-New")
p_base = root / "output" / "matching_results.tsv"
p_v4_90 = root / "output" / "v4_c4fr_frp_t90" / "matching_results.tsv"
p_v4_80 = root / "output" / "v4_c4fr_t80" / "matching_results.tsv"
p_v3 = root / "output" / "v3_roles" / "matching_results.tsv"

dest_dir = root / "output" / "v7_ultra_consensus"
dest_dir.mkdir(parents=True, exist_ok=True)
dest_tsv = dest_dir / "matching_results.tsv"

print("Building v7 Ultra Consensus (3-Way Intersection: v3_roles & v4_t90 & v4_t80)...")
with open(p_base, "r", encoding="utf-8") as fb, \
     open(p_v4_90, "r", encoding="utf-8") as f90, \
     open(p_v4_80, "r", encoding="utf-8") as f80, \
     open(p_v3, "r", encoding="utf-8") as f3, \
     open(dest_tsv, "w", encoding="utf-8") as f_out:
    
    header = fb.readline()
    f90.readline()
    f80.readline()
    f3.readline()
    f_out.write(header)
    
    line_count = 0
    empty_count = 0
    non_empty_count = 0
    total_matches = 0
    
    for lb, l90, l80, l3 in zip(fb, f90, f80, f3):
        line_count += 1
        pb = lb.rstrip("\r\n").split("\t")
        p90 = l90.rstrip("\r\n").split("\t")
        p80 = l80.rstrip("\r\n").split("\t")
        p3 = l3.rstrip("\r\n").split("\t")
        
        s1 = pb[0]
        m90 = p90[1] if len(p90) > 1 else ""
        m80 = p80[1] if len(p80) > 1 else ""
        m3 = p3[1] if len(p3) > 1 else ""
        
        set_90 = set(m90.split(",")) if m90 else set()
        set_80 = set(m80.split(",")) if m80 else set()
        set_3 = set(m3.split(",")) if m3 else set()
        
        # 3-Way Intersection: Absolute consensus across all architectures
        consensus = sorted(list(set_90 & set_80 & set_3))
        
        if consensus:
            f_out.write(f"{s1}\t{','.join(consensus)}\n")
            non_empty_count += 1
            total_matches += len(consensus)
        else:
            f_out.write(f"{s1}\t\n")
            empty_count += 1

print("v7 Ultra Consensus created successfully!")
print(f"  Total S1 rows: {line_count:,}")
print(f"  S1 with matches: {non_empty_count:,}")
print(f"  Singletons (clean 1.0 macro score): {empty_count:,}")
print(f"  Total verified consensus matches: {total_matches:,}")
