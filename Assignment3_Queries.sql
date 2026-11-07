-- ============================================================
-- Assignment3_Queries.sql
-- Extracted VERBATIM from Team11_Assignment3.docx. Not modified
-- or corrected in any way - this is exactly what was submitted.
-- ============================================================

-- Q1: List the products and corresponding vendor codes for products whose
-- inventory is less than the minimum stock quantity or products that are
-- priced less than $75 with discount greater than 5%.
SELECT p_code, v_code
FROM Product_T
WHERE p_onhand < p_min
   OR (p_price < 75 AND p_discount > 0.05);

-- Q2: List the distinct codes of vendors supplying products for which
-- minimum stock quantity is less than 10.
SELECT DISTINCT v_code
FROM Product_T
WHERE p_min < 10 AND v_code IS NOT NULL;

-- Q3: For each vendor, list the minimum price and the average discount
-- rate for their products for which the quantity on hand is less than
-- the minimum stock quantity.
SELECT v_code, MIN(p_price) AS min_price,
       AVG(p_discount) AS avg_discount
FROM Product_T
WHERE p_onhand < p_min AND v_code IS NOT NULL
GROUP BY v_code;

-- Q4: For each available discount rate of less than 10%, show the
-- minimum price and the maximum price of products with the same
-- discount rate.
SELECT p_discount, MIN(p_price) AS min_price,
       MAX(p_price) AS max_price
FROM Product_T
WHERE p_discount < 0.10
GROUP BY p_discount;

-- Q5: List the minimum and maximum prices of products for each vendor
-- for vendors who supply more than 3 items.
SELECT v_code, MIN(p_price) AS min_price,
       MAX(p_price) AS max_price
FROM Product_T
WHERE v_code IS NOT NULL
GROUP BY v_code
HAVING COUNT(*) > 3;

-- Q6: Which products are priced more than the average price? Display
-- product code and product price.
SELECT p_code, p_price
FROM Product_T
WHERE p_price > (SELECT AVG(p_price) FROM Product_T);

-- Q7: List all products supplied by the vendor with the highest-priced
-- product. Include vendor details together with product details.
SELECT p.p_code, p.p_onhand, p.p_min, p.p_price, p.p_discount,
       v.v_code, v.v_contact, v.v_areacode, v.v_phone, v.v_state
FROM Product_T p
JOIN Vendor_T v ON v.v_code = p.v_code
WHERE v.v_code IN (
    SELECT v_code
    FROM Product_T
    WHERE p_price = (SELECT MAX(p_price) FROM Product_T)
);

-- Q8: Get the detail of the vendor who has supplied the product for
-- which the dollar value of the on hand inventory is the highest.
SELECT v.*
FROM Vendor_T v
WHERE v.v_code IN (
    SELECT p.v_code
    FROM Product_T p
    WHERE p.p_onhand * p.p_price = (
        SELECT MAX(p_onhand * p_price) FROM Product_T
    )
);

-- Q9: For each vendor, list the product codes of products supplied
-- along with vendor code and vendor contact name. Display vendor
-- information even if there is no product currently supplied by the
-- vendor. Sort the results by vendor code.
SELECT v.v_code, v.v_contact, p.p_code
FROM Vendor_T v
LEFT JOIN Product_T p ON p.v_code = v.v_code
ORDER BY v.v_code, p.p_code;

-- Q10: Display the phone number and the area code of each vendor whose
-- average price of supplied products is greater than the average price
-- of the products manufactured in house.
SELECT v.v_phone, v.v_areacode
FROM Vendor_T v
JOIN Product_T p ON p.v_code = v.v_code
GROUP BY v.v_code, v.v_phone, v.v_areacode
HAVING AVG(p.p_price) > (
    SELECT AVG(p_price)
    FROM Product_T
    WHERE v_code IS NULL
);
