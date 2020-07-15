from flask import Blueprint, jsonify, request
from banco import db
from models.modelCarro import Carro
from flask_jwt_extended import jwt_required

carros = Blueprint('carros', __name__)


@carros.route('/carros')
def listagem():
    carros = Carro.query.order_by(Carro.modelo).all()
    return jsonify([carro.to_json() for carro in carros])


@carros.route('/carros', methods=['POST'])
#@jwt_required
def inclusao():
    carro = Carro.from_json(request.json)
    db.session.add(carro)
    db.session.commit()
    return jsonify(carro.to_json()), 201


@carros.errorhandler(404)
def id_invalido(error):
    return jsonify({'id': 0, 'message': 'not found'}), 404


@carros.route('/carros/<int:id>', methods=['PUT'])
#@jwt_required
def alteracao(id):
    # obtém o registro a ser alterado (ou gera um erro 404 - not found)
    carro = Carro.query.get_or_404(id)

    # recupera os dados enviados na requisição
    carro.modelo = request.json['modelo']
    carro.cor = request.json['cor']
    carro.ano = request.json['ano']
    carro.preco = request.json['preco']
    carro.foto = request.json['foto']
    carro.destaque = request.json['destaque']
    carro.marca_id = request.json['marca_id']

    # altera (pois o id já existe)
    db.session.add(carro)
    db.session.commit()
    return jsonify(carro.to_json()), 204


@carros.route('/carros/<int:id>')
def consulta(id):
    # obtém o registro a ser alterado (ou gera um erro 404 - not found)
    carro = Carro.query.get_or_404(id)
    return jsonify(carro.to_json()), 200


@carros.route('/carros/<int:id>', methods=['DELETE'])
#@jwt_required
def exclui(id):
    Carro.query.filter_by(id=id).delete()
    db.session.commit()
    return jsonify({'id': id, 'message': 'Carro excluído com sucesso'}), 200

# Parte 2 do Trabalho
@carros.route('/carros/destaque')
def destaqueCarro():
    carros = Carro.query.order_by(Carro.modelo).filter(
        Carro.destaque == 'x').all()
    return jsonify([carro.to_json() for carro in carros])


# @carros.route('/carros/destacar/<int:id>',methods=['PUT'])
# def destacarCarro(id):

#     carro = Carro.query.get_or_404(id)


#     carro.destaque = request.json['destaque']


#     db.session.add(carro)
#     db.session.commit()
#     return jsonify(carro.to_json()), 204

@carros.route('/carros/destacar/<int:id>', methods=['PUT'])
# @cross_origin()
def destacaVeiculo(id):
    carro = Carro.query.get_or_404(id)
    if carro.destaque == 'x':
        carro.destaque = '-'
    else:
        carro.destaque = 'x'
    db.session.add(carro)
    db.session.commit()

    if carro.destaque == 'x':
        return jsonify({'id': id, 'message': 'Veículo destacado com sucesso'}), 200
    else:
        return jsonify({'id': id, 'message': 'Veículo retirado dos destaques'}), 200


@carros.route('/carros/filtro/<palavra>')
def pesquisa(palavra):
    # obtém todos os registros da tabela veiculos em ordem de modelo
    carros = Carro.query.order_by(Carro.modelo).filter(
        Carro.modelo.like(f'%{palavra}%'))
    if carros == []:
        return jsonify({'Não foi encontrado veiculos com esse modelo'}), 404
    return jsonify([carro.to_json() for carro in carros])

@carros.route('/carros/total')
def total():
    carros = Carro.query.count()
    return jsonify({'total': carros})