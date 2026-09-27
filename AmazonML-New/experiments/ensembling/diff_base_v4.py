from pathlib import Path

root = Path(r"c:\Users\Prateek\Downloads\amazon\AmazonML-New")
base_tsv = root / "output" / "matching_results.tsv"
v4_tsv = root / "output" / "v4_c4fr_frp_t90" / "matching_results.tsv"
v3_tsv = root / "output" / "v3_roles" / "matching_results.tsv"

# Read first 10 rows of each
print("--- Base TSV header and first 5 rows ---")
with open(base_tsv, "r", encoding="utf-8") as f:
    for i in range(6):
        print(repr(f.readline().strip()))

print("\n--- Differences between Base TSV and v4_c4fr_frp_t90 ---")
diff_lines = 0
first_diffs = []
with open(base_tsv, "r", encoding="utf-8") as fb, open(v4_tsv, "r", encoding="utf-8") as f4:
    header_b = fb.readline()
    header_4 = f4.readline()
    line_num = 1
    for lb, l4 in zip(fb, f4):
        line_num += 1
        if lb != l4:
            diff_lines += 1
            if len(first_diffs) < 5:
                first_diffs.append((line_num, lb.strip(), l4.strip()))

print(f"Total differing S1 rows between Base and v4: {diff_lines:,}")
for ln, lb, l4 in first_diffs:
    print(f"Line {ln}:")
    print(f"  Base: {lb}")
    print(f"  v4:   {l4}")
