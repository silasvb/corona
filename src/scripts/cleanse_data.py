import pandas as pd

raw_pandemic = pd.read_csv('data/pandemic.csv')
raw_pandemic.set_index('name', inplace=True)
print(raw_pandemic)

raw_economic = pd.read_csv('data/economic_indicators.csv')
raw_economic.set_index('Name', inplace=True)
print(raw_economic)