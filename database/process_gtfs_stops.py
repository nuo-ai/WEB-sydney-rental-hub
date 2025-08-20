import pandas as pd
import psycopg2
from psycopg2.extras import execute_values
import os
from dotenv import load_dotenv
import logging
from io import StringIO

# 配置日志记录
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 加载 .env 文件中的环境变量
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env')) # .env 在项目根目录

def get_db_connection():
    """建立并返回数据库连接"""
    try:
        conn = psycopg2.connect(
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT")
        )
        logging.info("数据库连接成功。")
        return conn
    except Exception as e:
        logging.error(f"数据库连接失败: {e}")
        return None

def process_stops_data(conn, stops_file_path, chunk_size=10000, clear_table=True):
    """
    处理 stops.txt 文件并将其数据加载到 transport_stops 表。
    :param conn: 数据库连接对象
    :param stops_file_path: stops.txt 文件的路径
    :param chunk_size: Pandas 读取和处理数据的块大小
    :param clear_table: 是否在插入前清空表
    """
    if not conn:
        return

    cursor = None
    total_rows_processed = 0

    try:
        cursor = conn.cursor()

        if clear_table:
            logging.info("正在清空 transport_stops 表...")
            cursor.execute("TRUNCATE TABLE transport_stops;") # stop_id 是主键，不需要 RESTART IDENTITY
            logging.info("transport_stops 表已清空。")

        logging.info(f"开始从 {stops_file_path} 读取和处理站点数据...")
        
        # GTFS stops.txt 通常包含的列
        # 脚本将尝试匹配这些列名的小写形式
        gtfs_required_cols_lower = ['stop_id', 'stop_name', 'stop_lat', 'stop_lon']
        gtfs_optional_cols_lower = ['location_type', 'parent_station']
        
        # 读取文件第一行以获取实际列名并确定要使用的列
        try:
            header_df = pd.read_csv(stops_file_path, nrows=1, low_memory=False, na_filter=False)
            actual_header_cols_original_case = [col.strip() for col in header_df.columns]
            actual_header_cols_lower = [col.lower() for col in actual_header_cols_original_case]
        except Exception as e:
            logging.error(f"读取文件头失败: {e}. 请确保文件路径正确且文件可读。")
            return

        # 筛选出实际存在于文件中的必需列和可选列 (使用原始大小写，因为 read_csv 的 usecols 需要它)
        use_cols_original_case = []
        # 检查必需列
        for req_col_lower in gtfs_required_cols_lower:
            found = False
            for i, actual_col_lower in enumerate(actual_header_cols_lower):
                if actual_col_lower == req_col_lower:
                    use_cols_original_case.append(actual_header_cols_original_case[i])
                    found = True
                    break
            if not found:
                logging.error(f"stops.txt 文件中缺少必需的列: '{req_col_lower}' (或其任何大小写变体)")
                return
        
        # 添加可选列 (如果存在)
        for opt_col_lower in gtfs_optional_cols_lower:
            for i, actual_col_lower in enumerate(actual_header_cols_lower):
                if actual_col_lower == opt_col_lower:
                    use_cols_original_case.append(actual_header_cols_original_case[i])
                    break
        
        logging.info(f"将从文件中读取以下列: {use_cols_original_case}")

        for chunk_df in pd.read_csv(stops_file_path, chunksize=chunk_size, usecols=use_cols_original_case, low_memory=False, na_filter=False, dtype=str): # 读取所有列为字符串以进行初始处理
            # 将读取到的列名统一转换为小写，以便后续按小写键名访问
            chunk_df.columns = [col.strip().lower() for col in chunk_df.columns]
            
            logging.info(f"处理 {len(chunk_df)} 条站点数据...")
            records_to_insert = []

            for _, row in chunk_df.iterrows():
                try:
                    # 现在所有列名都是小写
                    stop_id = str(row['stop_id'])
                    stop_name = str(row['stop_name'])
                    
                    # 确保经纬度是有效的数值
                    try:
                        latitude = float(row['stop_lat'])
                        longitude = float(row['stop_lon'])
                    except ValueError:
                        logging.warning(f"站点 {stop_id} 的经纬度无效，跳过此站点: lat='{row['stop_lat']}', lon='{row['stop_lon']}'")
                        continue
                    
                    # 处理可选字段 (现在都用小写键名)
                    location_type = row.get('location_type', None)
                    # GTFS location_type 可以是空字符串，数据库中存为 NULL
                    if isinstance(location_type, str) and location_type.strip() == '':
                        location_type = None
                    elif location_type is not None:
                        try:
                            location_type = int(location_type)
                        except ValueError:
                            logging.warning(f"站点 {stop_id} 的 location_type 无效 ('{location_type}')，将设为 NULL。")
                            location_type = None
                            
                    parent_station = row.get('parent_station', None)
                    if isinstance(parent_station, str) and parent_station.strip() == '':
                        parent_station = None
                    
                    # transport_mode 和 serviced_routes_details 暂时不填充 (默认为 NULL)
                    records_to_insert.append((
                        stop_id,
                        stop_name,
                        latitude,
                        longitude,
                        location_type,
                        parent_station
                        # created_at 和 updated_at 会使用默认值
                    ))
                except Exception as e:
                    logging.error(f"处理行数据时出错: {row}, 错误: {e}")
                    continue
            
            if records_to_insert:
                # SQL 插入语句，包含 PostGIS 地理位置生成
                # ON CONFLICT DO NOTHING 避免因重复 stop_id 导致错误
                insert_query = """
                INSERT INTO transport_stops (
                    stop_id, stop_name, latitude, longitude, location, 
                    location_type, parent_station
                ) VALUES %s
                ON CONFLICT (stop_id) DO NOTHING; 
                """ 
                # 或者 ON CONFLICT (stop_id) DO UPDATE SET ... 如果需要更新现有记录

                # 注意：psycopg2 的 execute_values 需要一个包含元组的列表
                # ST_MakePoint 需要 (longitude, latitude) 顺序
                # execute_values 会自动处理 %s 占位符
                
                # 我们需要修改 records_to_insert 来适配 execute_values 的格式，
                # 并在 SQL 中直接使用 ST_MakePoint。
                # execute_values 不直接支持在 VALUES %s 中进行函数调用来生成 geometry。
                # 因此，我们将分批插入，并在插入时构造 geometry。

                # 更稳妥的方式是逐条插入或使用 COPY FROM STDIN，但为了简化，这里用 execute_values
                # 并假设数据量在可接受范围内，或者在外部循环中处理 geometry 生成。
                # 为了正确使用 execute_values 并生成 geometry，我们需要稍微调整策略：
                # 我们可以先插入不含 geometry 的数据，然后用 UPDATE 生成 geometry，
                # 或者在 Python 端准备好 WKT 格式的 geometry 字符串。

                # 这里采用在 VALUES 子句中直接构造 Point 的方式，但需要确保 psycopg2 版本支持
                # 或者使用更复杂的 SQL 构造。
                # 一个更简单且推荐的做法是使用 psycopg2 的 adapt 功能或字符串格式化（小心SQL注入）。
                
                # 为了安全和正确性，这里采用 execute_values 插入主要数据，
                # 然后用一个单独的 UPDATE 语句填充 location 字段。
                # 这不是最高效的，但对于一次性 ETL 是可接受的。

                # 插入不含 location 的数据
                simple_insert_query = """
                INSERT INTO transport_stops (
                    stop_id, stop_name, latitude, longitude, 
                    location_type, parent_station
                ) VALUES %s
                ON CONFLICT (stop_id) DO NOTHING;
                """
                execute_values(cursor, simple_insert_query, records_to_insert, page_size=chunk_size)
                
                # 更新 location 字段
                # 注意：这会在每次 chunk 后都执行一次 UPDATE，对于非常大的文件可能效率不高。
                # 更好的方法是所有插入完成后执行一次全局 UPDATE。
                # 但为了分块处理的原子性，暂时这样。
                update_location_query = """
                UPDATE transport_stops
                SET location = ST_SetSRID(ST_MakePoint(longitude, latitude), 4326)
                WHERE location IS NULL AND latitude IS NOT NULL AND longitude IS NOT NULL; 
                """
                # cursor.execute(update_location_query) # 移到循环外执行一次

                total_rows_processed += len(records_to_insert)
                logging.info(f"已处理 {total_rows_processed} 条站点数据。")
        
        # 所有 chunk 处理完毕后，执行一次全局的 location 更新
        logging.info("正在为所有新插入的站点更新地理位置信息...")
        update_location_query = """
        UPDATE transport_stops
        SET location = ST_SetSRID(ST_MakePoint(longitude, latitude), 4326)
        WHERE location IS NULL AND latitude IS NOT NULL AND longitude IS NOT NULL; 
        """
        cursor.execute(update_location_query)
        logging.info(f"地理位置信息更新完成。影响行数: {cursor.rowcount}")

        conn.commit()
        logging.info("所有站点数据已成功加载到 transport_stops 表。")

    except (Exception, psycopg2.Error) as error:
        logging.error(f"处理站点数据时出错: {error}")
        if conn:
            conn.rollback() # 出错时回滚
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
            logging.info("数据库连接已关闭。")

