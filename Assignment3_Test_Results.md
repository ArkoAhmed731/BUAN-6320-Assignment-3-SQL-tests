# Assignment 3 Test Results

**Engine used for this test run:** SQLite 3 (Python `sqlite3` module), via `Assignment3_Test.db` in this folder.

**Important:** No Oracle instance was available or configured in this environment, so these are SQLite execution results, not Oracle execution results. A SQLite PASS confirms the query's logic produces the right columns and rows against the assignment's sample data; it does not by itself guarantee Oracle-specific syntax compatibility (all 10 submitted queries here use only ANSI-standard SQL that runs unchanged on both engines - no Oracle-only functions were used).

## Setup verification

- [PASS] 5 vendors (actual: 5)
- [PASS] 12 products (actual: 12)
- [PASS] 2 products with no vendor (actual: 2)
- [PASS] 2 vendors with no products (actual: 2)

## Q1

**Question:** List the products and corresponding vendor codes for products whose inventory is less than the minimum stock quantity or products that are priced less than $75 with discount greater than 5%.

**Submitted SQL (verbatim from Team11_Assignment3.docx):**

```sql
SELECT p_code, v_code
FROM Product_T
WHERE p_onhand < p_min
   OR (p_price < 75 AND p_discount > 0.05);
```

**Result: PASS**

**Actual output (6 rows):**

| p_code | v_code |
|---|---|
| A104 | 21232 |
| B567 | 25489 |
| B709 | 21222 |
| C444 | 21222 |
| D476 | 21232 |
| D900 | 21222 |

**Why:** p_onhand<p_min (A104,B567,B709) UNION products priced<$75 with discount>5% (C444,D476,D900,B709). A product below minimum stock qualifies regardless of price/discount.

---

## Q2

**Question:** List the distinct codes of vendors supplying products for which minimum stock quantity is less than 10.

**Submitted SQL (verbatim from Team11_Assignment3.docx):**

```sql
SELECT DISTINCT v_code
FROM Product_T
WHERE p_min < 10 AND v_code IS NOT NULL;
```

**Result: PASS**

**Actual output (1 row):**

| v_code |
|---|
| 25489 |

**Why:** Only A250 and D897 have p_min<10 among vendor-supplied products; both belong to vendor 25489. B401 also has p_min<10 but is in-house (v_code NULL) and is excluded.

---

## Q3

**Question:** For each vendor, list the minimum price and the average discount rate for their products for which the quantity on hand is less than the minimum stock quantity.

**Submitted SQL (verbatim from Team11_Assignment3.docx):**

```sql
SELECT v_code, MIN(p_price) AS min_price,
       AVG(p_discount) AS avg_discount
FROM Product_T
WHERE p_onhand < p_min AND v_code IS NOT NULL
GROUP BY v_code;
```

**Result: PASS**

**Actual output (3 rows):**

| v_code | min_price | avg_discount |
|---|---|---|
| 21222 | 65.0 | 0.07 |
| 21232 | 53.75 | 0.1 |
| 25489 | 15.0 | 0.1 |

**Why:** Only A104(21232), B567(25489), B709(21222) have p_onhand<p_min; one qualifying row per vendor.

---

## Q4

**Question:** For each available discount rate of less than 10%, show the minimum price and the maximum price of products with the same discount rate.

**Submitted SQL (verbatim from Team11_Assignment3.docx):**

```sql
SELECT p_discount, MIN(p_price) AS min_price,
       MAX(p_price) AS max_price
FROM Product_T
WHERE p_discount < 0.10
GROUP BY p_discount;
```

**Result: PASS**

**Actual output (4 rows):**

| p_discount | min_price | max_price |
|---|---|---|
| 0.0 | 25.0 | 34.0 |
| 0.05 | 20.0 | 100.5 |
| 0.07 | 65.0 | 65.0 |
| 0.08 | 8.0 | 8.0 |

**Why:** Discounts 0.1 (A104,B567,C444) are excluded since the question asks for <10%.

---

## Q5

**Question:** List the minimum and maximum prices of products for each vendor for vendors who supply more than 3 items.

**Submitted SQL (verbatim from Team11_Assignment3.docx):**

```sql
SELECT v_code, MIN(p_price) AS min_price,
       MAX(p_price) AS max_price
FROM Product_T
WHERE v_code IS NOT NULL
GROUP BY v_code
HAVING COUNT(*) > 3;
```

**Result: PASS**

**Actual output (1 row):**

| v_code | min_price | max_price |
|---|---|---|
| 21222 | 8.0 | 100.5 |

**Why:** Vendor 21222 supplies 4 products (A102,B709,C444,D900); 21232 and 25489 supply only 3 each.

---

## Q6

**Question:** Which products are priced more than the average price? Display product code and product price.

**Submitted SQL (verbatim from Team11_Assignment3.docx):**

```sql
SELECT p_code, p_price
FROM Product_T
WHERE p_price > (SELECT AVG(p_price) FROM Product_T);
```

**Result: PASS**

