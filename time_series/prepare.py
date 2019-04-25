import pandas as pd
import numpy as np

def to_datetime_utc(df):
    s = df['sale_date'].apply(lambda x: x.split(','))
    df['weekday'] = s.apply(lambda x: x[0])
    df['sale_date'] = s.apply(lambda x: x[1])
    df['sale_date'] = pd.to_datetime(df['sale_date'], infer_datetime_format=True, utc=True)
    return df

def make_cols(df):
    df['year'] = df.sale_date.dt.year
    df['quarter'] = df.sale_date.dt.quarter
    df['month'] = df.sale_date.dt.month
    df['day_of_month'] = df.sale_date.dt.day
    df['is_weekday'] = df.sale_date.dt.weekday.apply(lambda x: 1 if x >= 5 else 0)
    return df

def make_new_sales_amounts(df):
    df['sales_total'] = df.sale_amount * df.item_price
    df.rename(columns={'sale_amount': 'quantity'}, inplace=True)
    return df

def re_index_by_time(df):
    df.set_index('sale_date', inplace=True)