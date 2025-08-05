#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
增强的数据比对脚本 - 健壮的三态逻辑数据比较工具
解决数据类型不一致、标准化缺陷等问题
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Any, Dict, List, Tuple, Union
import json
from datetime import datetime

def normalize_field_value(value: Any, field_name: str) -> str:
    """
    根据字段类型进行适当的标准化
    
    Args:
        value: 任意类型的输入值
        field_name: 字段名称，用于确定处理策略
        
    Returns:
        str: 标准化后的值
    """
    # 处理 NaN 和 None
    if pd.isna(value) or value is None:
        return 'unknown'
    
    # 转换为字符串并清理
    str_value = str(value).strip().lower()
    
    # 空字符串处理
    if not str_value or str_value in ['', 'nan', 'none', 'null']:
        return 'unknown'
    
    # 特殊处理：枚举型字段，保持原值
    if field_name in ['furnishing_status', 'air_conditioning_type']:
        # 标准化枚举值
        if field_name == 'furnishing_status':
            if str_value in ['furnished', 'unfurnished', 'optional']:
                return str_value
            elif str_value == 'unknown':
                return 'unknown'
            else:
                return 'unknown'
        
        elif field_name == 'air_conditioning_type':
            if str_value in ['none', 'ducted', 'split', 'reverse_cycle', 'general']:
                return str_value
            elif str_value == 'unknown':
                return 'unknown'
            else:
                return 'unknown'
    
    # 布尔型字段（has_xxx）的三态映射
    if field_name.startswith('has_') or field_name in ['allows_pets', 'is_furnished']:
        # 明确的 "是" 模式
        yes_patterns = {'true', '1', 'yes', 'y'}
        
        # 明确的 "否" 模式  
        no_patterns = {'no', 'n'}
        
        # 直接匹配
        if str_value in yes_patterns:
            return 'yes'
        elif str_value in no_patterns:
            return 'no'
        elif str_value == 'false' or str_value == '0':
            return 'unknown'  # 关键：旧系统的 False 映射为 unknown
        elif str_value in ['yes', 'no', 'unknown']:
            return str_value
        
        # 数值处理
        try:
            num_value = float(str_value)
            if num_value == 1.0:
                return 'yes'
            elif num_value == 0.0:
                return 'unknown'  # 关键：旧系统的 False/0 映射为 unknown
            else:
                return 'unknown'
        except (ValueError, TypeError):
            pass
        
        # 默认为 unknown
        return 'unknown'
    
    # 其他字段，返回清理后的原值
    return str_value

def analyze_column_types(df: pd.DataFrame, columns: List[str]) -> Dict[str, Dict]:
    """
    分析列的数据类型分布，帮助诊断潜在问题
    """
    analysis = {}
    for col in columns:
        if col in df.columns:
            try:
                # 转换value_counts结果为可序列化的格式
                value_counts = df[col].value_counts(dropna=False)
                unique_values = {}
                
                for key, value in value_counts.items():
                    # 简化的key处理
                    try:
                        str_key = str(key) if key is not None else 'None'
                    except:
                        str_key = 'Unknown'
                    unique_values[str_key] = int(value)
                
                # 获取样本值
                sample_values = []
                try:
                    non_null_samples = df[col].dropna().head(5)
                    sample_values = [str(val) for val in non_null_samples]
                except:
                    sample_values = ['Error']
                
                analysis[col] = {
                    'dtype': str(df[col].dtype),
                    'unique_values': unique_values,
                    'null_count': int(df[col].isnull().sum()),
                    'sample_values': sample_values
                }
            except Exception as e:
                analysis[col] = {
                    'dtype': 'Error',
                    'unique_values': {'Error': str(e)},
                    'null_count': 0,
                    'sample_values': ['Error']
                }
    return analysis

