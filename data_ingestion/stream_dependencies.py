import requests
import json
import base64
import time
import random
from kafka import KafkaProducer
from datetime import datetime

# ======= 配置 =======
GITHUB_TOKEN = ""
INTERVAL_SECONDS = 10
KAFKA_TOPIC = "raw_dependencies"
KAFKA_BOOTSTRAP_SERVERS = "localhost:9092"
REPO_FILE = "top_python_repos.json"

# ======= Kafka Producer =======
producer = KafkaProducer(
    bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

headers = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

def get_requirements(repo_full_name):
    url = f"https://api.github.com/repos/{repo_full_name}/contents/requirements.txt"
    res = requests.get(url, headers=headers)
    if res.status_code == 200:
        content = res.json().get('content', '')
        decoded = base64.b64decode(content).decode("utf-8")
        return [line.strip() for line in decoded.splitlines() if line and not line.startswith("#")]
    return []

def stream_dependencies():
    with open(REPO_FILE, "r") as f:
        repos = json.load(f)

    print("🚀 Streaming GitHub dependencies to Kafka...")
    while True:
        repo = random.choice(repos)
        deps = get_requirements(repo)
        if deps:
            payload = {
                "repo": repo,
                "dependencies": deps,
                "timestamp": datetime.utcnow().isoformat(),
                "language": "Python"
            }
            producer.send(KAFKA_TOPIC, payload)
            print(f"[→] Sent: {repo} with {len(deps)} deps")
        else:
            print(f"[×] No requirements.txt for {repo}")
        time.sleep(INTERVAL_SECONDS)

if __name__ == "__main__":
    stream_dependencies()
