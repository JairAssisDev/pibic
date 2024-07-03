import csv
from flask import send_file
from io import BytesIO
import pandas as pd
from io import StringIO
from entities.paciente import Paciente
from flask import Blueprint, request, jsonify
from pydantic import ValidationError
from predictions.predict import predict_and_explain , predict_and_explain_image
from shareds.database.comands.pacienteService import *

paciente_bp = Blueprint('paciente', __name__, url_prefix='/paciente')

@paciente_bp.route("", methods=["POST"])
def create_paciente():
    try:
        data = request.get_json()
        instance = Paciente(**data)
        
        instance.nome = instance.nome.lower()
        dados = predict_and_explain(instance.sex, instance.redo, instance.cpb, instance.age, instance.bsa, instance.hb)
        instance.probability = dados["true_probability"]
        instance.prediction = dados["prediction"]
        insert_paciente(instance)
        return jsonify({'message': 'Paciente criado com sucesso'}), 201
    except ValidationError as e:
        return jsonify({'message': 'Erro na validação dos dados', 'error': e.errors()}), 422
    except Exception as e:
        return jsonify({'message': 'Erro ao criar paciente', 'error': str(e)}), 400


@paciente_bp.route("/getallpacientes", methods=["GET"])
def get_all_pacientes():
    try:
        pacientes = paciente_get_all()
        return jsonify({"pacientes": pacientes},200)
    except Exception as e:
        return jsonify({'menssage':'pacente não existe ou foi encontrado'}),401
    

@paciente_bp.route("/getproballpacientes", methods=["GET"])
def get_prob_all_pacientes():
    try:
        pacientes = paciente_prob_get_all()
        return jsonify({"pacientes": pacientes},200)
    except Exception as e:
        return jsonify({'menssage':'pacente não existe ou foi encontrado'}),401

@paciente_bp.route("/<nome>/<cpf>", methods=["GET"])
def get_paciente(nome,cpf):
    paciente = get_by_name_cpf(nome,cpf)
    if paciente:
        return jsonify({"message":paciente}),200
    return jsonify({'message': 'Paciente não encontrado'}), 404

@paciente_bp.route("/img/<nome>/<cpf>", methods=["GET"])
def get_imagem_paciente(nome, cpf):
    paciente = get_by_name_cpf(nome, cpf)
    if paciente:
        instance = Paciente(**paciente)
        dados = predict_and_explain_image(instance.sex, instance.redo, instance.cpb, instance.age, instance.bsa, instance.hb)
        instance.probability = str(dados["true_probability"])
        instance.prediction = str(dados["prediction"])
        instance.imagem = dados["lime_image"]
        return jsonify({"nome": instance.nome, "imagem": instance.imagem}), 200
    return jsonify({'message': 'Paciente não encontrado'}), 404


    
@paciente_bp.route("/<nome>/<cpf>", methods=["DELETE"])
def delete_paciente(nome,cpf):
    paciente = verificar_paciente(nome,cpf)
    if paciente:
        delete_paciente_by_name_and_cpf(nome,cpf)
        return jsonify({'message': 'Paciente deletado com sucesso'})
    return jsonify({'message': 'Paciente não encontrado'}), 404


@paciente_bp.route("/<nome>/<cpf>", methods=["PUT"])
def use_update_paciente(nome, cpf):
    data = request.get_json()
    paciente = verificar_paciente(nome, cpf)
    if not paciente:
        return jsonify({'message': 'Paciente não encontrado'}), 404

    try:
        patient_data = Paciente(**data)
        patient_data.nome = patient_data.nome.lower()
        dados = predict_and_explain(patient_data.sex, patient_data.redo, patient_data.cpb, patient_data.age, patient_data.bsa, patient_data.hb)
        patient_data.probability = dados["true_probability"]
        patient_data.prediction = dados["prediction"]
        update_paciente(nome, cpf, patient_data)
        response_data = {
            "message": "Paciente atualizado com sucesso",
            "data": dados
        }
        return jsonify(response_data), 200

    except Exception as e:
        return jsonify({'error': "Erro ao atualizar paciente:"+str(e)}), 400



