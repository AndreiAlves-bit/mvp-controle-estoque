from extensions import db


class Produto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.String(200))
    quantidade = db.Column(db.Integer, nullable=False, default=0)
    estoque_minimo = db.Column(db.Integer, nullable=False, default=0)
    preco = db.Column(db.Float, nullable=False, default=0.0)

    def __repr__(self):
        return f"<Produto {self.nome}>"
