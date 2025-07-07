import pandas as pd
import psycopg2
from psycopg2.extras import execute_values
from sqlalchemy import create_engine # Using sqlalchemy for easier connection string parsing if needed later
import os
import glob
import logging

# 处理 dotenv 导入 - 添加错误处理来解决 Pylance 警告
try:
    from dotenv import load_dotenv
    DOTENV_AVAILABLE = True
except ImportError:
    logging.warning("python-dotenv not available. Environment variables will be loaded from system environment only.")
    DOTENV_AVAILABLE = False
    # 提供一个空的 load_dotenv 函数作为备选
    def load_dotenv(*args, **kwargs):
        pass
# from shapely.geometry import Point # Not strictly needed for direct EWKT string construction
# from geoalchemy2.shape import from_shape # Not strictly needed for direct EWKT string construction

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load environment variables from .env file if it exists
# Ensure .env is in the project root, one level up from 'etl' directory
dotenv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path, override=True) # Added override=True
    logging.info(f"Successfully loaded .env file from: {dotenv_path} (with override)")
else:
    # Fallback for cases where script might be run from a different context or .env is elsewhere in search path
    load_dotenv(override=True) # Added override=True
    logging.warning(
        f".env file not found at {dotenv_path}. Attempting default load_dotenv() search (with override). "
        "Ensure your .env file is correctly placed in the project root for reliable loading."
    )

# Database connection parameters from environment variables
DB_NAME = os.getenv("DB_NAME", "rental_mcp_db")
DB_USER = os.getenv("DB_USER", "etl_user")
DB_PASSWORD = os.getenv("DB_PASSWORD") # CRITICAL: No default for password
print(f"✅ DB_PASSWORD in .env: {repr(DB_PASSWORD)}")

# Initial check for DB_PASSWORD after attempting to load .env
if DB_PASSWORD is None:
    logging.critical("CRITICAL: DB_PASSWORD environment variable is not set or not loaded from .env file.")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")

# Initial check for DB_PASSWORD after attempting to load .env
# This provides an early warning if the crucial password is not set.
if DB_PASSWORD is None: # Check for None explicitly, as an empty string might be a (bad) password
    logging.critical("CRITICAL: DB_PASSWORD environment variable is not set or not loaded from .env file. ETL process cannot proceed without it.")
    # Depending on desired strictness, could raise ValueError here to halt script immediately.
    # raise ValueError("DB_PASSWORD not set. Halting script.")

def find_latest_csv_file():
    """Finds the most recent CSV file in the output directory."""
    # Construct the search path relative to this script's location
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(script_dir, '..', 'dist', 'output')
    search_pattern = os.path.join(output_dir, '*_results.csv')
    
    logging.info(f"Searching for CSV files in: {search_pattern}")
    
    list_of_files = glob.glob(search_pattern)
    
    if not list_of_files:
        logging.error(f"No CSV files found in {output_dir}")
        raise FileNotFoundError(f"No CSV files matching pattern found in {output_dir}")
        
    latest_file = max(list_of_files, key=os.path.getctime)
    logging.info(f"Found latest CSV file: {latest_file}")
    return latest_file

def get_db_connection():
    """Establishes a connection to the PostgreSQL database."""
    # Ensure DB_PASSWORD is available before attempting to connect.
    if DB_PASSWORD is None:
        logging.error("DB_PASSWORD is not set. Cannot establish database connection.")
        raise ValueError("DB_PASSWORD environment variable is not set. Please configure it in your .env file.")
    
    # Check if other essential DB parameters are present
    missing_vars = [var_name for var_name, var_val in {
                        "DB_NAME": DB_NAME, "DB_USER": DB_USER, 
                        "DB_HOST": DB_HOST, "DB_PORT": DB_PORT
                    }.items() if var_val is None]
    if missing_vars:
        logging.error(f"Missing essential database configuration: {', '.join(missing_vars)}. Cannot establish database connection.")
        raise ValueError(f"Missing database configuration for: {', '.join(missing_vars)}")

    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        logging.info(f"Successfully connected to the database: {DB_USER}@{DB_HOST}:{DB_PORT}/{DB_NAME}")
        return conn
    except psycopg2.OperationalError as e: # Catch specific operational errors like auth failure, db not found etc.
        logging.error(f"Database operational error: {e}")
        raise
    except Exception as e: # Catch any other psycopg2 or unexpected errors
        logging.error(f"An unexpected error occurred while connecting to the database: {e}")
        raise

