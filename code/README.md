# Documentação do Código

Documentação técnica dos módulos `repository_extractor.py` e `data_summarization.py`.

---

## repository_extractor.py

### Propósito
Extração de dados dos repositórios mais populares do GitHub via API. Busca repositórios ordenados por estrelas e coleta métricas detalhadas, salvando em CSV.

### Funções

#### `get_popular_repositories(num_repos)`
- **Parâmetros:** `num_repos` (int) - máximo de repositórios (limite: 1000)
- **Retorno:** Lista de dicionários com dados dos repositórios
- **Funcionalidade:** Paginação automática, delay de 2s entre requisições para não estourar o limite, busca por `stars:>0` (repositórios com mais estrelas no GitHub)

#### `get_repositories_details(owner, repository)`
- **Parâmetros:** `owner` (str), `repository` (str)
- **Retorno:** Dicionário com detalhes completos do repositório
- **Funcionalidade:** Acessa endpoint `/repos/{owner}/{repo}` da API

#### `get_repository_age_years(repo_details)`
- **Parâmetros:** `repo_details` (dict) - deve conter `created_at`
- **Retorno:** Idade em anos (float)
- **Funcionalidade:** Calcula diferença entre `created_at` e data atual

#### `get_merged_pull_requests_count(owner, repository)`
- **Parâmetros:** `owner` (str), `repository` (str)
- **Retorno:** Número total de PRs mergeados (int)
- **Funcionalidade:** API de busca com filtro `type:pr+is:merged`

#### `get_repository_releases_count(owner, repository)`
- **Parâmetros:** `owner` (str), `repository` (str)
- **Retorno:** Número total de releases (int)
- **Funcionalidade:** Paginação para contar todas as releases

#### `get_hours_since_last_update(repo_details)`
- **Parâmetros:** `repo_details` (dict) - deve conter `updated_at`
- **Retorno:** Horas desde última atualização (int)
- **Funcionalidade:** Diferença entre `updated_at` e agora, em horas

#### `get_primary_language(repo_details)`
- **Parâmetros:** `repo_details` (dict) - deve conter `language`
- **Retorno:** Nome da linguagem principal (str|None)
- **Funcionalidade:** Retorna campo `language` diretamente

#### `get_closed_issues(owner, repo)`
- **Parâmetros:** `owner` (str), `repo` (str)
- **Retorno:** Número de issues fechadas (int)
- **Funcionalidade:** API de busca com filtro `type:issue+state:closed`

#### `collect_and_save_repo_info(repos)`
- **Parâmetros:** `repos` (list) - lista de dicionários com info básica dos repositórios
- **Retorno:** None (salva em `repository_data.csv`)
- **Funcionalidade:** Coleta métricas de cada repositório, calcula percentuais, delay de 3s

---

## data_summarization.py

### Propósito
Cálculo de estatísticas de mediana sobre os dados coletados. Lê o CSV do extrator e gera resumo estatístico.

### Funções

#### `median_repository_age(df)`
- **Parâmetros:** `df` (DataFrame) - dados dos repositórios
- **Retorno:** Mediana da idade em anos (float, 2 casas decimais)
- **Funcionalidade:** Mediana da coluna `repo_age_years`

#### `median_merged_pull_requests_count(df)`
- **Parâmetros:** `df` (DataFrame)
- **Retorno:** Mediana de PRs mergeados (float, 2 casas decimais)
- **Funcionalidade:** Mediana da coluna `merged_pull_requests_count`

#### `median_releases_count(df)`
- **Parâmetros:** `df` (DataFrame)
- **Retorno:** Mediana de releases (float, 2 casas decimais)
- **Funcionalidade:** Mediana da coluna `releases_count`

#### `median_hours_since_last_update(df)`
- **Parâmetros:** `df` (DataFrame)
- **Retorno:** Mediana de horas desde última atualização (float, 2 casas decimais)
- **Funcionalidade:** Mediana da coluna `hours_since_last_update`

#### `median_primary_language(df)`
- **Parâmetros:** `df` (DataFrame)
- **Retorno:** Linguagem na posição mediana (str)
- **Funcionalidade:** Linguagem na posição do índice mediano da distribuição de frequências

#### `median_closed_issues_percentage(df)`
- **Parâmetros:** `df` (DataFrame)
- **Retorno:** Mediana da porcentagem de issues fechadas (float, 2 casas decimais)
- **Funcionalidade:** Mediana da coluna `closed_issues_percentage`
