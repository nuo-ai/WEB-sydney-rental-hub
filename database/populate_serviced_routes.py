import psycopg2
from psycopg2.extras import execute_values, Json
import os
from dotenv import load_dotenv
import logging
import requests
import json
import time
from datetime import datetime
from collections import defaultdict

# 配置日志记录
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 加载 .env 文件中的环境变量
# Ensure .env is in the project root, one level up from 'etl' directory
dotenv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path, override=True) # Added override=True
    logging.info(f"Successfully loaded .env file from: {dotenv_path} (with override)")
else:
    load_dotenv(override=True) # Fallback with override
    logging.warning(
        f".env file not found at {dotenv_path}. Attempting default load_dotenv() search (with override). "
        "Ensure your .env file is correctly placed in the project root."
    )

# TfNSW API 配置
TNSW_API_KEY = os.getenv("TNSW_API_KEY") # 确保 .env 文件中有 TNSW_API_KEY
TNSW_API_BASE_URL = "https://api.transport.nsw.gov.au/v1/tp/"

# 采样时间点 (HHMM格式)
SAMPLE_TIMES = ["0800", "1100", "1700"] # 早高峰, 平峰, 晚高峰

# API 调用之间的延迟（秒），以避免超出速率限制 (TfNSW 通常是每秒5次)
API_CALL_DELAY = 0.3 # 约每秒3次调用

# 交通模式映射 (基于 TfNSW API 文档中的 product.class)
# 参考: TripPlanner.json -> definitions -> RouteProduct -> properties -> class
# 和 trip-planner-api-manual-opendataproduction-v3.3.pdf (第22页)
TRANSPORT_MODE_MAP = {
    1: "TRAIN",       # Train (Sydney Trains, Intercity, Regional)
    2: "METRO",       # Metro
    4: "LIGHT_RAIL",  # Light Rail
    5: "BUS",         # Bus (Sydney Buses, Private Buses, On Demand)
    7: "COACH",       # Coach
    9: "FERRY",       # Ferry (Sydney Ferries, Private Ferries)
    11: "SCHOOL_BUS", # School Bus
    # 99: "WALK", # 步行等通常不作为站点服务模式
    # 100: "WALK",
    # 107: "CYCLE" # 自行车
}
# iconId 也可以用来辅助判断，但 product.class 更直接
# 例如 iconId 23 是 On Demand Bus (product.class 5)

def get_db_connection():
    """建立并返回数据库连接"""
    db_name = os.getenv("DB_NAME")
    db_user = os.getenv("DB_USER")
    db_password = os.getenv("DB_PASSWORD")
    db_host = os.getenv("DB_HOST")
    db_port = os.getenv("DB_PORT")

    if not db_password:
        logging.error("CRITICAL: DB_PASSWORD environment variable not set. Please set it in your .env file.")
        raise ValueError("DB_PASSWORD environment variable is not set. Cannot establish database connection.")
    
    if not all([db_name, db_user, db_host, db_port]):
        logging.error("One or more database connection environment variables (DB_NAME, DB_USER, DB_HOST, DB_PORT) are not set.")
        # Depending on policy, you might want to raise an error here as well.
        # For now, it will likely fail in psycopg2.connect if any are None.

    try:
        conn = psycopg2.connect(
            dbname=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port
        )
        logging.info(f"数据库连接成功: {db_user}@{db_host}:{db_port}/{db_name}")
        return conn
    except psycopg2.Error as e: # More specific exception
        logging.error(f"数据库连接失败: {e}")
        raise # Re-raise the specific psycopg2 error
    except Exception as e: # Catch other potential errors
        logging.error(f"获取数据库连接时发生未知错误: {e}")
        raise

