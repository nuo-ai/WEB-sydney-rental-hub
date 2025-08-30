# -*- coding: utf-8 -*-
import requests
import json
import sys
import io

# 设置输出编码
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 获取房源9070832的数据
response = requests.get("http://localhost:8000/api/properties/9070832")
data = response.json()
property_data = data['data']

print(f"房源地址: {property_data['address']}")
print(f"房源ID: {property_data['listing_id']}")
print(f"\n数据库中的图片链接（共{len(property_data['images'])}个）：")

for i, img in enumerate(property_data['images'], 1):
    print(f"{i}. {img}")

print("\n" + "="*80)
print("\n控制台报错的404链接：")

# 从控制台.txt提取的404错误链接
error_links = [
    "https://rimh2.domainstatic.com.au/DelQTp2a0BOehN48NaAy0LyO1gQ=/fit-in/1920x1080/filters:format(jpeg):quality(80):no_upscale()/9070832_6_1_240611_051153-w837-h1488",
    "https://rimh2.domainstatic.com.au/u_NrYsbyVVGoeUd9BzZgSH4NrX0=/fit-in/1920x1080/filters:format(jpeg):quality(80):no_upscale()/9070832_5_1_250805_021114-w800-h1422",
    "https://rimh2.domainstatic.com.au/4wfpKojkIfQ5UcLtJeh1j7WqP6o=/fit-in/1920x1080/filters:format(jpeg):quality(80):no_upscale()/9070832_7_1_240611_051153-w800-h600",
    "https://rimh2.domainstatic.com.au/JBx2Te7nPK7_4x3Kui6f2TXTEgQ=/fit-in/1920x1080/filters:format(jpeg):quality(80):no_upscale()/9070832_4_1_250805_021114-w1920-h1080",
    "https://rimh2.domainstatic.com.au/n_WHMIICA7rK8pj5yRQmI9ksFbU=/fit-in/1920x1080/filters:format(jpeg):quality(80):no_upscale()/9070832_3_1_250805_021117-w1860-h1046",
    "https://rimh2.domainstatic.com.au/Vxpv6MsPV2qbWhqIggD0s0bkt6A=/fit-in/1920x1080/filters:format(jpeg):quality(80):no_upscale()/9070832_2_1_250805_021117-w800-h600",
    "https://rimh2.domainstatic.com.au/KKpjfbt8hnnvGPj9phgoVj0_xuk=/fit-in/1920x1080/filters:format(jpeg):quality(80):no_upscale()/9070832_8_1_240611_051153-w1488-h837",
    "https://rimh2.domainstatic.com.au/k7mah4qwPRFNJrmdpIoT-8D-ETg=/fit-in/1920x1080/filters:format(jpeg):quality(80):no_upscale()/9070832_9_1_240611_051153-w1488-h837"
]

for i, link in enumerate(error_links, 1):
    print(f"{i}. {link}")

print("\n" + "="*80)
print("\n分析：")
print("1. 数据库中的图片链接和404错误的链接不同")
print("2. 错误链接中的日期：240611（2024年6月11日）和 250805（2025年8月5日）")
print("3. 数据库链接日期：250805（2025年8月5日）")
print("4. 看起来有些链接是旧版本，Domain.com.au 的图片URL已更新")

# 检查一个可用的链接
print("\n测试数据库中的第一个图片链接...")
test_url = property_data['images'][0]
try:
    r = requests.head(test_url, timeout=5)
    print(f"状态码: {r.status_code}")
    if r.status_code == 200:
        print("✓ 数据库中的链接有效")
    else:
        print("✗ 数据库中的链接也失效了")
except Exception as e:
    print(f"测试失败: {e}")