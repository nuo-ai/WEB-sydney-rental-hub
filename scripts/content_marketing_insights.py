#!/usr/bin/env python3
"""
内容营销数据洞察挖掘脚本
生成 Top 10 榜单和深度市场分析内容
"""

import requests
import json
import statistics
from collections import Counter, defaultdict
import re

# GraphQL API配置
API_URL = "http://localhost:8000/graphql"

def query_all_properties():
    """查询所有房源数据"""
    
    query = """
    query GetAllProperties {
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

def extract_street_info(address):
    """提取地址中的街道信息"""
    if not address:
        return "未知街道", "未知楼盘"
    
    # 提取街道名
    street_match = re.search(r'([A-Za-z\s]+(?:Street|St|Avenue|Ave|Road|Rd|Lane|Way|Place|Drive|Dr))', address, re.IGNORECASE)
    street = street_match.group(1).strip() if street_match else "未知街道"
    
    # 提取楼盘/单元号
    unit_match = re.search(r'^([^,]+)', address)
    unit_building = unit_match.group(1).strip() if unit_match else "未知楼盘"
    
    return street, unit_building

def calculate_value_score(prop, suburb_avg_rent):
    """计算房源的综合性价比得分"""
    rent = prop.get('rent_pw', 0)
    bedrooms = prop.get('bedrooms', 0)
    bathrooms = prop.get('bathrooms', 0)
    
    if rent <= 0:
        return 0
    
    # 基础得分：与区域平均价格的比较
    price_score = max(0, (suburb_avg_rent - rent) / suburb_avg_rent * 100)
    
    # 配置加分：房间数和卫生间数
    config_score = (bedrooms * 10) + (bathrooms * 5)
    
    # 综合得分
    total_score = price_score + config_score
    
    return total_score

def analyze_street_patterns(properties):
    """分析街道价格模式"""
    street_data = defaultdict(list)
    
    for prop in properties:
        if not prop.get('rent_pw'):
            continue
            
        street, _ = extract_street_info(prop.get('address', ''))
        street_data[street].append({
            'rent': prop.get('rent_pw'),
            'bedrooms': prop.get('bedrooms', 0),
            'address': prop.get('address', ''),
            'property': prop
        })
    
    # 分析每条街道的统计数据
    street_analysis = {}
    for street, props in street_data.items():
        if len(props) >= 2:  # 至少2套房源才分析
            rents = [p['rent'] for p in props]
            street_analysis[street] = {
                'property_count': len(props),
                'avg_rent': statistics.mean(rents),
                'min_rent': min(rents),
                'max_rent': max(rents),
                'properties': props
            }
    
    return street_analysis

def find_hidden_gems(properties, bedroom_filter=1):
    """发现隐藏宝藏房源 - 价格低但配置好"""
    filtered_props = [p for p in properties if p.get('bedrooms') == bedroom_filter and p.get('rent_pw')]
    
    if not filtered_props:
        return []
    
    rents = [p['rent_pw'] for p in filtered_props]
    avg_rent = statistics.mean(rents)
    q1_rent = statistics.quantiles(rents, n=4)[0]
    
    hidden_gems = []
    for prop in filtered_props:
        rent = prop.get('rent_pw')
        bathrooms = prop.get('bathrooms', 0)
        
        # 隐藏宝藏条件：价格低于Q1但卫生间数≥1
        if rent <= q1_rent and bathrooms >= 1:
            savings = avg_rent - rent
            hidden_gems.append({
                'property': prop,
                'savings': savings,
                'bathrooms': bathrooms,
                'address': prop.get('address', ''),
                'rent': rent
            })
    
    return sorted(hidden_gems, key=lambda x: x['savings'], reverse=True)

def analyze_price_gaps(properties, bedroom_filter=1):
    """分析价格空白区间"""
    filtered_props = [p for p in properties if p.get('bedrooms') == bedroom_filter and p.get('rent_pw')]
    
    if not filtered_props:
        return []
    
    rents = sorted([p['rent_pw'] for p in filtered_props])
    
    # 找出价格空白（相邻价格差距>50）
    gaps = []
    for i in range(len(rents) - 1):
        current_rent = rents[i]
        next_rent = rents[i + 1]
        gap = next_rent - current_rent
        
        if gap > 50:
            gaps.append({
                'lower_bound': current_rent,
                'upper_bound': next_rent,
                'gap_size': gap,
                'opportunity': f"${current_rent+1}-${next_rent-1}/周价格区间空白"
            })
    
    return sorted(gaps, key=lambda x: x['gap_size'], reverse=True)

def generate_top10_content(properties):
    """生成各种Top 10内容"""
    content_ideas = {}
    
    # 按区域分组
    suburbs = defaultdict(list)
    for prop in properties:
        suburb = prop.get('suburb', '').strip()
        if suburb and prop.get('rent_pw'):
            suburbs[suburb].append(prop)
    
    for suburb, suburb_props in suburbs.items():
        if len(suburb_props) < 10:
            continue
            
        suburb_rents = [p['rent_pw'] for p in suburb_props]
        suburb_avg = statistics.mean(suburb_rents)
        
        # 按房型分组
        bedroom_groups = defaultdict(list)
        for prop in suburb_props:
            bedrooms = prop.get('bedrooms', 0)
            bedroom_groups[bedrooms].append(prop)
        
        suburb_content = {}
        
        for bedrooms, bedroom_props in bedroom_groups.items():
            if len(bedroom_props) < 5:
                continue
                
            room_type = f"{bedrooms}室" if bedrooms > 0 else "Studio"
            
            # 1. Top 10 最实惠房源
            cheapest = sorted(bedroom_props, key=lambda x: x.get('rent_pw', 999999))[:10]
            
            # 2. Top 10 性价比房源
            value_props = []
            for prop in bedroom_props:
                score = calculate_value_score(prop, suburb_avg)
                value_props.append((prop, score))
            best_value = sorted(value_props, key=lambda x: x[1], reverse=True)[:10]
            
            # 3. 隐藏宝藏房源
            gems = find_hidden_gems(bedroom_props, bedrooms)[:5]
            
            suburb_content[room_type] = {
                'cheapest': cheapest,
                'best_value': best_value,
                'hidden_gems': gems,
                'total_properties': len(bedroom_props),
                'avg_rent': statistics.mean([p['rent_pw'] for p in bedroom_props])
            }
        
        content_ideas[suburb] = suburb_content
    
    return content_ideas

def generate_market_insights(properties):
    """生成市场深度洞察"""
    insights = {}
    
    # 1. 街道价格分析
    street_analysis = analyze_street_patterns(properties)
    most_affordable_streets = sorted(
        [(street, data) for street, data in street_analysis.items()],
        key=lambda x: x[1]['avg_rent']
    )[:10]
    
    # 2. 价格空白分析
    price_gaps_1br = analyze_price_gaps(properties, 1)
    price_gaps_2br = analyze_price_gaps(properties, 2)
    
    # 3. 楼盘分析
    building_analysis = defaultdict(list)
    for prop in properties:
        if not prop.get('rent_pw'):
            continue
        _, building = extract_street_info(prop.get('address', ''))
        building_analysis[building].append(prop)
    
    # 找出最实惠的楼盘
    affordable_buildings = []
    for building, props in building_analysis.items():
        if len(props) >= 3:  # 至少3套房源
            avg_rent = statistics.mean([p['rent_pw'] for p in props])
            affordable_buildings.append({
                'building': building,
                'property_count': len(props),
                'avg_rent': avg_rent,
                'min_rent': min([p['rent_pw'] for p in props]),
                'sample_properties': props[:3]
            })
    
    affordable_buildings = sorted(affordable_buildings, key=lambda x: x['avg_rent'])[:10]
    
    insights = {
        'most_affordable_streets': most_affordable_streets,
        'price_gaps_1br': price_gaps_1br,
        'price_gaps_2br': price_gaps_2br,
        'affordable_buildings': affordable_buildings
    }
    
    return insights

def main():
    print("🚀 租房市场内容营销数据洞察分析")
    print("=" * 60)
    
    # 1. 获取所有房源数据
    all_properties = query_all_properties()
    if not all_properties:
        print("❌ 无法获取房源数据")
        return
    
    print(f"✅ 成功获取 {len(all_properties)} 条房源数据")
    
    # 过滤有效数据
    valid_properties = [p for p in all_properties if p.get('rent_pw') and p.get('suburb')]
    print(f"📊 有效房源数据: {len(valid_properties)} 条")
    
    # 2. 生成Top 10内容素材
    print(f"\n📝 生成Top 10榜单内容...")
    top10_content = generate_top10_content(valid_properties)
    
    # 3. 生成市场深度洞察
    print(f"🔍 挖掘市场深度洞察...")
    market_insights = generate_market_insights(valid_properties)
    
    # 4. 输出内容营销素材
    print(f"\n" + "="*60)
    print(f"📰 内容营销文章素材库")
    print(f"="*60)
    
    # 4.1 Top 10 文章素材
    print(f"\n🏆 Top 10 榜单文章素材:")
    for suburb, suburb_data in list(top10_content.items())[:3]:  # 显示前3个区域
        print(f"\n📍 {suburb}区域:")
        for room_type, data in suburb_data.items():
            print(f"\n  📝 文章标题建议: 'Top 10 {suburb}区最实惠{room_type}公寓'")
            print(f"     房源总数: {data['total_properties']}套")
            print(f"     平均租金: ${data['avg_rent']:.0f}/周")
            
            if data['cheapest']:
                print(f"     最便宜房源: {data['cheapest'][0]['address']} (${data['cheapest'][0]['rent_pw']}/周)")
            
            if data['hidden_gems']:
                gem = data['hidden_gems'][0]
                print(f"     隐藏宝藏: {gem['address']} (${gem['rent']}/周, 比均价低${gem['savings']:.0f})")
    
    # 4.2 深度洞察文章素材
    print(f"\n🔍 深度洞察文章素材:")
    
    print(f"\n📰 文章1: '悉尼租房隐藏宝藏街道Top 10'")
    print(f"   素材来源: 最实惠街道排名")
    for i, (street, data) in enumerate(market_insights['most_affordable_streets'][:5]):
        print(f"   #{i+1} {street}: 平均${data['avg_rent']:.0f}/周 ({data['property_count']}套房源)")
    
    print(f"\n📰 文章2: '悉尼租房市场价格空白分析'")
    print(f"   素材来源: 价格空白区间发现")
    for gap in market_insights['price_gaps_1br'][:3]:
        print(f"   1室房源空白: {gap['opportunity']} (空白${gap['gap_size']}/周)")
    
    print(f"\n📰 文章3: '最实惠公寓楼盘Top 10'")
    print(f"   素材来源: 楼盘整体性价比分析")
    for i, building in enumerate(market_insights['affordable_buildings'][:5]):
        print(f"   #{i+1} {building['building']}: 平均${building['avg_rent']:.0f}/周 ({building['property_count']}套)")
    
    # 4.3 内容营销策略建议
    print(f"\n💡 内容营销策略建议:")
    print(f"\n🎯 高热度文章标题模板:")
    print(f"   • 'Top 10 最实惠[区域][房型]公寓 - 2025年最新'")
    print(f"   • '[区域]租房隐藏宝藏 - 性价比超高的5个选择'")
    print(f"   • '悉尼租房攻略：这些街道最便宜却很少人知道'")
    print(f"   • '租房预算不够？这些价格空白区间有惊喜'")
    print(f"   • '内行人才知道的悉尼最实惠公寓楼盘'")
    
    print(f"\n📊 数据支撑的内容亮点:")
    print(f"   • 基于{len(valid_properties)}套真实房源数据分析")
    print(f"   • 涵盖{len(top10_content)}个主要区域")
    print(f"   • 发现{len(market_insights['price_gaps_1br'])}个1室房源价格空白区间")
    print(f"   • 识别{len(market_insights['affordable_buildings'])}个高性价比楼盘")
    
    print(f"\n🚀 SEO优化建议:")
    print(f"   • 关键词: '悉尼租房', '[区域]公寓', '最便宜', '性价比'")
    print(f"   • 长尾关键词: '悉尼[区域]最实惠[房型]', '[区域]租房攻略'")
    print(f"   • 内容更新频率: 每月更新Top 10榜单，保持数据新鲜度")

if __name__ == "__main__":
    main()
