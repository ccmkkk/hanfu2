import requests
import time

# 构造测试数据集 (模拟用户的不同选项组合)
test_cases = [
    {"scene": "日常", "dynasty": "唐", "gender": "女", "season": "春"},
    {"scene": "拍照", "dynasty": "宋", "gender": "女", "season": "夏"},
    {"scene": "婚礼", "dynasty": "明", "gender": "男", "season": "冬"},
    {"scene": "日常", "dynasty": "汉", "gender": "男", "season": "秋"},
    {"scene": "婚礼", "dynasty": "唐", "gender": "女", "season": "春"},
] * 4 # 乘4，总计20个测试用例

API_URL = "http://127.0.0.1:5000/api/recommend"

def run_experiment(use_kg, experiment_name):
    print(f"\n开始运行: {experiment_name}...")

    total_time = 0
    basic_precision_count = 0
    valid_results = 0
    total_culture_match = 0
    total_dynasty_compatibility = 0
    has_meaning_info = 0
    no_meaning_info = 0

    for i, case in enumerate(test_cases):
        # 植入控制变量
        case["use_kg"] = use_kg

        start_time = time.time()
        try:
            response = requests.post(API_URL, json=case, timeout=10)
            data = response.json()
        except Exception as e:
            print(f"请求失败: {e}")
            continue

        total_time += (time.time() - start_time)

        # 如果返回了数据
        if len(data) > 0:
            valid_results += 1
            # 取第一个推荐结果进行评估
            top_item = data[0]

            # 指标1: 基础准确率 (朝代匹配)
            if top_item.get("dynasty") == case["dynasty"]:
                basic_precision_count += 1

            # 指标2: 文化匹配度 (从数据中获取)
            culture_match = top_item.get("culture_match", 0)
            total_culture_match += culture_match

            # 指标3: 历史适配度 (从数据中获取)
            dynasty_compatibility = top_item.get("dynasty_compatibility", 0)
            total_dynasty_compatibility += dynasty_compatibility

            # 判断是否有有效的文化内涵信息
            style_meaning = top_item.get("style_meaning", "")
            if "暂未收录" not in style_meaning and style_meaning not in ["制式", "纹样"]:
                has_meaning_info += 1
            else:
                no_meaning_info += 1

    # 计算最终数据
    total = len(test_cases)
    avg_time = (total_time / total) * 1000
    basic_rate = (basic_precision_count / total) * 100
    avg_culture_match = total_culture_match / valid_results if valid_results > 0 else 0
    avg_dynasty_compatibility = total_dynasty_compatibility / valid_results if valid_results > 0 else 0
    meaning_info_rate = (has_meaning_info / total) * 100

    print("-" * 50)
    print(f"【{experiment_name} 结果报告】")
    print(f"测试用例总数: {total} 个")
    print(f"有效返回结果数: {valid_results} 个")
    print(f"接口平均响应时间: {avg_time:.2f} ms")
    print(f"基础推荐准确率: {basic_rate:.2f}%")
    print(f"【核心指标】平均文化匹配度: {avg_culture_match:.2f}")
    print(f"【核心指标】平均历史适配度: {avg_dynasty_compatibility:.2f}")
    print(f"有效文化内涵信息覆盖率: {meaning_info_rate:.2f}%")
    print("-" * 50)

    return basic_rate, avg_culture_match, avg_dynasty_compatibility, meaning_info_rate, avg_time

if __name__ == "__main__":
    print("=== 汉服推荐系统 消融实验自动化测试启动 ===")
    print("核心评估指标: 文化匹配度 | 历史适配度")

    # 1. 跑对照组 (关闭知识图谱)
    base_acc, base_culture, base_dynasty, base_info_rate, base_time = run_experiment(
        use_kg=False,
        experiment_name="对照组 (单一基础算法)"
    )

    # 2. 跑实验组 (开启知识图谱)
    fusion_acc, fusion_culture, fusion_dynasty, fusion_info_rate, fusion_time = run_experiment(
        use_kg=True,
        experiment_name="实验组 (融合图谱算法)"
    )

    print("\n" + "=" * 50)
    print("【核心对比结论】")
    print("=" * 50)
    print(f"[核心指标] 文化匹配度提升: {fusion_culture - base_culture:.2f}")
    print(f"[核心指标] 历史适配度提升: {fusion_dynasty - base_dynasty:.2f}")
    print(f"文化内涵信息覆盖率提升: {fusion_info_rate - base_info_rate:.2f}%")
    print(f"响应时间变化: {fusion_time - base_time:.2f} ms")

    if fusion_culture > base_culture:
        print("\n[OK] 结论: 测试通过！融合知识图谱有效提升了系统的文化推荐准确性！")
    else:
        print("\n[WARNING] 结论: 融合知识图谱对文化推荐质量提升不明显")

    print("\n【评估指标说明】")
    print("  文化匹配度: 衡量推荐结果在文化内涵上的准确性和丰富程度")
    print("  历史适配度: 衡量推荐的汉服在历史朝代上的匹配程度")
    print("  数据来源: MySQL数据库预存值 + Neo4j知识图谱补充")