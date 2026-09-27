from pathlib import Path

root = Path(r"c:\Users\Prateek\Downloads\amazon\AmazonML-New")
base_tsv = root / "output" / "matching_results.tsv"
v4_tsv = root / "output" / "v4_c4fr_frp_t90" / "matching_results.tsv"
v3_tsv = root / "output" / "v3_roles" / "matching_results.tsv"

def load_dict(path):
    d = {}
    with open(path, "r", encoding="utf-8") as f:
        next(f)
        for line in f:
            parts = line.rstrip("\r\n").split("\t")
            s1 = parts[0]
            matches = set(parts[1].split(",")) if len(parts) > 1 and parts[1] else set()
            d[s1] = matches
    return d

print("Loading d_base, d_v4, d_v3...")
d_base = load_dict(base_tsv)
d_v4 = load_dict(v4_tsv)
d_v3 = load_dict(v3_tsv)

# Since v4 is identical to base on US/India:
# If d_base[s1] != d_v4[s1], then s1 is definitely France!
fr_known = {s1 for s1 in d_base if d_base[s1] != d_v4[s1]}
print(f"Definitely France (differed between Base and v4): {len(fr_known):,}")

# On S1 where d_base[s1] == d_v4[s1]:
# Did v3 change anything?
v3_diff_on_same = sum(1 for s1 in d_base if d_base[s1] == d_v4[s1] and d_v3[s1] != d_base[s1])
print(f"S1 where Base == v4 (mostly US/India), but v3 differs: {v3_diff_on_same:,}")
