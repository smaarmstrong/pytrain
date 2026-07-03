"""Receipt helpers: subtotal, discounts and a formatted summary line.

Every function WORKS — but `python -m ruff check solution.py` is livid.
Fix every violation without changing what any function returns.
"""
import os, sys
import json


def subtotal(prices):
    total = 0
    tax_rate = 0.2
    for price in prices:
        total += price
    return total


def apply_discount(total, code):
    if code == None:
        return total
    if (code == "HALF") == True:
        return total / 2
    try:
        percent = int(code)
    except:
        return total
    return total * (100 - percent) / 100


import math


def summary(prices, code=None):
    total = apply_discount(subtotal(prices), code)
    label = f"TOTAL"
    return label + ": " + str(math.floor(total * 100) / 100)
