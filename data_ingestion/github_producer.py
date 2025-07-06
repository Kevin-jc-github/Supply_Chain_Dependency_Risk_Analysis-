import requests
import json
import base64
import time
from kafka import KafkaProducer
from datetime import datetime
import random

# ==== 配置项 ====
GITHUB_TOKEN = ""  
KAFKA_TOPIC = "raw_dependencies"
KAFKA_BOOTSTRAP_SERVERS = "localhost:9092"
INTERVAL_SECONDS = 10  # 每轮推送间隔（秒）

# ==== Kafka Producer ====
producer = KafkaProducer(
    bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

headers = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

# ==== 仓库列表 ====
REPOS = [
    "pallets/flask",
    "psf/requests",
    "scikit-learn/scikit-learn",
    "pandas-dev/pandas",
    "tiangolo/fastapi",
    "explosion/spaCy",
    "apache/airflow",
    "PrefectHQ/prefect",
    "openai/CLIP",
    "huggingface/transformers"
]

def get_requirements(repo_full_name):
    """尝试获取 Python 项目的 requirements.txt"""
    url = f"https://api.github.com/repos/{repo_full_name}/contents/requirements.txt"
    res = requests.get(url, headers=headers)
    if res.status_code == 200:
        content = res.json()['content']
        decoded = base64.b64decode(content).decode("utf-8")
        dependencies = [line.strip() for line in decoded.splitlines() if line and not line.startswith("#")]
        return dependencies
    return []

def push_repo_dependency(repo_full_name):
    """构造 JSON 并发送到 Kafka"""
    deps = get_requirements(repo_full_name)
    if deps:
        timestamp = datetime.utcnow().isoformat()
        payload = {
            "repo": repo_full_name,
            "dependencies": deps,
            "timestamp": timestamp,
            "language": "Python"
        }
        producer.send(KAFKA_TOPIC, payload)
        print(f"[✓] Sent to Kafka: {repo_full_name} -> {len(deps)} deps")
    else:
        print(f"[×] Skipped (no requirements): {repo_full_name}")

if __name__ == "__main__":
    print("🚀 Starting streaming GitHub dependency producer...")
    while True:
        repo = random.choice(REPOS)
        push_repo_dependency(repo)
        time.sleep(INTERVAL_SECONDS)
