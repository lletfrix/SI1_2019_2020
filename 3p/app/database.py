import sqlalchemy as db

# Configure engine
engine = db.create_engine("postgresql://alumnodb:alumnodb@localhost/si1", echo=False)

def db_userData(nickname, password):
    try:
        # Connect to database
        conn = engine.connect()

        # Search for the user
        user_row = conn.execute()
        conn.close() # Close the connection
        if user_row.rowcount == 0:
            user_row.close()
            return None # Usuario no existente

        userdata = {}

        return  userdata
    except:
        if db_conn is not None:
            db_conn.close()
        print("Exception in DB access:")
        print("-"*60)
        traceback.print_exc(file=sys.stderr)
        print("-"*60)

        return None
