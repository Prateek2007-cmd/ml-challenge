from pathlib import Path

root = Path(r"c:\Users\Prateek\Downloads\amazon\AmazonML-New")
base_tsv = root / "output" / "matching_results.tsv"
v3_tsv = root / "output" / "v3_roles" / "matching_results.tsv"

diff_lines = 0
first_diffs = []
with open(base_tsv, "r", encoding="utf-8") as fb, open(v3_tsv, "r", encoding="utf-8") as f3:
    header_b = fb.readline()
    header_3 = f3.readline()
    line_num = 1
    for lb, l3 in zip(fb, f3):
        line_num += 1
        if lb != l3:
            diff_lines += 1
            if len(first_diffs) < 5:
                first_diffs.append((line_num, lb.strip(), l3.strip()))

print(f"Total differing S1 rows between Base and v3: {diff_lines:,}")
for ln, lb, l3 in first_diffs:
    print(f"Line {ln}:")
    print(f"  Base: {lb}")
    print(f"  v3:   {l3}")
