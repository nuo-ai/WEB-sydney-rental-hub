#!/usr/bin/env python3
"""
租房价格策略分析脚本 - 为价格敏感租客提供最优策略
"""

import requests
import json
import statistics
from collections import Counter

# GraphQL API配置
API_URL = "http://localhost:8000/graphql"

def query_zetland_properties():
    """查询Zetland区域的所有房源"""
    
    query = """
    query GetZetlandProperties {
        all_properties(limit: 5000) {
            items {
                listing_id
                address
                suburb
                rent_pw
                bedrooms
                bathrooms
                property_type
                postcode
            }
            totalCount
        }
    }
    """
    
    try:
        response = requests.post(
            API_URL,
            json={"query": query},
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        if not response.ok:
            print(f"❌ API请求失败: {response.status_code} {response.reason}")
            return None
            
        result = response.json()
        
        if "errors" in result:
            print(f"❌ GraphQL错误: {result['errors']}")
            return None
            
        return result["data"]["all_properties"]["items"]
        
    except requests.exceptions.RequestException as e:
        print(f"❌ 网络请求错误: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"❌ JSON解析错误: {e}")
        return None

def filter_zetland_properties(properties):
    """筛选出Zetland区域的房源"""
    zetland_properties = []
    
    for prop in properties:
        suburb = prop.get("suburb", "").lower().strip()
        address = prop.get("address", "").lower().strip()
        
        if "zetland" in suburb or "zetland" in address:
            zetland_properties.append(prop)
    
    return zetland_properties

def comprehensive_price_analysis(properties, bedroom_filter=1):
    """全面的价格分析"""
    # 筛选特定房型
    filtered_properties = [p for p in properties if p.get("bedrooms") == bedroom_filter]
    
    # 获取有效租金数据
    rents = []
    for prop in filtered_properties:
        rent = prop.get("rent_pw")
        if rent and isinstance(rent, (int, float)) and rent > 0:
            rents.append(rent)
    
    if not rents:
        return None
    
    # 排序数据
    sorted_rents = sorted(rents)
    
    # 基础统计
    avg_rent = statistics.mean(rents)
    median_rent = statistics.median(rents)
    mode_rents = statistics.multimode(rents)
    
    # 四分位数分析
    q1 = statistics.quantiles(rents, n=4)[0]  # 25%分位数
    q3 = statistics.quantiles(rents, n=4)[2]  # 75%分位数
    
    # 价格区间分析
    price_ranges = {
        "经济型 (≤Q1)": {"max": q1, "count": 0, "properties": []},
        "性价比型 (Q1-中位数)": {"min": q1, "max": median_rent, "count": 0, "properties": []},
        "中等价位 (中位数-Q3)": {"min": median_rent, "max": q3, "count": 0, "properties": []},
        "高端型 (≥Q3)": {"min": q3, "count": 0, "properties": []}
    }
    
    # 分类房源
    for prop in filtered_properties:
        rent = prop.get("rent_pw")
        if not rent:
            continue
            
        if rent <= q1:
            price_ranges["经济型 (≤Q1)"]["count"] += 1
            price_ranges["经济型 (≤Q1)"]["properties"].append(prop)
        elif rent <= median_rent:
            price_ranges["性价比型 (Q1-中位数)"]["count"] += 1
            price_ranges["性价比型 (Q1-中位数)"]["properties"].append(prop)
        elif rent <= q3:
            price_ranges["中等价位 (中位数-Q3)"]["count"] += 1
            price_ranges["中等价位 (中位数-Q3)"]["properties"].append(prop)
        else:
            price_ranges["高端型 (≥Q3)"]["count"] += 1
            price_ranges["高端型 (≥Q3)"]["properties"].append(prop)
    
    return {
        "total_properties": len(filtered_properties),
        "valid_rents": len(rents),
        "sorted_rents": sorted_rents,
        "mean": avg_rent,
        "median": median_rent,
        "mode": mode_rents,
        "q1": q1,
        "q3": q3,
        "min": min(rents),
        "max": max(rents),
        "price_ranges": price_ranges
    }

def price_strategy_recommendations(analysis):
    """基于分析数据提供价格策略建议"""
    
    strategies = {}
    
    # 策略1: 极度价格敏感 - 底部25%
    q1_properties = analysis["price_ranges"]["经济型 (≤Q1)"]["properties"]
    if q1_properties:
        strategies["极度价格敏感"] = {
            "target_range": f"≤${analysis['q1']:.0f}/周",
            "property_count": len(q1_properties),
            "percentage": f"{len(q1_properties)/analysis['valid_rents']*100:.1f}%",
            "strategy": "重点关注底部25%房源，但要仔细评估房屋条件",
            "risk": "可能房屋条件较差或位置偏远",
            "sample_properties": q1_properties[:3]
        }
    
    # 策略2: 价格敏感 - Q1到中位数
    value_properties = analysis["price_ranges"]["性价比型 (Q1-中位数)"]["properties"]
    if value_properties:
        strategies["价格敏感"] = {
            "target_range": f"${analysis['q1']:.0f}-${analysis['median']:.0f}/周",
            "property_count": len(value_properties),
            "percentage": f"{len(value_properties)/analysis['valid_rents']*100:.1f}%",
            "strategy": "最佳性价比区间，建议重点关注",
            "risk": "低风险，性价比高",
            "sample_properties": value_properties[:3]
        }
    
    # 策略3: 标准预算 - 中位数到Q3
    mid_properties = analysis["price_ranges"]["中等价位 (中位数-Q3)"]["properties"]
    if mid_properties:
        strategies["标准预算"] = {
            "target_range": f"${analysis['median']:.0f}-${analysis['q3']:.0f}/周",
            "property_count": len(mid_properties),
            "percentage": f"{len(mid_properties)/analysis['valid_rents']*100:.1f}%",
            "strategy": "市场中位价格，选择较多，条件较好",
            "risk": "中等风险，质量稳定",
            "sample_properties": mid_properties[:3]
        }
    
    return strategies

def main():
    print("🎯 Zetland区域1室房源价格策略分析")
    print("=" * 50)
    
    # 1. 获取数据
    all_properties = query_zetland_properties()
    if not all_properties:
        print("❌ 无法获取房源数据")
        return
    
    zetland_properties = filter_zetland_properties(all_properties)
    if not zetland_properties:
        print("❌ 没有找到Zetland区域的房源")
        return
    
    # 2. 综合价格分析
    analysis = comprehensive_price_analysis(zetland_properties, bedroom_filter=1)
    if not analysis:
        print("❌ 无法进行价格分析")
        return
    
    # 3. 基础统计展示
    print(f"\n📊 价格统计概览:")
    print(f"  有效房源数: {analysis['valid_rents']} 套")
    print(f"  平均价格: ${analysis['mean']:.0f}/周")
    print(f"  中位数价格: ${analysis['median']:.0f}/周")
    print(f"  众数价格: ${', '.join([f'${m:.0f}' for m in analysis['mode']])}/周")
    print(f"  价格区间: ${analysis['min']:.0f} - ${analysis['max']:.0f}/周")
    
    # 4. 四分位数分析
    print(f"\n📈 四分位数分析:")
    print(f"  Q1 (25%分位数): ${analysis['q1']:.0f}/周")
    print(f"  Q2 (中位数): ${analysis['median']:.0f}/周")
    print(f"  Q3 (75%分位数): ${analysis['q3']:.0f}/周")
    
    # 5. 价格区间分布
    print(f"\n🏠 价格区间分布:")
    for range_name, range_data in analysis['price_ranges'].items():
        count = range_data['count']
        percentage = count / analysis['valid_rents'] * 100
        
        if 'min' in range_data and 'max' in range_data:
            price_range = f"${range_data['min']:.0f}-${range_data['max']:.0f}"
        elif 'max' in range_data:
            price_range = f"≤${range_data['max']:.0f}"
        else:
            price_range = f"≥${range_data['min']:.0f}"
        
        print(f"  {range_name}: {count}套 ({percentage:.1f}%) | {price_range}/周")
    
    # 6. 策略建议
    strategies = price_strategy_recommendations(analysis)
    
    print(f"\n🎯 价格敏感租客策略建议:")
    print(f"\n💡 关键发现:")
    
    # 平均价 vs 中位数的解释
    mean_median_diff = analysis['mean'] - analysis['median']
    if abs(mean_median_diff) < 10:
        distribution_type = "价格分布相对均匀"
    elif mean_median_diff > 0:
        distribution_type = "少数高价房源拉高了平均价"
    else:
        distribution_type = "少数低价房源拉低了平均价"
    
    print(f"  • 平均价 vs 中位数: ${analysis['mean']:.0f} vs ${analysis['median']:.0f} ({distribution_type})")
    print(f"  • 对价格敏感租客，建议关注中位数而非平均价")
    print(f"  • 中位数更能反映市场主流价格水平")
    
    # 具体策略
    for strategy_name, strategy_data in strategies.items():
        print(f"\n🎪 {strategy_name}策略:")
        print(f"  目标价格区间: {strategy_data['target_range']}")
        print(f"  可选房源数量: {strategy_data['property_count']}套 ({strategy_data['percentage']})")
        print(f"  策略建议: {strategy_data['strategy']}")
        print(f"  风险评估: {strategy_data['risk']}")
        
        if strategy_data['sample_properties']:
            print(f"  推荐房源样例:")
            for i, prop in enumerate(strategy_data['sample_properties']):
                address = prop.get('address', '地址未知')
                rent = prop.get('rent_pw', 0)
                print(f"    {i+1}. {address} | ${rent}/周")
    
    # 7. 最优策略总结
    print(f"\n🏆 最优策略总结:")
    print(f"  1. 使用中位数(${analysis['median']:.0f}/周)作为价格基准，而非平均价")
    print(f"  2. 重点关注Q1-中位数区间(${analysis['q1']:.0f}-${analysis['median']:.0f}/周)的性价比房源")
    print(f"  3. 避免盲目追求最低价，底部25%房源可能存在质量问题")
    print(f"  4. 预算允许的情况下，中位数附近房源选择更多，性价比更高")

if __name__ == "__main__":
    main()