@paciente_bp.route("/upload", methods=["POST"])
def upload_pacientes():
    try:
        file = request.files['file']

        if file.filename == '':
            return jsonify({"error": "No selected file"}), 400

        file_extension = file.filename.split('.')[-1].lower()
        
        if file_extension == 'csv':
            file_data = file.read().decode('utf-8')
            data = pd.read_csv(StringIO(file_data))
        elif file_extension == 'xlsx':
            file_data = file.read()
            data = pd.read_excel(BytesIO(file_data))
        elif file_extension == 'xls':
            file_data = file.read()
            data = pd.read_excel(BytesIO(file_data), engine='xlrd')
        else:
            return jsonify({"error": "Unsupported file type"}), 400

        lista_de_pacieentes_n_salvos = []
        
        for index, row in data.iterrows():
            if row['nome'].lower() == 'nome':
                continue
            data_dict = {
                "nome": str(row['nome']),
                "cpf": str(row['cpf']),
                "sex": int(row['sex']),
                "redo": int(row['redo']),
                "cpb": int(row['cpb']),
                "age": int(row['age']),
                "bsa": float(row['bsa']),
                "hb": float(row['hb'])
            }
            instance = Paciente(**data_dict)
            instance.nome = instance.nome.lower()
            paciente = verificar_paciente(instance.nome, instance.cpf)
            if not paciente:
                dados = predict_and_explain(instance.sex, instance.redo, instance.cpb, instance.age, instance.bsa, instance.hb)
                instance.probability = dados["true_probability"]
                instance.prediction = dados["prediction"]
                insert_paciente(instance)
            else:
                lista_de_pacieentes_n_salvos.append(data_dict)

        if len(lista_de_pacieentes_n_salvos) == 0:
            return jsonify({"message": "Arquivo salvo com sucesso!"}), 200
        return jsonify({"message": "Parte dos pacientes foram salvos com sucesso.", "naosalvos": lista_de_pacieentes_n_salvos}), 207

    except Exception as e:
        return jsonify({"error": str(e)}), 400


'''



@paciente_bp.route("/upload", methods=["POST"])
def upload_pacientes():
    try:
        file = request.files['file']

        if file.filename == '':
            return jsonify({"error": "No selected file"}), 400

        # Identifica a extensão do arquivo
        file_extension = file.filename.split('.')[-1].lower()
        
        if file_extension == 'csv':
            file_data = file.read().decode('utf-8')
            data = pd.read_csv(StringIO(file_data))
        elif file_extension in ['xlsx', 'xls']:
            file_data = file.read()
            data = pd.read_excel(BytesIO(file_data))
        else:
            return jsonify({"error": "Unsupported file type"}), 400

        lista_de_pacieentes_n_salvos = []
        
        for index, row in data.iterrows():
            if row['nome'].lower() == 'nome':
                continue
            data_dict = {
                "nome": str(row['nome']),
                "cpf": str(row['cpf']),
                "sex": int(row['sex']),
                "redo": int(row['redo']),
                "cpb": int(row['cpb']),
                "age": int(row['age']),
                "bsa": float(row['bsa']),
                "hb": float(row['hb'])
            }
            instance = Paciente(**data_dict)
            instance.nome = instance.nome.lower()
            paciente = verificar_paciente(instance.nome, instance.cpf)
            if not paciente:
                dados = predict_and_explain(instance.sex, instance.redo, instance.cpb, instance.age, instance.bsa, instance.hb)
                instance.probability = dados["true_probability"]
                instance.prediction = dados["prediction"]
                insert_paciente(instance)
            else:
                lista_de_pacieentes_n_salvos.append(data_dict)

        if len(lista_de_pacieentes_n_salvos) == 0:
            # Criar um DataFrame vazio para evitar erro ao criar o arquivo Excel
            df_vazio = pd.DataFrame()
            output = BytesIO()
            writer = pd.ExcelWriter(output, engine='xlsxwriter')
            df_vazio.to_excel(writer, index=False, sheet_name='Pacientes_nao_salvos')
            writer.save()
            output.seek(0)
            return send_file(output, attachment_filename='pacientes_nao_salvos.xlsx', as_attachment=True), 200
        
        # Criar DataFrame com pacientes não salvos
        df_nao_salvos = pd.DataFrame(lista_de_pacieentes_n_salvos)
        output = BytesIO()
        writer = pd.ExcelWriter(output, engine='xlsxwriter')
        df_nao_salvos.to_excel(writer, index=False, sheet_name='Pacientes_nao_salvos')
        writer.save()
        output.seek(0)
        
        return send_file(output, attachment_filename='pacientes_nao_salvos.xlsx', as_attachment=True), 207

    except Exception as e:
        return jsonify({"error": str(e)}), 400

        '''