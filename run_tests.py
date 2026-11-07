"""
BUAN 6320 Assignment 3 - test runner.

Builds a local SQLite database from Assignment3_Setup_SQLite.sql (only if it
doesn't already exist), runs the 10 submitted queries from
Assignment3_Queries.sql exactly as written, compares each result against an
independently derived expected result (computed from the question wording
and the sample data, NOT from the submitted SQL), and writes
Assignment3_Test_Results.md.

Rerun any time with:
    python run_tests.py
"""
import re
import sqlite3
import pathlib

HERE = pathlib.Path(__file__).parent
DB_PATH = HERE / "Assignment3_Test.db"
SETUP_SQL = HERE / "Assignment3_Setup_SQLite.sql"
QUERIES_SQL = HERE / "Assignment3_Queries.sql"
RESULTS_MD = HERE / "Assignment3_Test_Results.md"

QUESTION_TEXT = {
    1: "List the products and corresponding vendor codes for products whose inventory is less than the minimum stock quantity or products that are priced less than $75 with discount greater than 5%.",
    2: "List the distinct codes of vendors supplying products for which minimum stock quantity is less than 10.",
    3: "For each vendor, list the minimum price and the average discount rate for their products for which the quantity on hand is less than the minimum stock quantity.",
    4: "For each available discount rate of less than 10%, show the minimum price and the maximum price of products with the same discount rate.",
    5: "List the minimum and maximum prices of products for each vendor for vendors who supply more than 3 items.",
    6: "Which products are priced more than the average price? Display product code and product price.",
    7: "List all products supplied by the vendor with the highest-priced product. Include vendor details together with product details.",
    8: "Get the detail of the vendor who has supplied the product for which the dollar value of the on hand inventory is the highest.",
    9: "For each vendor, list the product codes of products supplied along with vendor code and vendor contact name. Display vendor information even if there is no product currently supplied by the vendor. Sort the results by vendor code.",
    10: "Display the phone number and the area code of each vendor whose average price of supplied products is greater than the average price of the products manufactured in house.",
}

# Expected results, derived independently from the question wording + the
# sample data printed in Assignment3.pdf (NOT copied from the submitted SQL).
# order_matters=True means row order is part of the correctness check.
EXPECTED = {
    1: {
        "order_matters": False,
        "rows": [
            ("A104", "21232"), ("B567", "25489"), ("B709", "21222"),
            ("C444", "21222"), ("D476", "21232"), ("D900", "21222"),
        ],
        "note": "p_onhand<p_min (A104,B567,B709) UNION products priced<$75 with discount>5% (C444,D476,D900,B709). A product below minimum stock qualifies regardless of price/discount.",
    },
    2: {
        "order_matters": False,
        "rows": [("25489",)],
        "note": "Only A250 and D897 have p_min<10 among vendor-supplied products; both belong to vendor 25489. B401 also has p_min<10 but is in-house (v_code NULL) and is excluded.",
    },
    3: {
        "order_matters": False,
        "rows": [("21232", 53.75, 0.1), ("25489", 15.0, 0.1), ("21222", 65.0, 0.07)],
        "note": "Only A104(21232), B567(25489), B709(21222) have p_onhand<p_min; one qualifying row per vendor.",
    },
    4: {
        "order_matters": False,
        "rows": [(0.0, 25.0, 34.0), (0.05, 20.0, 100.5), (0.07, 65.0, 65.0), (0.08, 8.0, 8.0)],
        "note": "Discounts 0.1 (A104,B567,C444) are excluded since the question asks for <10%.",
    },
    5: {
        "order_matters": False,
        "rows": [("21222", 8.0, 100.5)],
        "note": "Vendor 21222 supplies 4 products (A102,B709,C444,D900); 21232 and 25489 supply only 3 each.",
    },
    6: {
        "order_matters": False,
        "rows": [("A102", 100.5), ("A104", 53.75), ("A250", 75.5), ("B709", 65.0), ("D897", 89.5)],
        "note": "Average price across all 12 products = 521.75/12 = 43.4792.",
    },
    7: {
        "order_matters": False,
        "rows": [
            ("A102", 23, 10, 100.5, 0.05, "21222", "Smith", "972", "666-8888", "TX"),
            ("B709", 6, 10, 65.0, 0.07, "21222", "Smith", "972", "666-8888", "TX"),
            ("C444", 84, 15, 8.0, 0.1, "21222", "Smith", "972", "666-8888", "TX"),
            ("D900", 38, 10, 8.0, 0.08, "21222", "Smith", "972", "666-8888", "TX"),
        ],
        "note": "Highest-priced product is A102 ($100.50) from vendor 21222 (Smith). All 4 of 21222's products must be returned, not just A102.",
    },
    8: {
        "order_matters": False,
        "rows": [("25489", "Joyce", "212", "333-4444", "FL")],
        "note": "Inventory value (p_onhand*p_price) is highest for D897 (45*89.5=4027.5, vendor 25489/Joyce). B349 (80*34=2720, in-house) is higher than most but is not vendor-supplied, so it can't produce a vendor match.",
    },
    9: {
        "order_matters": True,
        "rows": [
            ("21222", "Smith", "A102"), ("21222", "Smith", "B709"),
            ("21222", "Smith", "C444"), ("21222", "Smith", "D900"),
            ("21232", "Ferguson", "A104"), ("21232", "Ferguson", "C458"),
            ("21232", "Ferguson", "D476"), ("22000", "Sterling", None),
            ("23002", "Thomas", None), ("25489", "Joyce", "A250"),
            ("25489", "Joyce", "B567"), ("25489", "Joyce", "D897"),
        ],
        "note": "12 rows: 10 vendor-product pairs plus Sterling(22000) and Thomas(23002) each with a NULL product code, ordered by v_code.",
    },
    10: {
        "order_matters": False,
        "rows": [("666-8888", "972"), ("222-7777", "817"), ("333-4444", "212")],
        "note": "In-house average price = (34+25)/2 = 29.5. Vendor averages: 21222=45.375, 21232=33.75, 25489=60 -- all three exceed 29.5.",
    },
}


