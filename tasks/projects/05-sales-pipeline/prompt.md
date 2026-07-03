# Project: sales data pipeline

Build a batch pipeline: read a messy sales CSV with pandas, clean and
transform it, load the result into SQLite, and print a summary. The entry
point is **`pipeline.py`** — the grader runs it as a subprocess
(`python pipeline.py INPUT_CSV OUTPUT_DB`) and then inspects the SQLite file
and stdout. `clean.py` is scaffolded for the cleaning layer; only
`pipeline.py`'s behaviour is graded.

## Input

A CSV with header `order_id,date,product,quantity,unit_price`. Real-world
mess to expect: stray whitespace around product names, missing products,
non-numeric quantities/prices, zero/negative quantities, duplicated
order ids.

## Cleaning (apply in this order)

1. Strip leading/trailing whitespace from `product`; **drop** rows whose
   product is missing or empty after stripping.
2. Coerce `quantity` and `unit_price` to numbers (`pd.to_numeric(...,
   errors="coerce")`); **drop** rows where either is not numeric, and rows
   with `quantity <= 0`.
3. Among the remaining rows, **drop duplicate `order_id`s, keeping the
   first** occurrence.
4. Add a `revenue` column = `quantity * unit_price`, rounded to 2 decimals.
5. Keep the surviving rows in their original file order. Treat `quantity`
   as an integer from here on.

## Load

Write two tables into `OUTPUT_DB` (SQLite, e.g. `df.to_sql(...,
index=False, if_exists="replace")` — re-running the pipeline must replace,
not append):

- **`sales`** — the cleaned rows, columns exactly
  `order_id, date, product, quantity, unit_price, revenue`.
- **`summary`** — one row per product, sorted by product ascending, columns
  exactly `product, total_qty, total_revenue` (sums of `quantity` and
  `revenue`, revenue rounded to 2 decimals).

## Report (stdout)

One line per product in the same order as `summary`, then a total:

```
Gadget: qty=3 revenue=12.00
Widget: qty=4 revenue=10.00
TOTAL revenue=22.00
```

(revenue always with two decimals; `TOTAL` is the sum of the per-product
totals.)

## Errors

`INPUT_CSV` missing: print `error: no such file: <INPUT_CSV>` to **stderr**,
exit code **1**, and do not create the database. Exit code 0 on success.

## Acceptance example

With `sales.csv`:

```
order_id,date,product,quantity,unit_price
1,2026-01-05,Widget,3,2.50
2,2026-01-05, Widget ,1,2.50
3,2026-01-06,,5,1.00
4,2026-01-06,Gadget,two,4.00
5,2026-01-07,Gadget,3,4.00
5,2026-01-08,Gadget,9,4.00
```

rows 3 (no product) and 4 (bad quantity) are dropped, the second `order_id`
5 is dropped, ` Widget ` is normalised to `Widget`, and:

```
$ python pipeline.py sales.csv sales.db
Gadget: qty=3 revenue=12.00
Widget: qty=4 revenue=10.00
TOTAL revenue=22.00
```
