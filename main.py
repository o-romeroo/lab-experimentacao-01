import requests
from dotenv import load_dotenv
import os
from datetime import datetime, timezone
import pandas as pd
import time


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
    
def get_merged_pull_requests_count(owner, repository):
    url = f"https://api.github.com/search/issues?q=repo:{owner}/{repository}+type:pr+is:merged"
    headers = {"Authorization": f"Token {token}"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()["total_count"]
    else:
        raise Exception(f"Error fetching merged pull requests: {response.status_code}")

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
        print(f"Fetching releases for page {page}")
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
    
def get_hours_since_last_update(repo_details):
    updated_at = repo_details["updated_at"]
    updated_at_dt = datetime.strptime(updated_at, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
    now = datetime.now(timezone.utc)
    total = now - updated_at_dt
    return total.total_seconds() // 3600

def get_primary_language(repo_details):
    return repo_details["language"]

def get_closed_issues(owner, repo):
    url = f"https://api.github.com/search/issues?q=repo:{owner}/{repo}+type:issue+state:closed"
    headers = {"Authorization": f"Token {token}"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()["total_count"]
    else:
        raise Exception(f"Failed to fetch closed issues: {response.status_code}")

def collect_and_save_repo_info(repos):
    rows = []

    for index, repo in enumerate(repos):
        print(f"Processing repository: {repo['full_name']}\nTotal remaining: {len(repos) - index - 1}")
        owner = repo["owner"]["login"]
        repo_name = repo["name"]

        repo_details = get_repositories_details(owner, repo_name)

        open_issues_count = repo_details["open_issues_count"]
        closed_issues_count = get_closed_issues(owner, repo_name)
        total_issues = open_issues_count + closed_issues_count
        closed_issues_percentage = (closed_issues_count / total_issues * 100) if total_issues > 0 else 0.0

        pull_requests_count = get_merged_pull_requests_count(owner, repo_name)
        releases_count = get_repository_releases_count(owner, repo_name)
        hours_since_last_update = get_hours_since_last_update(repo_details)
        primary_language = get_primary_language(repo_details)
        repo_age = get_repository_age_years(repo_details)

        rows.append({
            "full_name": repo["full_name"],
            "repo_name": repo_name,
            "open_issues_count": open_issues_count,
            "closed_issues_count": closed_issues_count,
            "closed_issues_percentage": closed_issues_percentage,
            "merged_pull_requests_count": pull_requests_count,
            "releases_count": releases_count,
            "hours_since_last_update": hours_since_last_update,
            "primary_language": primary_language,
            "repo_age_years": repo_age,
        })
        time.sleep(3)
    df = pd.DataFrame(rows)
    df.to_excel("repository_data.xlsx", index=False)


if __name__ == "__main__":
    try:
        popular_repos = get_popular_repositories(100)
        collect_and_save_repo_info(popular_repos)
    except Exception as e:
        print(f"Erro ao obter repositórios populares: {e}")
    