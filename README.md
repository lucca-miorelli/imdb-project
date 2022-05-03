# Monitorando Tweets sobre os Top 1000 Filmes do IMDb

## Sobre:

A ideia de buscar tweets sobre filmes surgiu da curiosidade dos membros em consultar a opinião pública nas redes sociais acerca de filmes bem renomeados pela crítica, ao longo do tempo. 

O projeto consiste em uma Pipeline de ETL orquestrada pelo Apache Airflow, responsável pelas seguintes etapas.
* Extrair dados do dataset fixo de Top 1000 Filmes do IMDb, disponível no [Kaggle](https://www.kaggle.com/datasets/harshitshankhdhar/imdb-dataset-of-top-1000-movies-and-tv-shows).
* Coletar e contar tweets contendo o título dos filmes no Twitter, através da API para Python - tweepy.
* Transformar e carregar os dados da rede social em duas tabelas distintas:
    * Tweets contendo o título do filme.
    * Contagem de tweets por dia por filme.

As ferramentas utilizadas foram:
* **Amazon Relational Database Service:** banco de dados relacional PostgreSQL para armazenar os dados tratados.
* **Apache Airflow:** orquestrador para rodar o Pipeline com frequência desejada.
* **Docker / Docker Compose:** para rodar o Airflow em um contâiner local, podendo qualquer um utilizá-lo a partir deste repositório.

A arquitetura do projeto é ilustrada no diagrama abaixo:
![imdb_diagram](https://github.com/lucca-miorelli/imdb-project/blob/main/imdb_diagram.jpg)

Este projeto é resultado do desafio final da mentoria de Engenharia de Dados da Poatek, com o principal objetivo de estudar as ferramentas e aprender na prática.


## Pré-requisitos:
- Instalar Docker do [site oficial.](https://docs.docker.com/get-docker/)
- Instalar Docker Compose do [site oficial.](https://docs.docker.com/compose/install/)
- Configurar conta de desenvolvedor para[ API do Twitter.](https://twitter.com/i/flow/login?input_flow_data=%7B%22requested_variant%22%3A%22eyJyZWRpcmVjdF9hZnRlcl9sb2dpbiI6Imh0dHBzOi8vZGV2ZWxvcGVyLnR3aXR0ZXIuY29tL2VuL3BvcnRhbC9wZXRpdGlvbi9lc3NlbnRpYWwvYmFzaWMtaW5mbyJ9%22%7D)
- Instalar as bibliotecas que estão listadas no arquivos **requirements.txt**. Sugerimos primeiro criar um ambiente virtual para isso.

```bash
python -m venv .env
(.env) pip install -r requirements.txt # Tenha certeza de estar com o ambiente virtual ativo.
```


## Como usar este projeto?

1. Seu diretório deve ficar parecido com este exemplo:

    ```
    ├── ...  
    ├── airflow-docker
    │   ├── dags
    │   │   ├── tweets_processing_dag.py
    │   │   ├── get_counts_to_dataframe.py
    │   │   ├── get_recent_tweets_to_dataframe.py
    │   ├── dag_variables.json
    │   ├── docker-compose.yaml
    ├── code
    ├── ...    
    ```
    
    - **tweets_processing_dag.py**: é o arquivo lido pelo Airflow para orquestrar o Pipeline.
    - **get_recent_tweets_to_dataframe.py** e **get_counts_to_dataframe.py**: são arquivos com funções auxiliares.
    - **dag_variables.json**: é um arquivo *json* que armazena variáveis necessárias para a DAG, como credenciais da API ou da AWS.
    - **docker-compose.yaml**: é a imagem responsável por rodar o Airflow em contâiner.

2. Faça download da imagem *.yaml*.

    ```bash
    curl -LfO 'https://airflow.apache.org/docs/apache-airflow/stable/docker-compose.yaml'
    ```

3. Utilize os comandos do Docker para rodar ou parar o contâiner:

    ```bash
    docker-compose up -d    # iniciar
    docker-compose down     # parar
    ```

4. Utilize a UI Web se necessário na porta padrão: [http://localhost:8080](http://localhost:8080)

5. Para olhar acessar o dashboard:
    - Adapte a query dentro do arquivo **tweets_counts** dentro de *visualization* para o seu banco, seja ele local ou na nuvem.
    - Rode o arquivo **tweets_counts**.
    - Entre na porta padrão: [http://localhost:8050](http://localhost:8050).