CREATE VIEW AmountPerYearTable AS
SELECT movieid, DATE_PART('year', orderdate) as yr, sum(quantity) as amount_per_year
FROM orders, orderdetail, products
WHERE orders.orderid=orderdetail.orderid
    AND orderdetail.prod_id=products.prod_id
    AND DATE_PART('year', orderdate) >= $1
    GROUP BY yr, movieid;

CREATE VIEW Maximums AS
SELECT APYT.movieid, MaxAmountPerYearTable.MaxAmountYear, MaxAmountPerYearTable.yr
FROM AmountPerYearTable APYT INNER JOIN
    (SELECT yr, max(amount_per_year) as MaxAmountYear
    FROM AmountPerYearTable
    GROUP BY yr) MaxAmountPerYearTable
ON APYT.yr=MaxAmountPerYearTable.yr
AND APYT.amount_per_year=MaxAmountPerYearTable.MaxAmountYear;

SELECT yr, movietitle, MaxAmountYear
FROM imdb_movies, Maximums
WHERE imdb_movies.movieid=Maximums.movieid;

DROP VIEW Maximums;
DROP VIEW AmountPerYearTable;
