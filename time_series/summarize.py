import pandas as pd

def nulls_by_row(df):
    num_cols_missing = df.isnull().sum(axis=1)
    pct_cols_missing = df.isnull().sum(axis=1)/df.shape[1]*100
    rows_missing = pd.DataFrame({'num_cols_missing': num_cols_missing, 'pct_cols_missing': pct_cols_missing}).reset_index().groupby(['num_cols_missing','pct_cols_missing']).count().rename(index=str, columns={'index': 'num_rows'}).reset_index()
    return rows_missing

def df_value_counts(df):
    counts = pd.Series([])
    for i, col in enumerate(df.columns.values):
        if df[col].dtype == 'object':
            col_count = df[col].value_counts()
        else:
            col_count = df[col].value_counts(bins=10, sort=False)
        counts = counts.append(col_count)
    return counts

def get_nulls_by_column(df):
    sum_nulls_col = df.isna().sum()
    percent_nulls_col = df.isna().sum()/len(df.columns)
    nulls_by_col = pd.concat([sum_nulls_col, percent_nulls_col], names=['sum_nulls_col', 'percent_nulls_col'], axis=1)
    nulls_by_col['sum_nulls'] = nulls_by_col[0]
    nulls_by_col['nulls_by_percent'] = nulls_by_col[1]
    nulls_by_col.drop(columns=[0,1], inplace=True)
    nulls_by_col = nulls_by_col.loc[~(nulls_by_col==0).all(axis=1)]
    return nulls_by_col

def df_summary(df):
    print('--- Shape: {}'.format(df.shape))
    print('--- Info')
    df.info()
    print('--- Descriptions')
    print(df.describe(include='all'))
    print('--- Nulls By Column')
    print(get_nulls_by_column(df))
    print('--- Nulls By Row')
    print(nulls_by_row(df))
    print('--- Value Counts')
    print(df_value_counts(df))