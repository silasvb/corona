import pandas as pd
from functools import reduce
import numpy as np
import matplotlib.pyplot as plt

raw_pandemic = pd.read_csv('data/pandemic.csv')
#raw_pandemic.set_index('name', inplace=True)
print(raw_pandemic)

raw_economic = pd.read_csv('data/economic_indicators.csv')
#raw_economic.set_index('Name', inplace=True)
print(raw_economic)

df_e = pd.DataFrame(raw_economic)
df_p = pd.DataFrame(raw_pandemic)

def clean_economic_names(names):
    # Globally replace spaces with subscripts
    names = [name.replace(' ', '_') for name in names]

    # Some specific replacements
    i = names.index('Korea')
    names[i] = 'South_Korea'
    i = names.index('Belarus')
    names[i] = 'Republic_of_Belarus'

    return names

def combine_pandemic_substates(df):

    combinations = {
        'Australia': ['New_South_Wales', 'Victoria'],
        'Canada': ['British_Columbia', 'Ontario', 'Quebec', 'Alberta'],
        'China': ['Kinshasa', 'Hubei', 'Henan', 'Heilongjiang']
        }

    tmp_dict = df.to_dict('records')

    for state, sub_states in combinations.items():
        grad = 0
        grad = sum([row['grad_week_1'] for row in tmp_dict if row['name'] in sub_states])
        tmp_dict = [row for row in tmp_dict if not row['name'] in sub_states]
        tmp_dict.append({'name': state, 'grad_week_1': grad})
    return pd.DataFrame(tmp_dict)

df_e['Name'] = clean_economic_names(df_e['Name'].values)
df_p = combine_pandemic_substates(df_p)
x = df_e[~df_e['Name'].isin(raw_pandemic['name'])]
y = df_p[~df_p['name'].isin(raw_economic['Name'])]

# Combine the data frames
df_e.set_index('Name', inplace=True)
df_p.set_index('name', inplace=True)

df_combined = pd.concat([df_e, df_p], axis=1)
print(df_combined)
df_combined.to_csv('data/countries_combined.csv')

df_combined['Population (million)'] = pd.to_numeric(df_combined['Population (million)'],errors='coerce')
df_combined = df_combined[(df_combined["Population (million)"].notnull())]

df_combined["Imports (USD billion)"] = pd.to_numeric(df_combined["Imports (USD billion)"],errors='coerce')
df_combined["Imports (annual variation in %)"] = pd.to_numeric(df_combined["Imports (annual variation in %)"],errors='coerce')

df_combined["grad_week_1_per_capita"] = df_combined["grad_week_1"] / df_combined["Population (million)"]
x = df_combined.corr(method='pearson')
pd.DataFrame(x).to_csv("results/tmp.csv")

f = plt.figure()
plt.plot(df_combined["Imports (annual variation in %)"], df_combined["grad_week_1_per_capita"], '*')
plt.xlabel("Imports (annual variation in %)")
plt.ylabel("Gradient of Uptake of Covid-19 Week 1")
plt.show()


