import os
import sys
import psycopg2
from dotenv import load_dotenv

def load_env():
    # 加载项目根目录 .env（脚本位于 scripts/ 下，.env 在上一级目录）
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    dotenv_path = os.path.join(project_root, ".env")
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path, override=True)
        print(f"✅ Loaded .env from: {dotenv_path}")
    else:
        load_dotenv(override=True)
        print("⚠️ .env 未找到，尝试从系统环境变量读取连接信息")

def get_connection():
    database_url = os.getenv("DATABASE_URL")
    if database_url:
        print("🔗 Connecting via DATABASE_URL ...")
        return psycopg2.connect(dsn=database_url)
    # fallback to discrete params
    dbname = os.getenv("DB_NAME", "rental_mcp_db")
    user = os.getenv("DB_USER", "etl_user")
    password = os.getenv("DB_PASSWORD")
    host = os.getenv("DB_HOST", "localhost")
    port = os.getenv("DB_PORT", "5432")
    if not password:
        raise RuntimeError("DB_PASSWORD 未设置，无法建立数据库连接")
    print(f"🔗 Connecting to {user}@{host}:{port}/{dbname} ...")
    return psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)

def run_sql_file(cursor, path: str):
    with open(path, "r", encoding="utf-8") as f:
        sql = f.read()
    print(f"\n⚡ 执行迁移文件: {path}")
    cursor.execute(sql)
    print(f"✅ 执行完成: {path}")

def verify_is_furnished_type(cursor):
    cursor.execute("""
        SELECT data_type
        FROM information_schema.columns
        WHERE table_name = 'properties' AND column_name = 'is_furnished'
    """)
    row = cursor.fetchone()
    dtype = row[0] if row else "UNKNOWN"
    print(f"🔍 验证 is_furnished 列类型: {dtype}")

def main():
    load_env()
    if len(sys.argv) < 2:
        print("用法: python scripts/run_sql_migration.py <sql_file1> [<sql_file2> ...]")
        sys.exit(2)

    sql_files = sys.argv[1:]
    # 仅执行存在的文件，保持顺序
    sql_files = [p for p in sql_files if os.path.exists(p)]
    if not sql_files:
        print("❌ 未找到任何可执行的 SQL 文件路径")
        sys.exit(1)

    conn = None
    try:
        conn = get_connection()
        # 允许 SQL 文件自行控制事务（文件内部可含 BEGIN/COMMIT）
        conn.autocommit = True
        with conn.cursor() as cur:
            for path in sql_files:
                run_sql_file(cur, path)
            # 轻量校验
            verify_is_furnished_type(cur)
        print("\n🎉 所有迁移执行完成")
        sys.exit(0)
    except Exception as e:
        print(f"❌ 迁移执行失败: {e}")
        sys.exit(1)
    finally:
        if conn:
            conn.close()
            print("🔌 数据库连接已关闭")

if __name__ == "__main__":
    main()
