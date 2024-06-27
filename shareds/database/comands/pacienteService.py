import csv
from shareds.database.conn import get_connection
from flask import jsonify
from entities.paciente import Paciente
from predictions.predict import predict_and_explain

def insert_paciente(data: Paciente):
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        query = '''
                INSERT INTO paciente ( nome, cpf, sex, redo, cpb, age, bsa, hb, probability, prediction, imagem
                ) VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                );'''
        cursor.execute(query, (data.nome, data.cpf, data.sex, data.redo, data.cpb, data.age, data.bsa, data.hb, data.probability, data.prediction, data.imagem))
        conn.commit()
    except Exception as e:
        print(f"Error inserting patient: {e}")
        raise ValueError("Failed to insert patient") from e
    finally:
        if 'conn' in locals():
            conn.close()

def update_paciente(nome_original: str, cpf_original: str, data: Paciente):
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        query = """
            UPDATE paciente
            SET nome = %s, cpf = %s, sex = %s, redo = %s, cpb = %s, age = %s, bsa = %s, hb = %s,
                probability = %s, prediction = %s, imagem = %s
            WHERE nome = %s AND cpf = %s
        """
        cursor.execute(query, (data.nome, data.cpf, data.sex, data.redo, data.cpb, data.age, data.bsa, data.hb,
                                data.probability, data.prediction, data.imagem, nome_original, cpf_original))
        conn.commit()
        rows_affected = cursor.rowcount
        if rows_affected == 0:
            return jsonify({"message": "Paciente não encontrado"}), 404
        return jsonify({"message": "Paciente atualizado com sucesso"}), 200
    except Exception as e:
        print(f"Error updating patient: {e}")
        raise ValueError("Failed to update patient") from e
    finally:
        if 'conn' in locals():
            conn.close()


def paciente_get_all():
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        query = f"select nome, cpf, sex, redo, cpb, age, bsa, hb, probability, prediction AS prediction from paciente;"
        cursor.execute(query)
        data = cursor.fetchall()
        return data
    except Exception as e:
        raise
    finally:
        if 'conexao' in locals():
            conn.close()

def paciente_prob_get_all():
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        query = f"SELECT nome, cpf, sex, redo, cpb, age, bsa, hb, probability, prediction FROM paciente ORDER BY probability DESC;"
        cursor.execute(query)
        data = cursor.fetchall()
        return data
    except Exception as e:
        raise
    finally:
        if 'conexao' in locals():
            conn.close()


def get_by_name_cpf(nome,cpf):
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        query = """
            select nome, cpf, sex, redo, cpb, age, bsa, hb, probability, prediction,imagem
            from paciente
            where nome = %s AND cpf = %s
        """
        cursor.execute(query,(nome,cpf,))
        data = cursor.fetchall()
        return data
    except Exception as e:
        raise
    finally:
        if 'conexao' in locals():
            conn.close()

def get_img_by_name_cpf(nome,cpf):
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        query = """
            select nome, cpf, probability, prediction,imagem
            from paciente
            where nome = %s AND cpf = %s
        """
        cursor.execute(query,(nome,cpf,))
        data = cursor.fetchall()
        return data
    except Exception as e:
        raise
    finally:
        if 'conexao' in locals():
            conn.close()

def verificar_paciente(nome,cpf):
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        query = """
            select id
            from paciente
            where nome = %s AND cpf = %s
        """
        cursor.execute(query,(nome,cpf,))
        data = cursor.fetchall()
        return data
    except Exception as e:
        raise
    finally:
        if 'conexao' in locals():
            conn.close()

def delete_paciente_by_name_and_cpf(nome, cpf):
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        query = """
            DELETE FROM paciente
            WHERE nome = %s AND cpf = %s
        """
        cursor.execute(query, (nome, cpf))
        conn.commit()
        
        return True
    except Exception as e:
        print(f"Error deleting patient: {e}")
        raise
    finally:
        if 'conexao' in locals():
            conn.close()
