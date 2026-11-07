-- ============================================================
-- Assignment3_Setup_Oracle.sql
-- BUAN 6320 - Assignment 3 - Vendor_T / Product_T sample database
--
-- NOTE: No "Assignment3_Setup.sql" file was found on disk for this
-- assignment (searched Downloads, the course folder, and the Code
-- working directory). This script was reconstructed directly from
-- the table definitions and sample data printed in Assignment3.pdf
-- (pages 1-2), which match the required checks: 5 vendors, 12
-- products, 2 products with no vendor (B349, B401), and 2 vendors
-- with no products (Sterling/22000, Thomas/23002).
-- ============================================================

-- Safe drops: only remove these two tables if they already exist, and only
-- if you want to rebuild them from scratch. Comment out if you already have
-- data in them that you want to keep.
BEGIN
    EXECUTE IMMEDIATE 'DROP TABLE Product_T';
EXCEPTION
    WHEN OTHERS THEN
        IF SQLCODE != -942 THEN RAISE; END IF; -- ignore "table does not exist"
END;
/
BEGIN
    EXECUTE IMMEDIATE 'DROP TABLE Vendor_T';
EXCEPTION
    WHEN OTHERS THEN
        IF SQLCODE != -942 THEN RAISE; END IF;
END;
/

CREATE TABLE Vendor_T (
    v_code      VARCHAR2(10) PRIMARY KEY,
    v_contact   VARCHAR2(50),
    v_areacode  VARCHAR2(5),
    v_phone     VARCHAR2(20),
    v_state     VARCHAR2(5)
);

CREATE TABLE Product_T (
    p_code      VARCHAR2(10) PRIMARY KEY,
    p_onhand    NUMBER,
    p_min       NUMBER,
    p_price     NUMBER(8,2),
    p_discount  NUMBER(4,2),
    v_code      VARCHAR2(10),
    CONSTRAINT fk_product_vendor FOREIGN KEY (v_code) REFERENCES Vendor_T(v_code)
);

INSERT INTO Vendor_T VALUES ('21222', 'Smith',    '972', '666-8888', 'TX');
INSERT INTO Vendor_T VALUES ('21232', 'Ferguson', '817', '222-7777', 'TX');
INSERT INTO Vendor_T VALUES ('22000', 'Sterling', '304', '888-9999', 'FL');
INSERT INTO Vendor_T VALUES ('23002', 'Thomas',   '302', '111-2222', 'TX');
INSERT INTO Vendor_T VALUES ('25489', 'Joyce',    '212', '333-4444', 'FL');

INSERT INTO Product_T VALUES ('A102', 23, 10, 100.50, 0.05, '21222');
INSERT INTO Product_T VALUES ('A104', 8,  10, 53.75,  0.10, '21232');
INSERT INTO Product_T VALUES ('A250', 40, 5,  75.50,  0.05, '25489');
INSERT INTO Product_T VALUES ('B349', 80, 20, 34.00,  0.00, NULL);
INSERT INTO Product_T VALUES ('B401', 53, 5,  25.00,  0.00, NULL);
INSERT INTO Product_T VALUES ('B567', 8,  10, 15.00,  0.10, '25489');
INSERT INTO Product_T VALUES ('B709', 6,  10, 65.00,  0.07, '21222');
INSERT INTO Product_T VALUES ('C444', 84, 15, 8.00,   0.10, '21222');
INSERT INTO Product_T VALUES ('C458', 28, 10, 20.00,  0.05, '21232');
INSERT INTO Product_T VALUES ('D476', 65, 10, 27.50,  0.15, '21232');
INSERT INTO Product_T VALUES ('D897', 45, 5,  89.50,  0.12, '25489');
INSERT INTO Product_T VALUES ('D900', 38, 10, 8.00,   0.08, '21222');

COMMIT;
