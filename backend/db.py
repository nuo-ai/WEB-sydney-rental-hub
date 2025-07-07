# server/db.py
import os
import psycopg2
from psycopg2 import pool
from dotenv import load_dotenv
import logging
from typing import Optional, Any
from contextlib import contextmanager
from fastapi import HTTPException

# Configure logging for this module
logger = logging.getLogger(__name__)

# Global variable for the connection pool
db_pool: Optional[psycopg2.pool.SimpleConnectionPool] = None

def init_db_pool():
    """Initializes the database connection pool."""
    global db_pool
    if db_pool:
        logger.info("Database pool already initialized.")
        return

    # Load .env file from project root (two levels up from 'backend')
    dotenv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '.env')
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path, override=True) # Added override=True
        logger.info(f".env file loaded from {dotenv_path} for db pool (with override).")
    else:
        # Fallback for cases where .env might be in current working directory (e.g. running tests from root)
        load_dotenv(override=True) # Added override=True
        logger.warning(
            f".env file not found at {dotenv_path} for db pool. "
            "Attempting default load_dotenv() (searches current dir or parent dirs) (with override). "
            "Ensure your .env file is correctly placed in the project root."
        )

    db_name = os.getenv("DB_NAME")
    db_user = os.getenv("DB_USER")
    db_password = os.getenv("DB_PASSWORD")
    db_host = os.getenv("DB_HOST")
    db_port = os.getenv("DB_PORT")

    if not db_password:
        logger.critical("CRITICAL: DB_PASSWORD environment variable not set. Cannot initialize database pool.")
        # raise ValueError("DB_PASSWORD environment variable is not set.") # Or let it fail below
        return # Prevent pool initialization

    if not all([db_name, db_user, db_host, db_port]):
        logger.critical(
            "One or more database connection environment variables (DB_NAME, DB_USER, DB_HOST, DB_PORT) "
            "are not set. Cannot initialize pool."
        )
        return # Prevent pool initialization

    try:
        logger.info(f"Initializing database connection pool for {db_user}@{db_host}:{db_port}/{db_name}...")
        db_pool = psycopg2.pool.SimpleConnectionPool(
            minconn=1,
            maxconn=10, # Adjust maxconn based on expected load
            dbname=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port
        )
        # Test connection by getting and putting one
        conn_test = db_pool.getconn()
        db_pool.putconn(conn_test)
        logger.info("Database connection pool initialized and tested successfully.")
            
    except psycopg2.Error as e:
        logger.critical(f"Error initializing database connection pool: {e}", exc_info=True)
        db_pool = None
    except Exception as e:
        logger.critical(f"An unexpected error occurred during database pool initialization: {e}", exc_info=True)
        db_pool = None


def close_db_pool():
    """Closes all connections in the pool."""
    global db_pool
    if db_pool:
        logger.info("Closing database connection pool...")
        try:
            db_pool.closeall()
            logger.info("Database connection pool closed successfully.")
        except Exception as e:
            logger.error(f"Error closing database connection pool: {e}", exc_info=True)
        finally:
            db_pool = None
    else:
        logger.info("Database pool was not initialized or already closed.")

# Changed from generator to regular function for FastAPI dependency
def get_db_conn_dependency():
    """
    Provides a database connection from the pool as a FastAPI dependency.
    
    Instead of using a generator with yield (which FastAPI wraps in a context manager),
    we create a regular function that returns a connection wrapper object.
    """
    global db_pool
    if not db_pool:
        logger.error("Database pool is not initialized. Cannot provide a DB connection dependency.")
        raise HTTPException(status_code=503, detail="Database service unavailable: Pool not initialized for dependency.")
    
    conn = None
    try:
        conn = db_pool.getconn()
        if conn:
            # Return the connection directly (no yield)
            return conn
        else:
            logger.error("Failed to get connection from pool for dependency (getconn returned None).")
            raise HTTPException(status_code=503, detail="Database service unavailable: Failed to get connection for dependency.")
    except psycopg2.Error as e:
        logger.error(f"Error getting connection from pool for dependency: {e}", exc_info=True)
        if conn:
            try:
                db_pool.putconn(conn, close=True)
                logger.info("Released and closed potentially bad connection after error during getconn phase for dependency.")
            except Exception as put_err:
                logger.error(f"Error trying to putconn/close a bad connection for dependency: {put_err}")
        raise HTTPException(status_code=503, detail=f"Database error for dependency: {e}")
    except Exception as e:
        logger.error(f"Unexpected error in get_db_conn_dependency: {e}", exc_info=True)
        if conn:
            try:
                db_pool.putconn(conn, close=True)
            except:
                pass
        raise HTTPException(status_code=500, detail=f"Internal server error in DB dependency: {e}")
