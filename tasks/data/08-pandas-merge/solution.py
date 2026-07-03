import pandas as pd


def merge_sales(sales, products, how):
    return sales.merge(products, on="product_id", how=how)


def orders_with_names(orders, customers):
    return orders.merge(customers, on="customer_id", how="left")


def stack_frames(frames):
    return pd.concat(frames, ignore_index=True)
