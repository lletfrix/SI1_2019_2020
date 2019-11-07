-------------------------------------------------------------------------
-- Authors:
--          · Alejandro Santorum Varela
--          · Rafael Sanchez Sanchez
--  Date: October 7, 2019
--  File: actualiza.sql
--  Project: Computer Systems I Assignments
-------------------------------------------------------------------------

-------------------------------------------------------------------------
-- ADDING PRIMARY KEYS AND FOREIGN KEYS

-- Adding foreign key in orders
ALTER TABLE orders
ADD CONSTRAINT orders_customerid_fkey
FOREIGN KEY (customerid) REFERENCES customers(customerid); -- no action

-- Adding primary key in actormovies
ALTER TABLE imdb_actormovies
ADD CONSTRAINT imdb_actormovies_pkey
PRIMARY KEY (actorid, movieid);

-- Adding foreign key in actormovies (actorid)
ALTER TABLE imdb_actormovies
ADD CONSTRAINT imdb_actormovies_actorid_fkey
FOREIGN KEY (actorid) REFERENCES imdb_actors(actorid)
ON DELETE CASCADE;

-- Adding foreign key in actormovies (movieid)
ALTER TABLE imdb_actormovies
ADD CONSTRAINT imdb_actormovies_movieid_fkey
FOREIGN KEY (movieid) REFERENCES imdb_movies(movieid)
ON DELETE CASCADE;

-- Deleting num_participation from directormovies PK
ALTER TABLE imdb_directormovies
DROP CONSTRAINT imdb_directormovies_pkey;

ALTER TABLE imdb_directormovies
ADD CONSTRAINT imdb_directormovies_pkey
PRIMARY KEY (directorid, movieid);

-- Getting tuples (orderid, prod_id) with no repetitions and the added quantity
SELECT orderid, prod_id, sum(quantity) INTO od_aux
FROM orderdetail
GROUP BY orderid, prod_id;

-- Deleting old orderdetail table
DROP TABLE orderdetail;

-- Creating a new one
CREATE TABLE public.orderdetail (
    orderid integer NOT NULL,
    prod_id integer NOT NULL,
    price numeric,
    quantity integer NOT NULL
);
ALTER TABLE public.orderdetail OWNER TO alumnodb;

-- Inserting tuples with no repetitions
INSERT INTO orderdetail (orderid, prod_id, quantity)
SELECT *
FROM od_aux;

-- Droping auxiliary table
DROP TABLE od_aux;

-- Adding primary key in orderdetail
ALTER TABLE orderdetail
ADD CONSTRAINT orderdetail_pkey
PRIMARY KEY (orderid, prod_id);

-- Adding foreign key in orderdetail (orderid)
ALTER TABLE orderdetail
ADD CONSTRAINT orderdetail_orderid_fkey
FOREIGN KEY (orderid) REFERENCES orders(orderid)
ON DELETE CASCADE;

-- Adding foreign key in actormovies (movieid)
ALTER TABLE orderdetail
ADD CONSTRAINT imdb_prod_id_fkey
FOREIGN KEY (prod_id) REFERENCES products(prod_id); -- no action


-------------------------------------------------------------------------
-- MERGING INVENTORY TABLE WITH PRODUCTS TABLE (1-1 relation)

-- Creating new columns stock and sales in products' table
ALTER TABLE products
ADD COLUMN stock integer;

ALTER TABLE products
ADD COLUMN sales integer;

-- Merging stock values
UPDATE products
SET stock=inventory.stock
FROM inventory
WHERE products.prod_id=inventory.prod_id;

-- Merging sales values
UPDATE products
SET sales=inventory.sales
FROM inventory
WHERE products.prod_id=inventory.prod_id;

-- Deleting deprecated inventory table
DROP TABLE inventory;
-------------------------------------------------------------------------


-------------------------------------------------------------------------
CREATE TABLE public.languages(
    language_id integer PRIMARY KEY NOT NULL,
    language character varying(32) NOT NULL
);

CREATE SEQUENCE public.languages_seq
START WITH 1
INCREMENT BY 1
NO MINVALUE
NO MAXVALUE
CACHE 1;

ALTER TABLE public.languages OWNER TO alumnodb;
ALTER TABLE public.languages_seq OWNER TO alumnodb;
ALTER SEQUENCE public.languages_seq OWNED BY public.languages.language_id;
ALTER TABLE ONLY public.languages ALTER COLUMN languague_id SET DEFAULT nextval('languages:seq'::regclass);

INSERT INTO public.languages(language)
SELECT DISTINCT languages
FROM public.imdb_movielangue;

ALTER



-----------------------------------------------------------------------
