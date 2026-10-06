---
name: cleaned-record-output-conventions
description: Use when producing cleaned record outputs and summary JSON from tabular input.
---
1. Write `workspace/clean.csv` when a cleaned record file is required.
2. Use this exact CSV header order:
   `order_id,timestamp_utc,region,amount_cents`
3. Emit one row per distinct record with a known amount.
4. Count input rows with duplicates included.
5. Deduplicate records before computing `rows_used`.
6. Exclude records with missing, sentinel, or unknown amounts from `rows_used` and cleaned output.
7. Normalize timestamps to UTC as `YYYY-MM-DDTHH:MM:SSZ`.
8. Normalize categorical region values to canonical spelling:
   `North`, `South`, `East`, `West`.
9. Convert all money values to integer cents; do not write decimal currency values in JSON or CSV.
10. Write `answer.json` with a top-level `meta` object exactly containing:
    `{"source": <input file name>, "rows_in": <number of data rows>, "rows_used": <number of distinct records with a known amount>}`
11. Verify every monetary field in `answer.json` is an integer number of cents.
