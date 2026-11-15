
from extensions import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class Usuario(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)

    nome = db.Column(
        db.String(100),
        nullable=False
    )

    email = db.Column(
        db.String(120),
        unique=True,
        nullable=False
    )

    senha = db.Column(
        db.String(256),
        nullable=False
    )

    def definir_senha(self, senha):
        """Armazena a senha utilizando hash seguro."""
        self.senha = generate_password_hash(
            senha,
            method="scrypt"
        )

    def verificar_senha(self, senha):
        """Verifica a senha informada pelo usuário."""
        return check_password_hash(
            self.senha,
            senha
        )

    def __repr__(self):
        return f"<Usuario {self.email}>"
