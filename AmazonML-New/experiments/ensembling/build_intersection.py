from pathlib import Path

root = Path(r"c:\Users\Prateek\Downloads\amazon\AmazonML-New")
base_tsv = root / "output" / "matching_results.tsv"
v4_tsv = root / "output" / "v4_c4fr_frp_t90" / "matching_results.tsv"
v3_tsv = root / "output" / "v3_roles" / "matching_results.tsv"

dest_dir = root / "output" / "v6_high_precision_intersection"
dest_dir.mkdir(parents=True, exist_ok=True)
dest_tsv = dest_dir / "matching_results.tsv"

print("Building High-Precision Intersection file...")
with open(base_tsv, "r", encoding="utf-8") as fb, \
     open(v4_tsv, "r", encoding="utf-8") as f4, \
     open(v3_tsv, "r", encoding="utf-8") as f3, \
     open(dest_tsv, "w", encoding="utf-8") as f_out:
    
    header = fb.readline()
    f4.readline()
    f3.readline()
    f_out.write(header)
    
    line_count = 0
    empty_count = 0
    non_empty_count = 0
    total_matches = 0
    
    for lb, l4, l3 in zip(fb, f4, f3):
        line_count += 1
        pb = lb.rstrip("\r\n").split("\t")
        p4 = l4.rstrip("\r\n").split("\t")
        p3 = l3.rstrip("\r\n").split("\t")
        
        s1 = pb[0]
        m4 = p4[1] if len(p4) > 1 else ""
        m3 = p3[1] if len(p3) > 1 else ""
        
        set_4 = set(m4.split(",")) if m4 else set()
        set_3 = set(m3.split(",")) if m3 else set()
        
        # Intersect: Only keep matches that BOTH top models confirmed!
        inter = sorted(list(set_4 & set_3))
        
        if inter:
            f_out.write(f"{s1}\t{','.join(inter)}\n")
            non_empty_count += 1
            total_matches += len(inter)
        else:
            f_out.write(f"{s1}\t\n")
            empty_count += 1

print("High-Precision Intersection created successfully!")
print(f"  Total S1 rows: {line_count:,}")
print(f"  S1 with matches: {non_empty_count:,}")
print(f"  Singletons (perfect 1.0 if truly empty): {empty_count:,}")
print(f"  Total confirmed matches: {total_matches:,}")
