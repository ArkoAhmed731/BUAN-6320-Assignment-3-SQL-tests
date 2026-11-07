# BUAN 6320 – Assignment 3 Test Kit (Team 11)

This folder has a local test database that checks our 10 submitted SQL
answers against the sample data from `Assignment3.pdf`. It does **not**
change anything in `Team11_Assignment3.docx` — it just verifies the answers
we already wrote.

## Requirements

Just Python 3 (any recent version). No database server, no install, no
credentials. Nothing else needed.

## Files in this folder

| File | What it is |
|---|---|
| `Assignment3_Setup_SQLite.sql` | Creates `Vendor_T` / `Product_T` and loads the sample data (5 vendors, 12 products) into SQLite. |
| `Assignment3_Setup_Oracle.sql` | Same tables/data, Oracle syntax — for reference if anyone wants to build this in an Oracle/APEX schema instead. |
| `Assignment3_Queries.sql` | Our 10 submitted queries (Q1–Q10), copied verbatim from the Word doc. |
| `run_tests.py` | Builds the database (first run only) and runs all 10 queries against it, checking actual rows/values against what each question should produce. |
| `Assignment3_Test.db` | The SQLite database file itself. Safe to delete if you want a clean rebuild — `run_tests.py` will recreate it. |
| `Assignment3_Test_Results.md` | The generated report: PASS/FAIL per question, actual output tables, and explanations. |

## How to run it

1. Open a terminal in this folder (in VS Code: right-click the folder → "Open in Integrated Terminal").
2. Run:
   ```
   python run_tests.py
   ```
3. Open `Assignment3_Test_Results.md` to see the results.

Current status: **10/10 questions pass.**

## If you want to poke at the database yourself

```
python
```
```python
import sqlite3
conn = sqlite3.connect("Assignment3_Test.db")
cur = conn.cursor()
cur.execute("SELECT * FROM Product_T")
for row in cur.fetchall():
    print(row)
```
You can paste any query from `Assignment3_Queries.sql` into `cur.execute(...)` the same way.

## Notes / caveats

- These results come from **SQLite**, not Oracle — no Oracle/APEX access was
  available when this was built. All 10 queries use plain ANSI SQL with no
  Oracle-only syntax, so they should behave the same in Oracle, but nobody
  has actually run them there yet. If someone on the team has Oracle APEX
  access, it's worth a quick manual spot-check before the due date
  (Nov 8, 2026).
- `Assignment3_Setup.sql` (the file named in the assignment prep) wasn't
  found on this machine, so the sample data was rebuilt directly from the
  tables printed in `Assignment3.pdf` (pages 1–2). It matches exactly: 5
  vendors, 12 products, B349/B401 with no vendor, Sterling/Thomas with no
  products.
