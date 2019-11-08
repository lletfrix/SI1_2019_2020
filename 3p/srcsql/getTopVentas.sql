-------------------------------------------------------------------------
-- Authors:
--          · Alejandro Santorum Varela
--          · Rafael Sanchez Sanchez
--  Date: October 7, 2019
--  File: getTopVentas.sql
--  Project: Computer Systems I Assignments
-------------------------------------------------------------------------

CREATE OR REPLACE FUNCTION getTopVentas(integer)
    RETURNS TABLE (
        annio integer,
        title varchar,
        maxSales integer)
    AS $$

    BEGIN
        RETURN QUERY SELECT
            cast(yr as integer),
            movietitle,
            cast(MaxAmountYear as integer)

            FROM
                imdb_movies,
                (
                    SELECT APYT.movieid, MaxAmountPerYearTable.MaxAmountYear, MaxAmountPerYearTable.yr
                    FROM (
                        SELECT movieid, DATE_PART('year', orderdate) as yr, sum(quantity) as amount_per_year
                        FROM orders, orderdetail, products
                        WHERE orders.orderid=orderdetail.orderid
                            AND orderdetail.prod_id=products.prod_id
                            AND DATE_PART('year', orderdate) >= $1
                            GROUP BY yr, movieid
                    ) APYT
                    INNER JOIN
                        (SELECT yr, max(amount_per_year) as MaxAmountYear
                        FROM
                            (
                                SELECT movieid, DATE_PART('year', orderdate) as yr, sum(quantity) as amount_per_year
                                FROM orders, orderdetail, products
                                WHERE orders.orderid=orderdetail.orderid
                                    AND orderdetail.prod_id=products.prod_id
                                    AND DATE_PART('year', orderdate) >= $1
                                    GROUP BY yr, movieid
                            ) APYT2
                        GROUP BY yr) MaxAmountPerYearTable
                    ON APYT.yr=MaxAmountPerYearTable.yr
                    AND APYT.amount_per_year=MaxAmountPerYearTable.MaxAmountYear
                ) AS Auxiliar

            WHERE
                imdb_movies.movieid=Auxiliar.movieid;

    END;
$$ LANGUAGE plpgsql;
