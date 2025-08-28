# lab-experimentacao-01

Alunos: João Vitor Romero Sales e Lucas Randazzo

## Introdução

Este estudo investiga características de sistemas populares em repositórios de software do GitHub. O objetivo é compreender se alguns traços que costumam ser associados à popularidade realmente aparecem quando olhamos para os dados. Em especial, observamos aspectos relacionados a:

- ciclo de vida dos projetos (maturidade e frequência de atualização)
- colaboração da comunidade (contribuições externas e tratamento de issues)
- cadência de entrega (lançamento de releases)
- escolha de linguagem primária

Partimos de expectativas intuitivas sobre projetos populares e, na sequência, as confrontamos com evidências obtidas a partir dos dados. Em seguida, sintetizamos os resultados por valores medianos para embasar as conclusões de forma objetiva. Na última etapa, discutimos essas conclusões em comparação com as hipóteses levantadas, destacando convergências, divergências e possíveis explicações.

As expectativas iniciais (hipóteses) são:

- H1 (RQ01): Sistemas populares tendem a ser maduros/antigos, pois tiveram grande exposição (muitas visualizações) e contribuições ao longo do tempo; a popularidade pode estar associada a maior estrutura, boas práticas e documentação consolidada.
- H2 (RQ02): Sistemas populares recebem muita contribuição externa, devido à atuação de comunidades ativas que propõem novas funcionalidades, reportam bugs e sugerem melhorias.
- H3 (RQ03): Sistemas populares lançam releases com frequência, mantendo-se atualizados e funcionais, evitando depreciação e corrigindo eventuais bugs.
- H4 (RQ04): Sistemas populares são atualizados com frequência, em linha com a cadência de releases e a atividade contínua da comunidade.
- H5 (RQ05): Sistemas populares são escritos nas linguagens mais populares, tipicamente linguagens consolidadas como Java, C++ e PHP, ainda que não necessariamente na linguagem mais popular do momento (Python), acreditamos que estas estarão entre as 10 mais utilizadas.
- H6 (RQ06): Sistemas populares possuem alto percentual de issues fechadas, pois contam com muitos contribuidores ativos. Sendo assim, a proporção de issues encerradas em relação às abertas tende a ser maior.

## Metodologia

Para este estudo, adotamos duas abordagens complementares, primeiramente, elaboramos hipóteses informais (H1 a H6) que estão alinhadas com as questões de pesquisa definidas (RQ01 a RQ06). Depois, trabalhamos com o conjunto de dados bruto [repository_data.csv](data/repository_data.csv), extraindo as métricas diretamente das colunas disponíveis, como idade do repositório (repo_age_years), número de pull requests aceitos (merged_pull_requests_count), quantidade de releases (releases_count), tempo desde a última atualização em horas (hours_since_last_update) e percentual de issues fechadas (closed_issues_percentage). Vale destacar que, quando necessário, o percentual de issues fechadas foi calculado a partir das colunas closed_issues_count e open_issues_count, utilizando a fórmula closed / (closed + open) * 100. Para a questão de pesquisa 5 (RQ05), a distribuição das linguagens foi obtida pela contagem simples da coluna primary_language.

Com as métricas para cada repositório definidas, calculamos as estatísticas descritivas para as questões RQ01, RQ02, RQ03, RQ04, RQ05 e RQ06. Essas estatísticas incluíram a mediana, o número de casos válidos, mantendo as unidades originais (anos, horas e porcentagem). Paralelamente, utilizamos um arquivo com medianas agregadas [median_repository_data.csv](data/median_repository_data.csv)
 para validar e harmonizar os valores globais. A amostra analisada contou com 1.000 repositórios, e, caso algum dado estivesse ausente, ele foi excluído apenas da métrica correspondente, garantindo a integridade das demais análises.

## Resultados

Para análise, calculamos as medianas das métricas obtidas de uma amostra de 1.000 repositórios populares do GitHub. Os resultados estão apresentados a seguir:

1. RQ01. Sistemas populares são maduros/antigos?
	- Hipótese: Sim. Sistemas populares tendem a ser maduros/antigos em razão da ampla exposição e das contribuições acumuladas, estando geralmente mais estruturados, com boas práticas e documentação consolidada.
	- Mediana (idade, anos): 8.34

2. RQ02. Sistemas populares recebem muita contribuição externa?
	- Hipótese: Sim. A comunidade de sistemas populares é ativa, gerando ideias de novas funcionalidades, identificando bugs e propondo melhorias.
	- Mediana (PRs mergeados): 688

