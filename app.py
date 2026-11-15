
import os
from flask import Flask, render_template
from flask_login import LoginManager
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

# Inicialização do banco
db.init_app(app)

# Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

# Importação dos modelos
from models import Produto, Venda, ItemVenda, MovimentacaoEstoque, Usuario

# Importação e registro das rotas de produtos
from routes.produto_routes import produto_routes
app.register_blueprint(produto_routes)

# Importação e registro das rotas de movimentações
from routes.movimentacao_routes import movimentacao_routes
app.register_blueprint(movimentacao_routes)


@login_manager.user_loader
def carregar_usuario(usuario_id):
    return db.session.get(Usuario, int(usuario_id))


@app.route("/")
def index():
    return render_template("index.html")


# Criação das tabelas do banco de dados
# Funciona tanto localmente quanto no Render
with app.app_context():
    db.create_all()


# Execução local
if __name__ == "__main__":
    app.run(debug=os.environ.get("FLASK_DEBUG") == "1")
