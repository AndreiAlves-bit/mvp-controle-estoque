
from flask import Blueprint, request, jsonify
from extensions import db
from models.produto import Produto

produto_routes = Blueprint("produtos", __name__)


# Listar todos os produtos cadastrados
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


# Cadastrar novos produtos
@produto_routes.route("/produtos", methods=["POST"])
def cadastrar_produto():
    dados = request.get_json(silent=True)

    if not isinstance(dados, dict):
        return jsonify({
            "erro": "Envie um objeto JSON válido."
        }), 400

    nome = dados.get("nome")

    if not isinstance(nome, str) or not nome.strip():
        return jsonify({
            "erro": "O nome do produto é obrigatório."
        }), 400

    nome = nome.strip()

    if len(nome) > 100:
        return jsonify({
            "erro": "O nome deve ter no máximo 100 caracteres."
        }), 400

    descricao = dados.get("descricao")

    if descricao is not None:
        if not isinstance(descricao, str) or len(descricao) > 200:
            return jsonify({
                "erro": "A descrição deve ter no máximo 200 caracteres."
            }), 400

    quantidade = dados.get("quantidade", 0)
    estoque_minimo = dados.get("estoque_minimo", 0)
    preco = dados.get("preco", 0.0)

    if (
        type(quantidade) is not int
        or quantidade < 0
        or type(estoque_minimo) is not int
        or estoque_minimo < 0
    ):
        return jsonify({
            "erro": "Quantidade e estoque mínimo devem ser inteiros não negativos."
        }), 400

    try:
        if isinstance(preco, bool):
            raise ValueError

        preco = float(preco)

        import math
        if not math.isfinite(preco) or preco < 0:
            raise ValueError

    except (TypeError, ValueError):
        return jsonify({
            "erro": "O preço deve ser um número válido e não negativo."
        }), 400

    try:
        produto = Produto(
            nome=nome,
            descricao=descricao,
            quantidade=quantidade,
            estoque_minimo=estoque_minimo,
            preco=preco
        )

        db.session.add(produto)
        db.session.commit()

        return jsonify({
            "mensagem": "Produto cadastrado com sucesso!",
            "id": produto.id
        }), 201

    except Exception:
        db.session.rollback()

        return jsonify({
            "erro": "Não foi possível cadastrar o produto."
        }), 500


# Listar apenas produtos que precisam de reposição
@produto_routes.route("/produtos/reposicao", methods=["GET"])
def listar_produtos_reposicao():
    produtos = Produto.query.filter(
        Produto.quantidade <= Produto.estoque_minimo
    ).order_by(Produto.nome.asc()).all()

    return jsonify([
        {
            "id": p.id,
            "nome": p.nome,
            "quantidade": p.quantidade,
            "estoque_minimo": p.estoque_minimo
        }
        for p in produtos
    ])