3. RQ03. Sistemas populares lançam releases com frequência?
	- Hipótese: Sim. Lançam releases com frequência para manter-se atualizados e funcionais e para corrigir eventuais bugs.
	- Mediana (releases): 35

4. RQ04. Sistemas populares são atualizados com frequência?
	- Hipótese: Sim. Em consonância com releases frequentes e com uma comunidade ativa, as atualizações ocorrem com regularidade (melhorias, correções e novas funcionalidades).
	- Mediana (horas desde última atualização): 1.0 hora

5. RQ05. Sistemas populares são escritos nas linguagens mais populares?
	- Hipótese: Sim. Predominam linguagens populares e consolidadas (por exemplo, Java, C++ e PHP); mesmo que não na linguagem mais popular do momento, costumam figurar entre as 10 mais utilizadas.
	- Mediana (linguagem primária): MDX, mas não é adequada para esta análise, pois acreditamos que ela não é uma métrica eficaz para determinar se a linguagem principal dos repositórios analisados está entre as mais populares. Para esse fim, consideramos mais apropriado utilizar o somatório da quantidade de repositórios que possuem cada linguagem como principal.
	- Distribuição de linguagens (contagem de repositórios). Top 5 em negrito.

| **Linguagem** | **Popularidade em 2024** | **Contagem** |
|-----------|----------|----------|
| **Python** | 1º | 188 |
| **TypeScript** | 3º | 156 |
| **JavaScript** | 2º | 130 |
| **não informado** | Não se aplica | 104 |
| **Go** | 10º | 73 |
| Java | 4º | 50 |
| C++ | 6º | 47 |
| Rust | 20º | 45 |
| C | 9º | 25 |
| Jupyter Notebook | Não se aplica | 22 |

6. RQ06. Sistemas populares possuem um alto percentual de issues fechadas?
	- Hipótese: Sim. Como muitas contribuições partem de issues, é esperado um alto percentual de issues fechadas após a integração das mudanças.
	- Mediana (percentual de issues fechadas): 82.42%

[Arquivo de dados dos repositórios retornados pela API](data/repository_data.csv "Dados retornados pela chamada da API")

## Discussão

H1 (maturidade): A mediana de 8,34 anos indica que os projetos têm vários anos de existência, o que sustenta a hipótese de que repositórios populares tendem a ser maduros. Esse tempo de atividade sugere uma trajetória consolidada.

H2 (contribuições externas): A mediana de 688 PRs mergeados é significativa e indica uma colaboração ativa consistente. Esse número elevado reforça a hipótese.

H3 (releases frequentes): A mediana de 35 releases aponta para um histórico razoável de empacotamentos formais. Não podemos concluir sobre cadência temporal (faltam intervalos), mas o volume mediano sugere prática de versionamento relativamente ativa.

H4 (atualizações recentes): A mediana de 1 hora desde a última atualização indica forte atividade contínua, reforçando fortemente a hipótese de atualização frequente.

H5 (linguagens populares): A distribuição mostra domínio de Python, TypeScript e JavaScript, seguidos por “não informado” e Go. Linguagens clássicas previstas (Java, C++, PHP) aparecem fora do top 5 (Java em 6º, C++ em 7º e PHP em 19º), sinalizando deslocamento do núcleo de popularidade para ecossistemas web e data/AI modernos. A hipótese é parcialmente suportada: ainda são linguagens amplamente usadas, mas a centralidade de Python/TypeScript/JavaScript/Go supera as citadas na hipótese.

H6 (issues fechadas): O percentual mediano de 82,42% é alto e sugere boa taxa de resolução, apoiando a hipótese. Valores próximos de 100% aparecem em alguns repositórios, indicando possível variação significativa entre os casos.

Outliers e dados ausentes: A ausência de linguagem primária em 104 repositórios (10,4%) pode influenciar análise de RQ05. Sem quartis, a interpretação de variabilidade fica limitada. Repositórios com atividade extremamente recente (horas=0) podem puxar a mediana de atualização para baixo, reforçando a percepção de alta atividade.

Síntese: A maioria das hipóteses (H1, H2, H4, H6) é suportada diretamente pelos valores medianos observados. H3 e H5 recebem suporte parcial condicionado a interpretação (releases sem cadência temporal e mudança no perfil de linguagens dominantes).

