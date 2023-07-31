import psycopg2
from psycopg2 import DatabaseError
from decouple import config

def get_connection():

    try:
        return psycopg2.connect(
            dbname      =   config('PG_DBNAME'),
            user        =   config('PG_USER'),
            password    =   config('PG_PASSWORD'),
            host        =   config('PG_HOST'),
            port        =   config('PG_PORT'),
            options     =   config('PG_OPTIONS')
        )
    except DatabaseError as ex:
        raise ex
