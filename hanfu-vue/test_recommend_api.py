import requests
import json

# 测试推荐服务API
url = 'http://127.0.0.1:5000/recommend'

test_data = {
    'season': '春',
    'scene': '日常',
    'dynasty': '唐',
    'gender': '女',
    'skin_tone': '暖黄皮'
}

try:
    response = requests.post(url, json=test_data, timeout=10)
    print('Status Code:', response.status_code)
    print('Response:', response.json())
except Exception as e:
    print('Error:', str(e))