## Trabalhos Relacionados

Tomando como referência os limiares estabelecidos por **Coelho et al. (2020)** no artigo *"Is this GitHub Project Maintained? Measuring the Level of Maintenance Activity of Open-Source Projects"*. O objetivo central dos autores foi propor e validar a métrica **Level of Maintenance Activity (LMA)**, construída a partir de séries temporais de indicadores de repositórios no GitHub (commits, issues, pull requests, releases e atividade de contribuidores). Essa métrica procura responder a uma questão recorrente na literatura: como distinguir, de forma automática e confiável, projetos mantidos de projetos abandonados.

O modelo de LMA desenvolvido por Coelho et al. utiliza múltiplos atributos para gerar um índice contínuo de **0 a 100**, no qual valores mais altos indicam maior probabilidade de um projeto ser mantido ativamente. No conjunto de validação do estudo, projetos com LMA acima de **82 (mediana)** foram classificados como mantidos, enquanto valores próximos ou abaixo de **48 (Q1)** caracterizaram inatividade. O **Q3 (97)** representou projetos com manutenção muito intensa.

A **Figura 1** apresenta a comparação entre o percentual de issues fechadas da nossa amostra e os limiares de LMA descritos pelos autores. Embora nossa coleta não permita calcular o índice LMA diretamente (por exigir séries temporais completas), o percentual de issues fechadas atua como proxy relevante da capacidade de manutenção. O valor mediano obtido foi de **82,4%**, praticamente idêntico à mediana do LMA (82) reportada no artigo. Esse resultado sugere que os repositórios analisados apresentam padrões de resolução de issues compatíveis com aqueles que o estudo classificou como ativamente mantidos.

![Figura 1. Percentual de issues fechadas em comparação com os limiares de LMA descritos por Coelho et al. (2020).](graphs/closed_issues.png)

A **Figura 2** mostra o tempo decorrido desde a última atualização, em horas. Em nossos dados, a mediana foi de apenas **1 hora** desde a última atualização, ao passo que, segundo Coelho et al. (2020), limiares clássicos de inatividade consideram **30 dias (720h)** como ponto de atenção e **1 ano (8760h)** como forte sinal de abandono. Ainda que a métrica de LMA incorpore não apenas a última atualização, mas também a consistência da atividade ao longo do tempo, a discrepância encontrada é evidente: os repositórios analisados apresentam atualização substancialmente mais frequente que os parâmetros de referência, reforçando sua caracterização como plenamente ativos.

![Figura 2. Recência de atualização dos repositórios em horas.](graphs/update_recency.png)

A **Figura 3** apresenta o throughput de manutenção (isto é, a quantidade média de entregas e contribuições integradas por ano), considerando a cadência de releases e pull requests mesclados. Observamos uma média de **≈ 4,2 releases/ano** e **≈ 82,5 PRs/ano** em nossa amostra. Embora o artigo de Coelho et al. (2020) não estabeleça limiares fixos para essas métricas isoladamente, os autores destacam que a cadência de releases e a absorção de contribuições externas são componentes-chave do LMA, refletindo a vitalidade de um projeto. Assim, mesmo sem o cálculo formal do índice, nossos resultados reforçam que a amostra se aproxima do perfil de projetos com LMA elevado.

![Figura 3. Throughput de manutenção: cadência de releases e pull requests mesclados.](graphs/throughput_maintence.png)

Ao relacionar as métricas coletadas com os limiares propostos por **Coelho et al. (2020)**, verificamos que os repositórios minerados apresentam características compatíveis com projetos altamente mantidos, situando-se entre a **mediana (82)** e o **terceiro quartil (97)** do LMA. A alta taxa de fechamento de issues, a recência extrema das atualizações e o ritmo constante de releases e pull requests corroboram a presença de manutenção contínua e engajamento da comunidade, o que reforça a validade dos nossos resultados frente à literatura.

## Referências

GitHub Innovation Graph. Programming Languages metric. Disponível em: https://innovationgraph.github.com/global-metrics/programming-languages#programming-languages-rankings. Acesso em: 24 de agosto de 2025.

COELHO, F.; WERMELINGER, M.; MELO, F. de; VALENTE, M. T. Is this GitHub Project Maintained? Measuring the Level of Maintenance Activity of Open-Source Projects. In: Proceedings of the 17th International Conference on Mining Software Repositories (MSR '20). ACM, 2020.
