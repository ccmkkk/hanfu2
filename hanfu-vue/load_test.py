from locust import HttpUser, task, between
import json

class HanfuUser(HttpUser):
    wait_time = between(1, 3)  # 用户操作间隔1-3秒
    
    @task
    def recommend(self):
        # 测试推荐接口
        payload = {
            "season": "春",
            "scene": "日常",
            "dynasty": "唐",
            "gender": "女",
            "skin_tone": "暖黄皮"
        }
        self.client.post("/api/recommend", json=payload)
    
    @task(1)  # 权重为1，测试频率较低
    def health_check(self):
        # 测试健康检查接口
        self.client.get("/")
