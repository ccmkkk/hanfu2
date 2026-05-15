import requests

API_URL = "http://127.0.0.1:5000/api/recommend"

# 发送一个测试请求看看数据格式
test_case = {"scene": "日常", "dynasty": "唐", "gender": "女", "season": "春", "use_kg": True}

response = requests.post(API_URL, json=test_case)
data = response.json()

print(f"返回结果数: {len(data)}")
if len(data) > 0:
    print("\n第一个推荐结果:")
    print("-" * 50)
    for key, value in data[0].items():
        print(f"{key}: {value}")
