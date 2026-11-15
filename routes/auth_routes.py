
from flask import Blueprint, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from extensions import db
from models.usuario import Usuario

auth_routes = Blueprint("auth", __name__)


@auth_routes.route("/api/login", methods=["POST"])
def login():
    dados = request.get_json(silent=True) or {}

    email = str(dados.get("email", "")).strip().lower()
    senha = dados.get("senha", "")

    if not email or not isinstance(senha, str) or not senha:
        return jsonify({
            "erro": "Informe o e-mail e a senha."
        }), 400

    usuario = Usuario.query.filter_by(email=email).first()

    if not usuario or not usuario.verificar_senha(senha):
        return jsonify({
            "erro": "E-mail ou senha inválidos."
        }), 401

    login_user(usuario)

    return jsonify({
        "mensagem": "Login realizado com sucesso.",
        "usuario": {
            "id": usuario.id,
            "nome": usuario.nome
        }
    }), 200


@auth_routes.route("/api/logout", methods=["POST"])
@login_required
def logout():
    logout_user()

    return jsonify({
        "mensagem": "Logout realizado com sucesso."
    }), 200


@auth_routes.route("/api/me", methods=["GET"])
def usuario_atual():
    if not current_user.is_authenticated:
        return jsonify({
            "autenticado": False
        }), 401

    return jsonify({
        "autenticado": True,
        "usuario": {
            "id": current_user.id,
            "nome": current_user.nome
        }
    }), 200
