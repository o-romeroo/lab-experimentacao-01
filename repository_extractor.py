import requests
from dotenv import load_dotenv
import os
from datetime import datetime, timezone
import pandas as pd
import time


load_dotenv()

token = os.getenv("token")

def get_popular_repositories(num_repos):
    """
    Retorna os repositórios mais populares do GitHub, ordenados por número de estrelas.

    Parâmetros:
    - num_repos (int): número máximo de repositórios a buscar (até 1000).

    Retorna:
    - list: lista de dicionários, cada um representando um repositório conforme o campo "items" da resposta da API.

    Arremessa:
    - Exception: se alguma requisição HTTP não retornar status 200.

    Observações:
    - A função faz a paginação automaticamente para buscar mais de 100 repositórios, respeitando o limite de 1000 imposto pela API do GitHub.
    - Insere um delay de 2 segundos entre as requisições para evitar atingir o rate limit da API.
    """
    all_repos = []
    per_page = 100
    for page in range(1, (num_repos // per_page) + 2):
        url = f"https://api.github.com/search/repositories?q=stars:>0&sort=stars&order=desc&per_page={per_page}&page={page}"
        headers = {"Authorization": f"Token {token}"}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            items = response.json()["items"]
            all_repos.extend(items)
            if len(all_repos) >= num_repos or not items:
                break
        else:
            raise Exception(f"Error fetching repositories: {response.status_code} - {response.text}")
        time.sleep(2)  
    return all_repos[:num_repos]
    
def get_repository_age_years(repo_details):
    """Calcula a idade do repositório em anos.

    Parâmetros:
    - repo_details (dict): dicionário com os detalhes do repositório (deve conter a chave "created_at").

    Retorna:
    - float: idade em anos (aproximação usando 365.25 dias por ano).
    """
    created_at = repo_details["created_at"]
    created_at_dt = datetime.strptime(created_at, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
    now = datetime.now(timezone.utc)
    age_years = (now - created_at_dt).days / 365.25
    return age_years
    
def get_merged_pull_requests_count(owner, repository):
    """Retorna o número de pull requests mergeados em um repositório.

    Parâmetros:
    - owner (str): proprietário/organização do repositório.
    - repository (str): nome do repositório.

    Retorna:
    - int: contagem total de pull requests mergeados conforme o campo "total_count" da resposta da API.

    Arremessa:
    - Exception: se a requisição HTTP não retornar status 200.
    """
    url = f"https://api.github.com/search/issues?q=repo:{owner}/{repository}+type:pr+is:merged"
    headers = {"Authorization": f"Token {token}"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()["total_count"]
    else:
        raise Exception(f"Error fetching merged pull requests: {response.status_code}")

def get_repositories_details(owner, repository):
    """Busca os detalhes de um repositório pelo endpoint da API do GitHub.

    Parâmetros:
    - owner (str): proprietário/organização do repositório.
    - repository (str): nome do repositório.

    Retorna:
    - dict: JSON convertido para dicionário com os detalhes do repositório.

    Arremessa:
    - Exception: se a requisição HTTP não retornar status 200.
    """
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
    """Conta o número total de releases de um repositório paginando o endpoint de releases.

    Parâmetros:
    - owner (str): proprietário/organização do repositório.
    - repository (str): nome do repositório.

    Retorna:
    - int: número total de releases, após realizar a soma destas informações contidas em todas as páginas.

    Arremessa:
    - Exception: se alguma requisição HTTP de página retornar status diferente de 200.
    """
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
    """Calcula quantas horas se passaram desde a última atualização do repositório.

    Parâmetros:
    - repo_details (dict): dicionário com os detalhes do repositório (deve conter a chave "updated_at").

    Retorna:
    - float|int: número de horas (arredondado para baixo) desde a última atualização.
    """
    updated_at = repo_details["updated_at"]
    updated_at_dt = datetime.strptime(updated_at, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
    now = datetime.now(timezone.utc)
    total = now - updated_at_dt
    return total.total_seconds() // 3600

def get_primary_language(repo_details):
    """Retorna a linguagem de programação mais presente no repositório.

    Parâmetros:
    - repo_details (dict): dicionário com os detalhes do repositório (deve conter a chave "language").

    Retorna:
    - str|None: nome da linguagem de programação mais presente no repositório ou None se não houver.
    """
    return repo_details["language"]

def get_closed_issues(owner, repo):
    """Retorna a contagem de issues fechadas em um repositório.

    Parâmetros:
    - owner (str): proprietário/organização do repositório.
    - repo (str): nome do repositório.

    Retorna:
    - int: número total de issues fechadas conforme o campo "total_count" da resposta da API.

    Arremessa:
    - Exception: se a requisição HTTP não retornar status 200.
    """
    url = f"https://api.github.com/search/issues?q=repo:{owner}/{repo}+type:issue+state:closed"
    headers = {"Authorization": f"Token {token}"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()["total_count"]
    else:
        raise Exception(f"Failed to fetch closed issues: {response.status_code}")

def collect_and_save_repo_info(repos):
    """Coleta informações detalhadas de uma lista de repositórios e salva em um arquivo Excel.

    Parâmetros:
    - repos (list): lista de dicionários com informações dos repositórios; cada dicionário deve conter as chaves "full_name", "name" e "owner".

    Retorna:
    - None: função salva os dados em "repository_data.xlsx" e não retorna valor.

    Arremessa:
    - Exception: se alguma chamada à API feita durante a coleta falhar (propaga exceções das funções chamadoras).

    Observações:
    - Faz chamadas adicionais à API para cada repositório; insere um delay de 3 segundos entre requisições para suavizar a carga na API e não tomar timeout por excesso de requisições feitas em menos de 1 minuto.
    """
    rows = []

    for index, repo in enumerate(repos):
        print(f"Processing repository: {repo['full_name']}\nTotal remaining: {len(repos) - index - 1}")
        owner = repo["owner"]["login"]
        repo_name = repo["name"]

        repo_details = get_repositories_details(owner, repo_name)

        open_issues_count = repo_details["open_issues_count"]
        closed_issues_count = get_closed_issues(owner, repo_name)
        total_issues = open_issues_count + closed_issues_count
        closed_issues_percentage = round((closed_issues_count / total_issues * 100), 2) if total_issues > 0 else 0.0

        pull_requests_count = get_merged_pull_requests_count(owner, repo_name)
        releases_count = get_repository_releases_count(owner, repo_name)
        hours_since_last_update = get_hours_since_last_update(repo_details)
        primary_language = get_primary_language(repo_details)
        repo_age = round(get_repository_age_years(repo_details), 2)

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
    df.to_csv("repository_data.csv", index=False)


if __name__ == "__main__":
    try:
        popular_repos = get_popular_repositories(1000)
        collect_and_save_repo_info(popular_repos)
    except Exception as e:
        print(f"Error fetching popular repositories: {e}")
