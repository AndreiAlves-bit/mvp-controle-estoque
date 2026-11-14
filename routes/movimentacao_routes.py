
from flask import Blueprint, request, jsonify
from extensions import db
from models.produto import Produto
from models.venda import Venda, ItemVenda
from models.movimentacao import MovimentacaoEstoque

movimentacao_routes = Blueprint("movimentacoes", __name__)


@movimentacao_routes.route("/movimentacoes", methods=["POST"])
def registrar_movimentacao():
    dados = request.get_json(silent=True) or {}

    try:
        produto_id = int(dados.get("produto_id"))
        quantidade = int(dados.get("quantidade"))
    except (TypeError, ValueError):
        return jsonify({"erro": "Produto e quantidade devem ser números inteiros."}), 400

    tipo = dados.get("tipo")

    if tipo not in ("entrada", "venda"):
        return jsonify({"erro": "Tipo deve ser entrada ou venda."}), 400

    if quantidade <= 0:
        return jsonify({"erro": "A quantidade deve ser maior que zero."}), 400

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
        observacao=dados.get("observacao", "") if tipo == "entrada" else None
    )

    db.session.add(movimentacao)

    try:
        db.session.commit()
    except Exception:
        db.session.rollback()
        return jsonify({"erro": "Não foi possível salvar a movimentação."}), 500

    return jsonify({
        "mensagem": "Movimentação registrada com sucesso!",
        "produto": produto.nome,
        "tipo": tipo,
        "quantidade_movimentada": quantidade,
        "saldo_atual": produto.quantidade
    }), 201
