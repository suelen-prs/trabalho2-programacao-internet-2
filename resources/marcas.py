from flask import Blueprint, jsonify, request
from banco import db
from models.modelMarca import Marca
from flask_jwt_extended import jwt_required
from models.modelCarro import Carro

marcas = Blueprint('marcas', __name__)


@marcas.route('/marcas')
def listagem():
    marcas = Marca.query.order_by(Marca.id).all()
    return jsonify([marca.to_json() for marca in marcas])


@marcas.route('/marcas', methods=['POST'])
#@jwt_required
def inclusao():
    marca = Marca.from_json(request.json)
    db.session.add(marca)
    db.session.commit()
    return jsonify(marca.to_json()), 201

@marcas.route('/marcas/total')
def total():
    marcas = Marca.query.count()
    carros = Carro.query.count()
    return jsonify({'total de marcas': marcas, 'total de carros': carros})
