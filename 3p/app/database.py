import os
import random
import sys, traceback
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, text
from sqlalchemy.sql import select
from sqlalchemy.exc import IntegrityError
from psycopg2.errors import UniqueViolation

# Configure sqlalchemy engine
# db_engine = create_engine("postgresql://alumnodb:alumnodb@localhost/si1", echo=False)
db_engine = create_engine("postgresql://alumnodb:alumnodb@localhost/si1?client_encoding=utf8", echo=False)
db_meta = MetaData(bind=db_engine)
# load tables
db_tb_movies = Table('imdb_movies', db_meta, autoload=True, autoload_with=db_engine)
db_tb_customers = Table('customers', db_meta, autoload=True, autoload_with=db_engine)
db_tb_orderdetail = Table('orderdetail', db_meta, autoload=True, autoload_with=db_engine)
db_tb_genres = Table('genres', db_meta, autoload=True, autoload_with=db_engine)


def db_userData(email):
    try:
        # Connect to database
        db_conn = None
        db_conn = db_engine.connect()

        # Search for the user with the given email
        query = select([db_tb_customers]).where(text("email=\'"+email+"\'"))
        customer_rows = db_conn.execute(query)

        db_conn.close() # Close the connection
        if customer_rows.rowcount == 0:
            customer_rows.close()
            return None # Given customer is not registered

        # Email is primary key, so it is an unique result (if any)
        userdata = list(customer_rows)[0]
        ret_userdata = {
            'nickname': userdata[15],
            'password': userdata[16],
            'mail': userdata[10],
            'ccard': userdata[13],
            'cash': userdata[-1],
            'address': userdata[3],
        }
        customer_rows.close()
        return ret_userdata
    except:
        if db_conn is not None:
            db_conn.close()
        print("Exception in DB access:")
        print("-"*60)
        traceback.print_exc(file=sys.stderr)
        print("-"*60)

        return None


def db_userCart(email):
    try:
        # Connect to database
        db_conn = None
        db_conn = db_engine.connect()

        # Search for the cart of the user of the given email
        query_str = 'SELECT prod_id, quantity FROM orders, orderdetail, customers '
        query_str += 'WHERE customers.email=\''+email+'\' AND '
        query_str += 'customers.customerid=orders.customerid AND '
        query_str += 'orders.status IS NULL AND orders.orderid=orderdetail.orderid'
        cart_rows = db_conn.execute(query_str)

        db_conn.close() # Close the connection
        if cart_rows.rowcount == 0:
            cart_rows.close()
            return None # Given customer has anything in cart

        ret_list = list(cart_rows)
        ret_dict = {}
        for tuple in ret_list:
            ret_dict[tuple[0]] = tuple[1]
        cart_rows.close()
        return ret_dict

    except:
        if db_conn is not None:
            db_conn.close()
        print("Exception in DB access:")
        print("-"*60)
        traceback.print_exc(file=sys.stderr)
        print("-"*60)

        return None


SEP = "\'"
COMA = ", "
def _build_query_values(*argv):
    l = len(argv)
    qry_val = ""
    for i in range(l):
        if i != l-1:
            qry_val += SEP+argv[i]+SEP+COMA
        else:
            qry_val += SEP+argv[i]+SEP
    return qry_val


def db_registerUser(username, password, email, firstname, lastname, address1,
                    city, region, country, ccard_type, ccard_num, ccard_exp):
    try:
        # Connect to database
        db_conn = None
        db_conn = db_engine.connect()

        query = db_tb_customers.insert().values(
                                        firstname=firstname,
                                        lastname=lastname,
                                        address1=address1,
                                        city=city,
                                        country=country,
                                        region=region,
                                        email=email,
                                        creditcardtype=ccard_type,
                                        creditcard=ccard_num,
                                        creditcardexpiration=ccard_exp,
                                        username=username,
                                        password=password,
                                        age=random.randint(16, 75),
                                        income=random.randint(9999, 99999)
                                        )
        ret = db_conn.execute(query)

        db_conn.close() # Close the connection
        return True
    except IntegrityError as e: # Checking if the email is already registered
        assert isinstance(e.orig, UniqueViolation)
        return False
    except: # Other exceptions
        if db_conn is not None:
            db_conn.close()
        print("Exception in DB access:")
        print("-"*60)
        traceback.print_exc(file=sys.stderr)
        print("-"*60)
        return False #TODO: Maybe return None to differenciate from False?


def db_getGenres():
    try:
        # Connect to database
        db_conn = None
        db_conn = db_engine.connect()

        query = select([db_tb_genres.c.genre.distinct()])
        genres_ret = db_conn.execute(query)

        db_conn.close()

        genres_lst = []
        for item in genres_ret:
            genres_lst.append(item[0])
        genres_ret.close()
        return list(genres_lst)
    except:
        if db_conn is not None:
            db_conn.close()
        print("Exception in DB access:")
        print("-"*60)
        traceback.print_exc(file=sys.stderr)
        print("-"*60)

        return None


#TODO: Check what happens if the user searches with gender filter but no search string
def db_search(search_str, gender=None):
    try:
        # Connect to database
        db_conn = None
        db_conn = db_engine.connect()

        if gender == None:
            where_str = "movietitle LIKE \'%"+search_str+"%\'"
            query = select([db_tb_movies]).where(text(where_str))
            ret = db_conn.execute(query)

            db_conn.close() # Close the connection
            return list(ret)

    except: # Other exceptions
        if db_conn is not None:
            db_conn.close()
        print("Exception in DB access:")
        print("-"*60)
        traceback.print_exc(file=sys.stderr)
        print("-"*60)
        return None


#TODO: CHECK TRIGGER
def db_insertItemCart(orderid, prod_id, unit_price, quantity):
    try:
        # Connect to database
        db_conn = None
        db_conn = db_engine.connect()

        query = db_tb_orderdetail.insert().values(
                                        orderid=orderid,
                                        prod_id=prod_id,
                                        price=unit_price,
                                        quantity=quantity
                                        )
        ret = db_conn.execute(query)

        db_conn.close() # Close the connection
        ret.close()
        return True
    except:
        if db_conn is not None:
            db_conn.close()
        print("Exception in DB access:")
        print("-"*60)
        traceback.print_exc(file=sys.stderr)
        print("-"*60)

        return False #TODO: Maybe return None to differenciate from False?



if __name__ == "__main__":
    # print(db_userData('mail@mail.es'))
    # print(db_registerUser('hallow', '123456789', 'mail@mail.es', 'alex', 'santo', 'plaza marina', 'lalin', 'pont', 'espana', 'visa', '1234567891234567', '222203'))
    # print(db_insertItemCart(181791, 9, 19, 2))

    # title_part = "George"
    # print(db_search(title_part))
    # print("=======================")

    # print(db_getGenres(), "|||", len(db_getGenres()))
