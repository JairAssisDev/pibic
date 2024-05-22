from flask import Blueprint, request, jsonify
from app.models.paciente import Paciente
from app import db

paciente_bp = Blueprint('paciente', __name__, url_prefix='/paciente')

@paciente_bp.route("/", methods=["POST"])
def create_paciente():
    data = request.get_json()
    try:
        new_paciente = Paciente(**data)
        db.session.add(new_paciente)
        db.session.commit()
        return jsonify({'message': 'Paciente criado com sucesso'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@paciente_bp.route("/", methods=["GET"])
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

@paciente_bp.route('/test', methods=["GET"])
def test():
    novo_paciente = Paciente(nome='Novo Paciente', cpf='12345678901', sex=1, redo=0, cpb=1, age=30, bsa=1.5, hb=14.2, probability=0.8, prediction=1.0, imagem='imagem.jpg')

    # Adicionando o novo paciente ao banco de dados
    db.session.add(novo_paciente)

    # Commitando a transação para efetivar as mudanças no banco de dados
    db.session.commit()

    return {"Paciente criado com sucesso!"}
