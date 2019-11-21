import os
import random
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


def db_isAvailableEmail(email):
    try:
        # Connect to database
        db_conn = None
        db_conn = db_engine.connect()

        # Select users with given email
        query_str = "SELECT * FROM customers WHERE email=\''"+email+"\'"
        users_rows = db_conn.execute(query_str)

        db_conn.close() # Close the connection
        if users_rows.rowcount == 0:
            users_rows.close()
            return True # Given email is not in the db

        users_rows.close()
        return False

    except:
        if db_conn is not None:
            db_conn.close()
        print("Exception in DB access:")
        print("-"*60)
        traceback.print_exc(file=sys.stderr)
        print("-"*60)

        return False


def db_registerUser(username, password, email, firstname, lastname, address1,
                    city, region, country, ccard_type, ccard_num, ccard_exp):
    try:
        # Connect to database
        db_conn = None
        db_conn = db_engine.connect()

        sep = "\'"
        coma = ", "
        query_str = "INSERT INTO customers(firstname, lastname, address1, city, "
        query_str += "country, region, email, creditcardtype, creditcard, "
        query_str += "creditcardexpiration, username, password, age, income)"
        query_str += " VALUES ("+sep+firstname+sep+coma+sep+lastname+sep+coma
        query_str += sep+address1+sep+coma+sep+city+sep+coma+sep+country+sep+coma
        query_str += sep+region+sep+coma+sep+email+sep+coma+sep+ccard_type+sep+coma
        query_str += sep+ccard_num+sep+coma+sep+ccard_exp+sep+coma+sep+username+sep+coma
        query_str += sep+password+sep+coma+str(random.randint(16, 75))+coma
        query_str += str(random.randint(9999, 99999))+")"
        ret = db_conn.execute(query_str)

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

        return False




if __name__ == "__main__":
    print(db_registerUser('maria', 'qwertyu', 'dasnjdbnas@askjda.es', 'dasda', 'dsadsa', 'dasdsa', 'dsada', 'dasdsa', 'dasdsa', 'visa', '1234567891234567', '222203'))
