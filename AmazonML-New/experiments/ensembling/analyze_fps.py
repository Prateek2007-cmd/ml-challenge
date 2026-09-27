import polars as pl

df = pl.read_csv("reports/false_positive_analysis.tsv", separator="\t")
print(df.group_by("reason").len().sort("len", descending=True))
print("\nBy country:")
print(df.group_by(["country", "reason"]).len().sort("len", descending=True).head(10))
print("\nScore distribution of false positives:")
print(df["model_score"].describe())
