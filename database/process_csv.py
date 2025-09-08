import pandas as pd
import psycopg2
from psycopg2.extras import execute_values
from sqlalchemy import create_engine # 使用sqlalchemy便于后续解析连接字符串
import os
import glob
import logging
from datetime import datetime
import json # 用于处理配置和输出结构化数据

# 处理 dotenv 导入 - 添加错误处理来解决 Pylance 警告
try:
    from dotenv import load_dotenv
    DOTENV_AVAILABLE = True
except ImportError:
    logging.warning("python-dotenv not available. Environment variables will be loaded from system environment only.")
    DOTENV_AVAILABLE = False
    # 提供一个返回 False 的备用函数，以匹配原始函数的类型签名
    def load_dotenv(*args, **kwargs) -> bool:
        return False

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
    """查找爬虫输出目录中最新的CSV文件。
    
    我们使用文件创建时间而非文件名中的日期，因为爬虫可能在同一天多次运行，
    而我们总是需要处理最新的数据集以确保数据库反映最新市场状态。
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # 指向爬虫的实际输出目录
    output_dir = os.path.join(script_dir, '..', 'crawler', 'output')
    
    # 使用通配符匹配所有CSV文件，避免依赖特定命名格式
    # 这样即使爬虫输出文件命名规则变化，此脚本仍能正常工作
    search_pattern = os.path.join(output_dir, '*.csv')
    logging.info(f"Searching for CSV files in: {search_pattern}")
    list_of_files = glob.glob(search_pattern)
    if not list_of_files:
        logging.error(f"No CSV files found in {output_dir}")
        raise FileNotFoundError(f"No CSV files matching pattern found in {output_dir}")
    latest_file = max(list_of_files, key=os.path.getctime)
    logging.info(f"Found latest CSV file: {latest_file}")
    return latest_file

def get_db_connection():
    """建立与PostgreSQL数据库的连接。
    
    采用双重连接策略：优先使用DATABASE_URL环境变量（适用于云部署环境），
    如不存在则回退到分离参数模式（适用于本地开发环境）。
    这种设计使脚本能同时适应开发和生产环境，无需代码修改。
    """
    database_url = os.getenv("DATABASE_URL")
    try:
        if database_url:
            # 云环境通常提供完整的DATABASE_URL
            logging.info("Connecting to database using DATABASE_URL...")
            conn = psycopg2.connect(dsn=database_url)
            logging.info("Successfully connected to the database using DATABASE_URL.")
        else:
            # 本地开发环境通常使用分离的参数
            DB_NAME = os.getenv("DB_NAME", "rental_mcp_db")
            DB_USER = os.getenv("DB_USER", "etl_user") # ETL专用账户，权限受限
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
    """清洗和转换数据框。
    
    数据清洗策略基于悉尼租房市场的特殊性，确保数据质量和一致性。
    listing_id是整个系统的核心标识符，必须保证其完整性和唯一性。
    """
    logging.info("Starting data cleaning and transformation...")
    logging.info(f"Initial DataFrame shape: {df.shape}")

    # --- 关键步骤：首先验证和清洗listing_id ---
    # listing_id是系统中追踪房源的唯一标识，必须存在且有效
    if 'listing_id' not in df.columns:
        raise ValueError("CSV file must contain a 'listing_id' column.")
    
    initial_rows = len(df)
    # 强制转换为数值型，将非数字ID转为NaN
    # 这是因为某些爬虫可能错误地抓取了非标准ID格式
    df['listing_id'] = pd.to_numeric(df['listing_id'], errors='coerce')
    # 删除listing_id为NaN的行，因为没有有效ID的房源无法在系统中追踪
    df.dropna(subset=['listing_id'], inplace=True)
    
    # 将有效的listing_id转换为整数
    # 使用Int64而非int是为了兼容可能的大数值ID
    df['listing_id'] = df['listing_id'].astype('Int64')
    
    cleaned_rows = len(df)
    if initial_rows > cleaned_rows:
        logging.warning(f"Removed {initial_rows - cleaned_rows} rows with invalid or missing listing_id.")
    logging.info(f"DataFrame shape after listing_id cleaning: {df.shape}")
    # --- 关键验证结束 ---

    # 处理列名不匹配问题
    # 由于爬虫版本迭代，某些特性名称发生了变化，需要统一映射到当前数据库模式
    df.rename(columns={
        'has_wardrobes': 'has_built_in_wardrobe',  # 澳洲房产术语标准化
        'has_study': 'has_study_room'              # 完整描述更符合用户搜索习惯
    }, inplace=True)

    # 处理特性列，现在使用varchar('yes', 'no', 'unknown')而非布尔值
    # 这种三态设计比布尔值更适合悉尼租房市场，因为很多特性在房源描述中可能未明确提及
    feature_cols = [
        'has_air_conditioning', 'is_furnished', 'has_balcony', 'has_dishwasher',
        'has_laundry', 'has_built_in_wardrobe', 'has_gym', 'has_pool',
        'has_parking', 'allows_pets', 'has_security_system', 'has_storage',
        'has_study_room', 'has_garden', 'has_gas_cooking', 'has_heating',
        'has_intercom', 'has_lift', 'has_garbage_disposal', 'has_city_view',
        'has_water_view'
    ]
    for col in feature_cols:
        if col in df.columns:
            # 转换为小写并映射值，同时支持新旧格式
            # 这种设计确保了系统能处理不同来源和不同时期的数据格式
            df[col] = df[col].astype(str).str.lower().map({
                'yes': 'yes', 
                'no': 'no', 
                'unknown': 'unknown',
                'true': 'yes',   # 兼容旧格式
                'false': 'no',   # 兼容旧格式
                '1': 'yes',      # 兼容旧格式
                '0': 'no',       # 兼容旧格式
                'nan': 'unknown',
                'none': 'unknown'
            }).fillna('unknown')  # 默认未知，避免空值影响筛选功能
        else:
            # 如果列不存在，填充为'unknown'而非null
            # 这样可以避免SQL查询中的null比较问题
            df[col] = 'unknown'
    # 处理数值列，确保类型一致性和数据有效性
    numeric_cols = ['rent_pw', 'bond', 'bedrooms', 'bathrooms', 'parking_spaces']
    for col in numeric_cols:
        if col in df.columns:
            # 强制转换为数值，无效值转为NaN后填充为0
            # 这样处理是因为悉尼租房市场数据来源多样，格式不统一
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
            if col in ['bedrooms', 'bathrooms', 'parking_spaces']:
                 # 使用Int64类型以支持可能的大数值和保持整数特性
                 df[col] = df[col].astype('Int64')
            else:
                 # 租金和押金必须为整数，符合澳洲租房市场习惯
                 # 澳洲租金通常以整周计算，不存在小数
                 df[col] = df[col].astype(int)
        else:
            # 缺失列默认为0，保证数据库一致性
            df[col] = 0
    
    # 处理可用日期，转换为标准日期格式
    if 'available_date' in df.columns:
        # 使用pandas日期解析，处理多种可能的日期格式
        # 悉尼房源的日期格式多样，需要灵活处理
        df['available_date'] = pd.to_datetime(df['available_date'], errors='coerce').dt.date
    else:
        # 如果没有可用日期，设为None而非当前日期
        # 这样可以区分"未知"和"立即可用"的情况
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
    
    if 'agent_phone' in df.columns:
        # Ensure agent_phone is treated as a string, remove trailing .0 if it was inferred as float
        df['agent_phone'] = df['agent_phone'].astype(str).str.replace(r'\.0$', '', regex=True)
        
        # 修复电话号码前导零丢失问题
        # 为9位纯数字的电话号码添加前导零
        df['agent_phone'] = df['agent_phone'].apply(
            lambda x: '0' + x if x.isdigit() and len(x) == 9 and not x.startswith('0') else x
        )
    
    # 规范化邮编：统一为4位字符串，去除小数点等异常，例如 "2010.0" -> "2010"
    if 'postcode' in df.columns:
        # 转为字符串后提取首个4位数字；无匹配置为空字符串，避免出现 "nan"/"None"
        df['postcode'] = df['postcode'].astype(str).str.extract(r'(\d{4})')[0].fillna('').str.strip()
    else:
        df['postcode'] = ''
    
    db_columns_from_csv = [
        'listing_id', 'property_url', 'address', 'suburb', 'state', 'postcode',
        'property_type', 'rent_pw', 'bond', 'bedrooms', 'bathrooms', 'parking_spaces',
        'available_date', 'inspection_times', 'agency_name', 'agent_name', 'agent_phone',
        'agent_email', 'property_headline', 'property_description', 'latitude', 'longitude',
        'images', 'property_features', 'agent_profile_url', 'agent_logo_url',
        'enquiry_form_action', 'geom', 'cover_image', 'furnishing_status',
        'air_conditioning_type',
        # Feature flags (now varchar instead of boolean)
        'is_furnished', 'has_air_conditioning', 'has_built_in_wardrobe', 'has_laundry',
        'has_dishwasher', 'has_parking', 'has_gas_cooking', 'has_heating', 'has_intercom',
        'has_lift', 'has_gym', 'has_pool', 'has_garbage_disposal', 'has_study_room',
        'has_balcony', 'has_city_view', 'has_water_view', 'allows_pets',
        # Other DB columns that might be in the CSV
        'has_security_system', 'has_storage', 'has_garden',
        # New fields from the updated CSV format
        'bedroom_display'
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
        return {
            "new": 0, "updated": 0, "unchanged": 0, 
            "off_market": 0, "relisted": 0
        }

    table_name = "properties"
    csv_ids = set(int(x) for x in df['listing_id'])
    
    with conn.cursor() as cursor:
        try:
            # 1. Get existing properties from DB for comparison
            logging.info("Fetching existing properties from database for comparison...")
            cursor.execute("SELECT listing_id, rent_pw, is_active, available_date, inspection_times, postcode, property_headline FROM properties")
            db_properties = {
                row[0]: {
                    'rent_pw': row[1],
                    'is_active': row[2],
                    'available_date': row[3],
                    'inspection_times': row[4],
                    'postcode': (str(row[5]) if row[5] is not None else ''),
                    'property_headline': row[6],
                } for row in cursor.fetchall()
            }
            db_ids = set(db_properties.keys())
            logging.info(f"Found {len(db_ids)} existing properties in the database.")

            # 2. Identify new, updated, and unchanged properties
            new_listings = []
            updated_listings = []
            unchanged_listings_count = 0
            
            for _, row in df.iterrows():
                listing_id = row['listing_id']
                if listing_id not in db_ids:
                    new_listings.append(row)
                else:
                    existing = db_properties[listing_id]
                    new_postcode = str(row.get('postcode') or '').strip()
                    # 中文注释：将关键字段纳入对比，确保看房时间/空出日期/邮编变化也会触发更新
                    changed = (
                        row['rent_pw'] != existing['rent_pw'] or
                        (row.get('available_date') or None) != existing['available_date'] or
                        (row.get('inspection_times') or None) != existing['inspection_times'] or
                        new_postcode != existing['postcode'] or
                        (row.get('property_headline') or None) != existing['property_headline']
                    )
                    if changed:
                        updated_listings.append(row)
                    else:
                        unchanged_listings_count += 1
            
            logging.info(f"Identified {len(new_listings)} new, {len(updated_listings)} updated, and {unchanged_listings_count} unchanged listings.")

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
                update_query = f"""
                UPDATE {table_name} SET
                    rent_pw = %s,
                    available_date = %s,
                    inspection_times = %s,
                    postcode = %s,
                    property_headline = %s,
                    status = 'updated',
                    status_changed_at = %s,
                    is_active = TRUE
                WHERE listing_id = %s
                """
                update_tuples = []
                for row in updated_listings:
                    avail = row.get('available_date')
                    # 中文注释：兼容 NaT/NaN/字符串 'NaT'，统一写入 NULL
                    if pd.isna(avail) or str(avail) == 'NaT':
                        avail = None
                    update_tuples.append((
                        row.get('rent_pw'),
                        avail,
                        row.get('inspection_times'),
                        str(row.get('postcode') or '').strip(),
                        row.get('property_headline'),
                        datetime.now().isoformat(),
                        row['listing_id'],
                    ))
                
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
            relisted_ids = [int(pid) for pid in csv_ids if pid in db_ids and not db_properties[pid]['is_active']]
            if relisted_ids:
                relisted_query = "UPDATE properties SET is_active = TRUE, status = 'relisted', status_changed_at = %s WHERE listing_id IN %s"
                cursor.execute(relisted_query, (datetime.now().isoformat(), tuple(relisted_ids)))
                logging.info(f"Marked {len(relisted_ids)} properties as relisted.")

            conn.commit()
            logging.info("Database update process completed and transaction committed.")

            # Return a dictionary with the summary statistics
            summary_stats = {
                "new": len(new_listings),
                "updated": len(updated_listings),
                "unchanged": unchanged_listings_count,
                "off_market": len(active_off_market_ids),
                "relisted": len(relisted_ids)
            }
            return summary_stats

        except psycopg2.Error as e:
            logging.error(f"!!! DATABASE ERROR !!!: {e}")
            logging.error("Rolling back transaction...")
            conn.rollback()
            logging.error("Transaction has been rolled back.")
            raise
        return {} # Return empty dict on failure before summary

def main():
    """Main ETL process function."""
    logging.info("Starting ETL process...")
    conn = None
    summary_stats = {}
    try:
        csv_file_path = find_latest_csv_file()
        logging.info(f"Reading CSV file from: {csv_file_path}")
        try:
            # 显式将 postcode 读取为字符串，避免自动转换为浮点数
            df = pd.read_csv(csv_file_path, keep_default_na=True, na_values=['', '#N/A', '#N/A N/A', '#NA', '-1.#IND', '-1.#QNAN', '-NaN', '-nan', '1.#IND', '1.#QNAN', '<NA>', 'N/A', 'NULL', 'NaN', 'n/a', 'nan', 'null', 'NA'], dtype={'postcode': str})
        except UnicodeDecodeError:
            logging.warning("UTF-8 decoding failed, trying with 'latin1'")
            # 同样在此处应用 dtype
            df = pd.read_csv(csv_file_path, keep_default_na=True, na_values=['', '#N/A', '#N/A N/A', '#NA', '-1.#IND', '-1.#QNAN', '-NaN', '-nan', '1.#IND', '1.#QNAN', '<NA>', 'N/A', 'NULL', 'NaN', 'n/a', 'nan', 'null', 'NA'], encoding='latin1', dtype={'postcode': str})
        
        logging.info(f"Successfully read {len(df)} rows from CSV.")
        df.dropna(axis=1, how='all', inplace=True)
        logging.info(f"Columns after dropping empty ones: {df.columns.tolist()}")

        df_cleaned = clean_data(df.copy())
        conn = get_db_connection()
        summary_stats = load_data_to_db(df_cleaned, conn)
        
        logging.info("ETL process completed successfully.")

    except Exception as e:
        logging.error(f"An error occurred during the ETL process: {e}", exc_info=True)
    finally:
        if conn:
            conn.close()
            logging.info("Database connection closed.")
    
    return summary_stats

if __name__ == "__main__":
    summary = main()
    # Print summary as a JSON string, wrapped in markers, only when run as a script
    print("\n---ETL_SUMMARY_START---")
    print(json.dumps(summary))
    print("---ETL_SUMMARY_END---")