if __name__ == "__main__":
    # 提示：请将 'path/to/your/stops.txt' 替换为实际的 stops.txt 文件路径
    # 例如: gtfs_data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'gtfs_sydney', 'stops.txt')
    # 这里假设 stops.txt 与脚本在同一目录的 'gtfs_data' 子目录中
    
    # 用户需要提供 stops.txt 的路径
    stops_txt_path_input = input("请输入 stops.txt 文件的完整路径: ")
    
    # 清理用户输入的路径，去除首尾空格和可能存在的引号
    stops_txt_path = stops_txt_path_input.strip().strip('"').strip("'")

    if not os.path.exists(stops_txt_path):
        logging.error(f"错误: 文件未找到 - {stops_txt_path} (原始输入: '{stops_txt_path_input}')")
    else:
        db_conn = get_db_connection()
        if db_conn:
            # 可以选择是否在每次运行时清空表
            # clear_existing_data = input("是否在导入前清空 transport_stops 表? (yes/no): ").lower() == 'yes'
            clear_existing_data = True # 默认为 True，对于初次导入或每日更新
            process_stops_data(db_conn, stops_txt_path, clear_table=clear_existing_data)

    # 示例用法:
    # 1. 将 full_greater_sydney_gtfs_static_0.zip 解压到一个文件夹，例如项目根目录下的 'gtfs_data'
    # 2. 运行脚本时，输入 stops.txt 的路径，例如: c:/Users/nuoai/Desktop/rentalAU_mcp/gtfs_data/stops.txt
