
from flask import Blueprint, request, jsonify
from extensions import db
from models.produto import Produto
from models.venda import Venda, ItemVenda
from models.movimentacao import MovimentacaoEstoque

movimentacao_routes = Blueprint("movimentacoes", __name__)


def validar_inteiro_positivo(valor):
    if isinstance(valor, bool):
        return None

    if isinstance(valor, int):
        numero = valor
    elif isinstance(valor, str) and valor.isdecimal():
        numero = int(valor)
    else:
        return None

    return numero if numero > 0 else None


@movimentacao_routes.route("/movimentacoes", methods=["POST"])
def registrar_movimentacao():
    dados = request.get_json(silent=True)

    if not isinstance(dados, dict):
        return jsonify({"erro": "Envie um objeto JSON válido."}), 400

    produto_id = validar_inteiro_positivo(dados.get("produto_id"))
    quantidade = validar_inteiro_positivo(dados.get("quantidade"))

    if produto_id is None or quantidade is None:
        return jsonify({
            "erro": "Produto e quantidade devem ser números inteiros positivos."
        }), 400

    tipo = dados.get("tipo")

    if tipo not in ("entrada", "venda"):
        return jsonify({"erro": "Tipo deve ser entrada ou venda."}), 400

    observacao = dados.get("observacao", "")

    if tipo == "entrada" and not isinstance(observacao, str):
        return jsonify({"erro": "A observação deve ser um texto."}), 400

    try:
        produto = db.session.get(Produto, produto_id)

        if produto is None:
            return jsonify({"erro": "Produto não encontrado."}), 404

        if tipo == "venda" and quantidade > produto.quantidade:
            return jsonify({"erro": "Estoque insuficiente."}), 400

        if tipo == "entrada":
            produto.quantidade += quantidade
        else:
            produto.quantidade -= quantidade

            venda = Venda(
                valor_total=round(produto.preco * quantidade, 2)
            )
            db.session.add(venda)
            db.session.flush()

            item = ItemVenda(
                venda_id=venda.id,
                produto_id=produto.id,
                quantidade=quantidade,
                preco_unitario=produto.preco
            )
            db.session.add(item)

        movimentacao = MovimentacaoEstoque(
            produto_id=produto.id,
            tipo=tipo,
            quantidade=quantidade,
            observacao=observacao if tipo == "entrada" else None
        )

        db.session.add(movimentacao)
        db.session.commit()

        return jsonify({
            "mensagem": "Movimentação registrada com sucesso!",
            "produto": produto.nome,
            "tipo": tipo,
            "quantidade_movimentada": quantidade,
            "saldo_atual": produto.quantidade
        }), 201

    except Exception:
        db.session.rollback()
        app_erro = {"erro": "Não foi possível processar a movimentação."}
        return jsonify(app_erro), 500
