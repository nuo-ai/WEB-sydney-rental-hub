import psycopg2
import os
from dotenv import load_dotenv

# 加载环境变量
dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path)

# 读取SQL文件
with open('migration_add_property_features_v3.sql', 'r', encoding='utf-8') as f:
    sql_script = f.read()

# 连接数据库并执行迁移
try:
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
    cursor = conn.cursor()
    cursor.execute(sql_script)
    conn.commit()
    print('✅ 数据库迁移执行成功！')
    
    # 验证新字段
    cursor.execute("SELECT column_name FROM information_schema.columns WHERE table_name='properties' AND column_name IN ('has_intercom', 'has_gas', 'furnishing_status', 'air_conditioning_type');")
    results = cursor.fetchall()
    print(f'✅ 验证新字段: {[r[0] for r in results]}')
    
    cursor.close()
    conn.close()
except Exception as e:
    print(f'❌ 数据库迁移失败: {e}')
