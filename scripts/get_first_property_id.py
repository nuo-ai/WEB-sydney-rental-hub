import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def get_db_connection():
    """Establishes a connection to the PostgreSQL database."""
    try:
        database_url = os.getenv("DATABASE_URL")
        if database_url:
            conn = psycopg2.connect(database_url)
        else:
            conn = psycopg2.connect(
                dbname=os.getenv("DB_NAME"),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD"),
                host=os.getenv("DB_HOST"),
                port=os.getenv("DB_PORT")
            )
        return conn
    except psycopg2.Error as e:
        print(f"Error connecting to the database: {e}")
        raise

def get_first_property_id():
    """Fetches the listing_id of the first property from the database."""
    conn = get_db_connection()
    listing_id = None
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT listing_id FROM properties ORDER BY listing_id LIMIT 1")
            row = cur.fetchone()
            if row:
                listing_id = row[0]
                print(listing_id)
    except psycopg2.Error as e:
        print(f"Error fetching property ID: {e}")
    finally:
        if conn:
            conn.close()
    return listing_id

if __name__ == "__main__":
    get_first_property_id()
