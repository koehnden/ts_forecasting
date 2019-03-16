import pandas as pd


def join_sales_products(df_sales, df_products):
    df_sales = df_sales.set_index(['product_id'])
    return df_sales.merge(df_products, on='product_id', how='left')


def set_datetime_index(df):
    df = df.set_index(pd.DatetimeIndex(df['date']))
    return df.sort_index()
