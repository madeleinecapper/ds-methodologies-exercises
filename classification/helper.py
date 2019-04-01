def peekatdata(dataframe):
    ''' pandas dataframe -> no return
        prints basic information from pandas dataframe passed in argument'''
    head_df = dataframe.head()
    print(head_df)
    tail_df = dataframe.tail()
    print(tail_df)
    shape_tuple = dataframe.shape
    print()
    print(shape_tuple)
    print()
    describe_df = dataframe.describe()
    print(dataframe.info())

def df_value_counts(df):
    for col in df.columns: 
        n = df[col].unique().shape[0]
        col_bins = min(n,10)
        print('%s:' % col) 
        if df[col].dtype in ['int64','float64'] and n > 10: 
            print(df[col].value_counts(bins=col_bins, sort=False)) 
        else: print(df[col].value_counts()) 
        print('\n')