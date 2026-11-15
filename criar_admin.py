
import os

from extensions import db
from models.usuario import Usuario


def criar_administrador():
    nome = os.environ.get("ADMIN_NOME", "").strip()
    email = os.environ.get("ADMIN_EMAIL", "").strip().lower()
    senha = os.environ.get("ADMIN_SENHA", "")

    if not nome or not email or not senha:
        print("Administrador não configurado.")
        return

    if len(senha) < 6:
        print("A senha administrativa deve ter pelo menos 6 caracteres.")
        return

    usuario = Usuario.query.filter_by(email=email).first()

    if usuario:
        print("Usuário administrador já existe.")
        return

    administrador = Usuario(
        nome=nome,
        email=email
    )

    administrador.definir_senha(senha)

    db.session.add(administrador)
    db.session.commit()

    print("Administrador criado com sucesso.")
