import psycopg2
import os
from dotenv import load_dotenv
import logging
from typing import Any

# Load environment variables from .env file
load_dotenv()

# Global connection pool placeholder
_db_pool = None

def get_db_connection():
    """Establishes a connection to the PostgreSQL database."""
    try:
        # Try DATABASE_URL first (for cloud databases like Supabase)
        database_url = os.getenv("DATABASE_URL")
        if database_url:
            logging.info("Using DATABASE_URL for connection")
            conn = psycopg2.connect(database_url)
        else:
            # Fallback to individual environment variables
            logging.info("Using individual DB environment variables")
            conn = psycopg2.connect(
                dbname=os.getenv("DB_NAME"),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD"),
                host=os.getenv("DB_HOST"),
                port=os.getenv("DB_PORT")
            )
        logging.info("Database connection successful.")
        return conn
    except psycopg2.Error as e:
        logging.error(f"Error connecting to the database: {e}")
        raise

async def init_db_pool():
    """Initialize database connection pool (placeholder for future implementation)."""
    global _db_pool
    logging.info("Database pool initialized (placeholder)")
    _db_pool = True

async def close_db_pool():
    """Close database connection pool (placeholder for future implementation)."""
    global _db_pool
    logging.info("Database pool closed (placeholder)")
    _db_pool = None

def get_db_conn_dependency() -> Any:
    """FastAPI dependency to get database connection."""
    return get_db_connection()
