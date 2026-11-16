
# Mimo em Cesta

Sistema web de gerenciamento de clientes e pedidos de cestas personalizadas, desenvolvido como projeto de extensão acadêmica.

## Objetivo

Facilitar a organização das encomendas, centralizando informações de clientes, pedidos e acompanhamento das entregas.

## Funcionalidades implementadas

- Cadastro de clientes.
- Cadastro de pedidos.
- Listagem de pedidos.
- Atualização do status das encomendas.
- Armazenamento de dados em SQLite.
- Interface responsiva.

## Tecnologias utilizadas

- Python 3.14
- Flask
- SQLite
- HTML5
- CSS3
- Jinja2
- Git e GitHub

## Como executar no Windows

Clone o repositório:

```powershell
git clone https://github.com/augustodoso/mimo-em-cesta.git
cd mimo-em-cesta
```

Crie e ative o ambiente virtual:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Instale as dependências:

```powershell
pip install -r requirements.txt
```

Configure a chave secreta:

```powershell
$env:SECRET_KEY = (python -c "import secrets; print(secrets.token_hex(32))")
```

Execute a aplicação:

```powershell
python app.py
```

Acesse http://127.0.0.1:5000 no navegador.

O banco de dados será criado automaticamente.

## Estado do projeto

MVP em desenvolvimento para fins acadêmicos. A versão atual destina-se a testes locais com dados fictícios.

A autenticação administrativa e outras melhorias de segurança ainda serão implementadas.