def get_serviced_routes_for_stop(stop_id: str) -> list:
    """
    为单个站点ID，在多个采样时间点调用 /departure_mon API，
    获取并合并去重其服务的线路信息。
    """
    if not TNSW_API_KEY:
        logging.error("TNSW_API_KEY 未在 .env 文件中配置。")
        return []

    all_routes_for_stop = {} # 使用字典去重: (route_short_name, mode) -> route_details

    current_date_str = datetime.now().strftime("%Y%m%d")

    for sample_time in SAMPLE_TIMES:
        logging.info(f"正在为站点 {stop_id} 查询 {sample_time} 的班次...")
        params = {
            "outputFormat": "rapidJSON",
            "coordOutputFormat": "EPSG:4326",
            "mode": "direct",
            "type_dm": "stop",
            "name_dm": stop_id,
            "depArrMacro": "dep",
            "itdDate": current_date_str,
            "itdTime": sample_time,
            "TfNSWDM": "true", # 启用 TfNSW 特定选项
            "version": "10.2.1.42", # 与之前测试一致
            # "limit": 100 # 尝试获取更多班次，API文档未明确支持，需测试
        }
        headers = {"Authorization": f"apikey {TNSW_API_KEY}"}

        try:
            response = requests.get(TNSW_API_BASE_URL + "departure_mon", params=params, headers=headers, timeout=30)
            time.sleep(API_CALL_DELAY) # 控制API调用频率

            if response.status_code == 200:
                data = response.json()
                if data.get("error"):
                    logging.warning(f"站点 {stop_id} 在 {sample_time} 的API调用返回错误: {data['error']}")
                    continue
                
                stop_events = data.get("stopEvents", [])
                if not stop_events and len(data.get("locations", [])) == 1:
                    logging.info(f"站点 {stop_id} 在 {sample_time} 没有班次信息。")
                
                for event in stop_events:
                    transport = event.get("transportation")
                    if transport:
                        route_short_name = transport.get("number")
                        route_long_name = transport.get("name")
                        product_info = transport.get("product", {})
                        mode_class = product_info.get("class")
                        
                        transport_mode = TRANSPORT_MODE_MAP.get(mode_class, "UNKNOWN")
                        # 对于 On Demand (iconId 23, class 5), 模式仍是 BUS
                        if transport.get("iconId") == 23 and mode_class == 5:
                            transport_mode = "ON_DEMAND_BUS" # 或保持为 BUS，根据需求

                        if route_short_name and transport_mode != "UNKNOWN":
                            route_key = (route_short_name, transport_mode)
                            if route_key not in all_routes_for_stop:
                                all_routes_for_stop[route_key] = {
                                    "route_short_name": route_short_name,
                                    "route_long_name": route_long_name,
                                    "transport_mode": transport_mode,
                                    # "route_id": transport.get("id"), # 可选
                                    # "operator_name": transport.get("operator", {}).get("name") # 可选
                                }
            elif response.status_code == 401 or response.status_code == 403:
                logging.error(f"API Key 无效或权限不足 (状态码: {response.status_code})。请检查 TNSW_API_KEY。")
                return [] # 认证失败，停止后续调用
            else:
                logging.warning(f"站点 {stop_id} 在 {sample_time} 的API调用失败，状态码: {response.status_code}, 响应: {response.text[:200]}")
        
        except requests.exceptions.RequestException as e:
            logging.error(f"为站点 {stop_id} 在 {sample_time} 调用API时发生网络错误: {e}")
            # 可以考虑重试逻辑
        except Exception as e:
            logging.error(f"为站点 {stop_id} 在 {sample_time} 处理API响应时发生未知错误: {e}")
            
    return list(all_routes_for_stop.values())


