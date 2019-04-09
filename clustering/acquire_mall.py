import env
import pandas as pd
qry = 'SELECT * FROM customers;'
def get_connection(db, user=env.user, host=env.host, pw=env.pw):
    return f'mysql+pymysql://{user}:{pw}@{host}/{db}'
def get_mall_data():
    df =  pd.read_sql(qry, get_connection('mall_customers'))
    df.to_csv('mall_data.csv', index=False)
    return df

