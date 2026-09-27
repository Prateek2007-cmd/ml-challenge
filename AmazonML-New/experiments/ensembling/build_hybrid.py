import os
import subprocess
import sys
from pathlib import Path

root = Path(r"c:\Users\Prateek\Downloads\amazon\AmazonML-New")
base_tsv = root / "output" / "matching_results.tsv"
v4_tsv = root / "output" / "v4_c4fr_frp_t90" / "matching_results.tsv"
v3_tsv = root / "output" / "v3_roles" / "matching_results.tsv"

dest_dir = root / "output" / "v5_v3_v4_hybrid"
dest_dir.mkdir(parents=True, exist_ok=True)
dest_tsv = dest_dir / "matching_results.tsv"

print("Building Hybrid file...")
with open(base_tsv, "r", encoding="utf-8") as fb, \
     open(v4_tsv, "r", encoding="utf-8") as f4, \
     open(v3_tsv, "r", encoding="utf-8") as f3, \
     open(dest_tsv, "w", encoding="utf-8") as f_out:
    
    header = fb.readline()
    f4.readline()
    f3.readline()
    f_out.write(header)
    
    changed_fr = 0
    used_v3 = 0
    total_matches = 0
    empty_singletons = 0
    
    for lb, l4, l3 in zip(fb, f4, f3):
        pb = lb.rstrip("\r\n").split("\t")
        p4 = l4.rstrip("\r\n").split("\t")
        p3 = l3.rstrip("\r\n").split("\t")
        
        s1 = pb[0]
        mb = pb[1] if len(pb) > 1 else ""
        m4 = p4[1] if len(p4) > 1 else ""
        m3 = p3[1] if len(p3) > 1 else ""
        
        # If v4 differs from Base, it's definitely France where v4 applied French normalization + self-training
        if mb != m4:
            selected_m = m4
            changed_fr += 1
        else:
            # Otherwise (US, India, or France where Base already agreed with v4), use the upgraded v3_roles
            selected_m = m3
            used_v3 += 1
            
        if selected_m:
            f_out.write(f"{s1}\t{selected_m}\n")
            total_matches += len(selected_m.split(","))
        else:
            f_out.write(f"{s1}\t\n")
            empty_singletons += 1

print(f"Hybrid created successfully!")
print(f"  France specialized entities from v4: {changed_fr:,}")
print(f"  US/India upgraded entities from v3: {used_v3:,}")
print(f"  Total matched records: {total_matches:,}")
print(f"  Singletons identified: {empty_singletons:,}")

# Run official validator
print("\nRunning official submission validator...")
val_cmd = [
    sys.executable,
    str(root / "utils" / "validate_submission.py"),
    "--matching", str(dest_tsv),
    "--candidate", str(dest_dir / "__not_loaded__.tsv"),
    "--test-dir", str(root / "dataset" / "test")
]
res = subprocess.run(val_cmd, capture_output=True, text=True, encoding="utf-8")
print(res.stdout)
print(res.stderr)
if res.returncode == 0:
    print("VALIDATION STATUS: PASS!")
else:
    print("VALIDATION FAILED!")
