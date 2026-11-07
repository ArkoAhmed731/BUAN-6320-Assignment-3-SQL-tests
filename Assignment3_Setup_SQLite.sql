-- ============================================================
-- Assignment3_Setup_SQLite.sql
-- SQLite adaptation of Assignment3_Setup_Oracle.sql
-- Only the Oracle-specific DDL syntax (VARCHAR2/NUMBER types,
-- explicit DROP TABLE, COMMIT) was changed. All rows, column
-- order, and NULLs are preserved exactly as in the Oracle script.
-- ============================================================

PRAGMA foreign_keys = ON;

CREATE TABLE Vendor_T (
    v_code      TEXT PRIMARY KEY,
    v_contact   TEXT,
    v_areacode  TEXT,
    v_phone     TEXT,
    v_state     TEXT
);

CREATE TABLE Product_T (
    p_code      TEXT PRIMARY KEY,
    p_onhand    INTEGER,
    p_min       INTEGER,
    p_price     REAL,
    p_discount  REAL,
    v_code      TEXT,
    FOREIGN KEY (v_code) REFERENCES Vendor_T(v_code)
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
