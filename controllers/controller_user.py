from entities.user import User
from flask import Blueprint, request, jsonify
from shareds.database.comands.userService import get_user, insert_user
from entities.auth import Auth
from entities.userBase import UserBase
from shareds.jwt.main import encode
from shareds.crypto import check_password

user_bp = Blueprint('user', __name__, url_prefix='/user')

@user_bp.route("/auth", methods=["POST"])
def autenticar_usuario():
    dados = request.get_json()
    usuario = Auth(**dados)

    usuario_encontrado = get_user(usuario.matricula)
    if len(usuario_encontrado) > 0:
        senha_encriptada = usuario_encontrado[0]["password"]
        if not check_password(usuario.password, senha_encriptada):
            return jsonify({"content": {"User": "not found"}}),401
        nome_usuario = usuario_encontrado[0]["username"]
        instancia = {"userName": nome_usuario, "matricula": usuario.matricula}    
        token = encode(UserBase.parse_obj(instancia))
        return jsonify({"content": { "token": token }}),200 
    else:
        return jsonify({"content": {"User": "not found"}}),401

@user_bp.route("/create", methods=["POST"])
def criar_usuario():
    dados = request.get_json()
    usuario = User(**dados)
    try:
        usuario_encontrado = get_user(usuario.matricula)
        if len(usuario_encontrado) == 0:
            insert_user(usuario)
            return jsonify({"content": {}}),201
        else:
            return jsonify({"content": {}}),500
    except Exception:
        return jsonify({"detail": "Erro ao inserir usuário"}),409