def update_transport_stops_in_db(conn, stop_id: str, serviced_routes: list):
    """
    更新数据库中单个站点的 serviced_routes_details 和 transport_mode 字段。
    """
    if not conn or not serviced_routes:
        return False

    cursor = None
    success = False
    try:
        cursor = conn.cursor()
        
        # 更新 serviced_routes_details
        json_serviced_routes = json.dumps(serviced_routes)
        update_query = """
        UPDATE transport_stops
        SET serviced_routes_details = %s, 
            updated_at = NOW() 
        WHERE stop_id = %s;
        """
        cursor.execute(update_query, (Json(serviced_routes), stop_id)) # 使用 Json 适配器
        
        # (可选) 更新 transport_mode 字段
        # 策略：如果所有线路都是同一种模式，则设为该模式；否则设为 "MULTIMODAL" 或保持不变/NULL
        if serviced_routes:
            modes_in_routes = set(route['transport_mode'] for route in serviced_routes)
            if len(modes_in_routes) == 1:
                primary_mode = modes_in_routes.pop()
            else:
                primary_mode = "MULTIMODAL" # 或者可以根据线路数量等更复杂的逻辑
            
            mode_update_query = """
            UPDATE transport_stops
            SET transport_mode = %s,
                updated_at = NOW()
            WHERE stop_id = %s;
            """
            cursor.execute(mode_update_query, (primary_mode, stop_id))

        conn.commit()
        logging.info(f"站点 {stop_id} 的服务线路信息已更新。共 {len(serviced_routes)} 条线路。主要模式: {primary_mode if serviced_routes else 'N/A'}")
        success = True
    except (Exception, psycopg2.Error) as error:
        logging.error(f"更新站点 {stop_id} 数据时出错: {error}")
        if conn:
            conn.rollback()
    finally:
        if cursor:
            cursor.close()
    return success

def get_core_stop_ids_from_db(conn):
    """
    (替代方案) 从数据库动态获取核心站点列表。
    这里简化为获取所有在 UNIVERSITY_WALKABLE_STOPS 中定义的站点。
    实际应用中，可以从 find_nearby_stops.py 的输出文件加载，
    或者直接在数据库中查询大学附近的站点。
    """
    # 此函数需要用户提供 UNIVERSITY_WALKABLE_STOPS 的数据源
    # 例如，从之前 find_nearby_stops.py 生成的 JSON 文件读取
    # For now, returning a placeholder or requiring a file.
    # Placeholder:
    # return ["10101100", "203311"] # Example stop IDs

    # 更好的方式是让用户提供 find_nearby_stops.py 的输出文件路径
    json_file_path = input("请输入 `find_nearby_stops.py` 输出的包含 UNIVERSITY_WALKABLE_STOPS 的 JSON 文件路径: ")
    if not os.path.exists(json_file_path):
        logging.error(f"核心站点JSON文件未找到: {json_file_path}")
        return []
    
    try:
        with open(json_file_path, 'r') as f:
            university_walkable_stops = json.load(f)
        
        all_core_stop_ids = set()
        for uni_code, stop_list in university_walkable_stops.items():
            all_core_stop_ids.update(stop_list)
        
        logging.info(f"从 {json_file_path} 加载了 {len(all_core_stop_ids)} 个不重复的核心站点ID。")
        return list(all_core_stop_ids)
    except Exception as e:
        logging.error(f"读取或解析核心站点JSON文件时出错: {e}")
        return []


