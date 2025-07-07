import requests
import json

API_URL = 'http://127.0.0.1:8000/graphql'

query = """
    query GetAllProperties {
        all_properties(limit: 10) {
            items {
                listing_id
                address
                suburb
                rent_pw
            }
            totalCount
        }
    }
"""

try:
    print("正在测试后端API连接...")
    response = requests.post(
        API_URL,
        headers={'Content-Type': 'application/json'},
        json={'query': query},
        timeout=10  # 添加10秒超时，防止僵住
    )

    response.raise_for_status()  # Raise an exception for bad status codes

    print("✅ 后端API连接成功!")
    print("Status Code:", response.status_code)
    print("Response JSON:")
    print(json.dumps(response.json(), indent=2, ensure_ascii=False))

except requests.exceptions.Timeout:
    print("❌ 连接超时: 后端服务可能没有启动")
    print("请先运行: python run_backend.py")
except requests.exceptions.ConnectionError:
    print("❌ 连接失败: 无法连接到后端服务")
    print("请确认后端服务正在运行在 http://localhost:8000")
except requests.exceptions.RequestException as e:
    print(f"❌ 请求失败: {e}")
