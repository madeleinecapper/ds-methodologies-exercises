import pandas as pd
import numpy as np

def clean_puncts(df):
    '''removes extra punctuation from fitbit data for cleaning'''
    df['activity_calories'] = df.activity_calories.str.replace('"','')
    df['date'] = df.date.str.replace('"','')
    df["calories_burned"] = df.calories_burned.str.replace(',','')
    df["steps"] = df.steps.str.replace(',','')
    df["minutes_sedentary"] = df.minutes_sedentary.str.replace(',','')
    df["activity_calories"] = df.activity_calories.str.replace(',','')
    return df

def date_index(df):
    '''re-index dataframe by datetime'''
    df['date'] = pd.to_datetime(df.date)
    df.set_index('date', inplace=True)
    return df

def get_feature_list(df):
    '''creates a list of features from the dataframe'''
    columns = []
    [columns.append(col) for col in df]
    return columns

def make_numeric(df):
    '''ensures data in frame is of a numeric type for analysis'''
    columns = get_feature_list(df)
    df[columns] = df[columns].apply(pd.to_numeric, errors='coerce')
    return df

def expand_dt(df):
    '''creates columns that allow for analyzation by aspects of datetime'''
    df['time'] = df.index
    df['year'] = df.time.dt.year
    df['quarter'] = df.time.dt.quarter
    df['month'] = df.time.dt.month
    df['day_of_month'] = df.time.dt.day
    df['day_of_week'] = df.time.dt.day_name().str[:3]
    df['is_weekend'] = ((pd.DatetimeIndex(df.index).dayofweek) > 4)
    df.drop(columns=['time'], inplace=True)
    return df

def prep_data(df):
    df = clean_puncts(df)
    df = date_index(df)
    df = make_numeric(df)
    df = expand_dt(df)
    return df
