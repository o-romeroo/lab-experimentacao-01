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
    
def get_releases_count(owner, repository):
    url = f"https://api.github.com/repos/{owner}/{repository}/releases"
    headers = {
        "Authorization": f"Token {token}"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return len(response.json())
    else:
        raise Exception(f"Error fetching repository releases: {response.status_code} - {response.text}")
    
def hours_since_last_update(repo_details):
    updated_at = repo_details["updated_at"]
    updated_at_dt = datetime.strptime(updated_at, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
    now = datetime.now(timezone.utc)
    total = now - updated_at_dt
    return total.total_seconds() // 3600

def get_primary_language(repo_details):
    return repo_details["language"]

def get_closed_issues(owner, repo):
    url = f"https://api.github.com/repos/{owner}/{repo}/issues?state=closed"
    headers = {"Authorization": "token {token}"}
    page = 1
    closed_issues = []
    while True:
        response = requests.get(f"{url}&page={page}&per_page=100", headers=headers)
        if response.status_code == 200:
            page_closed_issues = response.json()
            if not page_closed_issues:
                break
            closed_issues.extend(page_closed_issues)
            page += 1
        else:
            raise Exception(f"Failed to fetch closed issues: {response.status_code}")
    return len(closed_issues)

if __name__ == "__main__":
    owner = "pallets"
    repo = "flask"
    releases_count = get_releases_count(owner, repo)
    print(f"O repositório {owner}/{repo} tem {releases_count} lançamentos.")