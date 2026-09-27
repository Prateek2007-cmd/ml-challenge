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

_, r_base = load_file(base_tsv)
_, r_v4 = load_file(v4_tsv)
_, r_v3 = load_file(v3_tsv)

# Strategy 1: Pure Hybrid (US/India -> v3_roles, France -> v4_c4fr_frp_t90)
# Notice: In v4, Base and v4 are IDENTICAL for US and India.
# So if v4 != Base, it is 100% France.
# What about the France entities where v4 == Base?
# If we take v4 wherever v4 != Base, and v3 wherever v4 == Base:
# That applies v4 to all changed French entities, and v3 to all US/India entities!
# Let's count how many entities that changes:
hybrid_matches = 0
for (s1_b, m_b), (s1_4, m_4), (s1_3, m_3) in zip(r_base, r_v4, r_v3):
    if m_b != m_4: # definitely France where v4 has a specific French fix
        m = m_4
    else: # US/India, or France where Base already agreed with v4 -> use v3_roles
        m = m_3
    if m:
        hybrid_matches += len(m.split(","))

print(f"Hybrid S2/S3 matches: {hybrid_matches:,}")

# Strategy 2: High-Precision Intersection between v4 and v3
# Keep match only if BOTH v4 and v3 agreed!
intersection_matches = 0
for (s1_4, m_4), (s1_3, m_3) in zip(r_v4, r_v3):
    set_4 = set(m_4.split(",")) if m_4 else set()
    set_3 = set(m_3.split(",")) if m_3 else set()
    inter = set_4 & set_3
    intersection_matches += len(inter)

print(f"Intersection S2/S3 matches: {intersection_matches:,}")
