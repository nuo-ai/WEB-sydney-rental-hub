#!/usr/bin/env python3
"""
一键执行ETL流程脚本
从爬取数据到数据库更新的完整流程
"""

import os
import sys
import subprocess
import time
from datetime import datetime

def print_header(title):
    """打印标题"""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)

def print_step(step_num, title):
    """打印步骤"""
    print(f"\n🚀 步骤 {step_num}: {title}")
    print("-" * 40)

def run_command(command, cwd, description, timeout=1800):
    """执行命令并返回结果"""
    print(f"📋 执行: {description}")
    print(f"📂 工作目录: {cwd}")
    print(f"⚡ 命令: {' '.join(command)}")
    
    try:
        start_time = time.time()
        result = subprocess.run(
            command,
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        end_time = time.time()
        duration = end_time - start_time
        
        if result.returncode == 0:
            print(f"✅ 成功完成 (耗时: {duration:.1f}秒)")
            if result.stdout.strip():
                print(f"📄 输出:\n{result.stdout}")
            return True
        else:
            print(f"❌ 失败 (返回码: {result.returncode})")
            if result.stderr.strip():
                print(f"❌ 错误信息:\n{result.stderr}")
            if result.stdout.strip():
                print(f"📄 输出:\n{result.stdout}")
            return False
            
    except subprocess.TimeoutExpired:
        print(f"❌ 超时 (超过 {timeout/60:.1f} 分钟)")
        return False
    except Exception as e:
        print(f"❌ 执行异常: {e}")
        return False

def main():
    print_header("悉尼租房数据 - 手动ETL执行器")
    print(f"🕐 开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 获取项目路径
    project_root = os.path.dirname(os.path.abspath(__file__))
    rentalAU_root = os.path.join(project_root, 'rentalAU_mcp')
    dist_dir = os.path.join(rentalAU_root, 'dist')
    etl_dir = os.path.join(rentalAU_root, 'etl')
    
    print(f"📂 项目根目录: {project_root}")
    print(f"📂 rentalAU_mcp目录: {rentalAU_root}")
    
    # 检查关键文件
    spider_script = os.path.join(dist_dir, 'v2.py')
    update_script = os.path.join(etl_dir, 'update_database.py')
    
    print("\n🔍 检查关键文件...")
    
    if not os.path.exists(spider_script):
        print(f"❌ 爬虫脚本不存在: {spider_script}")
        return False
    print(f"✅ 爬虫脚本: {spider_script}")
    
    if not os.path.exists(update_script):
        print(f"❌ 数据更新脚本不存在: {update_script}")
        return False
    print(f"✅ 数据更新脚本: {update_script}")
    
    print("\n🎯 准备执行完整ETL流程...")
    input("按 Enter 键继续...")
    
    # 步骤1: 执行爬虫
    print_step(1, "执行爬虫 - 抓取最新房源数据")
    
    spider_success = run_command(
        command=[sys.executable, 'v2.py'],
        cwd=dist_dir,
        description="执行爬虫脚本",
        timeout=1800  # 30分钟超时
    )
    
    if not spider_success:
        print("\n💔 爬虫执行失败，ETL流程终止")
        return False
    
    # 检查是否生成了新的CSV文件
    output_dir = os.path.join(dist_dir, 'output')
    if os.path.exists(output_dir):
        csv_files = [f for f in os.listdir(output_dir) if f.endswith('.csv')]
        if csv_files:
            latest_csv = max(csv_files, key=lambda x: os.path.getctime(os.path.join(output_dir, x)))
            print(f"📄 发现最新CSV文件: {latest_csv}")
        else:
            print("⚠️ 未发现CSV文件，但爬虫显示成功")
    
    # 步骤2: 执行数据库更新
    print_step(2, "更新数据库 - 处理爬取的数据")
    
    update_success = run_command(
        command=[sys.executable, 'update_database.py'],
        cwd=etl_dir,
        description="执行数据库更新脚本",
        timeout=600  # 10分钟超时
    )
    
    if not update_success:
        print("\n💔 数据库更新失败")
        return False
    
    # 完成
    print_header("ETL流程执行完成")
    print("🎉 所有步骤都已成功完成！")
    print(f"🕐 结束时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("\n✨ 数据库现在包含最新的房源信息")
    print("✨ 您可以启动后端服务来查看结果")
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️ 用户中断了执行")
        print("💡 可以重新运行脚本继续执行")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ 意外错误: {e}")
        sys.exit(1)
