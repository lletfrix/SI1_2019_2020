-- Adding foreign key in orders
ALTER TABLE orders
ADD CONSTRAINT orders_customerid_fkey
FOREIGN KEY (customerid) REFERENCES customers(customerid)
ON DELETE CASCADE;

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
