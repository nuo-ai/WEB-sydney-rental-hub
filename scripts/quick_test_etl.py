#!/usr/bin/env python3
"""
快速ETL测试脚本
跳过爬虫，直接使用现有最新CSV数据测试数据库更新
"""

import os
import sys
import subprocess
import time
import glob
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

def find_latest_csv():
    """找到最新的CSV文件"""
    project_root = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(project_root, 'rentalAU_mcp', 'dist', 'output')
    
    # 查找所有CSV文件
    csv_pattern = os.path.join(output_dir, '*_results.csv')
    csv_files = glob.glob(csv_pattern)
    
    if not csv_files:
        print(f"❌ 未找到CSV文件: {csv_pattern}")
        return None
    
    # 找到最新的文件
    latest_csv = max(csv_files, key=os.path.getctime)
    return latest_csv

def run_command(command, cwd, description, timeout=600):
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
    print_header("悉尼租房数据 - 快速ETL测试")
    print(f"🕐 开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("💡 此脚本跳过爬虫，直接使用现有CSV数据测试数据库更新")
    
    # 获取项目路径
    project_root = os.path.dirname(os.path.abspath(__file__))
    etl_dir = os.path.join(project_root, 'rentalAU_mcp', 'etl')
    
    print(f"📂 项目根目录: {project_root}")
    
    # 步骤1: 查找最新CSV文件
    print_step(1, "查找最新CSV数据文件")
    
    latest_csv = find_latest_csv()
    if not latest_csv:
        print("💔 未找到CSV文件，无法继续")
        return False
    
    # 获取文件信息
    file_size = os.path.getsize(latest_csv) / (1024 * 1024)  # MB
    mod_time = datetime.fromtimestamp(os.path.getmtime(latest_csv))
    
    print(f"✅ 找到最新CSV文件:")
    print(f"   📄 文件: {os.path.basename(latest_csv)}")
    print(f"   📍 路径: {latest_csv}")
    print(f"   📊 大小: {file_size:.1f} MB")
    print(f"   🕐 修改时间: {mod_time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 步骤2: 检查数据库更新脚本
    print_step(2, "检查数据库更新脚本")
    
    update_script = os.path.join(etl_dir, 'update_database.py')
    if not os.path.exists(update_script):
        print(f"❌ 数据更新脚本不存在: {update_script}")
        return False
    print(f"✅ 数据更新脚本: {update_script}")
    
    print("\n🎯 准备执行数据库更新...")
    input("按 Enter 键继续...")
    
    # 步骤3: 执行数据库更新
    print_step(3, "更新数据库 - 使用现有CSV数据")
    
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
    print_header("快速ETL测试完成")
    print("🎉 数据库更新成功完成！")
    print(f"🕐 结束时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"\n✨ 使用的数据文件: {os.path.basename(latest_csv)}")
    print("✨ 数据库现在包含最新的房源信息")
    print("✨ 您可以启动后端服务来查看结果")
    
    print("\n💡 提示:")
    print("   - 如需重新爬取数据，请等待完整爬虫执行完成")
    print("   - 此快速测试验证了数据库更新流程正常工作")
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️ 用户中断了执行")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ 意外错误: {e}")
        sys.exit(1)
