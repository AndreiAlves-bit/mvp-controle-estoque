
import os

from flask import Flask, render_template, jsonify
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from extensions import db

app = Flask(__name__)

# Configurações do sistema
app.config["SECRET_KEY"] = os.environ.get(
    "SECRET_KEY", "chave-temporaria-desenvolvimento"
)

app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "DATABASE_URL", "sqlite:///estoque.db"
)

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Configurações de segurança dos cookies
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
app.config["SESSION_COOKIE_SECURE"] = (
    os.environ.get("RENDER") == "true"
)

# Inicialização do banco
db.init_app(app)

# Preparação da proteção contra CSRF
# A ativação será feita após atualizar o frontend
csrf = CSRFProtect()

# Configuração do Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)


# Importação dos modelos
from models import (
    Produto,
    Venda,
    ItemVenda,
    MovimentacaoEstoque,
    Usuario
)


# Carregamento do usuário autenticado
@login_manager.user_loader
def carregar_usuario(usuario_id):
    try:
        return db.session.get(Usuario, int(usuario_id))
    except (ValueError, TypeError):
        return None


# Resposta para acessos não autorizados
@login_manager.unauthorized_handler
def acesso_nao_autorizado():
    return jsonify({
        "erro": "Acesso não autorizado. Faça login."
    }), 401


# Importação das rotas
from routes.produto_routes import produto_routes
from routes.movimentacao_routes import movimentacao_routes
from routes.auth_routes import auth_routes


# Registro dos Blueprints
app.register_blueprint(produto_routes)
app.register_blueprint(movimentacao_routes)
app.register_blueprint(auth_routes)


# Página principal
@app.route("/")
def index():
    return render_template("index.html")


# Inicialização do banco de dados
# Executada também quando o Gunicorn inicia a aplicação
with app.app_context():

    # Cria as tabelas que ainda não existem
    db.create_all()

    # Importa a função responsável pelo administrador
    from criar_admin import criar_administrador

    # Cria o administrador caso esteja configurado
    # e ainda não exista no banco
    criar_administrador()


# Execução local
if __name__ == "__main__":
    app.run(
        debug=os.environ.get("FLASK_DEBUG") == "1"
    )
