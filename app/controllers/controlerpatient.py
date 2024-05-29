from flask import Blueprint, request, jsonify
from app.models.paciente import Paciente
from app import db
from app.predictions.predict import predict_and_explain
import json

paciente_bp = Blueprint('paciente', __name__, url_prefix='/paciente')

@paciente_bp.route("", methods=["POST"])
def create_paciente():
    data = request.get_json()
    try:
        new_paciente = Paciente(**data)
        db.session.add(new_paciente)
        db.session.commit()

        dados = predict_and_explain(new_paciente.sex, new_paciente.redo, new_paciente.cpb, new_paciente.age, new_paciente.bsa, new_paciente.hb)
        lime_image = dados["lime_image"]
        prediction = dados["prediction"]
        true_probability = dados["true_probability"]

        new_paciente.probability = true_probability
        new_paciente.prediction = prediction
        new_paciente.imagem = lime_image

        db.session.commit()

        return jsonify({'message': 'Paciente criado com sucesso'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400



@paciente_bp.route("/getallpacientes", methods=["GET"])
def get_all_pacientes():
    pacientes = Paciente.query.all()
    pacientes_data = [{'id': paciente.id, 'nome': paciente.nome, 'cpf': paciente.cpf, 'sex': paciente.sex,
                    'redo': paciente.redo, 'cpb': paciente.cpb, 'age': paciente.age, 'bsa': paciente.bsa,
                    'hb': paciente.hb, 'probability': paciente.probability, 'prediction': paciente.prediction,
                    'imagem': paciente.imagem} for paciente in pacientes]
    return jsonify(pacientes_data)

@paciente_bp.route("/<int:paciente_id>", methods=["GET"])
def get_paciente(paciente_id):
    paciente = Paciente.query.get(paciente_id)
    if paciente:
        return jsonify({'id': paciente.id, 'nome': paciente.nome, 'cpf': paciente.cpf, 'sex': paciente.sex,
                        'redo': paciente.redo, 'cpb': paciente.cpb, 'age': paciente.age, 'bsa': paciente.bsa,
                        'hb': paciente.hb, 'probability': paciente.probability, 'prediction': paciente.prediction,
                        'imagem': paciente.imagem})
    else:
        return jsonify({'message': 'Paciente não encontrado'}), 404

@paciente_bp.route("/<int:paciente_id>", methods=["PUT"])
def update_paciente(paciente_id):
    data = request.get_json()
    paciente = Paciente.query.get(paciente_id)
    if paciente:
        try:
            paciente.nome = data.get('nome', paciente.nome)
            paciente.cpf = data.get('cpf', paciente.cpf)
            paciente.sex = data.get('sex', paciente.sex)
            paciente.redo = data.get('redo', paciente.redo)
            paciente.cpb = data.get('cpb', paciente.cpb)
            paciente.age = data.get('age', paciente.age)
            paciente.bsa = data.get('bsa', paciente.bsa)
            paciente.hb = data.get('hb', paciente.hb)
            paciente.probability = data.get('probability', paciente.probability)
            paciente.prediction = data.get('prediction', paciente.prediction)
            paciente.imagem = data.get('imagem', paciente.imagem)
            db.session.commit()
            return jsonify({'message': 'Paciente atualizado com sucesso'})
        except Exception as e:
            return jsonify({'error': str(e)}), 400
    else:
        return jsonify({'message': 'Paciente não encontrado'}), 404

@paciente_bp.route("/<int:paciente_id>", methods=["DELETE"])
def delete_paciente(paciente_id):
    paciente = Paciente.query.get(paciente_id)
    if paciente:
        db.session.delete(paciente)
        db.session.commit()
        return jsonify({'message': 'Paciente deletado com sucesso'})
    else:
        return jsonify({'message': 'Paciente não encontrado'}), 404

@paciente_bp.route("/predict/<string:paciente_nome>", methods=["GET"])
def predict_paciente_by_name(paciente_nome):
    paciente = Paciente.query.filter_by(nome=paciente_nome).first()
    if paciente:
        dados = predict_and_explain(paciente.sex, paciente.redo, paciente.cpb, paciente.age, paciente.bsa, paciente.hb)
        lime_image = dados["lime_image"]
        prediction = dados["prediction"]
        true_probability = dados["true_probability"]

        paciente.probability = true_probability
        paciente.prediction = prediction
        paciente.imagem = lime_image
        db.session.commit()
        paciente = Paciente.query.filter_by(nome=paciente_nome).first()
        return jsonify({'id': paciente.id, 'nome': paciente.nome, 'cpf': paciente.cpf, 'sex': paciente.sex,
                        'redo': paciente.redo, 'cpb': paciente.cpb, 'age': paciente.age, 'bsa': paciente.bsa,
                        'hb': paciente.hb, 'probability': paciente.probability, 'prediction': paciente.prediction,
                        'imagem': paciente.imagem})
    else:
        return jsonify({'message': 'Paciente não encontrado'}), 404

@paciente_bp.route("/nome/<string:paciente_nome>", methods=["GET"])
def get_paciente_by_name(paciente_nome):
    paciente = Paciente.query.filter_by(nome=paciente_nome).first()
    if paciente:
        return jsonify({'id': paciente.id, 'nome': paciente.nome, 'cpf': paciente.cpf, 'sex': paciente.sex,
                        'redo': paciente.redo, 'cpb': paciente.cpb, 'age': paciente.age, 'bsa': paciente.bsa,
                        'hb': paciente.hb, 'probability': paciente.probability, 'prediction': paciente.prediction,
                        'imagem': paciente.imagem})
    else:
        return jsonify({'message': 'Paciente não encontrado'}), 404


