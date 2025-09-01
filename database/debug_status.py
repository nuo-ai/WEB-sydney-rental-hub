#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
调试脚本：检查数据库中房源的实际状态
"""

import psycopg2
import os
from dotenv import load_dotenv
from datetime import datetime

# 加载环境变量
load_dotenv()

def check_database_status():
    """检查数据库中房源的状态分布"""
    
    conn = psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
    )
    
    cur = conn.cursor()
    
    print("=" * 60)
    print("数据库房源状态调试报告")
    print("=" * 60)
    
    # 1. 检查is_active状态分布
    cur.execute("""
        SELECT is_active, COUNT(*) as count
        FROM properties
        GROUP BY is_active
        ORDER BY is_active
    """)
    results = cur.fetchall()
    print("\n1. is_active状态分布：")
    total = 0
    for row in results:
        print(f"   is_active = {row[0]}: {row[1]} 套房源")
        total += row[1]
    print(f"   总计: {total} 套房源")
    
    # 2. 检查最近更新的记录
    cur.execute("""
        SELECT 
            DATE(last_updated) as update_date,
            COUNT(*) as count,
            COUNT(CASE WHEN is_active = TRUE THEN 1 END) as active_count,
            COUNT(CASE WHEN is_active = FALSE THEN 1 END) as inactive_count
        FROM properties
        WHERE last_updated IS NOT NULL
        GROUP BY DATE(last_updated)
        ORDER BY update_date DESC
        LIMIT 5
    """)
    results = cur.fetchall()
    print("\n2. 最近更新记录：")
    for row in results:
        print(f"   {row[0]}: 总计{row[1]}条 (活跃{row[2]}, 不活跃{row[3]})")
    
    # 3. 检查Ultimo区的房源
    cur.execute("""
        SELECT 
            COUNT(*) as total,
            COUNT(CASE WHEN is_active = TRUE THEN 1 END) as active,
            COUNT(CASE WHEN is_active = FALSE THEN 1 END) as inactive
        FROM properties
        WHERE UPPER(suburb) = 'ULTIMO'
    """)
    result = cur.fetchone()
    print(f"\n3. Ultimo区房源状态：")
    print(f"   总计: {result[0]} (活跃: {result[1]}, 不活跃: {result[2]})")
    
    # 4. 检查各区域的活跃房源数
    cur.execute("""
        SELECT 
            suburb,
            COUNT(*) as total,
            COUNT(CASE WHEN is_active = TRUE THEN 1 END) as active
        FROM properties
        GROUP BY suburb
        HAVING COUNT(CASE WHEN is_active = TRUE THEN 1 END) > 0
        ORDER BY active DESC
        LIMIT 10
    """)
    results = cur.fetchall()
    print("\n4. 活跃房源最多的10个区：")
    for row in results:
        print(f"   {row[0]}: {row[2]}个活跃 (总计{row[1]})")
    
    # 5. 检查last_seen_at字段
    cur.execute("""
        SELECT 
            COUNT(*) as total,
            COUNT(last_seen_at) as has_last_seen,
            MAX(last_seen_at) as latest_seen,
            MIN(last_seen_at) as earliest_seen
        FROM properties
    """)
    result = cur.fetchone()
    print(f"\n5. last_seen_at字段状态：")
    print(f"   总记录: {result[0]}")
    print(f"   有last_seen_at: {result[1]}")
    print(f"   最新: {result[2]}")
    print(f"   最早: {result[3]}")
    
    # 6. 最重要：检查今天更新的记录
    cur.execute("""
        SELECT 
            COUNT(*) as total,
            COUNT(CASE WHEN is_active = TRUE THEN 1 END) as active,
            COUNT(CASE WHEN is_active = FALSE THEN 1 END) as inactive
        FROM properties
        WHERE DATE(last_updated) = CURRENT_DATE
    """)
    result = cur.fetchone()
    print(f"\n6. 今天更新的房源：")
    print(f"   总计: {result[0]} (活跃: {result[1]}, 不活跃: {result[2]})")
    
    conn.close()
    print("\n" + "=" * 60)

if __name__ == "__main__":
    check_database_status()