import requests
from dotenv import load_dotenv
import os

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