if __name__ == "__main__":
    if not TNSW_API_KEY:
        logging.error("错误: TNSW_API_KEY 未在 .env 文件中配置。请添加 TNSW_API_KEY=<your_api_key> 到 .env 文件。")
    else:
        db_conn = get_db_connection()
        if db_conn:
            # 获取核心站点列表
            # 方案1: 从 find_nearby_stops.py 的输出文件加载 (如下)
            core_stop_ids = get_core_stop_ids_from_db(db_conn)
            
            # 方案2: 或者，如果 UNIVERSITY_WALKABLE_STOPS 字典不大，可以直接粘贴在这里
            # example_uni_walkable_stops = {
            #     "UNSW": ["stop_id_unsw_1", "stop_id_unsw_2"],
            #     "USYD": ["stop_id_usyd_1"]
            # }
            # core_stop_ids = list(set(sid for slist in example_uni_walkable_stops.values() for sid in slist))

            if not core_stop_ids:
                logging.warning("未能获取核心站点列表，脚本终止。")
            else:
                logging.info(f"将为 {len(core_stop_ids)} 个核心站点获取服务线路信息...")
                
                successful_updates = 0
                failed_updates = 0

                for i, stop_id in enumerate(core_stop_ids):
                    logging.info(f"正在处理核心站点 {i+1}/{len(core_stop_ids)}: {stop_id}")
                    serviced_routes = get_serviced_routes_for_stop(stop_id)
                    
                    if serviced_routes: # 只有当成功获取到线路时才更新
                        if update_transport_stops_in_db(db_conn, stop_id, serviced_routes):
                            successful_updates += 1
                        else:
                            failed_updates +=1
                    elif serviced_routes is None: # API Key 问题导致提前退出
                        logging.error("因API Key问题，处理提前终止。")
                        break 
                    else: # API 调用可能都失败了，或者该站点确实没有服务线路
                        logging.info(f"站点 {stop_id} 未能获取到服务线路信息，跳过数据库更新。")
                        # 可以考虑为这种情况在数据库中存入空数组 [] 而不是 NULL
                        # update_transport_stops_in_db(db_conn, stop_id, []) 

                logging.info(f"所有核心站点处理完毕。成功更新 {successful_updates} 个站点，失败 {failed_updates} 个站点。")

            if db_conn:
                db_conn.close()
                logging.info("数据库连接已关闭。")

# 脚本说明和使用方法：
# 1. .env 文件配置：
#    - 确保项目根目录下的 .env 文件包含正确的数据库连接信息 (DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT)。
#    - 新增配置：请在 .env 文件中添加您的 Transport for NSW API Key：
#      TNSW_API_KEY=your_actual_tfnsw_api_key_here
# 2. 核心站点列表输入：
#    - 脚本运行时会提示您输入 find_nearby_stops.py 脚本之前生成的包含 UNIVERSITY_WALKABLE_STOPS 字典的 JSON 文件的路径。
#    - 请确保您已保存该 JSON 输出到一个文件中。
# 3. 运行脚本：
#    - 在项目根目录下（确保虚拟环境已激活）运行：
#      python etl/populate_serviced_routes.py
#    - 按提示输入包含核心站点ID的 JSON 文件路径。
# 4. 脚本执行流程：
#    - 连接数据库。
#    - 加载核心站点ID列表。
#    - 遍历每个核心站点ID：
#        - 为每个站点的每个采样时间点 (SAMPLE_TIMES) 调用 TfNSW /departure_mon API。
#        - 在每次 API 调用之间有短暂延迟 (API_CALL_DELAY) 以避免超速。
#        - 从 API 响应中提取线路的短名称、长名称和交通模式（根据 product.class 映射）。
#        - 合并和去重为一个站点收集到的所有线路。
#        - 将去重后的线路列表（作为 JSON）更新到 transport_stops 表的 serviced_routes_details 字段。
#        - 根据获取到的线路模式，尝试更新 transport_mode 字段。
#    - 记录处理日志。
# 5. 交通模式映射：
#    - 脚本内置了一个 TRANSPORT_MODE_MAP 字典，用于将 API 返回的 product.class（整数）映射为我们定义的标准模式字符串。
# 6. 速率限制：
#    - 脚本通过 API_CALL_DELAY 控制 API 调用频率。
# 关于 transport_mode 字段的更新策略：
# 脚本当前采用的策略是：如果一个站点服务的所有线路都属于同一种交通模式，则 transport_mode 字段更新为该模式的名称。
# 如果服务多种模式，则更新为 "MULTIMODAL"。
# 请您准备好 .env 文件（特别是 TNSW_API_KEY）和核心站点ID的 JSON 文件，然后尝试运行此脚本。
# 由于涉及到多次 API 调用，处理所有核心站点可能需要一些时间。请留意脚本的日志输出。
