-------------------------------------------------------------------------
-- Authors:
--          · Alejandro Santorum Varela
--          · Rafael Sanchez Sanchez
--  Date: November 29, 2019
--  File: queryFormStudy.sql
--  Project: Computer Systems I Assignments
-------------------------------------------------------------------------

EXPLAIN
SELECT customerid
FROM customers
WHERE customerid NOT IN (
    SELECT customerid
    FROM orders
    WHERE status='Paid'
);

EXPLAIN
SELECT customerid
FROM (
    SELECT customerid
    FROM customers
    UNION ALL
    SELECT customerid
    FROM orders
    WHERE status='Paid'
) as A
GROUP BY customerid
HAVING COUNT(*)=1;

EXPLAIN
SELECT customerid
FROM customers
EXCEPT
    SELECT customerid
    FROM orders
    WHERE status='Paid';
