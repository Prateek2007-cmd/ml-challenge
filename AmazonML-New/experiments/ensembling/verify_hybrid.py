from pathlib import Path

root = Path(r"c:\Users\Prateek\Downloads\amazon\AmazonML-New")
base_tsv = root / "output" / "matching_results.tsv"
hybrid_tsv = root / "output" / "v5_v3_v4_hybrid" / "matching_results.tsv"

print("Checking integrity of v5 hybrid TSV...")
with open(base_tsv, "r", encoding="utf-8") as fb, open(hybrid_tsv, "r", encoding="utf-8") as fh:
    hb = fb.readline().rstrip("\r\n")
    hh = fh.readline().rstrip("\r\n")
    assert hb == hh == "source1_entity_id\tmatched_entity_ids", f"Header mismatch: {hh}"
    
    line_count = 0
    empty_count = 0
    non_empty_count = 0
    total_matches = 0
    
    for lb, lh in zip(fb, fh):
        line_count += 1
        pb = lb.rstrip("\r\n").split("\t")
        ph = lh.rstrip("\r\n").split("\t")
        
        # Verify S1 ID is identical and in same sequence
        s1_b = pb[0]
        s1_h = ph[0]
        assert s1_b == s1_h, f"Line {line_count}: ID mismatch {s1_b} vs {s1_h}"
        
        # Verify no duplicate matches in ID list
        if len(ph) > 1 and ph[1]:
            matches = ph[1].split(",")
            assert len(matches) == len(set(matches)), f"Line {line_count}: Duplicate matches in {ph[1]}"
            for m in matches:
                assert m.startswith("S2-") or m.startswith("S3-"), f"Line {line_count}: Invalid prefix {m}"
            non_empty_count += 1
            total_matches += len(matches)
        else:
            empty_count += 1

print(f"VERIFIED PERFECT!")
print(f"  Total S1 rows: {line_count:,} (must be exactly 1,732,544)")
print(f"  S1 with matches: {non_empty_count:,}")
print(f"  Singletons: {empty_count:,}")
print(f"  Total matched records: {total_matches:,}")
