#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
测试脚本 - 比较原始版本和增强版本的特征提取差异
"""

import json
import sys
from pathlib import Path
from datetime import datetime
import pandas as pd

# 添加当前目录到Python路径
sys.path.insert(0, str(Path(__file__).parent))

# 导入两个版本的特征提取器
from enhanced_feature_extractor import EnhancedFeatureExtractor, create_enhanced_property_features_class
from v5_furniture import (
    FeatureExtractor as OriginalFeatureExtractor, 
    create_property_features_class, 
    FEATURES_CONFIG,
    FURNITURE_KEYWORDS,
    AIRCON_KEYWORDS
)

def create_test_data():
    """创建测试数据模拟真实房源信息"""
    return [
        {
            "id": "test_001",
            "json_data": {
                "structuredFeatures": [
                    {"name": "Air Conditioning"},
                    {"name": "Built-in Wardrobes"}
                ]
            },
            "headline": "Modern 2BR Apartment with Pool and Gym",
            "description": "Beautiful modern apartment featuring spacious living areas. Located in a premium building with excellent facilities.",
            "feature_list": ["Central heating", "Built-in wardrobes", "Secure parking"]
        },
        {
            "id": "test_002", 
            "json_data": {
                "structuredFeatures": [
                    {"name": "Balcony"},
                    {"name": "Dishwasher"}
                ]
            },
            "headline": "Luxury Studio with City Views",
            "description": "Elegant studio apartment with panoramic city views. Modern kitchen with quality appliances including dishwasher.",
            "feature_list": ["City views", "Air conditioning", "Modern kitchen"]
        },
        {
            "id": "test_003",
            "json_data": {
                "structuredFeatures": [
                    {"name": "Swimming Pool"},
                    {"name": "Gym"}
                ]
            },
            "headline": "Family Home in Quiet Street",
            "description": "Spacious family home with large backyard. The property features gas cooking and plenty of storage space.",
            "feature_list": ["Gas cooking", "Large backyard", "Storage"]
        },
        {
            "id": "test_004",
            "json_data": {
                "structuredFeatures": []
            },
            "headline": "Furnished Apartment Available Now",
            "description": "Fully furnished one bedroom apartment. All furniture and appliances included. No pets allowed. Features include reverse cycle air conditioning.",
            "feature_list": ["Furnished", "No pets", "Reverse cycle air conditioning"]
        },
        {
            "id": "test_005",
            "json_data": {
                "structuredFeatures": [
                    {"name": "Lift Access"},
                    {"name": "Intercom"}
                ]
            },
            "headline": "Unfurnished Unit with Parking",
            "description": "Bright and airy unfurnished unit. Secure undercover parking included. Building features lift access and intercom system.",
            "feature_list": ["Unfurnished", "Parking", "Intercom system", "Lift access"]
        }
    ]

def run_comparison_test():
    """运行特征提取比较测试"""
    print("🧪 开始特征提取比较测试...")
    
    # 创建特征提取器实例
    original_extractor = OriginalFeatureExtractor(FEATURES_CONFIG)
    enhanced_extractor = EnhancedFeatureExtractor(
        features_config=FEATURES_CONFIG,
        furniture_keywords=FURNITURE_KEYWORDS,
        aircon_keywords=AIRCON_KEYWORDS
    )
    
    # 创建数据类
    OriginalFeatures = create_property_features_class(FEATURES_CONFIG)
    EnhancedFeatures = create_enhanced_property_features_class(FEATURES_CONFIG)
    
    # 获取测试数据
    test_data = create_test_data()
    
    results = []
    
    print(f"\n📊 对比 {len(test_data)} 个测试样本:")
    print("=" * 80)
    
    for test_case in test_data:
        print(f"\n🏠 测试样本: {test_case['id']}")
        print(f"   标题: {test_case['headline']}")
        print(f"   描述: {test_case['description'][:100]}...")
        
        # 原始版本特征提取
        original_features = original_extractor.extract(
            test_case['json_data'],
            test_case['headline'], 
            test_case['description'],
            test_case['feature_list']
        )
        
        # 增强版本特征提取
        enhanced_features = enhanced_extractor.extract(
            test_case['json_data'],
            test_case['headline'],
            test_case['description'], 
            test_case['feature_list']
        )
        
        # 转换为字典进行比较
        original_dict = original_features.to_dict()
        enhanced_dict = enhanced_features.to_dict()
        
        # 比较结果
        differences = []
        
        # 获取所有特征字段
        all_features = set(original_dict.keys()) | set(enhanced_dict.keys())
        
        for feature in sorted(all_features):
            original_val = original_dict.get(feature, 'N/A')
            enhanced_val = enhanced_dict.get(feature, 'N/A')
            
            # 标准化比较
            if isinstance(original_val, bool):
                if original_val == True:
                    original_normalized = 'yes'
                elif original_val == False:
                    original_normalized = 'unknown'  # 关键差异点
                else:
                    original_normalized = str(original_val)
            else:
                original_normalized = str(original_val)
            
            enhanced_normalized = str(enhanced_val)
            
            if original_normalized != enhanced_normalized:
                differences.append({
                    'feature': feature,
                    'original': original_normalized,
                    'enhanced': enhanced_normalized,
                    'change_type': f"{original_normalized}→{enhanced_normalized}"
                })
        
        # 记录结果
        test_result = {
            'test_id': test_case['id'],
            'headline': test_case['headline'],
            'differences': differences,
            'original_features': original_dict,
            'enhanced_features': enhanced_dict
        }
        results.append(test_result)
        
        # 显示差异
        if differences:
            print(f"   ✨ 发现 {len(differences)} 个改进:")
            for diff in differences:
                change_desc = ""
                if diff['change_type'].endswith('→unknown'):
                    change_desc = " (避免了假阴性)"
                elif diff['change_type'].startswith('unknown→'):
                    change_desc = " (发现了新信息)"
                elif diff['change_type'] == 'unknown→yes' or diff['change_type'] == 'unknown→no':
                    change_desc = " (明确了状态)"
                    
                print(f"      • {diff['feature']}: {diff['original']} → {diff['enhanced']}{change_desc}")
        else:
            print("   ✅ 无差异")
    
    # 生成汇总报告
    print("\n" + "=" * 80)
    print("📈 汇总报告")
    print("=" * 80)
    
    total_differences = sum(len(r['differences']) for r in results)
    samples_with_differences = len([r for r in results if r['differences']])
    
    print(f"📊 总体统计:")
    print(f"   • 测试样本总数: {len(results)}")
    print(f"   • 有改进的样本: {samples_with_differences}")
    print(f"   • 总改进项数: {total_differences}")
    print(f"   • 平均每样本改进: {total_differences/len(results):.1f}")
    
    # 分析改进类型
    all_differences = []
    for result in results:
        all_differences.extend(result['differences'])
    
    if all_differences:
        print(f"\n🎯 改进类型分析:")
        
        # 统计变化类型
        change_types = {}
        for diff in all_differences:
            change_type = diff['change_type']
            change_types[change_type] = change_types.get(change_type, 0) + 1
        
        for change_type, count in sorted(change_types.items(), key=lambda x: x[1], reverse=True):
            percentage = (count / total_differences) * 100
            print(f"   • {change_type}: {count} 次 ({percentage:.1f}%)")
        
        # 按特征统计
        feature_changes = {}
        for diff in all_differences:
            feature = diff['feature']
            feature_changes[feature] = feature_changes.get(feature, 0) + 1
        
        print(f"\n📋 按特征分类的改进:")
        for feature, count in sorted(feature_changes.items(), key=lambda x: x[1], reverse=True):
            percentage = (count / total_differences) * 100
            print(f"   • {feature}: {count} 次 ({percentage:.1f}%)")
    
    # 保存详细结果
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_file = f"test_results_{timestamp}.json"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump({
            'timestamp': timestamp,
            'summary': {
                'total_samples': len(results),
                'samples_with_differences': samples_with_differences,
                'total_differences': total_differences,
                'average_improvements_per_sample': total_differences/len(results)
            },
            'test_results': results
        }, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 详细结果已保存到: {output_file}")
    
    return results

if __name__ == '__main__':
    try:
        results = run_comparison_test()
        print(f"\n🎉 测试完成！共分析了 {len(results)} 个样本")
    except Exception as e:
        print(f"❌ 测试过程中发生错误: {e}")
        import traceback
        traceback.print_exc()