def enhanced_compare_feature_extraction(
    old_file_path: str,
    new_file_path: str,
    id_column: str,
    feature_columns: List[str],
    output_dir: str = 'comparison_output',
    generate_detailed_analysis: bool = True
) -> Dict[str, Any]:
    """
    增强的特征提取结果比较函数
    
    Returns:
        Dict: 包含比较结果和统计信息的字典
    """
    print("🚀 开始增强的数据比对分析...")
    
    # 创建输出目录
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    results = {
        'timestamp': datetime.now().isoformat(),
        'files_compared': {'old': old_file_path, 'new': new_file_path},
        'statistics': {},
        'errors': []
    }
    
    try:
        # 1. 读取数据
        print(f"📁 读取旧数据: {old_file_path}")
        df_old = pd.read_csv(old_file_path) if old_file_path.endswith('.csv') else pd.read_excel(old_file_path)
        
        print(f"📁 读取新数据: {new_file_path}")
        df_new = pd.read_csv(new_file_path) if new_file_path.endswith('.csv') else pd.read_excel(new_file_path)
        
        # 2. 数据类型分析（可选）
        if generate_detailed_analysis:
            print("🔍 分析数据类型分布...")
            old_analysis = analyze_column_types(df_old, feature_columns)
            new_analysis = analyze_column_types(df_new, feature_columns)
            
            # 保存分析结果
            with open(output_path / 'data_type_analysis.json', 'w', encoding='utf-8') as f:
                json.dump({
                    'old_data_analysis': old_analysis,
                    'new_data_analysis': new_analysis
                }, f, indent=2, ensure_ascii=False)
        
        # 3. 标准化数据
        print("🔄 标准化旧数据到三态逻辑...")
        df_old_normalized = df_old.copy()
        for col in feature_columns:
            if col in df_old_normalized.columns:
                df_old_normalized[col] = df_old_normalized[col].apply(
                    lambda x: normalize_field_value(x, col)
                )
        
        print("🔄 标准化新数据到三态逻辑...")
        df_new_normalized = df_new.copy()
        for col in feature_columns:
            if col in df_new_normalized.columns:
                df_new_normalized[col] = df_new_normalized[col].apply(
                    lambda x: normalize_field_value(x, col)
                )
        
        # 4. 合并数据
        print(f"🔗 根据 '{id_column}' 合并数据...")
        old_cols = [id_column] + [col for col in feature_columns if col in df_old_normalized.columns]
        new_cols = [id_column] + [col for col in feature_columns if col in df_new_normalized.columns]
        
        merged_df = pd.merge(
            df_old_normalized[old_cols],
            df_new_normalized[new_cols],
            on=id_column,
            suffixes=('_old', '_new'),
            how='inner'
        )
        
        if merged_df.empty:
            raise ValueError("合并后的数据为空，请检查ID列匹配")
        
        print(f"✅ 成功合并 {len(merged_df)} 条记录")
        results['statistics']['total_merged_records'] = len(merged_df)
        
        # 5. 差异分析
        print("📊 进行详细的差异分析...")
        differences = []
        feature_change_stats = {}
        
        for _, row in merged_df.iterrows():
            record_diff = {id_column: row[id_column]}
            has_changes = False
            
            # 添加 URL（如果存在）
            if 'property_url' in df_new.columns:
                url_match = df_new[df_new[id_column] == row[id_column]]
                if not url_match.empty:
                    record_diff['property_url'] = url_match['property_url'].iloc[0]
            
            for feature in feature_columns:
                old_col = f"{feature}_old"
                new_col = f"{feature}_new"
                
                if old_col in row.index and new_col in row.index:
                    old_val = row[old_col]
                    new_val = row[new_col]
                    
                    if old_val != new_val:
                        has_changes = True
                        record_diff[f"{feature}_old"] = old_val
                        record_diff[f"{feature}_new"] = new_val
                        record_diff[f"{feature}_change"] = f"{old_val}→{new_val}"
                        
                        # 统计变化模式
                        if feature not in feature_change_stats:
                            feature_change_stats[feature] = {}
                        
                        change_pattern = f"{old_val}→{new_val}"
                        feature_change_stats[feature][change_pattern] = \
                            feature_change_stats[feature].get(change_pattern, 0) + 1
            
            if has_changes:
                differences.append(record_diff)
        
        # 6. 生成统计报告
        print("\n" + "="*60)
        print("📈 详细统计报告")
        print("="*60)
        
        total_records = len(merged_df)
        changed_records = len(differences)
        unchanged_records = total_records - changed_records
        
        print(f"📊 总体统计:")
        print(f"  • 总记录数: {total_records:,}")
        print(f"  • 发生变化: {changed_records:,} ({changed_records/total_records*100:.1f}%)")
        print(f"  • 保持不变: {unchanged_records:,} ({unchanged_records/total_records*100:.1f}%)")
        
        results['statistics'].update({
            'total_records': total_records,
            'changed_records': changed_records,
            'unchanged_records': unchanged_records,
            'change_percentage': changed_records/total_records*100
        })
        
        # 特征级统计
        print(f"\n📋 按特征分类的变化统计:")
        feature_stats = {}
        for feature, changes in feature_change_stats.items():
            total_changes = sum(changes.values())
            feature_stats[feature] = {
                'total_changes': total_changes,
                'change_patterns': changes,
                'change_percentage': (total_changes / total_records) * 100
            }
            
            print(f"\n--- {feature} ---")
            print(f"  变化记录数: {total_changes} ({total_changes/total_records*100:.1f}%)")
            
            # 按频率排序显示变化模式
            sorted_patterns = sorted(changes.items(), key=lambda x: x[1], reverse=True)
            for pattern, count in sorted_patterns[:5]:  # 只显示前5个最常见的变化
                print(f"    {pattern}: {count} ({count/total_changes*100:.1f}%)")
            
            if len(sorted_patterns) > 5:
                print(f"    ... 还有 {len(sorted_patterns)-5} 种其他变化模式")
        
        results['feature_statistics'] = feature_stats
        
        # 7. 质量改进分析
        print(f"\n🎯 数据质量改进分析:")
        quality_improvements = analyze_quality_improvements(feature_change_stats)
        results['quality_analysis'] = quality_improvements
        
        for improvement_type, details in quality_improvements.items():
            if details['count'] > 0:
                print(f"  • {improvement_type}: {details['count']} 项改进 ({details['percentage']:.1f}%)")
        
        # 8. 保存详细报告
        if differences:
            diff_df = pd.DataFrame(differences)
            
            # 重新排列列的顺序
            priority_cols = [id_column, 'property_url']
            other_cols = sorted([col for col in diff_df.columns if col not in priority_cols])
            final_cols = [col for col in priority_cols if col in diff_df.columns] + other_cols
            diff_df = diff_df[final_cols]
            
            report_path = output_path / f"detailed_comparison_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            diff_df.to_csv(report_path, index=False, encoding='utf-8-sig')
            print(f"\n💾 详细差异报告已保存: {report_path}")
            
            # 保存汇总统计
            summary_path = output_path / f"comparison_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(summary_path, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, ensure_ascii=False)
            print(f"💾 统计汇总已保存: {summary_path}")
        else:
            print("\n✅ 未发现任何差异！数据完全一致。")
        
        return results
        
    except Exception as e:
        error_msg = f"比对过程中发生错误: {str(e)}"
        print(f"❌ {error_msg}")
        results['errors'].append(error_msg)
        return results

