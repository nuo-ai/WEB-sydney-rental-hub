#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
自动化数据更新脚本（包含Discord通知）
定期运行爬虫和数据导入，并发送Discord通知
"""

import os
import sys
import logging
import subprocess
import time
import requests
from datetime import datetime
from pathlib import Path
import schedule
import psycopg2
from dotenv import load_dotenv
from typing import Tuple

# 设置路径
PROJECT_ROOT = Path(__file__).parent.parent
CRAWLER_SCRIPT = PROJECT_ROOT / "crawler" / "v5_furniture.py"
ETL_SCRIPT = PROJECT_ROOT / "database" / "process_csv.py"
LOG_DIR = PROJECT_ROOT / "logs" / "automated_updates"

# 创建日志目录
LOG_DIR.mkdir(parents=True, exist_ok=True)

# 加载环境变量
load_dotenv(PROJECT_ROOT / ".env")

# Discord webhook配置
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

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

def send_discord_notification(message: str, success: bool, stage: str = ""):
    """发送Discord通知"""
    if not DISCORD_WEBHOOK_URL:
        logger.warning("DISCORD_WEBHOOK_URL not set. Skipping notification.")
        return

    color = 65280 if success else 16711680  # Green for success, Red for failure
    if success:
        title = f"✅ {stage}成功" if stage else "✅ 数据更新成功"
    else:
        title = f"❌ {stage}失败" if stage else "❌ 数据更新失败"

    payload = {
        "embeds": [{
            "title": title,
            "description": message,
            "color": color,
            "timestamp": datetime.utcnow().isoformat(),
            "footer": {
                "text": f"悉尼租房平台 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            }
        }]
    }
    
    try:
        response = requests.post(DISCORD_WEBHOOK_URL, json=payload, timeout=10)
        response.raise_for_status()
        logger.info(f"Successfully sent Discord notification: {title}")
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to send Discord notification: {e}")

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
        send_discord_notification(
            f"数据库连接失败: {e}", 
            success=False, 
            stage="数据库连接"
        )
        return False

def run_crawler() -> Tuple[bool, str]:
    """运行爬虫脚本"""
    try:
        logger.info("开始运行爬虫...")
        
        # 确保爬虫脚本存在
        if not CRAWLER_SCRIPT.exists():
            error_msg = f"爬虫脚本不存在: {CRAWLER_SCRIPT}"
            logger.error(error_msg)
            return False, error_msg
        
        # 运行爬虫
        result = subprocess.run(
            [sys.executable, str(CRAWLER_SCRIPT)],
            capture_output=True,
            text=True,
            cwd=str(CRAWLER_SCRIPT.parent),
            timeout=3600  # 1小时超时
        )
        
        if result.returncode == 0:
            # 从输出中提取有用信息
            output_lines = result.stdout.strip().split('\n')
            summary = []
            
            for line in output_lines:
                if any(keyword in line for keyword in ['completed', '完成', 'saved', '保存', 'properties', '房源']):
                    summary.append(line)
            
            summary_text = '\n'.join(summary[-5:])  # 最后5行关键信息
            logger.info(f"爬虫运行成功")
            return True, summary_text
        else:
            error_msg = f"爬虫运行失败: {result.stderr}"
            logger.error(error_msg)
            return False, error_msg
            
    except subprocess.TimeoutExpired:
        error_msg = "爬虫运行超时（1小时）"
        logger.error(error_msg)
        return False, error_msg
    except Exception as e:
        error_msg = f"运行爬虫时出错: {e}"
        logger.error(error_msg, exc_info=True)
        return False, error_msg

def run_etl() -> Tuple[bool, str]:
    """运行ETL脚本导入数据"""
    try:
        logger.info("开始运行ETL导入...")
        
        # 确保ETL脚本存在
        if not ETL_SCRIPT.exists():
            error_msg = f"ETL脚本不存在: {ETL_SCRIPT}"
            logger.error(error_msg)
            return False, error_msg
        
        # 运行ETL
        result = subprocess.run(
            [sys.executable, str(ETL_SCRIPT)],
            capture_output=True,
            text=True,
            cwd=str(ETL_SCRIPT.parent),
            timeout=1800,  # 30分钟超时
            encoding='utf-8',
            errors='ignore'
        )
        
        if result.returncode == 0:
            logger.info("ETL导入成功")
            
            # 提取摘要信息用于通知
            summary_lines = []
            for line in result.stdout.splitlines():
                if any(keyword in line for keyword in ["房源", "下架", "新增", "更新", "条记录"]):
                    summary_lines.append(line)
            
            summary = '\n'.join(summary_lines[-10:])  # 最后10行关键信息
            return True, summary
        else:
            error_msg = f"ETL导入失败: {result.stderr}"
            logger.error(error_msg)
            return False, error_msg
            
    except subprocess.TimeoutExpired:
        error_msg = "ETL运行超时（30分钟）"
        logger.error(error_msg)
        return False, error_msg
    except Exception as e:
        error_msg = f"运行ETL时出错: {e}"
        logger.error(error_msg, exc_info=True)
        return False, error_msg

def update_data():
    """执行完整的数据更新流程"""
    start_time = datetime.now()
    logger.info("="*50)
    logger.info("开始数据更新流程...")
    
    # 发送开始通知
    send_discord_notification(
        f"🚀 数据更新流程开始\n开始时间: {start_time.strftime('%Y-%m-%d %H:%M:%S')}", 
        success=True, 
        stage="流程启动"
    )
    
    total_success = True
    status_report = []
    
    # 1. 测试数据库连接
    if not test_db_connection():
        logger.error("数据库连接失败，终止更新")
        return
    status_report.append("✅ 数据库连接正常")
    
    # 2. 运行爬虫
    crawler_success, crawler_summary = run_crawler()
    if not crawler_success:
        logger.error("爬虫运行失败，终止更新")
        send_discord_notification(
            f"爬虫运行失败:\n```\n{crawler_summary}\n```", 
            success=False, 
            stage="爬虫"
        )
        total_success = False
        return
    
    status_report.append("✅ 爬虫运行成功")
    
    # 3. 等待一段时间确保文件写入完成
    logger.info("等待5秒确保文件写入完成...")
    time.sleep(5)
    
    # 4. 运行ETL导入
    etl_success, etl_summary = run_etl()
    if not etl_success:
        logger.error("ETL导入失败")
        send_discord_notification(
            f"ETL导入失败:\n```\n{etl_summary}\n```", 
            success=False, 
            stage="ETL导入"
        )
        total_success = False
        return
    
    status_report.append("✅ ETL导入成功")
    
    # 5. 发送成功完成通知
    end_time = datetime.now()
    duration = end_time - start_time
    
    final_message = f"""
