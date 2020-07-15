from banco import db
from datetime import datetime

class Carro(db.Model):
    __tablename__ = 'carros'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    modelo = db.Column(db.String(40), nullable=False)
    cor = db.Column(db.String(30), nullable=False)
    ano = db.Column(db.Integer, nullable=False)
    preco = db.Column(db.Float, nullable=False)
    foto = db.Column(db.String(120), nullable=False)
    destaque = db.Column(db.String(1), nullable=False)
    data_cad = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    marca_id = db.Column(db.Integer, db.ForeignKey(
        'marcas.id'), nullable=False)

    marca = db.relationship('Marca')
    proposta = db.relationship('Proposta')
    

    def to_json(self):
        json_carros = {
            'id': self.id,
            'modelo': self.modelo,
            'cor': self.cor,
            'ano': self.ano,
            'preco': self.preco,
            'foto' : self.foto,
            'destaque': self.destaque,
            'marca_id': self.marca_id,
            'marca': self.marca.nome,
            'num_propostas': len(self.proposta)
        }
        return json_carros

    @staticmethod
    def from_json(json_carros):
        modelo = json_carros.get('modelo')
        cor = json_carros.get('cor')
        ano = json_carros.get('ano')
        preco = json_carros.get('preco')
        foto = json_carros.get('foto')
        destaque = json_carros.get('destaque')
        marca_id = json_carros.get('marca_id')
        return Carro(modelo=modelo, cor=cor, ano=ano, preco=preco, foto=foto, destaque=destaque, marca_id=marca_id)
