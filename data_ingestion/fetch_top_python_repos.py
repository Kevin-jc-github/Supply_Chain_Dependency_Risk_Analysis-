import requests
import json

# ======= 配置 =======
GITHUB_TOKEN = ""
TOP_N = 500  # 想抓多少个 top Python 仓库
OUTPUT_FILE = "top_python_repos.json"

headers = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

def fetch_top_python_repos():
    repos = []
    per_page = 100
    pages = (TOP_N + per_page - 1) // per_page

    for page in range(1, pages + 1):
        url = f"https://api.github.com/search/repositories?q=language:python&sort=stars&order=desc&per_page={per_page}&page={page}"
        print(f"[📦] Fetching page {page} ...")
        res = requests.get(url, headers=headers)

        if res.status_code != 200:
            print("❌ Error fetching:", res.text)
            break

        items = res.json().get("items", [])
        repos.extend(item["full_name"] for item in items)
        if len(repos) >= TOP_N:
            break

    repos = repos[:TOP_N]
    with open(OUTPUT_FILE, "w") as f:
        json.dump(repos, f, indent=2)
    print(f"[✅] Saved {len(repos)} repos to {OUTPUT_FILE}")

if __name__ == "__main__":
    fetch_top_python_repos()
