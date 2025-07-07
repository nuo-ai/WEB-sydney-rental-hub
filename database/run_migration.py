import psycopg2
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv('../.env')

# 读取SQL文件
with open('add_last_seen_field.sql', 'r', encoding='utf-8') as f:
    sql_script = f.read()

# 连接数据库并执行迁移
try:
    conn = psycopg2.connect(
        dbname='rental_mcp_db',
        user='etl_user', 
        password='etluser123',
        host='localhost',
        port='5432'
    )
    cursor = conn.cursor()
    cursor.execute(sql_script)
    conn.commit()
    print('✅ 数据库迁移执行成功！')
    
    # 验证新字段
    cursor.execute("SELECT column_name FROM information_schema.columns WHERE table_name='properties' AND column_name IN ('last_seen_at', 'bedroom_display');")
    results = cursor.fetchall()
    print(f'✅ 验证新字段: {[r[0] for r in results]}')
    
    cursor.close()
    conn.close()
except Exception as e:
    print(f'❌ 数据库迁移失败: {e}')
