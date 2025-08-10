import requests
from dotenv import load_dotenv
import os
from datetime import datetime, timezone

load_dotenv()

token = os.getenv("token")

def get_popular_repositories(keyword, num_repos):
    url = f"https://api.github.com/search/repositories?q={keyword}&sort=stars&order=desc&per_page={num_repos}"
    headers = {
        "Authorization": f"Token {token}"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()["items"]
    else:
        raise Exception(f"Error fetching repositories: {response.status_code} - {response.text}")

def get_repositories_details(owner, repository):
    url = f"https://api.github.com/repos/{owner}/{repository}"
    headers = {
        "Authorization": f"Token {token}"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error fetching repository details: {response.status_code} - {response.text}")
    
def hours_since_last_update(repo_details):
    updated_at = repo_details["updated_at"]
    updated_at_dt = datetime.strptime(updated_at, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
    now = datetime.now(timezone.utc)
    total = now - updated_at_dt
    return total.total_seconds() // 3600



if __name__ == "__main__":
    # Exemplo usando um repositório público do GitHub
    owner = "pallets"
    repo = "flask"
    horas = hours_since_last_update(owner, repo)
    print(f"O repositório {owner}/{repo} foi atualizado há {int(horas)} horas.")
    
