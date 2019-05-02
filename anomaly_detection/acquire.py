import requests
import pandas as pd
import os

base_url = 'https://python.zach.lol'

def get_sales():
    if os.path.exists('sales.csv'):
        return pd.read_csv('sales.csv')
    else:
        response = requests.get(base_url + '/api/v1/sales')
        data = response.json()
        sales = data['payload']['sales']
        i = 1
        end = int(data['payload']['max_page'])
        while i < end:
            response = requests.get(base_url + data['payload']['next_page'])
            data = response.json()
            sales += data['payload']['sales']
            i += 1
        df_sales =  pd.DataFrame(sales)
        df_sales.to_csv('sales.csv', index=False)
        return df_sales

def get_stores():
    if os.path.exists('stores.csv'):
        return pd.read_csv('stores.csv')
    else:
        response = requests.get(base_url + '/api/v1/stores')
        data = response.json()
        df_stores = pd.DataFrame(data['payload']['stores'])
        df_stores.to_csv('stores.csv', index=False)
        return df_stores

def get_items():
    if os.path.exists('items.csv'):
        return pd.read_csv('items.csv')
    else:
        response = requests.get(base_url + '/api/v1/items')
        data = response.json()
        items = data['payload']['items']
        response = requests.get(base_url + data['payload']['next_page'])
        data = response.json()
        items += data['payload']['items']
        response = requests.get(base_url + data['payload']['next_page'])
        data = response.json()
        items += data['payload']['items']
        df_items = pd.DataFrame(items)
        df_items.to_csv('items.csv', index=False)
        return df_items

def merge_stores_to_sales(df1, df2):
    df1.rename(columns={'store': 'store_id'}, inplace=True)
    df_merged = pd.merge(df1, df2, on='store_id', how='left')
    return df_merged

def merge_items_to_first_merge(df1, df2):
    df1.rename(columns={'item': 'item_id'}, inplace=True)
    df_merged = pd.merge(df1, df2, on='item_id', how='left')
    return df_merged

def big_merge(df1, df2, df3):
    first_merge = merge_stores_to_sales(df1, df2)
    return merge_items_to_first_merge(first_merge, df3)

def get_all_stuff():
    sales = get_sales()
    stores = get_stores()
    items = get_items()
    real_deal = big_merge(sales, stores, items)
    return real_deal