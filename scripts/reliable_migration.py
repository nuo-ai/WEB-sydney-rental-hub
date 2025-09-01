import psycopg2
import os
import sys
from dotenv import load_dotenv

def run_migration():
    print("🚀 开始数据库迁移...")
    
    # 获取项目根目录的绝对路径
    project_root = os.path.dirname(os.path.abspath(__file__))
    env_file = os.path.join(project_root, 'rentalAU_mcp', '.env')
    sql_file = os.path.join(project_root, 'rentalAU_mcp', 'etl', 'add_last_seen_field.sql')
    
    print(f"📂 项目根目录: {project_root}")
    print(f"📄 .env 文件路径: {env_file}")
    print(f"📄 SQL 文件路径: {sql_file}")
    
    # 检查文件是否存在
    if not os.path.exists(env_file):
        print(f"❌ .env 文件不存在: {env_file}")
        print("请确保 .env 文件在 rentalAU_mcp 目录下")
        return False
        
    if not os.path.exists(sql_file):
        print(f"❌ SQL 文件不存在: {sql_file}")
        return False
    
    # 加载环境变量
    print("📋 加载环境变量...")
    load_dotenv(env_file)
    
    # 从环境变量获取数据库连接信息
    db_host = os.getenv("DB_HOST", "localhost")
    db_port = os.getenv("DB_PORT", "5432")
    db_name = os.getenv("DB_NAME", "rental_mcp_db")
    db_user = os.getenv("DB_USER", "etl_user")
    db_password = os.getenv("DB_PASSWORD")
    
    print(f"🔗 数据库连接信息:")
    print(f"   主机: {db_host}")
    print(f"   端口: {db_port}")
    print(f"   数据库: {db_name}")
    print(f"   用户: {db_user}")
    print(f"   密码: {'已设置' if db_password else '未设置'}")
    
    if not db_password:
        print("❌ 数据库密码未设置，请在 .env 文件中设置 DB_PASSWORD")
        return False
    
    # 读取SQL文件
    print("📖 读取SQL迁移脚本...")
    try:
        with open(sql_file, 'r', encoding='utf-8') as f:
            sql_script = f.read()
        print("✅ SQL脚本读取成功")
    except Exception as e:
        print(f"❌ 读取SQL文件失败: {e}")
        return False
    
    # 连接数据库并执行迁移
    print("🔌 连接数据库...")
    try:
        conn = psycopg2.connect(
            host=db_host,
            port=db_port,
            dbname=db_name,
            user=db_user,
            password=db_password
        )
        print("✅ 数据库连接成功")
        
        cursor = conn.cursor()
        
        print("⚡ 执行迁移脚本...")
        cursor.execute(sql_script)
        conn.commit()
        print("✅ 数据库迁移执行成功！")
        
        # 验证新字段
        print("🔍 验证新字段...")
        cursor.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name='properties' 
            AND column_name IN ('last_seen_at', 'bedroom_display')
        """)
        results = cursor.fetchall()
        new_fields = [r[0] for r in results]
        print(f"✅ 验证新字段: {new_fields}")
        
        if 'last_seen_at' in new_fields and 'bedroom_display' in new_fields:
            print("🎉 所有字段都已成功添加！")
        else:
            print(f"⚠️ 部分字段可能未添加成功。预期: ['last_seen_at', 'bedroom_display'], 实际: {new_fields}")
        
        cursor.close()
        conn.close()
        print("🔌 数据库连接已关闭")
        return True
        
    except psycopg2.OperationalError as e:
        print(f"❌ 数据库连接失败: {e}")
        print("请检查:")
        print("  1. PostgreSQL 服务是否正在运行")
        print("  2. 数据库连接信息是否正确")
        print("  3. 用户权限是否足够")
        return False
    except Exception as e:
        print(f"❌ 数据库迁移失败: {e}")
        if 'conn' in locals():
            conn.rollback()
            conn.close()
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("  数据库迁移脚本")
    print("=" * 50)
    
    success = run_migration()
    
    print("=" * 50)
    if success:
        print("🎉 迁移完成！现在可以运行ETL管道了。")
    else:
        print("💔 迁移失败！请解决上述问题后重试。")
    print("=" * 50)
    
    sys.exit(0 if success else 1)
