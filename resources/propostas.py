from flask import Blueprint, jsonify, request
from banco import db
from models.modelProposta import Proposta
from models.modelCarro import Carro
from flask_jwt_extended import jwt_required
from datetime import datetime, timedelta
# from flask_cors import CORS, cross_origin
import smtplib

propostas = Blueprint('propostas', __name__)


@propostas.route('/propostas')
def listagem():
    # propostas = Proposta.query.order_by(Proposta.lance).all()
    propostas = Proposta.query.all()
    return jsonify([proposta.to_json() for proposta in propostas])


@propostas.route('/propostas', methods=['POST'])
# @jwt_required
# @cross_origin()
def inclusao():
    proposta = Proposta.from_json(request.json)
    db.session.add(proposta)
    db.session.commit()
    return jsonify(proposta.to_json()), 201



@propostas.errorhandler(404)
def id_invalido(error):
    return jsonify({'id': 0, 'message': 'not found'}), 404


@propostas.route('/propostas/<int:id>', methods=['PUT'])
def alteracao(id):
    # obtém o registro a ser alterado (ou gera um erro 404 - not found)
    proposta = Proposta.query.get_or_404(id)

    # recupera os dados enviados na requisição
    proposta.lance = request.json['lance']
    proposta.carro_id = request.json['carro_id']
    proposta.nomePessoa = request.json['nomePessoa']
    proposta.telefone = request.json['telefone']
    proposta.email = request.json['email']

    # altera (pois o id já existe)
    db.session.add(proposta)
    db.session.commit()
    return jsonify(proposta.to_json()), 204


@propostas.route('/propostas/<int:id>')
def consulta(id):
    # obtém o registro a ser alterado (ou gera um erro 404 - not found)
    proposta = Proposta.query.get_or_404(id)
    return jsonify(proposta.to_json()), 200


@propostas.route('/propostas/<int:id>', methods=['DELETE'])
def exclui(id):
    Proposta.query.filter_by(id=id).delete()
    db.session.commit()
    return jsonify({'id': id, 'message': 'Proposta excluída com sucesso'}), 200





