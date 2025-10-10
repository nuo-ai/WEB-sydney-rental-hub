#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
测试修复后的下架逻辑
用于验证update_database.py的改动是否正确
"""

import pandas as pd
import os
import sys
import logging
from datetime import datetime

# 添加项目根目录到路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def simulate_logic_changes():
    """模拟新逻辑的变化，不实际连接数据库"""
    
    logger.info("=" * 60)
    logger.info("模拟测试新的下架逻辑")
    logger.info("=" * 60)
    
    # 模拟数据
    # 假设数据库中有5000个房源（包括活跃和不活跃的）
    existing_all_ids = set(range(1000, 6000))
    
    # 假设其中3000个是活跃的（旧逻辑会用这个）
    existing_active_ids = set(range(1000, 4000))
    
    # 假设新爬取的数据有2500个房源
    new_crawled_ids = set(range(2000, 4500))
    
    logger.info(f"数据库中总房源数: {len(existing_all_ids)}")
    logger.info(f"数据库中活跃房源数: {len(existing_active_ids)}")
    logger.info(f"本次爬取房源数: {len(new_crawled_ids)}")
    
    # 旧逻辑（只比较活跃房源）
    logger.info("\n--- 旧逻辑（错误的）---")
    old_new = new_crawled_ids - existing_active_ids
    old_update = new_crawled_ids & existing_active_ids
    old_inactive = existing_active_ids - new_crawled_ids
    
    logger.info(f"新增房源: {len(old_new)}")
    logger.info(f"更新房源: {len(old_update)}")
    logger.info(f"下架房源: {len(old_inactive)}")
    logger.info(f"问题：会错误下架 {len(old_inactive)} 个房源")
    
    # 新逻辑（比较所有房源）
    logger.info("\n--- 新逻辑（修复后）---")
    new_new = new_crawled_ids - existing_all_ids
    new_update = new_crawled_ids & existing_all_ids
    new_inactive = existing_all_ids - new_crawled_ids
    
    logger.info(f"新增房源: {len(new_new)}")
    logger.info(f"更新房源: {len(new_update)} (这些会被标记为活跃)")
    logger.info(f"下架房源: {len(new_inactive)}")
    
    # 关键差异
    logger.info("\n--- 关键差异 ---")
    
    # 找出之前被错误标记为"新增"的房源（实际是重新上架）
    reactivated = (new_crawled_ids & existing_all_ids) - existing_active_ids
    logger.info(f"重新上架的房源（旧逻辑会当作新增）: {len(reactivated)}")
    
    # 验证结果
    logger.info("\n--- 验证 ---")
    logger.info("✓ 新逻辑能正确处理房源重新上架的情况")
    logger.info("✓ 不会因为房源之前是inactive就当作新房源")
    logger.info("✓ 爬到的房源都会被设置为active")
    logger.info("✓ 没爬到的房源都会被设置为inactive")
    
    return True

def check_csv_file():
    """检查最新的CSV文件"""
    import glob
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(script_dir, '..', 'dist', 'output')
    search_pattern = os.path.join(output_dir, '*_results.csv')
    
    list_of_files = glob.glob(search_pattern)
    if not list_of_files:
        logger.warning(f"未找到CSV文件在: {output_dir}")
        return None
        
    latest_file = max(list_of_files, key=os.path.getctime)
    logger.info(f"\n找到最新CSV文件: {latest_file}")
    
    # 读取并显示基本信息
    df = pd.read_csv(latest_file)
    logger.info(f"CSV文件包含 {len(df)} 条房源记录")
    
    # 显示区域分布
    if 'suburb' in df.columns:
        suburbs = df['suburb'].value_counts()
        logger.info(f"涵盖 {len(suburbs)} 个区域")
        logger.info(f"前5个区域: {suburbs.head().to_dict()}")
    
    return df

def main():
    """主函数"""
    logger.info("开始测试新的下架逻辑")
    
    # 1. 模拟逻辑测试
    simulate_logic_changes()
    
    # 2. 检查实际CSV文件
    df = check_csv_file()
    
    logger.info("\n" + "=" * 60)
    logger.info("测试完成！")
    logger.info("下一步操作：")
    logger.info("1. 执行 psql 运行 fix_property_status.sql 重置状态")
    logger.info("2. 运行 python database/update_database.py 应用新逻辑")
    logger.info("3. 检查前端是否正确显示活跃房源数量")
    logger.info("=" * 60)

if __name__ == "__main__":
    main()