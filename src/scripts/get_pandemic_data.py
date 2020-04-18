#!/usr/bin/env python
# coding: utf-8

# # Main data analysis scripts
# 
# Cells are organised as functions with the bottom cells being the calling functions
# - Add docstrings to function cells
# 
# To Do
# - Add more economic indicators
# - Explore more curve characterisations
# 

"""
Imports
"""
import json
import pandas as pd

"""
Reading raw data
"""

def read_raw_data():
    with open('data/projection.json') as file:
        raw_data = file.read()

    parsed_data = json.loads(raw_data)

    countries = parsed_data['subjects']
    
    return countries

"""
Pre-process data into data frames
"""

def preprocess(countries):
    
    def episode_filter(episode):
        """
        A filter function that returns true if we want to keep the episode
        """
        return any(key == 'Deaths' and value != None for key, value in episode['entityTypeAttributes'].items())

    # Restructure data
    country_dict = {}
    for country in countries:
        # Initialise dictionary for this country
        tmp_dict = {'timestamp': []}
        for episode in country['episodes']:
            if episode_filter(episode):
                # Get the info for each row of our dataframe
                tmp_dict['timestamp'].append(episode['timestamp'])
                for key, value in episode['entityTypeAttributes'].items():
                    try:
                        tmp_dict[key].append(value)
                    except:
                        tmp_dict[key] = [value]
        # Timestamp having values is indicator that this country has episodes we want to keep
        if tmp_dict['timestamp']:
            # Convert to data frame
            df = pd.DataFrame.from_dict(tmp_dict)

            if max(df['Deaths']) < 10:
                continue

            # Convert timestamps to pandas datetime
            df['timestamp'] = pd.to_datetime(df['timestamp'])

            # Sort by date and reset index
            df.sort_values('timestamp', inplace=True)
            df.reset_index(drop=True, inplace=True)

            # Drop all data before 10th death
            df = df[df['Deaths'] >= 10]

            # Create offset time
            t_offset = df['timestamp'].dt.tz_convert(None).values[0]
            df['offset_time'] = df['timestamp'].dt.tz_convert(None).subtract(t_offset).dt.days
            df.set_index('offset_time', inplace=True)

            country_dict[country['individualId']] = df
        
    return country_dict
              

"""
Get dataframe of country by curve metrics
"""

countries = read_raw_data()
countries_dict = preprocess(countries)

correlation_data = {'name': [], 'grad_week_1': []}
for country_name, country_data in countries_dict.items():
    correlation_data['name'].append(country_name)
    week_1_days = min([7, len(country_data)])
    correlation_data['grad_week_1'].append((country_data['Deaths'].values[week_1_days -1] - country_data['Deaths'].values[0]) / week_1_days)
    
df = pd.DataFrame.from_dict(correlation_data)
print(df)
df.to_csv('data/pandemic.csv')
