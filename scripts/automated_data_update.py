#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
自动化数据更新脚本
定期运行爬虫和数据导入
"""

import os
import sys
import logging
import subprocess
import time
from datetime import datetime
from pathlib import Path
import schedule
import psycopg2
from dotenv import load_dotenv

# 设置路径
PROJECT_ROOT = Path(__file__).parent.parent
CRAWLER_SCRIPT = PROJECT_ROOT / "crawler" / "dist" / "v2.py"
ETL_SCRIPT = PROJECT_ROOT / "database" / "process_csv.py"
LOG_DIR = PROJECT_ROOT / "logs" / "automated_updates"

# 创建日志目录
LOG_DIR.mkdir(parents=True, exist_ok=True)

# 配置日志
def setup_logger():
    log_file = LOG_DIR / f"update_{datetime.now():%Y%m%d}.log"
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler(sys.stdout)
        ]
    )
    return logging.getLogger('automated_update')

logger = setup_logger()

# 加载环境变量
load_dotenv(PROJECT_ROOT / ".env")

def test_db_connection():
    """测试数据库连接"""
    try:
        database_url = os.getenv("DATABASE_URL")
        if database_url:
            conn = psycopg2.connect(database_url)
        else:
            conn = psycopg2.connect(
                dbname=os.getenv("DB_NAME", "rental_mcp_db"),
                user=os.getenv("DB_USER", "etl_user"),
                password=os.getenv("DB_PASSWORD"),
                host=os.getenv("DB_HOST", "localhost"),
                port=os.getenv("DB_PORT", "5432")
            )
        conn.close()
        logger.info("数据库连接测试成功")
        return True
    except Exception as e:
        logger.error(f"数据库连接失败: {e}")
        return False

def run_crawler():
    """运行爬虫脚本"""
    try:
        logger.info("开始运行爬虫...")
        
        # 确保爬虫脚本存在
        if not CRAWLER_SCRIPT.exists():
            logger.error(f"爬虫脚本不存在: {CRAWLER_SCRIPT}")
            return False
        
        # 运行爬虫
        result = subprocess.run(
            [sys.executable, str(CRAWLER_SCRIPT)],
            capture_output=True,
            text=True,
            cwd=str(CRAWLER_SCRIPT.parent)
        )
        
        if result.returncode == 0:
            # 获取输出的CSV文件路径
            output_file = result.stdout.strip()
            logger.info(f"爬虫运行成功，输出文件: {output_file}")
            return True
        else:
            logger.error(f"爬虫运行失败: {result.stderr}")
            return False
            
    except Exception as e:
        logger.error(f"运行爬虫时出错: {e}", exc_info=True)
        return False

def run_etl():
    """运行ETL脚本导入数据"""
    try:
        logger.info("开始运行ETL导入...")
        
        # 确保ETL脚本存在
        if not ETL_SCRIPT.exists():
            logger.error(f"ETL脚本不存在: {ETL_SCRIPT}")
            return False
        
        # 运行ETL
        result = subprocess.run(
            [sys.executable, str(ETL_SCRIPT)],
            capture_output=True,
            text=True,
            cwd=str(ETL_SCRIPT.parent)
        )
        
        if result.returncode == 0:
            logger.info("ETL导入成功")
            return True
        else:
            logger.error(f"ETL导入失败: {result.stderr}")
            return False
            
    except Exception as e:
        logger.error(f"运行ETL时出错: {e}", exc_info=True)
        return False

def update_data():
    """执行完整的数据更新流程"""
    logger.info("="*50)
    logger.info("开始数据更新流程...")
    
    # 1. 测试数据库连接
    if not test_db_connection():
        logger.error("数据库连接失败，终止更新")
        return
    
    # 2. 运行爬虫
    if not run_crawler():
        logger.error("爬虫运行失败，终止更新")
        return
    
    # 3. 等待一段时间确保文件写入完成
    time.sleep(5)
    
    # 4. 运行ETL导入
    if not run_etl():
        logger.error("ETL导入失败")
        return
    
    logger.info("数据更新流程完成！")
    logger.info("="*50)

def run_scheduled_updates():
    """运行定时更新"""
    logger.info("启动自动化数据更新服务...")
    
    # 立即运行一次
    update_data()
    
    # 设置定时任务
    # 每天凌晨3点更新
    schedule.every().day.at("03:00").do(update_data)
    
    # 每8小时更新一次（可根据需要调整）
    # schedule.every(8).hours.do(update_data)
    
    logger.info("定时任务已设置，等待执行...")
    
    while True:
        schedule.run_pending()
        time.sleep(60)  # 每分钟检查一次

def run_once():
    """只运行一次更新"""
    update_data()

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='自动化数据更新脚本')
    parser.add_argument('--run-once', action='store_true', help='只运行一次更新流程然后退出')
    args = parser.parse_args()
    
    logger.info("脚本启动...")
    
    if args.run_once:
        logger.info("检测到 --run-once 参数，将执行单次更新。")
        run_once()
        logger.info("单次更新完成，脚本退出。")
    else:
        logger.info("未提供 --run-once 参数，将启动定时更新服务。")
        run_scheduled_updates()
