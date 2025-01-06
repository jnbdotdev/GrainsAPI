# **GrainsAPI - API de Parcelas Geográficas**

A GrainsAPI é uma API que permite a criação e consulta de parcelas geográficas (representadas por polígonos) armazenadas em um banco de dados PostgreSQL com suporte a geometria espacial (usando o PostGIS). A API fornece endpoints para criar novas parcelas e consultar parcelas dentro de uma área específica utilizando o conceito de bounding box (caixa delimitadora).

----------

## **Índice**

1.  [Pré-requisitos](https://chatgpt.com/c/677babc3-e094-800e-946b-601bde2e5f1e#pr%C3%A9-requisitos)
2.  [Instalação](https://chatgpt.com/c/677babc3-e094-800e-946b-601bde2e5f1e#instala%C3%A7%C3%A3o)
3.  [Configuração do Banco de Dados](https://chatgpt.com/c/677babc3-e094-800e-946b-601bde2e5f1e#configura%C3%A7%C3%A3o-do-banco-de-dados)
4.  [Executando a API](https://chatgpt.com/c/677babc3-e094-800e-946b-601bde2e5f1e#executando-a-api)
5.  [Endpoints](https://chatgpt.com/c/677babc3-e094-800e-946b-601bde2e5f1e#endpoints)
    -   [POST /parcels](https://chatgpt.com/c/677babc3-e094-800e-946b-601bde2e5f1e#post-parcels)
    -   [GET /parcels](https://chatgpt.com/c/677babc3-e094-800e-946b-601bde2e5f1e#get-parcels)
6.  [Estrutura do Projeto](https://chatgpt.com/c/677babc3-e094-800e-946b-601bde2e5f1e#estrutura-do-projeto)
7.  [Testes Automatizados](https://chatgpt.com/c/677babc3-e094-800e-946b-601bde2e5f1e#testes-automatizados)
8.  [Contribuindo](https://chatgpt.com/c/677babc3-e094-800e-946b-601bde2e5f1e#contribuindo)

----------

## **Pré-requisitos**

Antes de rodar a API, você precisa garantir que tenha as seguintes ferramentas instaladas:

-   **Python 3.7+**: A API foi construída usando Python.
-   **PostgreSQL com PostGIS**: Banco de dados PostgreSQL com a extensão PostGIS instalada.
-   **pip**: O gerenciador de pacotes Python.

----------

## **Instalação**

1.  **Clone o repositório**:
    
    ```bash
    git clone https://github.com/seu_usuario/GrainsAPI.git
    cd GrainsAPI
    
    ```
    
2.  **Crie um ambiente virtual** (opcional, mas recomendado):
    
    ```bash
    python -m venv venv
    
    ```
    
3.  **Ative o ambiente virtual**:
    
    -   No Windows:
        
        ```bash
        .\venv\Scripts\activate
        
        ```
        
    -   No Linux/macOS:
        
        ```bash
        source venv/bin/activate
        
        ```
        
4.  **Instale as dependências**:
    
    ```bash
    pip install -r requirements.txt
    
    ```
    

----------

## **Configuração do Banco de Dados**

A API requer um banco de dados PostgreSQL com a extensão PostGIS. Siga os passos abaixo para configurar o banco de dados:

1.  **Crie o banco de dados no PostgreSQL**:
    
    ```sql
    CREATE DATABASE grainsdatabase;
    
    ```
    
2.  **Instale a extensão PostGIS**: No banco de dados `grainsdatabase`, execute o comando:
    
    ```sql
    CREATE EXTENSION postgis;
    
    ```
    
3.  **Configure a string de conexão no arquivo `database.py`**: Abra o arquivo `app/database.py` e edite a variável `DATABASE_URL` para apontar para o seu banco de dados:
    
    ```python
    DATABASE_URL = "postgresql://postgres:root123@localhost/grainsdatabase"
    
    ```
    
4.  **Crie as tabelas no banco de dados**: Acesse a API e rode a criação das tabelas:
    
    ```bash
    uvicorn app.main:app --reload
    
    ```
    
    Isso automaticamente cria as tabelas no banco de dados PostgreSQL.
    

----------

## **Executando a API**

Para rodar a API, basta executar o servidor utilizando o Uvicorn:

```bash
uvicorn app.main:app --reload

```

Isso iniciará o servidor na URL `http://127.0.0.1:8000`. O parâmetro `--reload` permite que as alterações no código sejam aplicadas automaticamente sem a necessidade de reiniciar o servidor.

----------

## **Endpoints**

### **POST /parcels**

Este endpoint cria uma nova parcela no banco de dados.

#### **Requisição**

-   **Método**: `POST`
-   **URL**: `/parcels`
-   **Body**: JSON com os seguintes campos:
    -   `name`: Nome da parcela (string)
    -   `owner`: Nome do proprietário (string)
    -   `geometry`: Coordenadas do polígono em formato WKT (String)

Exemplo de Requisição:

```json
{
  "name": "Parcela de milho",
  "owner": "BRF",
  "geometry": "POLYGON((2 5, 5 2, 2 5, 5 2, 4 4))"
}

```

#### **Resposta**

-   **Status**: 200 OK
-   **Body**:
    
    ```json
    {
      "id": "b637e925-79a2-4d46-844c-1f39d0cb67f9",
      "name": "Parcela de milho",
      "owner": "BRF"
    }
    
    ```
    

### **GET /parcels**

Este endpoint consulta as parcelas dentro de uma área especificada por um bounding box (caixa delimitadora).

#### **Requisição**

-   **Método**: `GET`
-   **URL**: `/parcels?minx=<min_x>&miny=<min_y>&maxx=<max_x>&maxy=<max_y>`
    -   `minx`: Proporção/Coordenada mínima X (longitude inferior).
    -   `miny`: Proporção/Coordenada mínima Y (latitude inferior).
    -   `maxx`: Proporção/Coordenada máxima X (longitude superior).
    -   `maxy`: Proporção/Coordenada máxima Y (latitude superior).

Exemplo de Requisição:

```
GET /parcels?minx=-100&miny=-100&maxx=100&maxy=100

```

#### **Resposta**

-   **Status**: 200 OK
-   **Body**:
    
    ```json
    [
      {
        "id": "b637e925-79a2-4d46-844c-1f39d0cb67f9",
        "name": "Parcela de trigo",
        "owner": "BRF"
      }
    ]
    
    ```
    

----------

## **Estrutura do Projeto**

### **app/**

-   `main.py`: Arquivo principal que configura a API com FastAPI e define os endpoints.
-   `crud.py`: Contém as funções que interagem com o banco de dados (CRUD - Create, Read, Update, Delete).
-   `schemas.py`: Define os esquemas de dados (modelos Pydantic) para entrada e saída de dados.
-   `models.py`: Define os modelos de banco de dados (SQLAlchemy).
-   `database.py`: Configura o banco de dados e a sessão de conexão.

### **test/**

-   `test_main.py`: Arquivo de testes para os endpoints da API utilizando o `pytest` e `TestClient` do FastAPI.

### **requirements.txt**

-   Arquivo que lista as dependências do projeto, como `fastapi`, `sqlalchemy`, `psycopg2`, `uvicorn`, `pytest`.

----------

## **Testes Automatizados**

Para rodar os testes automatizados, utilize o `pytest`:

1.  **Instale o `pytest`** (se ainda não instalado):
    
    ```bash
    pip install pytest
    
    ```
    
2.  **Rodar os testes**:
    
    ```bash
    pytest
    
    ```
    

Os testes estão na pasta `test/` e verificam se os endpoints estão funcionando corretamente.

----------

## **Contribuindo**

Sinta-se à vontade para contribuir com melhorias ou correções. Para isso:

1.  Faça um fork do repositório.
2.  Crie uma branch para sua feature ou correção.
3.  Envie um pull request com uma descrição detalhada da mudança.