def clean_data(df):
    """Cleans and transforms the DataFrame."""
    logging.info("Starting data cleaning and transformation...")

    # Rename columns to match database (snake_case) - if not already
    # df.rename(columns={'Old Name': 'new_name'}, inplace=True)

    # Handle boolean string columns (example, adjust as per your CSV)
    bool_cols = [
        'has_air_conditioning', 'is_furnished', 'has_balcony', 'has_dishwasher',
        'has_laundry', 'has_built_in_wardrobe', 'has_gym', 'has_pool',
        'has_parking', 'allows_pets', 'has_security_system', 'has_storage',
        'has_study_room', 'has_garden'
    ]
    for col in bool_cols:
        if col in df.columns:
            # Convert various string representations of True/False to actual booleans
            df[col] = df[col].astype(str).str.upper().map({'TRUE': True, 'FALSE': False, 'YES': True, 'NO': False, '1': True, '0': False}).fillna(False).astype(bool)
        else:
            logging.warning(f"Boolean column '{col}' not found in CSV. Will be skipped or defaulted in DB.")
            df[col] = False # Default to False if column is missing

    # Convert numeric columns
    numeric_cols = ['rent_pw', 'bond', 'bedrooms', 'bathrooms', 'parking_spaces']
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0) # Coerce errors to NaN, then fill with 0
            if col in ['bedrooms', 'bathrooms', 'parking_spaces']:
                 df[col] = df[col].astype('Int64') # Use Int64 to allow for NA if needed, or int if 0 is acceptable for NA
            else:
                 df[col] = df[col].astype(int)
        else:
            logging.warning(f"Numeric column '{col}' not found in CSV.")
            df[col] = 0


    # Convert date columns
    if 'available_date' in df.columns:
        df['available_date'] = pd.to_datetime(df['available_date'], errors='coerce').dt.date
    else:
        logging.warning("Date column 'available_date' not found in CSV.")
        df['available_date'] = None


    # Handle latitude and longitude, create geom
    if 'latitude' in df.columns and 'longitude' in df.columns:
        df['latitude'] = pd.to_numeric(df['latitude'], errors='coerce')
        df['longitude'] = pd.to_numeric(df['longitude'], errors='coerce')
        # Create EWKT string for PostGIS geom column
        # SRID 4326 is standard for GPS coordinates
        df['geom'] = df.apply(
            lambda row: f"SRID=4326;POINT({row['longitude']} {row['latitude']})"
            if pd.notnull(row['longitude']) and pd.notnull(row['latitude']) else None,
            axis=1
        )
    else:
        logging.warning("Latitude or Longitude columns not found. 'geom' will be null.")
        df['geom'] = None

    # For JSONB columns (images, property_features), ensure they are valid JSON strings or None
    # Pandas read_csv might interpret "[]" as a string, not an empty list for JSON.
    # We'll handle actual JSON conversion/validation during insertion if psycopg2 needs it,
    # or ensure they are None if empty/invalid.
    json_cols = ['images', 'property_features']
    for col in json_cols:
        if col in df.columns:
            # Example: if it's an empty string or "[]", make it None so DB stores NULL
            df[col] = df[col].apply(lambda x: x if isinstance(x, str) and x.strip() and x.strip() != '[]' else None)
        else:
            logging.warning(f"JSON column '{col}' not found in CSV.")
            df[col] = None
            
    # Select and order columns to match the database table structure
    # This is CRITICAL for execute_values to work correctly.
    # Add any missing columns that have defaults in the DB (like is_active, created_at, last_updated)
    # or ensure they are handled appropriately.
    # 'created_at' and 'last_updated' have defaults in DB, 'is_active' also defaults to TRUE.
    # We only need to provide columns that are present in the CSV.
    
    db_columns_from_csv = [
        'listing_id', 'property_url', 'address', 'suburb', 'state', 'postcode',
        'property_type', 'rent_pw', 'bond', 'bedrooms', 'bathrooms', 'parking_spaces',
        'available_date', 'inspection_times', 'agency_name', 'agent_name', 'agent_phone',
        'agent_email', 'property_headline', 'property_description', 'has_air_conditioning',
        'is_furnished', 'has_balcony', 'has_dishwasher', 'has_laundry',
        'has_built_in_wardrobe', 'has_gym', 'has_pool', 'has_parking', 'allows_pets',
        'has_security_system', 'has_storage', 'has_study_room', 'has_garden',
        'latitude', 'longitude', 'images', 'property_features', 'agent_profile_url',
        'agent_logo_url', 'enquiry_form_action', 'geom'
    ]
    
    # Filter df to only include columns that exist in the CSV and are in our target list
    final_df_columns = [col for col in db_columns_from_csv if col in df.columns]
    df_processed = df[final_df_columns].copy()

    # Deduplicate based on listing_id, keeping the first occurrence
    if 'listing_id' in df_processed.columns:
        initial_row_count = len(df_processed)
        df_processed.drop_duplicates(subset=['listing_id'], keep='first', inplace=True)
        deduplicated_row_count = len(df_processed)
        if initial_row_count > deduplicated_row_count:
            logging.info(f"Removed {initial_row_count - deduplicated_row_count} duplicate rows based on listing_id.")
    else:
        logging.warning("listing_id column not found, cannot perform deduplication.")


    logging.info("Data cleaning and transformation finished.")
    return df_processed