**Actual output (5 rows):**

| p_code | p_price |
|---|---|
| A102 | 100.5 |
| A104 | 53.75 |
| A250 | 75.5 |
| B709 | 65.0 |
| D897 | 89.5 |

**Why:** Average price across all 12 products = 521.75/12 = 43.4792.

---

## Q7

**Question:** List all products supplied by the vendor with the highest-priced product. Include vendor details together with product details.

**Submitted SQL (verbatim from Team11_Assignment3.docx):**

```sql
SELECT p.p_code, p.p_onhand, p.p_min, p.p_price, p.p_discount,
       v.v_code, v.v_contact, v.v_areacode, v.v_phone, v.v_state
FROM Product_T p
JOIN Vendor_T v ON v.v_code = p.v_code
WHERE v.v_code IN (
    SELECT v_code
    FROM Product_T
    WHERE p_price = (SELECT MAX(p_price) FROM Product_T)
);
```

**Result: PASS**

**Actual output (4 rows):**

| p_code | p_onhand | p_min | p_price | p_discount | v_code | v_contact | v_areacode | v_phone | v_state |
|---|---|---|---|---|---|---|---|---|---|
| A102 | 23 | 10 | 100.5 | 0.05 | 21222 | Smith | 972 | 666-8888 | TX |
| B709 | 6 | 10 | 65.0 | 0.07 | 21222 | Smith | 972 | 666-8888 | TX |
| C444 | 84 | 15 | 8.0 | 0.1 | 21222 | Smith | 972 | 666-8888 | TX |
| D900 | 38 | 10 | 8.0 | 0.08 | 21222 | Smith | 972 | 666-8888 | TX |

**Why:** Highest-priced product is A102 ($100.50) from vendor 21222 (Smith). All 4 of 21222's products must be returned, not just A102.

---

## Q8

**Question:** Get the detail of the vendor who has supplied the product for which the dollar value of the on hand inventory is the highest.

**Submitted SQL (verbatim from Team11_Assignment3.docx):**

```sql
SELECT v.*
FROM Vendor_T v
WHERE v.v_code IN (
    SELECT p.v_code
    FROM Product_T p
    WHERE p.p_onhand * p.p_price = (
        SELECT MAX(p_onhand * p_price) FROM Product_T
    )
);
```

**Result: PASS**

**Actual output (1 row):**

| v_code | v_contact | v_areacode | v_phone | v_state |
|---|---|---|---|---|
| 25489 | Joyce | 212 | 333-4444 | FL |

**Why:** Inventory value (p_onhand*p_price) is highest for D897 (45*89.5=4027.5, vendor 25489/Joyce). B349 (80*34=2720, in-house) is higher than most but is not vendor-supplied, so it can't produce a vendor match.

---

## Q9

**Question:** For each vendor, list the product codes of products supplied along with vendor code and vendor contact name. Display vendor information even if there is no product currently supplied by the vendor. Sort the results by vendor code.

**Submitted SQL (verbatim from Team11_Assignment3.docx):**

```sql
SELECT v.v_code, v.v_contact, p.p_code
FROM Vendor_T v
LEFT JOIN Product_T p ON p.v_code = v.v_code
ORDER BY v.v_code, p.p_code;
```

**Result: PASS**

**Actual output (12 rows):**

| v_code | v_contact | p_code |
|---|---|---|
| 21222 | Smith | A102 |
| 21222 | Smith | B709 |
| 21222 | Smith | C444 |
| 21222 | Smith | D900 |
| 21232 | Ferguson | A104 |
| 21232 | Ferguson | C458 |
| 21232 | Ferguson | D476 |
| 22000 | Sterling | NULL |
| 23002 | Thomas | NULL |
| 25489 | Joyce | A250 |
| 25489 | Joyce | B567 |
| 25489 | Joyce | D897 |

**Why:** 12 rows: 10 vendor-product pairs plus Sterling(22000) and Thomas(23002) each with a NULL product code, ordered by v_code.

---

## Q10

**Question:** Display the phone number and the area code of each vendor whose average price of supplied products is greater than the average price of the products manufactured in house.

**Submitted SQL (verbatim from Team11_Assignment3.docx):**

```sql
SELECT v.v_phone, v.v_areacode
FROM Vendor_T v
JOIN Product_T p ON p.v_code = v.v_code
GROUP BY v.v_code, v.v_phone, v.v_areacode
HAVING AVG(p.p_price) > (
    SELECT AVG(p_price)
    FROM Product_T
    WHERE v_code IS NULL
);
```

**Result: PASS**

**Actual output (3 rows):**

| v_phone | v_areacode |
|---|---|
| 666-8888 | 972 |
| 222-7777 | 817 |
| 333-4444 | 212 |

**Why:** In-house average price = (34+25)/2 = 29.5. Vendor averages: 21222=45.375, 21232=33.75, 25489=60 -- all three exceed 29.5.

---

## Summary

**10 / 10 answers passed** against the SQLite test database.

No changes needed before submission based on this test.
