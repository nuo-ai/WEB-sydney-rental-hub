import requests
import json

def test_unsw_commute_search():
    """
    直接测试后端的 get_university_commute_profile GraphQL 查询。
    """
    graphql_url = "http://localhost:8000/graphql"
    
    query = """
    query GetUniversityCommute($universityName: UniversityNameEnum!) {
      get_university_commute_profile(university_name: $universityName, limit: 10) {
        directWalkOptions {
          items {
            property {
              listing_id
              address
              suburb
              rent_pw
              bedrooms
            }
            walkTimeToUniversityMinutes
          }
          totalCount
        }
      }
    }
    """
    
    variables = {
        "universityName": "UNSW"
    }
    
    print("🚀 正在向后端API发送GraphQL请求...")
    print(f"   - 端点: {graphql_url}")
    print(f"   - 查询: UNSW附近的房源")
    
    try:
        response = requests.post(
            graphql_url,
            json={"query": query, "variables": variables},
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            if "errors" in data:
                print("❌ GraphQL查询返回错误:")
                print(json.dumps(data['errors'], indent=2))
            else:
                print("✅ GraphQL查询成功！")
                results = data.get("data", {}).get("get_university_commute_profile", {}).get("directWalkOptions", {})
                total_count = results.get("totalCount", 0)
                items = results.get("items", [])
                
                print(f"\n📊 找到了 {total_count} 个UNSW附近的房源。")
                print("--- 前5个结果示例 ---")
                
                if not items:
                    print("   (无步行可达的房源)")
                else:
                    for i, item in enumerate(items[:5]):
                        prop = item.get("property", {})
                        walk_time = item.get("walkTimeToUniversityMinutes")
                        print(f"  {i+1}. {prop.get('address', 'N/A')}")
                        print(f"     - 租金: ${prop.get('rent_pw', 'N/A')}/周")
                        print(f"     - 房型: {prop.get('bedrooms', 'N/A')}房")
                        print(f"     - 步行时间: {walk_time}分钟")
                print("--------------------")
        else:
            print(f"❌ API请求失败，状态码: {response.status_code}")
            print(f"   - 响应内容: {response.text}")
            
    except requests.RequestException as e:
        print(f"❌ API请求异常: {e}")

if __name__ == "__main__":
    test_unsw_commute_search()
