# 测试汉服推荐接口 - 稳定版
import requests

# 后端地址（必须和 app.py 运行的地址一致）
url = "http://127.0.0.1:5000/recommend"

# 用户画像：冬 / 结婚 / 唐制
user_data = {
    "season": "冬",
    "scene": "结婚",
    "style": "唐"
}

try:
    print("🔄 正在请求推荐系统...")
    # 发起 POST 请求
    response = requests.post(url, json=user_data, timeout=10)

    if response.status_code == 200:
        result = response.json()
        print("✅ 推荐成功！结果如下：")
        print("=" * 50)

        # 遍历推荐方案（不管字段名是什么，都能打印）
        for idx, item in enumerate(result.get("推荐方案", [])):
            print(f"\n🏆 第 {idx + 1} 套推荐方案")
            for key, value in item.items():
                print(f"   {key}: {value}")
            print("-" * 30)
    else:
        print(f"❌ 接口调用失败，状态码: {response.status_code}")

except Exception as e:
    print(f"❌ 发生异常: {e}")