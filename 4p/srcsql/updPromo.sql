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
        UPDATE orderdetail
        SET price=products.price*(1-(NEW.promo/100)) -- discount
        FROM products, orders, customers
        WHERE orders.customerid=NEW.customerid -- NEW.customerid is equal to customers.customerid
            AND orders.status IS NULL -- cart item
            AND orders.orderid=orderdetail.orderid
            AND orderdetail.prod_id=products.prod_id;
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
