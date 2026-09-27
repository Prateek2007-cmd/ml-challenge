from pathlib import Path

root = Path(r"c:\Users\Prateek\Downloads\amazon\AmazonML-New\output")
p_base = root / "matching_results.tsv"
p_v4_90 = root / "v4_c4fr_frp_t90" / "matching_results.tsv"
p_v4_80 = root / "v4_c4fr_t80" / "matching_results.tsv"
p_v3 = root / "v3_roles" / "matching_results.tsv"
p_v5 = root / "v5_v3_v4_hybrid" / "matching_results.tsv"
p_v6 = root / "v6_high_precision_intersection" / "matching_results.tsv"

def load_sets(p):
    d = []
    with open(p, "r", encoding="utf-8") as f:
        next(f)
        for line in f:
            parts = line.rstrip("\r\n").split("\t")
            s1 = parts[0]
            m = set(parts[1].split(",")) if len(parts) > 1 and parts[1] else set()
            d.append((s1, m))
    return d

print("Loading files...")
d_base = load_sets(p_base)
d_v4_90 = load_sets(p_v4_90)
d_v4_80 = load_sets(p_v4_80)
d_v3 = load_sets(p_v3)

print("Calculating intersections...")
# Count matches
m_base = sum(len(m) for _, m in d_base)
m_v4_90 = sum(len(m) for _, m in d_v4_90)
m_v4_80 = sum(len(m) for _, m in d_v4_80)
m_v3 = sum(len(m) for _, m in d_v3)

print(f"Base matches:    {m_base:,}")
print(f"v4_t90 matches:  {m_v4_90:,}")
print(f"v4_t80 matches:  {m_v4_80:,}")
print(f"v3 matches:      {m_v3:,}")

# v6 is intersection of v4_t90 and v3
inter_v4_90_v3 = sum(len(m4 & m3) for (_, m4), (_, m3) in zip(d_v4_90, d_v3))
print(f"v6 (v4_t90 & v3) matches: {inter_v4_90_v3:,}")

# 3-way intersection: v4_t90 & v4_t80 & v3
inter_3way = sum(len(m4 & m4_80 & m3) for (_, m4), (_, m4_80), (_, m3) in zip(d_v4_90, d_v4_80, d_v3))
print(f"3-way (v4_t90 & v4_t80 & v3) matches: {inter_3way:,}")

# Base & v4_t90 & v3
inter_base_v4_v3 = sum(len(mb & m4 & m3) for (_, mb), (_, m4), (_, m3) in zip(d_base, d_v4_90, d_v3))
print(f"3-way (Base & v4_t90 & v3) matches: {inter_base_v4_v3:,}")
