
SELECT Aux.month, Aux.year, Aux.total_cash
FROM (
    SELECT DATE_PART('month', orderdate) as month,
           DATE_PART('year', orderdate) as year,
           sum(totalamount) as total_cash
    FROM orders
    GROUP BY month, year
) Aux
WHERE Aux.total_cash > 300000;

-------------------------------------------------

SELECT Aux.month, Aux.year, Aux.total_prod
FROM (
    SELECT DATE_PART('month', orderdate) as month,
           DATE_PART('year', orderdate) as year,
           sum(quantity) as total_prod
    FROM orders INNER JOIN orderdetail
        ON orders.orderid=orderdetail.orderid
    GROUP BY month, year
) Aux
WHERE Aux.total_prod > 19000;


-------------------------------------------------

SELECT month, year, total_prod, total_cash
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
WHERE (total_prod > 19000)
     OR (total_cash > 300000);


-------------------------------------------------
