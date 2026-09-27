from pathlib import Path

root = Path(r"c:\Users\Prateek\Downloads\amazon\AmazonML-New")
base_tsv = root / "output" / "matching_results.tsv"
v4_tsv = root / "output" / "v4_c4fr_frp_t90" / "matching_results.tsv"
v3_tsv = root / "output" / "v3_roles" / "matching_results.tsv"

def load_file(path):
    rows = []
    with open(path, "r", encoding="utf-8") as f:
        header = next(f)
        for line in f:
            parts = line.rstrip("\r\n").split("\t")
            s1 = parts[0]
            matches = parts[1] if len(parts) > 1 else ""
            rows.append((s1, matches))
    return header, rows

h_base, r_base = load_file(base_tsv)
h_v4, r_v4 = load_file(v4_tsv)
h_v3, r_v3 = load_file(v3_tsv)

assert len(r_base) == len(r_v4) == len(r_v3)

diff_v4_base = 0
diff_v3_base = 0
diff_both = 0
same_v4_diff_v3 = 0

for (s1_b, m_b), (s1_4, m_4), (s1_3, m_3) in zip(r_base, r_v4, r_v3):
    assert s1_b == s1_4 == s1_3
    d4 = (m_b != m_4)
    d3 = (m_b != m_3)
    if d4: diff_v4_base += 1
    if d3: diff_v3_base += 1
    if d4 and d3: diff_both += 1
    if not d4 and d3: same_v4_diff_v3 += 1

print(f"Total S1 entities: {len(r_base):,}")
print(f"Entities where v4 differs from Base (Known France): {diff_v4_base:,}")
print(f"Entities where v3 differs from Base: {diff_v3_base:,}")
print(f"Entities where BOTH v4 and v3 differ from Base: {diff_both:,}")
print(f"Entities where Base == v4 (US/India + untouched France) but v3 differs: {same_v4_diff_v3:,}")
