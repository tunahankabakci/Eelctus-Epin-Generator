import psycopg2
from configparser import ConfigParser


def config(filename='database.ini', section='postgresql'):
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)

    # get section, default to postgresql
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))

    return db


def connect():
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)

        # create a cursor
        cur = conn.cursor()

        # execute a statement
        print('PostgreSQL database version:')
        cur.execute('SELECT version()')

        # display the PostgreSQL database server version
        db_version = cur.fetchone()
        print(db_version)

        # close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')


def set_query(sql):
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute(sql)
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return 0
    finally:
        if conn is not None:
            conn.commit()
            conn.close()


def get_query(sql):
    conn = None
    response = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute(sql)
        response = cur.fetchone()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return 0
    finally:
        if conn is not None:
            conn.close()
            return response


def get_query_all(sql):
    conn = None
    response = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute(sql)
        response = cur.fetchall()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return 0
    finally:
        if conn is not None:
            conn.close()
            return response


def create_table():
    sql = """ CREATE TABLE accounts(
       created_at TIMESTAMPTZ DEFAULT Now(),
       android_id VARCHAR(255) UNIQUE NOT NULL,
       username VARCHAR(255),
       session_ticket VARCHAR(255),
       entity_token VARCHAR(1000),
       device_name VARCHAR(255),
       device_uid VARCHAR(255),
       device_os VARCHAR(255),
       device_gpu VARCHAR(255),
       device_cpu VARCHAR(255),
       playfab_id VARCHAR (255),
       entity_id VARCHAR (255),
       client_session_id VARCHAR (255),
       focus_id VARCHAR(255),
       device_token VARCHAR(255)       
    )
    """
    set_query(sql)
