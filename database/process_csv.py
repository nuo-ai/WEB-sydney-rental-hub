import pandas as pd
import psycopg2
from psycopg2.extras import execute_values
from sqlalchemy import create_engine # Using sqlalchemy for easier connection string parsing if needed later
import os
import glob
import logging
from datetime import datetime

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

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load environment variables from .env file if it exists
dotenv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path, override=True)
    logging.info(f"Successfully loaded .env file from: {dotenv_path} (with override)")
else:
    load_dotenv(override=True)
    logging.warning(
        f".env file not found at {dotenv_path}. Attempting default load_dotenv() search (with override). "
        "Ensure your .env file is correctly placed in the project root for reliable loading."
    )

def find_latest_csv_file():
    """Finds the most recent CSV file in the output directory."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(script_dir, '..', 'crawler', 'dist', 'output')
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
    database_url = os.getenv("DATABASE_URL")
    try:
        if database_url:
            logging.info("Connecting to database using DATABASE_URL...")
            conn = psycopg2.connect(dsn=database_url)
            logging.info("Successfully connected to the database using DATABASE_URL.")
        else:
            # Fallback to individual components if DATABASE_URL is not set
            DB_NAME = os.getenv("DB_NAME", "rental_mcp_db")
            DB_USER = os.getenv("DB_USER", "etl_user")
            DB_PASSWORD = os.getenv("DB_PASSWORD")
            DB_HOST = os.getenv("DB_HOST", "localhost")
            DB_PORT = os.getenv("DB_PORT", "5432")
            if DB_PASSWORD is None:
                raise ValueError("DB_PASSWORD environment variable is not set.")
            conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
            logging.info(f"Successfully connected to the database: {DB_USER}@{DB_HOST}:{DB_PORT}/{DB_NAME}")
        return conn
    except Exception as e:
        logging.error(f"An unexpected error occurred while connecting to the database: {e}")
        raise

def clean_data(df):
    """Cleans and transforms the DataFrame."""
    logging.info("Starting data cleaning and transformation...")
    bool_cols = [
        'has_air_conditioning', 'is_furnished', 'has_balcony', 'has_dishwasher',
        'has_laundry', 'has_built_in_wardrobe', 'has_gym', 'has_pool',
        'has_parking', 'allows_pets', 'has_security_system', 'has_storage',
        'has_study_room', 'has_garden'
    ]
    for col in bool_cols:
        if col in df.columns:
            df[col] = df[col].astype(str).str.upper().map({'TRUE': True, 'FALSE': False, 'YES': True, 'NO': False, '1': True, '0': False}).fillna(False).astype(bool)
        else:
            df[col] = False
    numeric_cols = ['rent_pw', 'bond', 'bedrooms', 'bathrooms', 'parking_spaces']
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
            if col in ['bedrooms', 'bathrooms', 'parking_spaces']:
                 df[col] = df[col].astype('Int64')
            else:
                 df[col] = df[col].astype(int)
        else:
            df[col] = 0
    if 'available_date' in df.columns:
        df['available_date'] = pd.to_datetime(df['available_date'], errors='coerce').dt.date
    else:
        df['available_date'] = None
    if 'latitude' in df.columns and 'longitude' in df.columns:
        df['latitude'] = pd.to_numeric(df['latitude'], errors='coerce')
        df['longitude'] = pd.to_numeric(df['longitude'], errors='coerce')
        df['geom'] = df.apply(
            lambda row: f"SRID=4326;POINT({row['longitude']} {row['latitude']})"
            if pd.notnull(row['longitude']) and pd.notnull(row['latitude']) else None,
            axis=1
        )
    else:
        df['geom'] = None
    json_cols = ['images', 'property_features']
    for col in json_cols:
        if col in df.columns:
            df[col] = df[col].apply(lambda x: x if isinstance(x, str) and x.strip() and x.strip() != '[]' else None)
        else:
            df[col] = None
    
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
    
    final_df_columns = [col for col in db_columns_from_csv if col in df.columns]
    df_processed = df[final_df_columns].copy()

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
    """Loads the DataFrame into the PostgreSQL database using an intelligent UPSERT strategy."""
    if df.empty:
        logging.info("DataFrame is empty. No data to load.")
        return

    table_name = "properties"
    csv_ids = set(df['listing_id'])
    
    with conn.cursor() as cursor:
        try:
            # 1. Get existing properties from DB for comparison
            logging.info("Fetching existing properties from database for comparison...")
            cursor.execute("SELECT listing_id, rent_pw, is_active FROM properties")
            db_properties = {row[0]: {'rent_pw': row[1], 'is_active': row[2]} for row in cursor.fetchall()}
            db_ids = set(db_properties.keys())
            logging.info(f"Found {len(db_ids)} existing properties in the database.")

            # 2. Identify new, updated, and unchanged properties
            new_listings = []
            updated_listings = []
            
            for _, row in df.iterrows():
                listing_id = row['listing_id']
                if listing_id not in db_ids:
                    new_listings.append(row)
                else:
                    # Check for changes (e.g., rent)
                    if row['rent_pw'] != db_properties[listing_id]['rent_pw']:
                        updated_listings.append(row)
            
            logging.info(f"Identified {len(new_listings)} new listings and {len(updated_listings)} updated listings.")

            # 3. Batch INSERT new listings
            if new_listings:
                new_df = pd.DataFrame(new_listings)
                # Add status columns
                new_df['status'] = 'new'
                new_df['status_changed_at'] = datetime.now().isoformat()
                
                # Ensure all columns in the dataframe exist in the database table before creating the query
                cursor.execute(f"SELECT column_name FROM information_schema.columns WHERE table_name = '{table_name}'")
                db_cols = [row[0] for row in cursor.fetchall()]
                
                columns = [col for col in new_df.columns if col in db_cols]
                
                insert_query = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES %s"
                data_tuples = [tuple(x) for x in new_df[columns].replace({pd.NaT: None, pd.NA: None}).to_numpy()]
                
                execute_values(cursor, insert_query, data_tuples, page_size=500)
                logging.info(f"Successfully inserted {len(new_listings)} new properties.")

            # 4. Batch UPDATE updated listings
            if updated_listings:
                update_query = f"UPDATE {table_name} SET rent_pw = %s, status = 'updated', status_changed_at = %s, is_active = TRUE WHERE listing_id = %s"
                update_tuples = [(row['rent_pw'], datetime.now().isoformat(), row['listing_id']) for row in updated_listings]
                
                cursor.executemany(update_query, update_tuples)
                logging.info(f"Successfully updated {len(updated_listings)} properties.")

            # 5. Identify and mark off-market properties
            off_market_ids = db_ids - csv_ids
            active_off_market_ids = [pid for pid in off_market_ids if db_properties[pid]['is_active']]

            if active_off_market_ids:
                off_market_query = "UPDATE properties SET is_active = FALSE, status = 'off-market', status_changed_at = %s WHERE listing_id IN %s"
                cursor.execute(off_market_query, (datetime.now().isoformat(), tuple(active_off_market_ids)))
                logging.info(f"Marked {len(active_off_market_ids)} properties as off-market.")

            # 6. Mark properties that are back on the market
            relisted_ids = [pid for pid in csv_ids if pid in db_ids and not db_properties[pid]['is_active']]
            if relisted_ids:
                relisted_query = "UPDATE properties SET is_active = TRUE, status = 'relisted', status_changed_at = %s WHERE listing_id IN %s"
                cursor.execute(relisted_query, (datetime.now().isoformat(), tuple(relisted_ids)))
                logging.info(f"Marked {len(relisted_ids)} properties as relisted.")

            conn.commit()
            logging.info("Database update process completed and transaction committed.")

            # Print summary for GitHub Actions
            print(f"新增房源: {len(new_listings)}")
            print(f"更新房源: {len(updated_listings)}")
            print(f"下架房源: {len(active_off_market_ids)}")
            print(f"重新上架: {len(relisted_ids)}")

        except psycopg2.Error as e:
            logging.error(f"!!! DATABASE ERROR !!!: {e}")
            logging.error("Rolling back transaction...")
            conn.rollback()
            logging.error("Transaction has been rolled back.")
            raise

def main():
    """Main ETL process function."""
    logging.info("Starting ETL process...")
    conn = None
    try:
        csv_file_path = find_latest_csv_file()
        logging.info(f"Reading CSV file from: {csv_file_path}")
        try:
            df = pd.read_csv(csv_file_path, keep_default_na=True, na_values=['', '#N/A', '#N/A N/A', '#NA', '-1.#IND', '-1.#QNAN', '-NaN', '-nan', '1.#IND', '1.#QNAN', '<NA>', 'N/A', 'NULL', 'NaN', 'n/a', 'nan', 'null', 'NA'])
        except UnicodeDecodeError:
            logging.warning("UTF-8 decoding failed, trying with 'latin1'")
            df = pd.read_csv(csv_file_path, keep_default_na=True, na_values=['', '#N/A', '#N/A N/A', '#NA', '-1.#IND', '-1.#QNAN', '-NaN', '-nan', '1.#IND', '1.#QNAN', '<NA>', 'N/A', 'NULL', 'NaN', 'n/a', 'nan', 'null', 'NA'], encoding='latin1')
        
        logging.info(f"Successfully read {len(df)} rows from CSV.")
        df.dropna(axis=1, how='all', inplace=True)
        logging.info(f"Columns after dropping empty ones: {df.columns.tolist()}")

        df_cleaned = clean_data(df.copy())
        conn = get_db_connection()
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
