
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "mimo_em_cesta.db"


def conectar():
    conexao = sqlite3.connect(DB_PATH)
    conexao.row_factory = sqlite3.Row
    conexao.execute("PRAGMA foreign_keys = ON")
    return conexao


def inicializar_banco():
    with conectar() as conexao:
        conexao.executescript("""
            CREATE TABLE IF NOT EXISTS clientes (
                id_cliente INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                telefone TEXT NOT NULL,
                email TEXT,
                data_cadastro TEXT NOT NULL
                    DEFAULT (datetime('now'))
            );

            CREATE TABLE IF NOT EXISTS modelos_cestas (
                id_modelo INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL UNIQUE,
                descricao TEXT,
                preco_base REAL NOT NULL
                    CHECK (preco_base >= 0),
                ativo INTEGER NOT NULL DEFAULT 1
                    CHECK (ativo IN (0, 1))
            );

            CREATE TABLE IF NOT EXISTS pedidos (
                id_pedido INTEGER PRIMARY KEY AUTOINCREMENT,
                id_cliente INTEGER NOT NULL,
                id_modelo INTEGER NOT NULL,
                personalizacao TEXT,
                valor_total REAL NOT NULL
                    CHECK (valor_total >= 0),
                data_entrega TEXT NOT NULL,
                endereco_entrega TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'Novo Pedido'
                    CHECK (status IN (
                        'Novo Pedido',
                        'Confirmado',
                        'Em Preparação',
                        'Pronto',
                        'Saiu para Entrega',
                        'Entregue'
                    )),
                forma_pagamento TEXT,
                FOREIGN KEY (id_cliente)
                    REFERENCES clientes(id_cliente),
                FOREIGN KEY (id_modelo)
                    REFERENCES modelos_cestas(id_modelo)
            );

            CREATE INDEX IF NOT EXISTS idx_pedidos_cliente
                ON pedidos(id_cliente);

            CREATE INDEX IF NOT EXISTS idx_pedidos_status
                ON pedidos(status);
        """)

        modelos = [
            ("Modelo 1 — Clássica", "Cesta clássica", 89.90),
            ("Modelo 2 — Especial", "Cesta especial", 119.90),
            ("Modelo 3 — Premium", "Cesta premium", 169.90)
        ]

        conexao.executemany(
            """
            INSERT OR IGNORE INTO modelos_cestas
                (nome, descricao, preco_base)
            VALUES (?, ?, ?)
            """,
            modelos
        )


if __name__ == "__main__":
    inicializar_banco()
    print("Banco de dados inicializado com sucesso!")
