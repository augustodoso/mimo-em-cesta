
import os
from datetime import date
from decimal import Decimal, InvalidOperation

from flask import (
    Flask, render_template, request,
    redirect, url_for, flash
)

from database import conectar, inicializar_banco

app = Flask(__name__)
app.secret_key = os.environ["SECRET_KEY"]


inicializar_banco()

STATUS_PEDIDOS = [
    "Novo Pedido",
    "Confirmado",
    "Em Preparação",
    "Pronto",
    "Saiu para Entrega",
    "Entregue",
]


@app.route("/")
def dashboard():
    return render_template("dashboard.html")


@app.route("/clientes", methods=["GET", "POST"])
def clientes():
    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        telefone = request.form.get("telefone", "").strip()
        email = request.form.get("email", "").strip()

        if not nome or not telefone:
            flash("Informe nome e telefone.", "erro")
        elif len(nome) > 120 or len(telefone) > 20 or len(email) > 150:
            flash("Verifique o tamanho dos campos.", "erro")
        else:
            with conectar() as conexao:
                conexao.execute(
                    """
                    INSERT INTO clientes (nome, telefone, email)
                    VALUES (?, ?, ?)
                    """,
                    (nome, telefone, email or None)
                )

            flash("Cliente cadastrado com sucesso!", "sucesso")
            return redirect(url_for("clientes"))

    with conectar() as conexao:
        lista = conexao.execute(
            """
            SELECT id_cliente, nome, telefone, email
            FROM clientes
            ORDER BY id_cliente DESC
            """
        ).fetchall()

    return render_template("clientes.html", clientes=lista)


@app.route("/novo-pedido", methods=["GET", "POST"])
def novo_pedido():
    with conectar() as conexao:
        clientes = conexao.execute(
            "SELECT id_cliente, nome FROM clientes ORDER BY nome"
        ).fetchall()

        modelos = conexao.execute(
            """
            SELECT id_modelo, nome, preco_base
            FROM modelos_cestas
            WHERE ativo = 1
            ORDER BY id_modelo
            """
        ).fetchall()

    if request.method == "POST":
        try:
            cliente_id = int(request.form.get("cliente", ""))
            modelo_id = int(request.form.get("modelo", ""))

            valor = Decimal(
                request.form.get("valor", "").replace(",", ".")
            )

            data_entrega = request.form.get("data_entrega", "")
            endereco = request.form.get("endereco", "").strip()
            personalizacao = request.form.get(
                "personalizacao", ""
            ).strip()

            if (
                not valor.is_finite()
                or valor < 0
                or valor.as_tuple().exponent < -2
            ):
                raise ValueError("Valor inválido")

            if not endereco or len(endereco) > 250:
                raise ValueError("Endereço inválido")

            if len(personalizacao) > 500:
                raise ValueError("Personalização inválida")

            if date.fromisoformat(data_entrega) < date.today():
                raise ValueError("Data inválida")

            ids_clientes = {c["id_cliente"] for c in clientes}
            ids_modelos = {m["id_modelo"] for m in modelos}

            if cliente_id not in ids_clientes:
                raise ValueError("Cliente inválido")

            if modelo_id not in ids_modelos:
                raise ValueError("Modelo inválido")

            with conectar() as conexao:
                conexao.execute(
                    """
                    INSERT INTO pedidos (
                        id_cliente, id_modelo, personalizacao,
                        valor_total, data_entrega, endereco_entrega
                    )
                    VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    (
                        cliente_id, modelo_id,
                        personalizacao or None,
                        float(valor), data_entrega, endereco
                    )
                )

            flash("Pedido cadastrado com sucesso!", "sucesso")
            return redirect(url_for("pedidos"))

        except (ValueError, TypeError, InvalidOperation):
            flash(
                "Confira os campos e informe dados válidos.",
                "erro"
            )

    return render_template(
        "novo_pedido.html",
        clientes=clientes,
        modelos=modelos
    )


@app.route("/pedidos")
def pedidos():
    with conectar() as conexao:
        lista = conexao.execute(
            """
            SELECT
                p.id_pedido,
                c.nome AS cliente,
                m.nome AS modelo,
                p.valor_total,
                p.data_entrega,
                p.status
            FROM pedidos p
            JOIN clientes c ON c.id_cliente = p.id_cliente
            JOIN modelos_cestas m ON m.id_modelo = p.id_modelo
            ORDER BY p.id_pedido DESC
            """
        ).fetchall()

    return render_template(
        "pedidos.html",
        pedidos=lista,
        status_disponiveis=STATUS_PEDIDOS
    )


@app.route("/pedidos/<int:pedido_id>/status", methods=["POST"])
def atualizar_status(pedido_id):
    novo_status = request.form.get("status", "")

    if novo_status not in STATUS_PEDIDOS:
        flash("Selecione um status válido.", "erro")
        return redirect(url_for("pedidos"))

    with conectar() as conexao:
        cursor = conexao.execute(
            """
            UPDATE pedidos
            SET status = ?
            WHERE id_pedido = ?
            """,
            (novo_status, pedido_id)
        )

        atualizado = cursor.rowcount > 0

    if atualizado:
        flash("Status atualizado com sucesso!", "sucesso")
    else:
        flash("Pedido não encontrado.", "erro")

    return redirect(url_for("pedidos"))


if __name__ == "__main__":
    app.run(debug=True)
