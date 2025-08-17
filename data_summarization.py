import pandas as pd

df = pd.read_csv("repository_csv")

def median_repository_age(df):
    """Calcula a mediana da idade dos repositórios.

    Parâmetros:
    - df (pd.DataFrame): DataFrame contendo os dados dos repositórios.

    Retorna:
    - float: mediana da idade dos repositórios em anos com 2 casas decimais.
    """
    return round(df["repo_age_years"].median(), 2)

def median_merged_pull_requests_count(df):
    """Calcula a mediana do número de pull requests mergeados.

    Parâmetros:
    - df (pd.DataFrame): DataFrame contendo os dados dos repositórios.

    Retorna:
    - float: mediana do número de pull requests mergeados com 2 casas decimais.
    """
    return round(df["merged_prs_count"].median(), 2)

def median_releases_count(df):
    """Calcula a mediana do número de releases.

    Parâmetros:
    - df (pd.DataFrame): DataFrame contendo os dados dos repositórios.

    Retorna:
    - float: mediana do número de releases com 2 casas decimais.
    """
    return round(df["releases_count"].median(), 2)