📊 **数据更新完成**

**流程状态:**
{chr(10).join(status_report)}

**爬虫结果:**
```
{crawler_summary}
```

**ETL处理结果:**
```
{etl_summary}
```

**执行时间:** {duration.total_seconds():.1f} 秒
**完成时间:** {end_time.strftime('%Y-%m-%d %H:%M:%S')}
    """.strip()
    
    send_discord_notification(final_message, success=True, stage="数据更新")
    
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
    
    # 发送服务启动通知
    send_discord_notification(
        "🤖 自动化数据更新服务已启动\n定时任务: 每天凌晨03:00", 
        success=True, 
        stage="服务启动"
    )
    
    while True:
        schedule.run_pending()
        time.sleep(60)  # 每分钟检查一次

def run_once():
    """只运行一次更新"""
    update_data()

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='自动化数据更新脚本（包含Discord通知）')
    parser.add_argument('--run-once', action='store_true', help='只运行一次更新流程然后退出')
    parser.add_argument('--test-notification', action='store_true', help='测试Discord通知功能')
    args = parser.parse_args()
    
    logger.info("脚本启动...")
    
    if args.test_notification:
        logger.info("测试Discord通知功能...")
        send_discord_notification(
            "🧪 这是一条测试通知\n系统时间: " + datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 
            success=True, 
            stage="通知测试"
        )
        logger.info("测试通知已发送")
    elif args.run_once:
        logger.info("检测到 --run-once 参数，将执行单次更新。")
        run_once()
        logger.info("单次更新完成，脚本退出。")
    else:
        logger.info("未提供 --run-once 参数，将启动定时更新服务。")
        run_scheduled_updates()