def analyze_quality_improvements(feature_change_stats: Dict) -> Dict:
    """
    分析数据质量改进情况
    """
    improvements = {
        'unknown_to_specific': {'count': 0, 'details': []},
        'false_to_unknown': {'count': 0, 'details': []},
        'new_information_discovered': {'count': 0, 'details': []},
        'corrections_made': {'count': 0, 'details': []}
    }
    
    total_changes = 0
    
    for feature, changes in feature_change_stats.items():
        for pattern, count in changes.items():
            total_changes += count
            
            if 'unknown→yes' in pattern or 'unknown→no' in pattern:
                improvements['unknown_to_specific']['count'] += count
                improvements['unknown_to_specific']['details'].append({
                    'feature': feature, 'pattern': pattern, 'count': count
                })
            
            elif pattern.startswith('unknown→') and not pattern.endswith('→unknown'):
                improvements['new_information_discovered']['count'] += count
                improvements['new_information_discovered']['details'].append({
                    'feature': feature, 'pattern': pattern, 'count': count
                })
            
            elif '→unknown' in pattern and not pattern.startswith('unknown'):
                improvements['false_to_unknown']['count'] += count
                improvements['false_to_unknown']['details'].append({
                    'feature': feature, 'pattern': pattern, 'count': count
                })
            
            else:
                improvements['corrections_made']['count'] += count
                improvements['corrections_made']['details'].append({
                    'feature': feature, 'pattern': pattern, 'count': count
                })
    
    # 计算百分比
    for improvement_type in improvements:
        if total_changes > 0:
            improvements[improvement_type]['percentage'] = \
                (improvements[improvement_type]['count'] / total_changes) * 100
        else:
            improvements[improvement_type]['percentage'] = 0.0
    
    return improvements