def load_data_to_db(df, conn):
    """Loads the DataFrame into the PostgreSQL database."""
    if df.empty:
        logging.info("DataFrame is empty. No data to load.")
        return

    table_name = "properties"
    # Columns in the DataFrame must match the order of columns in the INSERT statement
    # and the table structure if not explicitly listing columns in INSERT.
    columns = df.columns.tolist()
    
    # Ensure 'geom' is properly formatted if it exists
    if 'geom' in columns and not df['geom'].empty:
         # Assuming 'geom' column already contains WKT strings from from_shape
         pass # It should be ready for psycopg2

    # Convert DataFrame to list of tuples for execute_values
    # Handle NaT for dates and NaN for numbers appropriately for psycopg2 (should become NULL)
    data_tuples = [tuple(x) for x in df.replace({pd.NaT: None, float('nan'): None}).to_numpy()]

    insert_query = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES %s"
    # Add last_updated to be set by trigger, or explicitly:
    # insert_query += ", last_updated = CURRENT_TIMESTAMP"


    with conn.cursor() as cursor:
        try:
            logging.info(f"Clearing all existing data from {table_name} table before loading new data...")
            cursor.execute(f"TRUNCATE TABLE {table_name} RESTART IDENTITY CASCADE;") # Added CASCADE for dependent objects if any
            logging.info(f"Table {table_name} truncated.")
            
            logging.info(f"Loading data into {table_name}...")
            execute_values(cursor, insert_query, data_tuples)
            conn.commit()
            logging.info(f"Successfully loaded {len(data_tuples)} rows into {table_name}.")
        except psycopg2.Error as e:
            conn.rollback()
            logging.error(f"Error loading data into database: {e}")
            logging.error(f"Failed query: {cursor.query}") # Log the failed query if possible
            raise

def main():
    """Main ETL process function."""
    logging.info("Starting ETL process...")
    conn = None
    try:
        csv_file_path = find_latest_csv_file()
        logging.info(f"Reading CSV file from: {csv_file_path}")
        # Specify dtype for problematic columns if necessary, e.g., dtype={'postcode': str}
        # Handle potential "मिक्स" encoding issues if they arise by specifying encoding
        try:
            df = pd.read_csv(csv_file_path, keep_default_na=True, na_values=['', '#N/A', '#N/A N/A', '#NA', '-1.#IND', '-1.#QNAN', '-NaN', '-nan', '1.#IND', '1.#QNAN', '<NA>', 'N/A', 'NULL', 'NaN', 'n/a', 'nan', 'null', 'NA'])
        except UnicodeDecodeError:
            logging.warning("UTF-8 decoding failed, trying with 'latin1'")
            df = pd.read_csv(csv_file_path, keep_default_na=True, na_values=['', '#N/A', '#N/A N/A', '#NA', '-1.#IND', '-1.#QNAN', '-NaN', '-nan', '1.#IND', '1.#QNAN', '<NA>', 'N/A', 'NULL', 'NaN', 'n/a', 'nan', 'null', 'NA'], encoding='latin1')
        except Exception as e:
            logging.error(f"Error reading CSV file: {e}")
            return

        logging.info(f"Successfully read {len(df)} rows from CSV.")
        
        # Drop fully empty columns that might have been read as 'Column 1', 'Column 2'
        df.dropna(axis=1, how='all', inplace=True)
        logging.info(f"Columns after dropping empty ones: {df.columns.tolist()}")


        df_cleaned = clean_data(df.copy()) # Use .copy() to avoid SettingWithCopyWarning
        
        conn = get_db_connection()
        
        # For the simplified "clear and insert" strategy, we'll use ON CONFLICT DO UPDATE
        # which effectively replaces rows based on listing_id or inserts new ones.
        # If we wanted a true "clear all then insert", we'd TRUNCATE or DELETE ALL first.
        # The current ON CONFLICT is a good compromise for idempotency.
        load_data_to_db(df_cleaned, conn)
        
        logging.info("ETL process completed successfully.")

    except Exception as e:
        logging.error(f"An error occurred during the ETL process: {e}", exc_info=True)
    finally:
        if conn:
            conn.close()
            logging.info("Database connection closed.")

if __name__ == "__main__":
    main()
