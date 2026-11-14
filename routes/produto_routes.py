from flask import Blueprint, request, jsonify
from extensions import db
from models.produto import Produto

produto_routes = Blueprint("produtos", __name__)


@produto_routes.route("/produtos", methods=["GET"])
def listar_produtos():
    produtos = Produto.query.all()

    return jsonify([
        {
            "id": p.id,
            "nome": p.nome,
            "descricao": p.descricao,
            "quantidade": p.quantidade,
            "estoque_minimo": p.estoque_minimo,
            "preco": p.preco
        }
        for p in produtos
    ])


@produto_routes.route("/produtos", methods=["POST"])
def cadastrar_produto():
    dados = request.get_json()

    if not dados or not dados.get("nome"):
        return jsonify({"erro": "O nome do produto é obrigatório."}), 400

    produto = Produto(
        nome=dados["nome"],
        descricao=dados.get("descricao"),
        quantidade=dados.get("quantidade", 0),
        estoque_minimo=dados.get("estoque_minimo", 0),
        preco=dados.get("preco", 0.0)
    )

    db.session.add(produto)
    db.session.commit()

    return jsonify({"mensagem": "Produto cadastrado!", "id": produto.id}), 201