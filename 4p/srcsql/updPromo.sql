-------------------------------------------------------------------------
-- Authors:
--          · Alejandro Santorum Varela
--          · Rafael Sanchez Sanchez
--  Date: November 29, 2019
--  File: updPromo.sql
--  Project: Computer Systems I Assignments
-------------------------------------------------------------------------

-- Creating column promo in customers table
ALTER TABLE public.customers
ADD promo float DEFAULT 0;


-- Trigger function: It performs a discount on the cart products price of
--                   the user who has received a promotional discount
CREATE OR REPLACE FUNCTION updPromo_func()
RETURNS TRIGGER AS $$
    BEGIN
        ----- > TODO: Probably SLEEP HERE !!!!!!!!!!!!!!!!!!!

        -- 1st: Update orderdetail price
        UPDATE orderdetail
        SET price=products.price * (1-(NEW.promo/100)) -- discount
        FROM products, orders, customers
        WHERE orders.customerid=NEW.customerid -- NEW.customerid is equal to customers.customerid
            AND orders.status IS NULL -- cart item
            AND orders.orderid=orderdetail.orderid
            AND orderdetail.prod_id=products.prod_id;

        -- 2nd: Update orders netamount
        UPDATE orders
        SET netamount=aux_tb.value
        FROM (
            SELECT orderdetail.orderid, sum(orderdetail.price * orderdetail.quantity) as value
            FROM orders, orderdetail
            WHERE orders.orderid=orderdetail.orderid
            GROUP BY orderdetail.orderid
        ) AS aux_tb
        WHERE orders.customerid=NEW.customerid
            AND orders.status IS NULL
            AND orders.orderid=aux_tb.orderid;

        -- 3rd: Update orders totalamount
        UPDATE orders
        SET totalamount=netamount * (1+(tax/100))
        WHERE customerid=NEW.customerid
            AND orders.status IS NULL;

    RETURN NULL;
    END;
$$ LANGUAGE plpgsql;


-- Init trigger
CREATE TRIGGER updPromo_trigger
AFTER UPDATE
ON customers
FOR EACH ROW
WHEN (OLD.promo IS DISTINCT FROM NEW.promo)
EXECUTE PROCEDURE updPromo_func();


-- TODO: Insert SLEEP in the correct version of deleteCustomer page.
-- TODO: Create several carts (orderid with status = NULL).
-- TODO: Access to deleteCustomer page with an user with an initialized cart
--       and, at the same time, update promo column of the same user.
-- TODO: Check during SLEEPS changed data (page changes and trigger changes)
--       are not visible.
-- TODO: Check SLEEPS with pgAdmin (force them to get stuck in a deadlock)
-- TODO: Comment them
-- TODO: Think about how to avoid this type of problems
