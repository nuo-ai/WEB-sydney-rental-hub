import pandas as pd
import psycopg2
from psycopg2.extras import execute_values, RealDictCursor
import os
import glob
import logging
import requests
from datetime import datetime, timezone
from typing import List, Dict, Set
import json

# 处理 dotenv 导入
try:
    from dotenv import load_dotenv
    DOTENV_AVAILABLE = True
except ImportError:
    logging.warning("python-dotenv not available. Environment variables will be loaded from system environment only.")
    DOTENV_AVAILABLE = False
    def load_dotenv(*args, **kwargs):
        pass

# Configure logging with more detailed format
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables
dotenv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path, override=True)
    logger.info(f"Successfully loaded .env file from: {dotenv_path}")
else:
    load_dotenv(override=True)
    logger.warning(f".env file not found at {dotenv_path}. Using system environment.")

# Database connection parameters
DB_NAME = os.getenv("DB_NAME", "rental_mcp_db")
DB_USER = os.getenv("DB_USER", "etl_user")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")

# Webhook configuration for notifications
WEBHOOK_URL = os.getenv("WEBHOOK_URL")  # Optional webhook for new property notifications

class PropertyDataProcessor:
    """处理房源数据的增量更新逻辑"""
    
    def __init__(self):
        self.connection = None
        self.current_timestamp = datetime.now(timezone.utc)
        
    def get_db_connection(self):
        """建立数据库连接"""
        if DB_PASSWORD is None:
            raise ValueError("DB_PASSWORD environment variable is not set.")
            
        try:
            self.connection = psycopg2.connect(
                dbname=DB_NAME,
                user=DB_USER,
                password=DB_PASSWORD,
                host=DB_HOST,
                port=DB_PORT
            )
            logger.info(f"Successfully connected to database: {DB_USER}@{DB_HOST}:{DB_PORT}/{DB_NAME}")
            return self.connection
        except psycopg2.OperationalError as e:
            logger.error(f"Database connection failed: {e}")
            raise
            
    def find_latest_csv_file(self) -> str:
        """查找最新的CSV文件"""
        script_dir = os.path.dirname(os.path.abspath(__file__))
        output_dir = os.path.join(script_dir, '..', 'dist', 'output')
        search_pattern = os.path.join(output_dir, '*_results.csv')
        
        logger.info(f"Searching for CSV files in: {search_pattern}")
        
        list_of_files = glob.glob(search_pattern)
        if not list_of_files:
            raise FileNotFoundError(f"No CSV files found in {output_dir}")
            
        latest_file = max(list_of_files, key=os.path.getctime)
        logger.info(f"Found latest CSV file: {latest_file}")
        return latest_file
        
    def clean_and_prepare_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """清理和准备数据 - 基于现有的 clean_data 函数优化"""
        logger.info("Starting data cleaning and transformation...")
        
        # 处理布尔值列
        bool_cols = [
            'has_air_conditioning', 'is_furnished', 'has_balcony', 'has_dishwasher',
            'has_laundry', 'has_built_in_wardrobe', 'has_gym', 'has_pool',
            'has_parking', 'allows_pets', 'has_security_system', 'has_storage',
            'has_study_room', 'has_garden'
        ]
        for col in bool_cols:
            if col in df.columns:
                df[col] = df[col].astype(str).str.upper().map({
                    'TRUE': True, 'FALSE': False, 'YES': True, 'NO': False, 
                    '1': True, '0': False
                }).fillna(False).astype(bool)
            else:
                df[col] = False
                
        # 处理数值列
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
                
        # 处理日期列 - 增强NaT处理
        if 'available_date' in df.columns:
            df['available_date'] = pd.to_datetime(df['available_date'], errors='coerce')
            # 关键修复：先处理NaT，再转换为date
            df['available_date'] = df['available_date'].apply(
                lambda x: x.date() if pd.notna(x) else None
            )
        else:
            df['available_date'] = None
            
        # 处理地理位置数据
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
            
        # 生成 bedroom_display 字段
        if 'bedrooms' in df.columns:
            df['bedroom_display'] = df['bedrooms'].apply(
                lambda x: 'Studio' if x == 0 else str(x)
            )
        else:
            df['bedroom_display'] = 'Studio'
            
        # 处理JSON列
        json_cols = ['images', 'property_features']
        for col in json_cols:
            if col in df.columns:
                df[col] = df[col].apply(
                    lambda x: x if isinstance(x, str) and x.strip() and x.strip() != '[]' else None
                )
            else:
                df[col] = None
                
        # 规范化邮编：统一为4位字符串，移除小数/噪声（例如 "2010.0" -> "2010"）
        # 原因：CSV 列混型时 pandas 会将整列推断为 float，导致写回 DB 变成 "2010.0"，
        # 前端只能用 Math.floor 兜底，带来不一致与显示瑕疵。这里在入库前统一清洗。
        if 'postcode' in df.columns:
            df['postcode'] = df['postcode'].astype(str).str.extract(r'(\d{4})')[0].fillna('').str.strip()
        else:
            df['postcode'] = ''
                
        # 去重
        if 'listing_id' in df.columns:
            initial_count = len(df)
            df.drop_duplicates(subset=['listing_id'], keep='first', inplace=True)
            final_count = len(df)
            if initial_count > final_count:
                logger.info(f"Removed {initial_count - final_count} duplicate rows")
                
        logger.info("Data cleaning completed")
        return df
        
    def get_existing_listings(self) -> Set[int]:
        """获取数据库中所有房源的listing_id（不区分活跃状态）
        
        修正：获取所有房源，而不仅仅是活跃房源
        这样可以正确处理房源重新上架的情况
        """
        query = "SELECT listing_id FROM properties"  # 移除 WHERE is_active = TRUE
        
        with self.connection.cursor() as cursor:
            cursor.execute(query)
            existing_ids = {row[0] for row in cursor.fetchall()}
            
        logger.info(f"Found {len(existing_ids)} total listings in database")
        return existing_ids
        
    def identify_data_changes(self, new_df: pd.DataFrame, existing_ids: Set[int]) -> Dict[str, List]:
        """识别数据变化：新增、更新、需要激活、需要下架
        
        核心逻辑：
        - 爬虫爬到的房源 = 活跃（is_active = TRUE）
        - 爬虫没爬到的房源 = 不活跃（is_active = FALSE）
        """
        new_ids = set(new_df['listing_id'].astype(int))
        
        # 新增房源：在新数据中有，但数据库中没有
        new_listings = new_ids - existing_ids
        
        # 更新房源：在新数据和数据库中都有（需要更新内容并设置为活跃）
        update_listings = new_ids & existing_ids
        
        # 需要激活的房源：所有本次爬取到的已存在房源都应该是活跃的
        # （包括之前被标记为inactive但这次又出现的房源）
        activate_listings = update_listings  # 所有更新的房源都要确保是活跃的
        
        # 需要下架的房源：在数据库中有，但新数据中没有
        inactive_listings = existing_ids - new_ids
        
        logger.info(f"Data analysis complete:")
        logger.info(f"  - New listings: {len(new_listings)}")
        logger.info(f"  - Listings to update: {len(update_listings)}")
        logger.info(f"  - Listings to activate: {len(activate_listings)}")
        logger.info(f"  - Listings to mark inactive: {len(inactive_listings)}")
        
        return {
            'new': list(new_listings),
            'update': list(update_listings),
            'activate': list(activate_listings),
            'inactive': list(inactive_listings)
        }
        
    def insert_new_listings(self, new_df: pd.DataFrame, new_listing_ids: List[int]) -> int:
        """插入新房源"""
        if not new_listing_ids:
            logger.info("No new listings to insert")
            return 0
            
        # 筛选新房源数据
        new_records = new_df[new_df['listing_id'].isin(new_listing_ids)].copy()
        
        # 确保所有必需字段都存在
        db_columns = [
            'listing_id', 'property_url', 'address', 'suburb', 'state', 'postcode',
            'property_type', 'rent_pw', 'bond', 'bedrooms', 'bathrooms', 'parking_spaces',
            'available_date', 'inspection_times', 'agency_name', 'agent_name', 'agent_phone',
            'agent_email', 'property_headline', 'property_description', 'has_air_conditioning',
            'is_furnished', 'has_balcony', 'has_dishwasher', 'has_laundry',
            'has_built_in_wardrobe', 'has_gym', 'has_pool', 'has_parking', 'allows_pets',
            'has_security_system', 'has_storage', 'has_study_room', 'has_garden',
            'latitude', 'longitude', 'images', 'property_features', 'agent_profile_url',
            'agent_logo_url', 'enquiry_form_action', 'geom', 'bedroom_display'
        ]
        
        # 只保留存在的列
        final_columns = [col for col in db_columns if col in new_records.columns]
        new_records = new_records[final_columns]
        
        # 转换为插入数据
        new_records['available_date'] = new_records['available_date'].replace({pd.NaT: None})
        data_tuples = [tuple(x) for x in new_records.replace({float('nan'): None}).to_numpy()]
        
        insert_query = f"""
        INSERT INTO properties ({', '.join(final_columns)}, last_seen_at) 
        VALUES %s
        """
        
        # 为每个记录添加当前时间戳
        data_tuples_with_timestamp = [tuple(list(record) + [self.current_timestamp]) for record in data_tuples]
        
        with self.connection.cursor() as cursor:
            try:
                execute_values(cursor, insert_query, data_tuples_with_timestamp)
                self.connection.commit()
                logger.info(f"Successfully inserted {len(data_tuples)} new listings")
                return len(data_tuples)
            except psycopg2.Error as e:
                self.connection.rollback()
                logger.error(f"Error inserting new listings: {e}")
                raise
                
    def update_existing_listings(self, new_df: pd.DataFrame, update_listing_ids: List[int]) -> int:
        """更新现有房源并确保标记为活跃"""
        if not update_listing_ids:
            logger.info("No listings to update")
            return 0
            
        update_records = new_df[new_df['listing_id'].isin(update_listing_ids)]
        updated_count = 0
        
        # 构建更新查询 - 更新所有字段，设置 last_seen_at，并确保 is_active = TRUE
        update_query = """
        UPDATE properties SET
            property_url = %s, address = %s, suburb = %s, state = %s, postcode = %s,
            property_type = %s, rent_pw = %s, bond = %s, bedrooms = %s, bathrooms = %s,
            parking_spaces = %s, available_date = %s, inspection_times = %s, agency_name = %s,
            agent_name = %s, agent_phone = %s, agent_email = %s, property_headline = %s,
            property_description = %s, has_air_conditioning = %s, is_furnished = %s,
            has_balcony = %s, has_dishwasher = %s, has_laundry = %s, has_built_in_wardrobe = %s,
            has_gym = %s, has_pool = %s, has_parking = %s, allows_pets = %s,
            has_security_system = %s, has_storage = %s, has_study_room = %s, has_garden = %s,
            latitude = %s, longitude = %s, images = %s, property_features = %s,
            agent_profile_url = %s, agent_logo_url = %s, enquiry_form_action = %s,
            geom = %s, bedroom_display = %s, last_seen_at = %s, is_active = TRUE
        WHERE listing_id = %s
        """
        
        with self.connection.cursor() as cursor:
            try:
                for _, row in update_records.iterrows():
                    # 准备更新参数 - 增强NaT处理
                    available_date = row.get('available_date')
                    # 增强检查：同时处理NaT、NaN和字符串形式的NaT
                    if pd.isna(available_date) or str(available_date) == 'NaT' or available_date is pd.NaT:
                        available_date = None

                    update_params = [
                        row.get('property_url'), row.get('address'), row.get('suburb'), 
                        row.get('state'), row.get('postcode'), row.get('property_type'),
                        row.get('rent_pw'), row.get('bond'), row.get('bedrooms'), 
                        row.get('bathrooms'), row.get('parking_spaces'), available_date,
                        row.get('inspection_times'), row.get('agency_name'), row.get('agent_name'),
                        row.get('agent_phone'), row.get('agent_email'), row.get('property_headline'),
                        row.get('property_description'), row.get('has_air_conditioning'), 
                        row.get('is_furnished'), row.get('has_balcony'), row.get('has_dishwasher'),
                        row.get('has_laundry'), row.get('has_built_in_wardrobe'), row.get('has_gym'),
                        row.get('has_pool'), row.get('has_parking'), row.get('allows_pets'),
                        row.get('has_security_system'), row.get('has_storage'), row.get('has_study_room'),
                        row.get('has_garden'), row.get('latitude'), row.get('longitude'),
                        row.get('images'), row.get('property_features'), row.get('agent_profile_url'),
                        row.get('agent_logo_url'), row.get('enquiry_form_action'), row.get('geom'),
                        row.get('bedroom_display'), self.current_timestamp, int(row['listing_id'])
                    ]
                    
                    cursor.execute(update_query, update_params)
                    updated_count += 1
                    
                self.connection.commit()
                logger.info(f"Successfully updated {updated_count} existing listings")
                return updated_count
            except psycopg2.Error as e:
                self.connection.rollback()
                logger.error(f"Error updating listings: {e}")
                raise
                
    def mark_inactive_listings(self, inactive_listing_ids: List[int]) -> int:
        """标记下架房源为不活跃
        
        关键修复：该方法现在会标记所有不在本次爬取中的房源为inactive
        """
        if not inactive_listing_ids:
            logger.info("No listings to mark as inactive")
            return 0
            
        # 修复：移除 AND is_active = TRUE 条件，确保所有房源都能被标记
        update_query = """
        UPDATE properties 
        SET is_active = FALSE, 
            last_updated = %s,
            status = CASE 
                WHEN status IN ('new', 'updated', 'relisted') THEN 'off-market'
                ELSE status
            END
        WHERE listing_id = ANY(%s)
        """
        
        with self.connection.cursor() as cursor:
            try:
                cursor.execute(update_query, (self.current_timestamp, inactive_listing_ids))
                affected_rows = cursor.rowcount
                self.connection.commit()
                logger.info(f"Successfully marked {affected_rows} listings as inactive (off-market)")
                return affected_rows
            except psycopg2.Error as e:
                self.connection.rollback()
                logger.error(f"Error marking listings as inactive: {e}")
                raise
                
    def send_new_listing_notification(self, new_listing_ids: List[int]):
        """发送新房源通知"""
        if not WEBHOOK_URL or not new_listing_ids:
            return
            
        # 获取新房源的基本信息
        if len(new_listing_ids) == 0:
            return
            
        query = """
        SELECT listing_id, address, suburb, rent_pw, bedrooms, property_type, property_url
        FROM properties 
        WHERE listing_id = ANY(%s)
        """
        
        with self.connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(query, (new_listing_ids,))
            new_listings = cursor.fetchall()
            
        notification_data = {
            'event': 'new_listings',
            'timestamp': self.current_timestamp.isoformat(),
            'count': len(new_listings),
            'listings': [dict(listing) for listing in new_listings]
        }
        
        try:
            response = requests.post(
                WEBHOOK_URL, 
                json=notification_data,
                headers={'Content-Type': 'application/json'},
                timeout=10
            )
            if response.status_code == 200:
                logger.info(f"Successfully sent notification for {len(new_listing_ids)} new listings")
            else:
                logger.warning(f"Notification webhook returned status {response.status_code}")
        except requests.RequestException as e:
            logger.error(f"Failed to send notification: {e}")
            
    def process_data_update(self):
        """主要的数据更新流程"""
        logger.info("Starting property data update process...")
        
        try:
            # 1. 建立数据库连接
            self.get_db_connection()
            
            # 2. 读取最新CSV文件
            csv_file = self.find_latest_csv_file()
            logger.info(f"Processing CSV file: {csv_file}")
            
            try:
                new_df = pd.read_csv(csv_file, keep_default_na=True)
            except UnicodeDecodeError:
                logger.warning("UTF-8 decoding failed, trying with 'latin1'")
                new_df = pd.read_csv(csv_file, keep_default_na=True, encoding='latin1')
                
            logger.info(f"Read {len(new_df)} rows from CSV")
            
            # 3. 清理数据
            new_df = self.clean_and_prepare_data(new_df)
            
            # 4. 获取现有房源
            existing_ids = self.get_existing_listings()
            
            # 5. 识别数据变化
            changes = self.identify_data_changes(new_df, existing_ids)
            
            # 6. 执行数据库更新
            # 注意：更新操作会同时将房源标记为活跃
            new_count = self.insert_new_listings(new_df, changes['new'])
            update_count = self.update_existing_listings(new_df, changes['update'])
            inactive_count = self.mark_inactive_listings(changes['inactive'])
            
            # 7. 发送通知
            if changes['new']:
                self.send_new_listing_notification(changes['new'])
                
            # 8. 记录总结
            logger.info("Data update process completed successfully!")
            logger.info(f"Summary: {new_count} new, {update_count} updated, {inactive_count} marked inactive")
            
            return {
                'success': True,
                'new_listings': new_count,
                'updated_listings': update_count,
                'inactive_listings': inactive_count,
                'timestamp': self.current_timestamp.isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error in data update process: {e}", exc_info=True)
            return {
                'success': False,
                'error': str(e),
                'timestamp': self.current_timestamp.isoformat()
            }
        finally:
            if self.connection:
                self.connection.close()
                logger.info("Database connection closed")

def main():
    """主函数"""
    processor = PropertyDataProcessor()
    result = processor.process_data_update()
    
    if result['success']:
        logger.info("ETL process completed successfully")
        print(json.dumps(result, indent=2))
    else:
        logger.error("ETL process failed")
        print(json.dumps(result, indent=2))
        exit(1)

if __name__ == "__main__":
    main()