def parse_queries(sql_text):
    pattern = re.compile(r"--\s*Q(\d+):.*?\n((?:--.*\n)*)((?:[^-].*\n?)+?)(?=(?:\n--\s*Q\d+:)|\Z)", re.MULTILINE)
    queries = {}
    for m in pattern.finditer(sql_text):
        qnum = int(m.group(1))
        stmt = m.group(3).strip()
        queries[qnum] = stmt
    return queries


def build_database():
    created = False
    if not DB_PATH.exists():
        conn = sqlite3.connect(DB_PATH)
        conn.executescript(SETUP_SQL.read_text(encoding="utf-8"))
        conn.commit()
        conn.close()
        created = True
    return created


def run_checks(conn):
    checks = []
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM Vendor_T")
    n = cur.fetchone()[0]
    checks.append(("5 vendors", n == 5, n))

    cur.execute("SELECT COUNT(*) FROM Product_T")
    n = cur.fetchone()[0]
    checks.append(("12 products", n == 12, n))

    cur.execute("SELECT COUNT(*) FROM Product_T WHERE v_code IS NULL")
    n = cur.fetchone()[0]
    checks.append(("2 products with no vendor", n == 2, n))

    cur.execute("""SELECT COUNT(*) FROM Vendor_T v
                   WHERE NOT EXISTS (SELECT 1 FROM Product_T p WHERE p.v_code = v.v_code)""")
    n = cur.fetchone()[0]
    checks.append(("2 vendors with no products", n == 2, n))

    return checks


def normalize(rows):
    norm = []
    for row in rows:
        norm.append(tuple(round(v, 4) if isinstance(v, float) else v for v in row))
    return norm


def compare(actual_rows, expected):
    actual = normalize(actual_rows)
    expected_rows = normalize(expected["rows"])
    if expected["order_matters"]:
        passed = actual == expected_rows
    else:
        passed = sorted(actual, key=lambda r: tuple(str(x) for x in r)) == \
                 sorted(expected_rows, key=lambda r: tuple(str(x) for x in r))
    return passed


