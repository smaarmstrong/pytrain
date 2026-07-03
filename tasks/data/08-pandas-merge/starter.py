import pandas as pd


def merge_sales(sales, products, how):
    """Merge on 'product_id' with the given how ("inner"/"left"/"outer")."""
    raise NotImplementedError


def orders_with_names(orders, customers):
    """Left-merge: every order keeps its row, gains the customer 'name'."""
    raise NotImplementedError


def stack_frames(frames):
    """Concatenate vertically with a fresh RangeIndex."""
    raise NotImplementedError
