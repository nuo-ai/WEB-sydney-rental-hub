import os
import psycopg2
import logging
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_db_connection():
    """Establishes a connection to the PostgreSQL database."""
    # Load environment variables from .env file in the project root
    dotenv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '.env')
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path, override=True)
        logging.info(f"Loaded .env file from: {dotenv_path}")
    else:
        logging.warning(f".env file not found at {dotenv_path}. Relying on system environment variables.")

    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise ValueError("DATABASE_URL environment variable is not set or .env file is missing.")
        
    try:
        logging.info("Connecting to database using DATABASE_URL...")
        conn = psycopg2.connect(dsn=database_url)
        logging.info("Successfully connected to the database.")
        return conn
    except Exception as e:
        logging.error(f"An unexpected error occurred while connecting to the database: {e}")
        raise

def apply_sql_file(conn, file_path):
    """Reads and executes an SQL file within a transaction."""
    logging.info(f"Attempting to apply migration from: {file_path}")
    with conn.cursor() as cursor:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                sql_script = f.read()
            
            if not sql_script.strip():
                logging.warning(f"SQL file is empty: {file_path}")
                return

            cursor.execute(sql_script)
            conn.commit()
            logging.info(f"Successfully applied SQL script: {os.path.basename(file_path)}")
        except psycopg2.Error as e:
            logging.error(f"!!! DATABASE ERROR while applying {file_path} !!!: {e}")
            logging.error("Rolling back transaction...")
            conn.rollback()
            logging.error("Transaction has been rolled back.")
            raise
        except FileNotFoundError:
            logging.error(f"Migration file not found: {file_path}")
            raise

def main():
    """Main function to apply a specific SQL migration."""
    import argparse
    parser = argparse.ArgumentParser(description="Apply a specific SQL migration file to the database.")
    parser.add_argument(
        '--file', 
        type=str, 
        required=True,
        help='The name of the SQL file to apply from the "database" directory.'
    )
    args = parser.parse_args()

    conn = None
    try:
        # Define the path to the migration script
        script_dir = os.path.dirname(os.path.abspath(__file__))
        migration_file = os.path.join(script_dir, args.file)
        
        if not os.path.exists(migration_file):
            raise FileNotFoundError(f"Specified migration file not found: {migration_file}")

        conn = get_db_connection()
        apply_sql_file(conn, migration_file)
        
    except Exception as e:
        logging.error(f"An error occurred during the migration process: {e}", exc_info=True)
    finally:
        if conn:
            conn.close()
            logging.info("Database connection closed.")

if __name__ == "__main__":
    main()
