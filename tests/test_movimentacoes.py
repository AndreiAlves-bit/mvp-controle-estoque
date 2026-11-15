
import pytest

from app import app
from extensions import db
from models.produto import Produto
from routes.movimentacao_routes import validar_inteiro_positivo


# TESTES UNITÁRIOS

@pytest.mark.parametrize(
    "valor, esperado",
    [
        (1, 1),
        (10, 10),
        ("5", 5),
        (0, None),
        (-3, None),
        (2.5, None),
        (True, None),
        ("abc", None),
        (None, None),
    ],
)
def test_validar_inteiro_positivo(valor, esperado):
    assert validar_inteiro_positivo(valor) == esperado


# PREPARAÇÃO DOS TESTES DE INTEGRAÇÃO

@pytest.fixture
def cliente(tmp_path):
    app.config.update(
        TESTING=True,
        SQLALCHEMY_DATABASE_URI=(
            "sqlite:///" + (tmp_path / "teste_estoque.db").as_posix()
        ),
    )

    with app.app_context():
        db.session.remove()
        db.engine.dispose()
        db.create_all()

        produto = Produto(
            nome="Arroz 5kg",
            descricao="Produto para testes",
            quantidade=10,
            estoque_minimo=3,
            preco=25.90,
        )

        db.session.add(produto)
        db.session.commit()
        produto_id = produto.id

        yield app.test_client(), produto_id

        db.session.remove()
        db.drop_all()
        db.engine.dispose()


# TESTES DE INTEGRAÇÃO

def test_registrar_entrada(cliente):
    navegador, produto_id = cliente

    resposta = navegador.post(
        "/movimentacoes",
        json={
            "produto_id": produto_id,
            "quantidade": 5,
            "tipo": "entrada",
        },
    )

    assert resposta.status_code == 201
    assert resposta.json["saldo_atual"] == 15

    with app.app_context():
        produto = db.session.get(Produto, produto_id)
        assert produto.quantidade == 15


def test_registrar_venda(cliente):
    navegador, produto_id = cliente

    resposta = navegador.post(
        "/movimentacoes",
        json={
            "produto_id": produto_id,
            "quantidade": 3,
            "tipo": "venda",
        },
    )

    assert resposta.status_code == 201
    assert resposta.json["saldo_atual"] == 7

    with app.app_context():
        produto = db.session.get(Produto, produto_id)
        assert produto.quantidade == 7


def test_estoque_insuficiente(cliente):
    navegador, produto_id = cliente

    resposta = navegador.post(
        "/movimentacoes",
        json={
            "produto_id": produto_id,
            "quantidade": 20,
            "tipo": "venda",
        },
    )

    assert resposta.status_code == 400
    assert resposta.json["erro"] == "Estoque insuficiente."


def test_quantidade_fracionaria(cliente):
    navegador, produto_id = cliente

    resposta = navegador.post(
        "/movimentacoes",
        json={
            "produto_id": produto_id,
            "quantidade": 2.5,
            "tipo": "entrada",
        },
    )

    assert resposta.status_code == 400


def test_tipo_invalido(cliente):
    navegador, produto_id = cliente

    resposta = navegador.post(
        "/movimentacoes",
        json={
            "produto_id": produto_id,
            "quantidade": 2,
            "tipo": "invalido",
        },
    )

    assert resposta.status_code == 400


def test_produto_inexistente(cliente):
    navegador, produto_id = cliente

    resposta = navegador.post(
        "/movimentacoes",
        json={
            "produto_id": 999999,
            "quantidade": 2,
            "tipo": "entrada",
        },
    )

    assert resposta.status_code == 404


def test_json_invalido(cliente):
    navegador, produto_id = cliente

    resposta = navegador.post(
        "/movimentacoes",
        data="conteudo invalido",
        content_type="application/json",
    )

    assert resposta.status_code == 400


def test_observacao_invalida(cliente):
    navegador, produto_id = cliente

    resposta = navegador.post(
        "/movimentacoes",
        json={
            "produto_id": produto_id,
            "quantidade": 2,
            "tipo": "entrada",
            "observacao": 123,
        },
    )

    assert resposta.status_code == 400
