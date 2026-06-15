import os
import psycopg
from dotenv import load_dotenv

load_dotenv() # Loads environment variables from .env file into os.environ

def get_connection():
    try:
        return psycopg.connect(
            os.environ["DATABASE_URL"],
        )
    except KeyError as err:
        raise RuntimeError(f'Missing environment variable: {err}')
    except psycopg.Error as err:
        raise RuntimeError(f'Database connection failed: {err}')