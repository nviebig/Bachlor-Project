# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt

import pandas as pd

df =pd.read_csv("Data.csv")
print(df)

print(df.columns)

df.loc[-1] = ['1.002;2.434']  # adding a row
df.index = df.index + 1  # shifting index
df.sort_index(inplace=True) 
df = df.rename(columns={"1.002;2.434":"First"})
print(df)
df[['A', 'B']] = df['First'].str.split(';', 1, expand=True)
print(df)
plt.figure(figsize=(12,8))
plt.scatter(df["A"],df["B"],marker="x")
plt.show()