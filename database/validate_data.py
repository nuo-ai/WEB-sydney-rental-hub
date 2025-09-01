#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
数据验证脚本：确保数据库状态正确
"""

import psycopg2
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv()

def validate_database():
    """验证数据库状态的一致性"""
    
    # 连接数据库
    database_url = os.getenv("DATABASE_URL")
    if database_url:
        conn = psycopg2.connect(database_url)
    else:
        conn = psycopg2.connect(
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT")
        )
    
    cur = conn.cursor()
    issues = []
    
    print("=" * 60)
    print("数据库验证报告")
    print("=" * 60)
    
    # 1. 检查is_active与status的一致性
    cur.execute("""
        SELECT COUNT(*) 
        FROM properties 
        WHERE status = 'off-market' AND is_active = TRUE
    """)
    count = cur.fetchone()[0]
    if count > 0:
        issues.append(f"❌ {count}条off-market房源的is_active仍为TRUE")
    else:
        print("✅ off-market状态与is_active一致")
    
    # 2. 检查活跃房源的status
    cur.execute("""
        SELECT status, COUNT(*) 
        FROM properties 
        WHERE is_active = TRUE 
        GROUP BY status
    """)
    results = cur.fetchall()
    print("\n活跃房源的状态分布：")
    for status, count in results:
        print(f"  {status}: {count}")
        if status == 'off-market':
            issues.append(f"❌ 有{count}条活跃房源的status是off-market")
    
    # 3. 检查最近更新时间
    cur.execute("""
        SELECT 
            MAX(last_updated) as latest,
            MIN(last_updated) as earliest
        FROM properties
        WHERE is_active = TRUE
    """)
    latest, earliest = cur.fetchone()
    print(f"\n活跃房源更新时间：")
    print(f"  最新: {latest}")
    print(f"  最早: {earliest}")
    
    if earliest and latest:
        time_diff = latest - earliest
        if time_diff > timedelta(days=7):
            issues.append(f"⚠️ 活跃房源更新时间跨度超过7天")
    
    # 4. 总体统计
    cur.execute("""
        SELECT 
            COUNT(*) as total,
            COUNT(CASE WHEN is_active = TRUE THEN 1 END) as active,
            COUNT(CASE WHEN is_active = FALSE THEN 1 END) as inactive
        FROM properties
    """)
    total, active, inactive = cur.fetchone()
    print(f"\n总体统计：")
    print(f"  总计: {total}")
    print(f"  活跃: {active} ({active*100.0/total:.1f}%)")
    print(f"  不活跃: {inactive} ({inactive*100.0/total:.1f}%)")
    
    # 5. 报告问题
    print("\n" + "=" * 60)
    if issues:
        print("发现的问题：")
        for issue in issues:
            print(f"  {issue}")
        print("\n建议执行修复脚本：")
        print("  python database/fix_off_market_status.sql")
    else:
        print("✅ 数据库状态验证通过，无异常")
    
    conn.close()
    
    return len(issues) == 0

if __name__ == "__main__":
    is_valid = validate_database()
    exit(0 if is_valid else 1)