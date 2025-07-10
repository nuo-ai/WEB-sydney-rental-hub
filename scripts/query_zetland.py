#!/usr/bin/env python3
"""
查询Zetland区域房源统计脚本
"""

import requests
import json
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
        
        # 检查suburb字段或address字段是否包含zetland
        if "zetland" in suburb or "zetland" in address:
            zetland_properties.append(prop)
    
    return zetland_properties

def analyze_bedroom_distribution(properties):
    """分析房间数分布"""
    bedroom_counts = Counter()
    
    for prop in properties:
        bedrooms = prop.get("bedrooms")
        if bedrooms is not None:
            bedroom_counts[bedrooms] += 1
        else:
            bedroom_counts["未知"] += 1
    
    return bedroom_counts

def analyze_price_statistics(properties, bedroom_filter=None, show_details=False):
    """分析价格统计信息"""
    if bedroom_filter is not None:
        properties = [p for p in properties if p.get("bedrooms") == bedroom_filter]
    
    # 获取有效租金数据
    rents = []
    for prop in properties:
        rent = prop.get("rent_pw")
        if rent and isinstance(rent, (int, float)) and rent > 0:
            rents.append(rent)
    
    if not rents:
        return None
    
    # 排序租金数据
    sorted_rents = sorted(rents)
    
    # 计算统计数据
    avg_rent = sum(rents) / len(rents)
    min_rent = min(rents)
    max_rent = max(rents)
    
    # 详细计算中位数
    n = len(sorted_rents)
    if n % 2 == 1:
        # 奇数个数据，取中间值
        median_index = n // 2
        median_rent = sorted_rents[median_index]
    else:
        # 偶数个数据，取中间两个数的平均值
        mid1 = sorted_rents[n // 2 - 1]
        mid2 = sorted_rents[n // 2]
        median_rent = (mid1 + mid2) / 2
    
    # 计算低于均价的房源数量
    below_avg_count = len([r for r in rents if r < avg_rent])
    
    result = {
        "total_count": len(properties),
        "valid_rent_count": len(rents),
        "average": avg_rent,
        "median": median_rent,
        "min": min_rent,
        "max": max_rent,
        "below_average_count": below_avg_count,
        "below_average_percentage": (below_avg_count / len(rents)) * 100 if rents else 0,
        "sorted_rents": sorted_rents
    }
    
    if show_details:
        result["median_calculation"] = {
            "count": n,
            "is_odd": n % 2 == 1,
            "median_index": n // 2 if n % 2 == 1 else None,
            "mid_indices": None if n % 2 == 1 else [n // 2 - 1, n // 2],
            "mid_values": None if n % 2 == 1 else [sorted_rents[n // 2 - 1], sorted_rents[n // 2]]
        }
    
    return result

def main():
    print("🔍 正在查询Zetland区域房源数据...")
    
    # 1. 获取所有房源数据
    all_properties = query_zetland_properties()
    if not all_properties:
        print("❌ 无法获取房源数据")
        return
    
    print(f"✅ 成功获取 {len(all_properties)} 条房源数据")
    
    # 2. 筛选Zetland区域房源
    zetland_properties = filter_zetland_properties(all_properties)
    
    if not zetland_properties:
        print("❌ 没有找到Zetland区域的房源")
        return
    
    print(f"\n🏠 Zetland区域房源统计:")
    print(f"总房源数: {len(zetland_properties)} 套")
    
    # 3. 分析房间数分布
    bedroom_distribution = analyze_bedroom_distribution(zetland_properties)
    
    print(f"\n📊 房间数分布:")
    
    # 按房间数排序显示
    sorted_bedrooms = sorted(bedroom_distribution.items(), key=lambda x: x[0] if isinstance(x[0], int) else 999)
    
    for bedrooms, count in sorted_bedrooms:
        if isinstance(bedrooms, int):
            if bedrooms == 0:
                print(f"  Studio: {count} 套")
            else:
                print(f"  {bedrooms}室: {count} 套")
        else:
            print(f"  {bedrooms}: {count} 套")
    
    # 4. 分析1室房源价格统计（包含详细计算过程）
    one_bedroom_stats = analyze_price_statistics(zetland_properties, bedroom_filter=1, show_details=True)
    
    if one_bedroom_stats:
        print(f"\n💰 1室房源价格分析:")
        print(f"  有效房源数: {one_bedroom_stats['valid_rent_count']} 套")
        print(f"  平均租金: ${one_bedroom_stats['average']:.0f}/周")
        print(f"  中位数租金: ${one_bedroom_stats['median']:.0f}/周")
        print(f"  最低租金: ${one_bedroom_stats['min']:.0f}/周")
        print(f"  最高租金: ${one_bedroom_stats['max']:.0f}/周")
        print(f"  低于均价房源: {one_bedroom_stats['below_average_count']} 套 ({one_bedroom_stats['below_average_percentage']:.1f}%)")
        
        # 4.1 显示中位数计算详细过程
        if "median_calculation" in one_bedroom_stats:
            calc = one_bedroom_stats["median_calculation"]
            sorted_rents = one_bedroom_stats["sorted_rents"]
            
            print(f"\n📐 中位数计算过程详解:")
            print(f"  总数据量: {calc['count']} 个租金值")
            print(f"  数据类型: {'奇数个' if calc['is_odd'] else '偶数个'}数据")
            
            # 显示排序后的所有租金
            print(f"  排序后租金列表: {sorted_rents}")
            
            if calc['is_odd']:
                print(f"  中位数位置: 第{calc['median_index'] + 1}个数据 (索引{calc['median_index']})")
                print(f"  中位数值: ${sorted_rents[calc['median_index']]}/周")
            else:
                mid_indices = calc['mid_indices']
                mid_values = calc['mid_values']
                print(f"  中位数位置: 第{mid_indices[0] + 1}和第{mid_indices[1] + 1}个数据的平均值")
                print(f"  中位数计算: (${mid_values[0]} + ${mid_values[1]}) ÷ 2 = ${one_bedroom_stats['median']:.0f}/周")
                print(f"  详细计算: ({mid_values[0]} + {mid_values[1]}) ÷ 2 = {(mid_values[0] + mid_values[1]) / 2}/周")
    
    # 5. 显示低于均价的1室房源详情
    if one_bedroom_stats:
        avg_rent = one_bedroom_stats['average']
        one_bedroom_properties = [p for p in zetland_properties if p.get("bedrooms") == 1]
        below_avg_properties = [
            p for p in one_bedroom_properties 
            if p.get("rent_pw") and p.get("rent_pw") < avg_rent
        ]
        
        if below_avg_properties:
            print(f"\n🔻 低于均价的1室房源 (低于${avg_rent:.0f}/周):")
            for i, prop in enumerate(below_avg_properties):
                address = prop.get("address", "地址未知")
                rent = prop.get("rent_pw", "价格未知")
                savings = avg_rent - rent if rent else 0
                print(f"  {i+1}. {address} | ${rent}/周 | 比均价低${savings:.0f}")
    
    # 6. 显示详细信息示例
    print(f"\n📝 房源样例 (显示前5套):")
    for i, prop in enumerate(zetland_properties[:5]):
        bedrooms = prop.get("bedrooms", "未知")
        address = prop.get("address", "地址未知")
        rent = prop.get("rent_pw", "价格未知")
        
        bedroom_str = f"{bedrooms}室" if isinstance(bedrooms, int) and bedrooms > 0 else ("Studio" if bedrooms == 0 else "未知房型")
        
        print(f"  {i+1}. {address} | {bedroom_str} | ${rent}/周")
    
    if len(zetland_properties) > 5:
        print(f"  ... 还有 {len(zetland_properties) - 5} 套房源")

if __name__ == "__main__":
    main()
