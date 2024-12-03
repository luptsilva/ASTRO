import pandas as pd

sample = pd.read_csv("AMUSING_PRAM_sample.csv", index_col="Name")
p = pd.read_csv("AMUSING_PRAM_cubes.csv", index_col="Name")
p["has_cube"] = True
m = pd.merge(p, sample, on="Name" ,how = "left")
m.to_csv("AMUSING_PRAM_sample2.csv")
print(m)