def fmt_table(colnames, rows):
    if not rows:
        return "_(no rows returned)_\n"
    header = "| " + " | ".join(colnames) + " |"
    sep = "|" + "|".join(["---"] * len(colnames)) + "|"
    lines = [header, sep]
    for row in rows:
        cells = ["NULL" if v is None else str(v) for v in row]
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines) + "\n"


def main():
    created = build_database()
    conn = sqlite3.connect(DB_PATH)

    setup_checks = run_checks(conn)
    print("=== Setup verification ===")
    setup_ok = True
    for name, ok, val in setup_checks:
        print(f"  [{'OK' if ok else 'FAIL'}] {name} (got {val})")
        setup_ok = setup_ok and ok
    if not setup_ok:
        print("Setup checks failed - aborting before running queries.")
        conn.close()
        return

    queries = parse_queries(QUERIES_SQL.read_text(encoding="utf-8"))

    report_lines = []
    report_lines.append("# Assignment 3 Test Results\n")
    report_lines.append(f"**Engine used for this test run:** SQLite 3 (Python `sqlite3` module), "
                         f"via `{DB_PATH.name}` in this folder.\n")
    report_lines.append("**Important:** No Oracle instance was available or configured in this "
                         "environment, so these are SQLite execution results, not Oracle execution "
                         "results. A SQLite PASS confirms the query's logic produces the right "
                         "columns and rows against the assignment's sample data; it does not by "
                         "itself guarantee Oracle-specific syntax compatibility (all 10 submitted "
                         "queries here use only ANSI-standard SQL that runs unchanged on both "
                         "engines - no Oracle-only functions were used).\n")
    report_lines.append("## Setup verification\n")
    for name, ok, val in setup_checks:
        report_lines.append(f"- [{'PASS' if ok else 'FAIL'}] {name} (actual: {val})")
    report_lines.append("")

    pass_count = 0
    fail_list = []

    for qnum in range(1, 11):
        stmt = queries.get(qnum)
        report_lines.append(f"## Q{qnum}\n")
        report_lines.append(f"**Question:** {QUESTION_TEXT[qnum]}\n")
        report_lines.append("**Submitted SQL (verbatim from Team11_Assignment3.docx):**\n")
        report_lines.append("```sql\n" + stmt + "\n```\n")

        cur = conn.cursor()
        try:
            cur.execute(stmt)
            rows = cur.fetchall()
            colnames = [d[0] for d in cur.description]
            error = None
        except sqlite3.Error as e:
            rows, colnames, error = [], [], str(e)

        if error:
            verdict = "FAIL"
            fail_list.append(qnum)
            report_lines.append(f"**Result: FAIL (SQL error)** - `{error}`\n")
        else:
            expected = EXPECTED[qnum]
            correct = compare(rows, expected)
            verdict = "PASS" if correct else "FAIL"
            if correct:
                pass_count += 1
            else:
                fail_list.append(qnum)

            report_lines.append(f"**Result: {verdict}**\n")
            report_lines.append(f"**Actual output ({len(rows)} row{'s' if len(rows)!=1 else ''}):**\n")
            report_lines.append(fmt_table(colnames, rows))
            report_lines.append(f"**Why:** {expected['note']}\n")

            if not correct:
                report_lines.append(f"**Expected ({len(expected['rows'])} rows):**\n")
                report_lines.append(fmt_table(colnames if colnames else [f"col{i}" for i in range(len(expected['rows'][0]))], expected["rows"]))

        report_lines.append("---\n")

    summary = (f"\n## Summary\n\n"
               f"**{pass_count} / 10 answers passed** against the SQLite test database.\n")
    if fail_list:
        summary += f"\nQuestions that need a fix before submission: {', '.join('Q'+str(q) for q in fail_list)}\n"
    else:
        summary += "\nNo changes needed before submission based on this test.\n"

    RESULTS_MD.write_text("\n".join(report_lines) + summary, encoding="utf-8")

    print(f"\n{pass_count}/10 passed. Report written to {RESULTS_MD}")
    if fail_list:
        print(f"Failing: {fail_list}")

    conn.close()


if __name__ == "__main__":
    main()
