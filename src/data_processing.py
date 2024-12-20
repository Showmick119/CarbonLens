import pandas as pd
data = pd.read_csv("data/emissions_data.csv", index_col=0)
print(data.head())
print(data.isnull().sum())
filtered_data = data.loc[:,["Manufacturer,"]]