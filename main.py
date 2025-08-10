import requests
from dotenv import load_dotenv
import os
from datetime import datetime, timezone

load_dotenv()

token = os.getenv("token")

def get_popular_repositories(num_repos):
    url = f"https://api.github.com/search/repositories?q=stars:>0&sort=stars&order=desc&per_page={num_repos}"
    headers = {
        "Authorization": f"Token {token}"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()["items"]
    else:
        raise Exception(f"Error fetching repositories: {response.status_code} - {response.text}")
    
def get_repository_age_years(repo_details):
    created_at = repo_details["created_at"]
    created_at_dt = datetime.strptime(created_at, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
    now = datetime.now(timezone.utc)
    age_years = (now - created_at_dt).days / 365.25
    return age_years
    
def get_repository_pull_requests(owner, repository):
    url = f"https://api.github.com/repos/{owner}/{repository}/pulls?state=all"
    headers = {"Authorization": f"Token {token}"}
    page = 1
    pull_requests = []
    while True:
        response = requests.get(f"{url}&page={page}&per_page=100", headers=headers)
        if response.status_code == 200:
            page_pull_requests = response.json()
            if not page_pull_requests:
                break
            pull_requests.extend(page_pull_requests)
            page += 1
        else:
            raise Exception(f"Error fetching repository pull requests: {response.status_code}")
    return len(pull_requests)

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

def get_repository_releases_count(owner, repository):
    url = f"https://api.github.com/repos/{owner}/{repository}/releases"
    headers = {"Authorization": f"Token {token}"}
    page = 1
    releases = []
    while True:
        response = requests.get(f"{url}?page={page}&per_page=100", headers=headers)
        if response.status_code == 200:
            page_releases = response.json()
            if not page_releases:
                break
            releases.extend(page_releases)
            page += 1
        else:
            raise Exception(f"Error fetching repository releases: {response.status_code} - {response.text}")
    return len(releases)
    
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
    try:
        popular_repos = get_popular_repositories(10)
        for idx, repo in enumerate(popular_repos, start=1):
            full_name = repo.get("full_name", "unknown")
            stars = repo.get("stargazers_count", 0)
            print(f"{idx}. {full_name} - {stars} stars")
    except Exception as e:
        print(f"Erro ao obter repositórios populares: {e}")