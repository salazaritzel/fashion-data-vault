import os
import psycopg
from dotenv import load_dotenv

load_dotenv() # Loads environment variables from .env file into os.environ

def get_connection():
    try:
        return psycopg.connect(
            os.environ["DATABASE_URL"],
            # user = os.environ["DB_USER"],
            # password = os.environ["DB_PASSWORD"],
            # dbname = os.environ["DB_NAME"],
            # host = os.environ["DB_HOST"],
            # port = os.environ["DB_PORT"],
            # sslmode = 'prefer'
        )
    except KeyError as err:
        raise RuntimeError(f'Missing environment variable: {err}')
    except psycopg.Error as err:
        raise RuntimeError(f'Database connection failed: {err}')