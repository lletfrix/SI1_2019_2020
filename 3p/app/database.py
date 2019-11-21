import os
import sys, traceback
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, text
from sqlalchemy.sql import select

# Configure sqlalchemy engine
db_engine = create_engine("postgresql://alumnodb:alumnodb@localhost/si1", echo=False)
db_meta = MetaData(bind=db_engine)
# load a table
#####db_table_movies = Table('customers', db_meta, autoload=True, autoload_with=db_engine)


def db_userData(email):
    try:
        # Connect to database
        db_conn = None
        db_conn = db_engine.connect()

        # Search for the user with the given email
        query_str = 'SELECT * FROM customers WHERE email=\''+email+'\''
        customer_rows = db_conn.execute(query_str)

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
        return ret_dict

    except:
        if db_conn is not None:
            db_conn.close()
        print("Exception in DB access:")
        print("-"*60)
        traceback.print_exc(file=sys.stderr)
        print("-"*60)

        return None



if __name__ == "__main__":
    print(db_userCart('taco.bed@jmail.com'))
