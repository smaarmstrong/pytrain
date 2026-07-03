# sales data pipeline — scaffold

`pipeline.py` is the graded entry point
(`python pipeline.py INPUT_CSV OUTPUT_DB`). `clean.py` is a suggested home
for the pandas cleaning layer; how you split the code is up to you.

`sales.csv` is the sample from the acceptance example in the prompt — handy
for eyeballing (`python pipeline.py sales.csv sales.db`, then open the db
with `sqlite3`). The grader uses its own fixture CSVs.
