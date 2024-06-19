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
            return jsonify({"status_code": 401, "content": {"User": "not found"}})
        nome_usuario = usuario_encontrado[0]["username"]
        instancia = {"userName": nome_usuario, "matricula": usuario.matricula}    
        token = encode(UserBase.parse_obj(instancia))
        return jsonify({"status_code": 200, "content": { "token": token }})
    else:
        return jsonify({"status_code": 401, "content": {"User": "not found"}})

@user_bp.route("/create", methods=["POST"])
def criar_usuario():
    dados = request.get_json()
    usuario = User(**dados)
    try:
        usuario_encontrado = get_user(usuario.matricula)
        if len(usuario_encontrado) == 0:
            insert_user(usuario)
            return jsonify({"status_code": 201, "content": {}})
        else:
            return jsonify({"status_code": 500, "content": {}})
    except Exception:
        return jsonify({"status_code": 409, "detail": "Erro ao inserir usuário"})
