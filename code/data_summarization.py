import pandas as pd

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
    return round(df["merged_pull_requests_count"].median(), 2)

def median_releases_count(df):
    """Calcula a mediana do número de releases.

    Parâmetros:
    - df (pd.DataFrame): DataFrame contendo os dados dos repositórios.

    Retorna:
    - float: mediana do número de releases com 2 casas decimais.
    """
    return round(df["releases_count"].median(), 2)

def median_hours_since_last_update(df):
    """Calcula a mediana do número de horas desde a última atualização.

    Parâmetros:
    - df (pd.DataFrame): DataFrame contendo os dados dos repositórios.

    Retorna:
    - float: mediana do número de horas desde a última atualização com 2 casas decimais.
    """
    return round(df["hours_since_last_update"].median(), 2)

def median_primary_language(df):
    """Calcula a mediana do número de linguagens principais.

    Parâmetros:
    - df (pd.DataFrame): DataFrame contendo os dados dos repositórios.

    Retorna:
    - float: mediana do número de linguagens principais com 2 casas decimais.
    """
    freq = df["primary_language"].value_counts().sort_index()
    median_idx = int((len(freq) - 1) / 2)
    return freq.index[median_idx]

def median_closed_issues_percentage(df):
    """Calcula a mediana da porcentagem de issues fechadas.

    Parâmetros:
    - df (pd.DataFrame): DataFrame contendo os dados dos repositórios.

    Retorna:
    - float: mediana da porcentagem de issues fechadas com 2 casas decimais.
    """
    return round(df["closed_issues_percentage"].median(), 2)

def main():
    df = pd.read_csv("data/repository_data.csv")

    median_data = {
        "median_repository_age": median_repository_age(df),
        "median_merged_pull_requests": median_merged_pull_requests_count(df),
        "median_releases": median_releases_count(df),
        "median_hours_since_last_update": median_hours_since_last_update(df),
        "median_primary_language": median_primary_language(df),
        "median_closed_issues_percentage": median_closed_issues_percentage(df)
    }
    median_df = pd.DataFrame([median_data])
    median_df.to_csv("data/median_repository_data.csv", index=False)

if __name__ == "__main__":
    main()
