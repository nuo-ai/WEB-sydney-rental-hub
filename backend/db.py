import psycopg2
from psycopg2 import pool
import os
from dotenv import load_dotenv
import logging
from typing import Any, Optional

# Load environment variables from .env file
load_dotenv()

# 全局连接池实例
_db_pool: Optional[pool.ThreadedConnectionPool] = None

def _create_connection_pool():
    """创建数据库连接池"""
    global _db_pool
    try:
        # 从环境变量获取连接池配置
        min_conn = int(os.getenv("DB_POOL_MIN_SIZE", "2"))
        max_conn = int(os.getenv("DB_POOL_MAX_SIZE", "10"))
        
        # 优先使用 DATABASE_URL
        database_url = os.getenv("DATABASE_URL")
        if database_url:
            logging.info(f"创建连接池: min={min_conn}, max={max_conn}, 使用 DATABASE_URL")
            _db_pool = pool.ThreadedConnectionPool(
                min_conn, max_conn,
                database_url
            )
        else:
            # 使用独立的环境变量
            logging.info(f"创建连接池: min={min_conn}, max={max_conn}, 使用独立环境变量")
            _db_pool = pool.ThreadedConnectionPool(
                min_conn, max_conn,
                dbname=os.getenv("DB_NAME"),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD"),
                host=os.getenv("DB_HOST"),
                port=os.getenv("DB_PORT")
            )
        logging.info("数据库连接池创建成功")
    except psycopg2.Error as e:
        logging.error(f"创建连接池失败: {e}")
        raise

def get_db_connection():
    """从连接池获取数据库连接
    
    重要：使用完后必须调用 release_db_connection(conn) 归还连接
    """
    global _db_pool
    
    # 如果连接池不存在，创建它
    if _db_pool is None:
        _create_connection_pool()
    
    try:
        # 从连接池获取连接
        conn = _db_pool.getconn()
        return conn
    except pool.PoolError as e:
        logging.error(f"连接池错误: {e}")
        # 连接池耗尽时的降级处理：直接创建新连接
        logging.warning("连接池已耗尽，创建临时连接")
        database_url = os.getenv("DATABASE_URL")
        if database_url:
            return psycopg2.connect(database_url)
        else:
            return psycopg2.connect(
                dbname=os.getenv("DB_NAME"),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD"),
                host=os.getenv("DB_HOST"),
                port=os.getenv("DB_PORT")
            )
    except Exception as e:
        logging.error(f"数据库连接错误: {e}")
        raise

def release_db_connection(conn):
    """将连接归还到连接池
    
    Args:
        conn: 要归还的数据库连接
    """
    global _db_pool
    if conn:
        try:
            if _db_pool:
                _db_pool.putconn(conn)
            else:
                # 没有连接池时，直接关闭连接
                conn.close()
        except Exception as e:
            logging.error(f"归还连接失败: {e}")
            try:
                conn.close()
            except:
                pass

async def init_db_pool():
    """初始化数据库连接池"""
    global _db_pool
    if _db_pool is None:
        _create_connection_pool()
    logging.info("数据库连接池初始化完成")

async def close_db_pool():
    """关闭数据库连接池"""
    global _db_pool
    if _db_pool:
        _db_pool.closeall()
        logging.info("数据库连接池已关闭")
    _db_pool = None

def get_db_conn_dependency():
    """FastAPI 依赖项：获取数据库连接
    
    注意：这个函数返回一个上下文管理器，需要在使用时用 with 语句
    """
    # 直接返回连接对象供 FastAPI 使用
    global _db_pool
    
    # 如果连接池不存在，创建它
    if _db_pool is None:
        _create_connection_pool()
    
    try:
        conn = _db_pool.getconn()
        return conn
    except pool.PoolError as e:
        logging.error(f"连接池错误: {e}")
        # 降级：直接创建连接
        database_url = os.getenv("DATABASE_URL")
        if database_url:
            return psycopg2.connect(database_url)
        else:
            return psycopg2.connect(
                dbname=os.getenv("DB_NAME"),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD"),
                host=os.getenv("DB_HOST"),
                port=os.getenv("DB_PORT")
            )
