#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
三态逻辑升级效果全面分析脚本
对比升级前后的数据质量，验证三态逻辑的实际效果
"""

import pandas as pd
import numpy as np
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Tuple

class UpgradeAnalyzer:
    def __init__(self, old_file_path: str, new_file_path: str):
        """
        初始化分析器
        
        Args:
            old_file_path: 升级前的数据文件路径
            new_file_path: 升级后的数据文件路径
        """
        self.old_file_path = Path(old_file_path)
        self.new_file_path = Path(new_file_path)
        self.old_data = None
        self.new_data = None
        
        # 重点分析的特征（基于用户的勾选）
        self.focus_features = [
            'furnishing_status',  # 家具 ✔️
            'has_air_conditioning',  # 空调 ✔️
            'air_conditioning_type',  # 空调类型
            'has_gas_cooking',  # 煤气 ✔️
            'has_internal_laundry'  # 内部洗衣房 ✔️
        ]
        
        # 所有可能的布尔特征
        self.boolean_features = [
            'has_pool', 'has_gym', 'has_parking', 'allows_pets',
            'has_dishwasher', 'has_air_conditioning', 'has_gas_cooking',
            'has_built_in_wardrobe', 'has_balcony', 'has_study',
            'has_ensuite', 'has_internal_laundry', 'has_outdoor_space',
            'has_intercom', 'has_lift', 'has_heating'
        ]
        
        # 报告数据
        self.analysis_results = {}
        
    def load_data(self):
        """加载新旧数据文件"""
        print("📁 加载数据文件...")
        
        try:
            self.old_data = pd.read_excel(self.old_file_path)
            print(f"   ✅ 旧数据加载成功: {len(self.old_data)} 条记录")
        except Exception as e:
            print(f"   ❌ 旧数据加载失败: {e}")
            return False
            
        try:
            self.new_data = pd.read_excel(self.new_file_path)
            print(f"   ✅ 新数据加载成功: {len(self.new_data)} 条记录")
        except Exception as e:
            print(f"   ❌ 新数据加载失败: {e}")
            return False
            
        return True
    
    def analyze_data_structure(self):
        """分析数据结构变化"""
        print("\n🔍 分析数据结构变化...")
        
        if self.old_data is None or self.new_data is None:
            print("   ❌ 数据未正确加载，无法进行结构分析")
            return None
        
        # 检查字段变化
        old_columns = set(self.old_data.columns)
        new_columns = set(self.new_data.columns)
        
        common_columns = old_columns & new_columns
        added_columns = new_columns - old_columns
        removed_columns = old_columns - new_columns
        
        structure_analysis = {
            'old_record_count': len(self.old_data),
            'new_record_count': len(self.new_data),
            'common_columns_count': len(common_columns),
            'added_columns': list(added_columns),
            'removed_columns': list(removed_columns),
            'total_columns_old': len(old_columns),
            'total_columns_new': len(new_columns)
        }
        
        print(f"   📊 旧数据: {structure_analysis['old_record_count']} 条记录, {structure_analysis['total_columns_old']} 个字段")
        print(f"   📊 新数据: {structure_analysis['new_record_count']} 条记录, {structure_analysis['total_columns_new']} 个字段")
        print(f"   📊 共同字段: {structure_analysis['common_columns_count']} 个")
        
        if added_columns:
            print(f"   ➕ 新增字段: {added_columns}")
        if removed_columns:
            print(f"   ➖ 删除字段: {removed_columns}")
            
        self.analysis_results['structure'] = structure_analysis
        return structure_analysis
    
    def analyze_data_types(self):
        """分析数据类型变化"""
        print("\n🔬 分析数据类型变化...")
        
        if self.old_data is None or self.new_data is None:
            print("   ❌ 数据未正确加载，无法进行类型分析")
            return None
        
        type_changes = {}
        
        for feature in self.focus_features:
            if feature in self.old_data.columns and feature in self.new_data.columns:
                old_type = str(self.old_data[feature].dtype)
                new_type = str(self.new_data[feature].dtype)
                
                old_unique = sorted(list(self.old_data[feature].dropna().unique()))
                new_unique = sorted(list(self.new_data[feature].dropna().unique()))
                
                type_changes[feature] = {
                    'old_type': old_type,
                    'new_type': new_type,
                    'old_unique_values': old_unique,
                    'new_unique_values': new_unique,
                    'type_changed': old_type != new_type
                }
                
                print(f"   📋 {feature}:")
                print(f"      旧类型: {old_type} → 新类型: {new_type}")
                print(f"      旧值: {old_unique}")
                print(f"      新值: {new_unique}")
                print()
        
        self.analysis_results['type_changes'] = type_changes
        return type_changes
    
    def analyze_tristate_logic(self):
        """分析三态逻辑的实现效果"""
        print("\n🎯 分析三态逻辑实现效果...")
        
        if self.new_data is None:
            print("   ❌ 新数据未正确加载，无法进行三态逻辑分析")
            return None
        
        tristate_analysis = {}
        
        for feature in self.boolean_features:
            if feature in self.new_data.columns:
                values = self.new_data[feature].dropna()
                value_counts = values.value_counts()
                
                # 检查是否为三态逻辑
                is_tristate = all(val in ['yes', 'no', 'unknown'] for val in values.unique() if pd.notna(val))
                
                tristate_analysis[feature] = {
                    'is_tristate': is_tristate,
                    'value_counts': value_counts.to_dict(),
                    'total_non_null': len(values),
                    'unknown_ratio': value_counts.get('unknown', 0) / len(values) if len(values) > 0 else 0,
                    'yes_ratio': value_counts.get('yes', 0) / len(values) if len(values) > 0 else 0,
                    'no_ratio': value_counts.get('no', 0) / len(values) if len(values) > 0 else 0
                }
                
                if is_tristate:
                    print(f"   ✅ {feature}: 三态逻辑 ✓")
                    print(f"      📊 分布: yes={tristate_analysis[feature]['yes_ratio']:.1%}, "
                          f"no={tristate_analysis[feature]['no_ratio']:.1%}, "
                          f"unknown={tristate_analysis[feature]['unknown_ratio']:.1%}")
                else:
                    print(f"   ❌ {feature}: 非三态逻辑 ❌")
                    print(f"      📊 值: {value_counts.to_dict()}")
        
        self.analysis_results['tristate'] = tristate_analysis
        return tristate_analysis
    
    def compare_feature_distributions(self):
        """对比重点特征的分布变化"""
        print("\n📊 对比重点特征分布变化...")
        
        if self.old_data is None or self.new_data is None:
            print("   ❌ 数据未正确加载，无法进行分布对比")
            return None
        
        distribution_comparison = {}
        
        for feature in self.focus_features:
            if feature in self.old_data.columns and feature in self.new_data.columns:
                old_dist = self.old_data[feature].value_counts(normalize=True)
                new_dist = self.new_data[feature].value_counts(normalize=True)
                
                distribution_comparison[feature] = {
                    'old_distribution': old_dist.to_dict(),
                    'new_distribution': new_dist.to_dict(),
                    'old_null_ratio': self.old_data[feature].isnull().sum() / len(self.old_data),
                    'new_null_ratio': self.new_data[feature].isnull().sum() / len(self.new_data)
                }
                
                print(f"   🔍 {feature}:")
                print(f"      旧分布: {old_dist.to_dict()}")
                print(f"      新分布: {new_dist.to_dict()}")
                print(f"      空值比例: {distribution_comparison[feature]['old_null_ratio']:.1%} → {distribution_comparison[feature]['new_null_ratio']:.1%}")
                print()
        
        self.analysis_results['distribution_comparison'] = distribution_comparison
        return distribution_comparison
    
    def analyze_information_gain(self):
        """分析信息增益：三态逻辑相比二元逻辑的信息量提升"""
        print("\n📈 分析信息增益...")
        
        if self.old_data is None or self.new_data is None:
            print("   ❌ 数据未正确加载，无法进行信息增益分析")
            return None
        
        information_gain = {}
        
        for feature in self.focus_features:
            if feature in self.old_data.columns and feature in self.new_data.columns:
                # 计算新数据中unknown的比例
                new_values = self.new_data[feature].dropna()
                unknown_count = sum(1 for val in new_values if val == 'unknown')
                unknown_ratio = unknown_count / len(new_values) if len(new_values) > 0 else 0
                
                # 在旧数据中，这些unknown值可能被错误地标记为False
                old_false_count = sum(1 for val in self.old_data[feature].dropna() if val == False)
                old_false_ratio = old_false_count / len(self.old_data[feature].dropna()) if len(self.old_data[feature].dropna()) > 0 else 0
                
                information_gain[feature] = {
                    'unknown_count_new': unknown_count,
                    'unknown_ratio_new': unknown_ratio,
                    'false_count_old': old_false_count,
                    'false_ratio_old': old_false_ratio,
                    'potential_misclassification_reduction': unknown_ratio  # 这部分原本可能被误分类
                }
                
                print(f"   📊 {feature}:")
                print(f"      新数据中unknown比例: {unknown_ratio:.1%}")
                print(f"      旧数据中False比例: {old_false_ratio:.1%}")
                print(f"      潜在误分类减少: {unknown_ratio:.1%}")
                print()
        
        self.analysis_results['information_gain'] = information_gain
        return information_gain
    
    def find_sample_improvements(self, sample_size: int = 10):
        """寻找具体的改进示例"""
        print(f"\n🔍 寻找具体改进示例（样本大小: {sample_size}）...")
        
        if self.old_data is None or self.new_data is None:
            print("   ❌ 数据未正确加载，无法寻找改进示例")
            return None
        
        improvements = {}
        
        # 找到两个数据集中共同的房源（基于listing_id或地址）
        common_records = []
        if 'listing_id' in self.old_data.columns and 'listing_id' in self.new_data.columns:
            common_ids = set(self.old_data['listing_id']) & set(self.new_data['listing_id'])
            common_records = list(common_ids)[:sample_size]
        
        for i, record_id in enumerate(common_records):
            old_record = self.old_data[self.old_data['listing_id'] == record_id].iloc[0]
            new_record = self.new_data[self.new_data['listing_id'] == record_id].iloc[0]
            
            record_improvements = {}
            
            for feature in self.focus_features:
                if feature in self.old_data.columns and feature in self.new_data.columns:
                    old_value = old_record[feature]
                    new_value = new_record[feature]
                    
                    # 特别关注从False变为unknown的情况（可能的误分类纠正）
                    if old_value == False and new_value == 'unknown':
                        record_improvements[feature] = {
                            'old_value': old_value,
                            'new_value': new_value,
                            'improvement_type': 'false_to_unknown',
                            'description': '从错误的"否定"改为"信息不确定"'
                        }
                    elif old_value != new_value:
                        record_improvements[feature] = {
                            'old_value': old_value,
                            'new_value': new_value,
                            'improvement_type': 'value_change',
                            'description': f'值变更: {old_value} → {new_value}'
                        }
            
            if record_improvements:
                improvements[record_id] = {
                    'record_info': {
                        'address': new_record.get('address', 'N/A'),
                        'property_headline': new_record.get('property_headline', 'N/A')[:100] + '...'
                    },
                    'improvements': record_improvements
                }
        
        print(f"   🎯 找到 {len(improvements)} 个有改进的记录")
        
        for record_id, data in list(improvements.items())[:5]:  # 只显示前5个
            print(f"\n   📋 记录 {record_id}:")
            print(f"      地址: {data['record_info']['address']}")
            print(f"      标题: {data['record_info']['property_headline']}")
            
            for feature, improvement in data['improvements'].items():
                print(f"      🔄 {feature}: {improvement['old_value']} → {improvement['new_value']} ({improvement['description']})")
        
        self.analysis_results['sample_improvements'] = improvements
        return improvements
    
    def generate_summary_statistics(self):
        """生成汇总统计"""
        print("\n📋 生成汇总统计...")
        
        summary = {
            'analysis_timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'data_files': {
                'old_file': str(self.old_file_path),
                'new_file': str(self.new_file_path)
            },
            'focus_features': self.focus_features,
            'key_findings': {}
        }
        
        # 统计三态逻辑实现情况
        tristate_features = 0
        for feature, analysis in self.analysis_results.get('tristate', {}).items():
            if analysis.get('is_tristate', False):
                tristate_features += 1
        
        summary['key_findings']['tristate_implementation'] = {
            'total_analyzed_features': len(self.boolean_features),
            'tristate_features_count': tristate_features,
            'tristate_success_rate': tristate_features / len(self.boolean_features) if self.boolean_features else 0
        }
        
        # 统计信息增益
        total_unknown_ratio = 0
        analyzed_features = 0
        for feature, analysis in self.analysis_results.get('information_gain', {}).items():
            total_unknown_ratio += analysis.get('unknown_ratio_new', 0)
            analyzed_features += 1
        
        average_unknown_ratio = total_unknown_ratio / analyzed_features if analyzed_features > 0 else 0
        
        summary['key_findings']['information_gain'] = {
            'average_unknown_ratio': average_unknown_ratio,
            'estimated_misclassification_reduction': average_unknown_ratio
        }
        
        # 记录改进样本数量
        improvements_count = len(self.analysis_results.get('sample_improvements', {}))
        summary['key_findings']['sample_improvements'] = {
            'improved_records_found': improvements_count
        }
        
        print(f"   📊 三态逻辑实现率: {summary['key_findings']['tristate_implementation']['tristate_success_rate']:.1%}")
        print(f"   📊 平均未知信息比例: {average_unknown_ratio:.1%}")
        print(f"   📊 找到改进记录: {improvements_count} 个")
        
        self.analysis_results['summary'] = summary
        return summary
    
    def save_results(self, output_dir: str = "upgrade_analysis_output"):
        """保存分析结果"""
        print(f"\n💾 保存分析结果到 {output_dir}...")
        
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # 保存完整的JSON报告
        json_file = output_path / f"upgrade_analysis_report_{timestamp}.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(self.analysis_results, f, ensure_ascii=False, indent=2, default=str)
        
        print(f"   ✅ JSON报告已保存: {json_file}")
        
        # 生成简化的markdown报告
        md_file = output_path / f"upgrade_analysis_summary_{timestamp}.md"
        self._generate_markdown_report(md_file)
        
        print(f"   ✅ Markdown摘要已保存: {md_file}")
        
        return json_file, md_file
    
    def _generate_markdown_report(self, md_file: Path):
        """生成Markdown格式的报告摘要"""
        summary = self.analysis_results.get('summary', {})
        
        with open(md_file, 'w', encoding='utf-8') as f:
            f.write("# 三态逻辑升级效果分析报告\n\n")
            f.write(f"**分析时间**: {summary.get('analysis_timestamp', 'N/A')}\n\n")
            
            f.write("## 数据文件\n\n")
            f.write(f"- **旧数据**: {summary.get('data_files', {}).get('old_file', 'N/A')}\n")
            f.write(f"- **新数据**: {summary.get('data_files', {}).get('new_file', 'N/A')}\n\n")
            
            f.write("## 关键发现\n\n")
            
            # 三态逻辑实现情况
            tristate = summary.get('key_findings', {}).get('tristate_implementation', {})
            f.write(f"### 三态逻辑实现\n")
            f.write(f"- 分析特征数量: {tristate.get('total_analyzed_features', 0)}\n")
            f.write(f"- 成功实现三态逻辑: {tristate.get('tristate_features_count', 0)}\n")
            f.write(f"- 实现成功率: {tristate.get('tristate_success_rate', 0):.1%}\n\n")
            
            # 信息增益
            info_gain = summary.get('key_findings', {}).get('information_gain', {})
            f.write(f"### 信息质量提升\n")
            f.write(f"- 平均未知信息比例: {info_gain.get('average_unknown_ratio', 0):.1%}\n")
            f.write(f"- 估计误分类减少: {info_gain.get('estimated_misclassification_reduction', 0):.1%}\n\n")
            
            # 改进示例
            improvements = summary.get('key_findings', {}).get('sample_improvements', {})
            f.write(f"### 改进示例\n")
            f.write(f"- 发现改进记录: {improvements.get('improved_records_found', 0)} 个\n\n")
            
            f.write("## 结论\n\n")
            
            success_rate = tristate.get('tristate_success_rate', 0)
            if success_rate >= 0.8:
                f.write("✅ **升级成功**: 三态逻辑实现率超过80%，数据质量显著提升。\n")
            elif success_rate >= 0.5:
                f.write("⚠️ **部分成功**: 三态逻辑部分实现，建议进一步优化。\n")
            else:
                f.write("❌ **需要改进**: 三态逻辑实现率较低，需要检查配置。\n")
    
    def run_full_analysis(self):
        """运行完整分析"""
        print("🚀 开始三态逻辑升级效果全面分析")
        print("=" * 60)
        
        # 加载数据
        if not self.load_data():
            return None
        
        # 运行各项分析
        self.analyze_data_structure()
        self.analyze_data_types()
        self.analyze_tristate_logic()
        self.compare_feature_distributions()
        self.analyze_information_gain()
        self.find_sample_improvements()
        self.generate_summary_statistics()
        
        # 保存结果
        json_file, md_file = self.save_results()
        
        print("\n" + "=" * 60)
        print("🎉 分析完成!")
        print(f"📄 详细报告: {json_file}")
        print(f"📝 摘要报告: {md_file}")
        
        return self.analysis_results


def main():
    """主函数"""
    # 文件路径
    old_file = r"D:\WEB-sydney-rental-hub\crawler\output\20250805_004531_Zetland_154properties.xlsx"
    new_file = r"D:\WEB-sydney-rental-hub\crawler\output\20250805_124003_Zetland_149properties.xlsx"
    
    # 创建分析器并运行分析
    analyzer = UpgradeAnalyzer(old_file, new_file)
    results = analyzer.run_full_analysis()
    
    return results


if __name__ == "__main__":
    results = main()
