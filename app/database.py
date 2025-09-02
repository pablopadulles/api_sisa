import redis.asyncio as redis
import mariadb
from contextlib import contextmanager, asynccontextmanager
import os
from urllib.parse import urlparse


if os.getenv('DATABASE_URL', False):
    DATABASE_URL = os.getenv('DATABASE_URL')
else:
    DATABASE_URL = 'mysql://username:password@localhost:3306/mydatabase'

connection = None

@contextmanager
def get_db():
    global connection
    if not connection:
        connection = mariadb.connect(
                DATABASE_URL
            )        
        # dbc = urlparse(DATABASE_URL)
        # connection = mariadb.connect(
        #         user=dbc.username,
        #         password=dbc.password,
        #         host=dbc.hostname,
        #         port=dbc.port,
        #         database=dbc.path.lstrip('/')
        #     )
    try:
        yield connection
    finally:
        pass

def close_db():
    global connection
    if connection:
        connection.close()