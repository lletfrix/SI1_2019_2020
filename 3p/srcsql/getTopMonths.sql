-------------------------------------------------------------------------
-- Authors:
--          · Alejandro Santorum Varela
--          · Rafael Sanchez Sanchez
--  Date: October 7, 2019
--  File: getTopMonths.sql
--  Project: Computer Systems I Assignments
-------------------------------------------------------------------------

-- ARG 1 : threshold for product amount
-- ARG 2 : threshold for totalamount
CREATE OR REPLACE FUNCTION getTopMonths(integer, integer)
    RETURNS TABLE (
        m integer,
        y integer,
        t_prod bigint,
        t_cash numeric
    )
    AS $$
    BEGIN
        RETURN QUERY SELECT
            CAST(month AS integer),
            CAST(year AS integer),
            total_prod,
            total_cash
        FROM (
                SELECT DATE_PART('month', orderdate) as month,
                       DATE_PART('year', orderdate) as year,
                       sum(quantity) as total_prod
                FROM orders INNER JOIN orderdetail
                    ON orders.orderid=orderdetail.orderid
                GROUP BY month, year
            ) TotalProd
        NATURAL JOIN
            (
                SELECT DATE_PART('month', orderdate) as month,
                       DATE_PART('year', orderdate) as year,
                       sum(totalamount) as total_cash
                FROM orders
                GROUP BY month, year
            ) TotalCash
        WHERE (total_prod > $1)
             OR (total_cash > $2);
    END;
$$ LANGUAGE plpgsql;

-------------------------------------------------