# 测试和验证函数
def validate_normalization_function():
    """
    验证标准化函数的正确性
    """
    print("🧪 测试数据标准化函数...")
    
    test_cases = [
        # 布尔字段测试用例 (输入值, 期望输出, 描述)
        (True, 'yes', '布尔值 True'),
        (False, 'unknown', '布尔值 False - 应映射为unknown'),
        ('True', 'yes', '字符串 True'),
        ('False', 'unknown', '字符串 False'),
        (1, 'yes', '数值 1'),
        (0, 'unknown', '数值 0'),
        ('yes', 'yes', '字符串 yes'),
        ('no', 'no', '字符串 no'),
        ('unknown', 'unknown', '字符串 unknown'),
        (np.nan, 'unknown', 'NaN 值'),
        (None, 'unknown', 'None 值'),
        ('', 'unknown', '空字符串'),
        ('   ', 'unknown', '空白字符串'),
    ]
    
    all_passed = True
    for input_val, expected, description in test_cases:
        # 为测试目的，使用默认的布尔字段处理逻辑
        result = normalize_field_value(input_val, 'has_test')
        if result == expected:
            print(f"✅ {description}: {input_val} → {result}")
        else:
            print(f"❌ {description}: {input_val} → {result} (期望: {expected})")
            all_passed = False
    
    if all_passed:
        print("\n🎉 所有测试用例通过！标准化函数工作正常。")
    else:
        print("\n⚠️ 部分测试用例失败，请检查标准化函数。")
    
    return all_passed

if __name__ == '__main__':
    # 首先验证标准化函数
    validate_normalization_function()
    
    print("\n" + "="*60)
    
    # 配置文件路径
    OLD_DATA_FILE = r"D:\WEB-sydney-rental-hub\crawler\output\20250805_114044_Zetland_150properties.xlsx"
    NEW_DATA_FILE = r"D:\WEB-sydney-rental-hub\crawler\output\20250805_004531_Zetland_154properties.xlsx"
    
    UNIQUE_ID_COLUMN = "listing_id"
    
    FEATURE_COLUMNS_TO_COMPARE = [
        'furnishing_status',
        'has_air_conditioning', 
        'air_conditioning_type',
        'has_wardrobes',
        'has_laundry',
        'has_dishwasher',
        'has_parking',
        'has_gas_cooking',
        'has_heating',
        'has_intercom',
        'has_lift',
        'has_gym',
        'has_pool',
        'has_garbage_disposal',
        'has_study',
        'has_balcony',
        'has_city_view',
        'has_water_view',
        'allows_pets'
    ]
    
    # 执行比较
    if Path(OLD_DATA_FILE).exists() and Path(NEW_DATA_FILE).exists():
        results = enhanced_compare_feature_extraction(
            old_file_path=OLD_DATA_FILE,
            new_file_path=NEW_DATA_FILE,
            id_column=UNIQUE_ID_COLUMN,
            feature_columns=FEATURE_COLUMNS_TO_COMPARE,
            output_dir='enhanced_comparison_output'
        )
    else:
        print("⚠️ 请检查文件路径是否正确")
