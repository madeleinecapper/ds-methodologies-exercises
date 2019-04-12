import pandas as pd
import numpy as np

import statsmodels.api as sm
from sklearn.linear_model import LinearRegression

def handle_missing_values(df, prop_required_column, prop_required_row):
    '''drops rows and columns based on inputted threshold proportions from user'''
    threshold = int(round(prop_required_column*len(df.index),0))
    df.dropna(axis=1, thresh=threshold, inplace=True)
    threshold = int(round(prop_required_row*len(df.columns),0))
    df.dropna(axis=0, thresh=threshold, inplace=True)
    return df

def groom_singles(dfz):
    '''removes entries from database perceived to not be single unit properties'''
    single_cats = ['Single Family Residential', 'Mobile Home', 'Manufactured, Modular, Prefabricated Homes', 'Residential General', 'Townhouse']
    dfz[['propertylandusedesc', 'unitcnt']][dfz.propertylandusedesc.isin(single_cats)]
    dfz = dfz.assign(unitcnt = dfz.unitcnt.fillna(0))
    dfz = dfz[(dfz.propertylandusedesc.isin(single_cats)) & (dfz.unitcnt == 1)]
    dfz = dfz[~(dfz.bathroomcnt == 0) & ~(dfz.bedroomcnt == 0)]
    return dfz


def numeric_to_categorical(df: pd.DataFrame) -> pd.DataFrame:
    '''converts certain column data types to 'category' type in pandas'''
    col_num = []
    col_cat = []

    for cols in df:
        if cols in('id', 'parcelid', 'transactiondate'): 
            col_cat.append(cols)
    to_coerce = {col: "category" for col in col_cat}
    return df.astype(to_coerce)

def drop_nas(df):
    '''drops all data entries that have NaN values in row'''
    df.dropna(axis=0, how='any', inplace=True)
    return df

def impute_lotsize(df):
    '''uses linear regression to predict lot sizes'''
    x = df.loc[df.lotsizesquarefeet.isna(), 'landtaxvaluedollarcnt']
    X = [[a] for a in x]
    xt = df.loc[~df.lotsizesquarefeet.isna(), 'landtaxvaluedollarcnt']
    Xt = [[a] for a in xt]
    yt = df.loc[~df.lotsizesquarefeet.isna(), 'lotsizesquarefeet']
    lotsize_model = LinearRegression(fit_intercept=True)
    lotsize_model.fit(Xt, yt)
    y_pred = lotsize_model.predict(X)
    df.loc[df.lotsizesquarefeet.isna(), 'lotsizesquarefeet'] = y_pred
    return df

def get_nulls_by_column(df):
    sum_nulls_col = df.isna().sum()
    percent_nulls_col = df.isna().sum()/len(df.columns)
    nulls_by_col = pd.concat([sum_nulls_col, percent_nulls_col], names=['sum_nulls_col', 'percent_nulls_col'], axis=1)
    nulls_by_col['sum_nulls'] = nulls_by_col[0]
    nulls_by_col['nulls_by_percent'] = nulls_by_col[1]
    nulls_by_col.drop(columns=[0,1], inplace=True)
    nulls_by_col = nulls_by_col.loc[~(nulls_by_col==0).all(axis=1)]
    print(nulls_by_col)
    return nulls_by_col

def show_numerical_outliers(df):
    '''Parses any numerical columns and removes outliers based on inner quartile range.'''
    for col in df:
        if np.issubdtype(df[col].dtype, np.number):
            q1 = float(df[[col]].quantile(.25))
            q3 = float(df[[col]].quantile(.75))
            iqr = q3 - q1
            if df[(df[col] > (q3 + 1.5 * iqr)) | (df[col] < (q1 - 1.5 * iqr))].empty:
                print(f'No outliers in {col}')
            else:
                print(f'OUTLIERS FOR {col}: \n')
                print(df[col][(df[col] > (q3 + 1.5 * iqr)) | (df[col] < (q1 - 1.5 * iqr))])

def remove_numerical_outliers(df, cols):
    '''Parses any numerical columns and removes outliers based on inner quartile range.'''
    for col in cols:
        if np.issubdtype(df[col].dtype, np.number):
            q1 = float(df[[col]].quantile(.25))
            q3 = float(df[[col]].quantile(.75))
            iqr = q3 - q1
            df = df[~(df[col] > (q3 + 1.5 * iqr)) & ~(df[col] < (q1 - 1.5 * iqr))]
    return df

def maggies_manual_outliers(df):
    '''this consitutes cheating probably'''
    keys = ['bathroomcnt','bedroomcnt','calculatedfinishedsquarefeet',
                      'structuretaxvaluedollarcnt','landtaxvaluedollarcnt']
    values = [(1,7), (1,7), (500,8000), (25000,2000000), (10000,2500000)]

    dictionary = dict(zip(keys, values))

    for key, value in dictionary.items():
        df = df[df[key] >= value[0]]
        df = df[df[key] <= value[1]]
    return df



def prep_zillow(df):
    df = handle_missing_values(df, prop_required_column=.5, prop_required_row=.75)
    df = groom_singles(df)
    df = numeric_to_categorical(df)
    df = impute_lotsize(df)
    df = maggies_manual_outliers(df)
    df = drop_nas(df)
    return df

