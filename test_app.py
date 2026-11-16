
import os
import tempfile
from pathlib import Path

os.environ.setdefault("SECRET_KEY", "chave-exclusiva-de-teste")

import database

pasta_temporaria = tempfile.TemporaryDirectory()
database.DB_PATH = Path(pasta_temporaria.name) / "teste.db"

from app import app

app.config["TESTING"] = True
client = app.test_client()


def test_dashboard():
    assert client.get("/").status_code == 200


def test_clientes():
    assert client.get("/clientes").status_code == 200


def test_novo_pedido():
    assert client.get("/novo-pedido").status_code == 200


def test_pedidos():
    assert client.get("/pedidos").status_code == 200


def test_cadastro_cliente():
    resposta = client.post("/clientes", data={
        "nome": "Cliente Teste",
        "telefone": "83999999999",
        "email": "teste@example.com"
    })
    assert resposta.status_code == 302


def test_cliente_invalido():
    resposta = client.post("/clientes", data={})
    assert resposta.status_code == 200


def test_status_invalido():
    resposta = client.post(
        "/pedidos/1/status",
        data={"status": "Invalido"}
    )
    assert resposta.status_code == 302
