import os
import psycopg2
from psycopg2.pool import SimpleConnectionPool
from dotenv import load_dotenv
import logging
from contextlib import contextmanager

# Load environment variables
dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path, override=True)
    logging.info(f".env file loaded from {dotenv_path} for db pool (with override).")
else:
    load_dotenv(override=True)
    logging.warning(f".env file not found at {dotenv_path}. Attempting default load_dotenv() search.")

# Configure logging
logger = logging.getLogger(__name__)

# Global connection pool variable
db_pool = None

def init_db_pool():
    """Initializes the PostgreSQL connection pool."""
    global db_pool
    if db_pool is not None:
        logger.warning("Database pool already initialized.")
        return

    try:
        database_url = os.getenv("DATABASE_URL")
        
        if database_url:
            logger.info("Initializing database connection pool using DATABASE_URL...")
            db_pool = SimpleConnectionPool(minconn=1, maxconn=10, dsn=database_url)
        else:
            logger.warning("DATABASE_URL not found, falling back to individual DB_* variables.")
            db_name = os.getenv("DB_NAME")
            db_user = os.getenv("DB_USER")
            db_password = os.getenv("DB_PASSWORD")
            db_host = os.getenv("DB_HOST")
            db_port = os.getenv("DB_PORT")

            if not all([db_name, db_user, db_password, db_host, db_port]):
                logger.critical("Individual database environment variables (DB_NAME, DB_USER, etc.) are not set.")
                raise ValueError("Missing database configuration in environment variables.")

            logger.info(f"Initializing database connection pool for {db_user}@{db_host}:{db_port}/{db_name}...")
            db_pool = SimpleConnectionPool(
                minconn=1,
                maxconn=10,
                dbname=db_name,
                user=db_user,
                password=db_password,
                host=db_host,
                port=db_port
            )

        # Test the connection pool
        conn = db_pool.getconn()
        db_pool.putconn(conn)
        logger.info("Database connection pool initialized and tested successfully.")

    except psycopg2.OperationalError as e:
        logger.error(f"Failed to initialize database pool due to operational error: {e}", exc_info=True)
        db_pool = None
        raise
    except Exception as e:
        logger.error(f"An unexpected error occurred during database pool initialization: {e}", exc_info=True)
        db_pool = None
        raise

def close_db_pool():
    """Closes all connections in the pool."""
    global db_pool
    if db_pool:
        logger.info("Closing database connection pool.")
        db_pool.closeall()
        db_pool = None
    else:
        logger.warning("Attempted to close a non-existent database pool.")

@contextmanager
def get_db_connection():
    """
    Context manager to get a connection from the pool.
    Ensures the connection is returned to the pool.
    """
    if db_pool is None:
        logger.error("Database pool is not initialized. Cannot get connection.")
        raise ConnectionError("Database pool not initialized.")
    
    conn = None
    try:
        conn = db_pool.getconn()
        yield conn
    except Exception as e:
        logger.error(f"Error with database connection: {e}", exc_info=True)
        if conn:
            conn.rollback()
        raise
    finally:
        if conn:
            db_pool.putconn(conn)

def get_db_conn_dependency():
    """
    FastAPI dependency to get a database connection.
    This function will be used by FastAPI's `Depends()` system.
    """
    with get_db_connection() as conn:
        yield conn
