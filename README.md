# API Simples de Gestão de Estudantes

## Esta é uma API RESTful simples, construída com Python e Flask, para gerir um registo de estudantes. Permite criar, listar e consultar estudantes, armazenando os dados numa base de dados SQLite.

## Este projeto foi desenvolvido como um exercício prático para avaliar conceitos de lógica de programação, sintaxe, manipulação de estruturas de dados simples e desenvolvimento de APIs.
### Funcionalidades

    Registar Estudante: Adiciona um novo estudante com nome e nota.

    Listar Estudantes: Retorna uma lista de todos os estudantes registados.

    Consultar Estudante por ID: Retorna os dados de um estudante específico.

    Validação de Dados: Garante que a nota de um estudante esteja sempre entre 0 e 10.

    Lógica Personalizada: Para cada estudante retornado, calcula a primeira letra do nome que não se repete.

### Tecnologias Utilizadas

    Python3: Linguagem de programação principal.

    Flask: Micro-framework web para a criação da API.

    SQLite: Base de dados SQL para armazenamento persistente dos dados.

### Pré-requisitos

Antes de começar, garanta que tem o seguinte software instalado:

    Python 3.8+

    venv (normalmente incluído com a instalação do Python)

### Configuração do Projeto

Siga os passos abaixo para configurar o ambiente de desenvolvimento.

    Clone o repositório (ou crie a pasta do projeto):

    git clone https://... 
    cd nome-da-pasta

    Crie e ative um ambiente virtual:

        No macOS/Linux (Bash):

        python3 -m venv venv
        source venv/bin/activate

        No macOS/Linux (Fish):

        python3 -m venv venv
        source venv/bin/activate.fish

        No Windows:

        python -m venv venv
        .\venv\Scripts\activate

    Instale as dependências:

    pip install Flask

### Como Executar a API

Com o ambiente virtual ativado, execute o seguinte comando no terminal para iniciar o servidor:

python api.py

O servidor estará rodando em http://127.0.0.1:5000/students

### Endpoints da API

A seguir estão detalhados os endpoints disponíveis.
1. Registar um Estudante

    Método: POST

    URL: /students

    Descrição: Cria um novo registo de estudante.

    Corpo da Requisição (JSON):

    {
        "name": "Nome do Estudante",
        "grade": 8
    }

    Respostas:

        201 Created (Sucesso):

        {
            "message": "Student created successfully"
        }

        400 Bad Request (Erro de validação):

        {
            "error": "Grade must be between 0 and 10"
        }

        {
            "error": "Missing or invalid name/grade field"
        }

2. Listar todos os Estudantes

    Método: GET

    URL: /students

    Descrição: Retorna uma lista com todos os estudantes registados.

    Resposta (200 OK):

    [
        {
            "id": 1,
            "name": "Ana",
            "grade": 9,
            "first_non_repeating": "_"
        },
        {
            "id": 2,
            "name": "Bruno",
            "grade": 7,
            "first_non_repeating": "b"
        }
    ]

3. Obter um Estudante por ID

    Método: GET

    URL: /students/<id>

    Descrição: Retorna os dados de um estudante específico.

    Respostas:

        200 OK (Sucesso):

        {
            "id": 2,
            "name": "Bruno",
            "grade": 7,
            "first_non_repeating": "b"
        }

        404 Not Found (Estudante não encontrado):

        {
            "error": "Student not found"
        }

### Como Testar (usando curl)

Abra um novo terminal (deixe o servidor a correr no primeiro) e use os seguintes comandos:

    Registar um novo estudante:

    curl -X POST -H "Content-Type: application/json" -d '{"name": "Carlos", "grade": 10}' [http://127.0.0.1:5000/students](http://127.0.0.1:5000/students)

    Listar todos os estudantes:

    curl [http://127.0.0.1:5000/students](http://127.0.0.1:5000/students)

    Obter o estudante com ID 1:

    curl [http://127.0.0.1:5000/students/1](http://127.0.0.1:5000/students/1)

