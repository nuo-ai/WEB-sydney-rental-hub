#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
数据迁移脚本：将原有的布尔值数据转换为三态字符串值
用于升级现有数据库/CSV文件到新的三态逻辑格式
"""

import pandas as pd
from pathlib import Path

def migrate_boolean_to_ternary(input_file: str, output_file: str):
    """
    将布尔值特征字段迁移为三态字符串值
    """
    
    # 需要迁移的布尔字段列表
    boolean_fields = [
        'is_furnished', 'has_air_conditioning', 'has_wardrobes', 'has_laundry',
        'has_dishwasher', 'has_parking', 'has_gas_cooking', 'has_heating',
        'has_intercom', 'has_lift', 'has_gym', 'has_pool', 'has_garbage_disposal',
        'has_study', 'has_balcony', 'has_city_view', 'has_water_view', 'allows_pets'
    ]
    
    # 读取原始数据
    df = pd.read_csv(input_file) if input_file.endswith('.csv') else pd.read_excel(input_file)
    
    print(f"📁 读取文件: {input_file}")
    print(f"📊 原始数据行数: {len(df)}")
    
    # 转换布尔字段
    for field in boolean_fields:
        if field in df.columns:
            # True -> 'yes', False -> 'unknown' (因为原来的False可能是误判)
            df[field] = df[field].map({True: 'yes', False: 'unknown'})
            print(f"✅ 转换字段: {field}")
    
    # 特殊处理furnishing_status
    if 'furnishing_status' in df.columns:
        # 如果已经是字符串，保持不变；如果是布尔值，需要转换
        if df['furnishing_status'].dtype == 'bool':
            df['furnishing_status'] = df['furnishing_status'].map({
                True: 'furnished', 
                False: 'unknown'  # 保守处理，避免误判
            })
    
    # 保存迁移后的数据
    output_path = Path(output_file)
    if output_path.suffix == '.csv':
        df.to_csv(output_file, index=False, encoding='utf-8-sig')
    else:
        df.to_excel(output_file, index=False, engine='openpyxl')
    
    print(f"💾 保存迁移后文件: {output_file}")
    print(f"✅ 迁移完成!")

if __name__ == "__main__":
    # 示例用法
    input_file = "output/old_format_data.xlsx"
    output_file = "output/migrated_ternary_data.xlsx"
    
    migrate_boolean_to_ternary(input_file, output_file)
