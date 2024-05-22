from flask import Blueprint, request, jsonify
from app.models.user import User
from app import db

user_bp = Blueprint('user', __name__, url_prefix='/user')

@user_bp.route("/", methods=["POST"])
def create_user():
    data = request.get_json()
    try:
        new_user = User(**data)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'User created successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@user_bp.route("/", methods=["GET"])
def get_all_users():
    users = User.query.all()
    users_data = [{'id': user.id, 'username': user.username, 'email': user.email} for user in users]
    return jsonify(users_data)

@user_bp.route("/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = User.query.get(user_id)
    if user:
        return jsonify({'id': user.id, 'username': user.username, 'email': user.email})
    else:
        return jsonify({'message': 'User not found'}), 404

@user_bp.route("/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    data = request.get_json()
    user = User.query.get(user_id)
    if user:
        try:
            user.username = data.get('username', user.username)
            user.email = data.get('email', user.email)
            db.session.commit()
            return jsonify({'message': 'User updated successfully'})
        except Exception as e:
            return jsonify({'error': str(e)}), 400
    else:
        return jsonify({'message': 'User not found'}), 404

@user_bp.route("/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({'message': 'User deleted successfully'})
    else:
        return jsonify({'message': 'User not found'}), 404

@user_bp.route('/test',methods=["get"])
def test():
    novo_usuario = User(username='novo_usuario', email='novo_usuario@example.com')

    # Adicionando o novo usuário ao banco de dados
    db.session.add(novo_usuario)

    # Commitando a transação para efetivar as mudanças no banco de dados
    db.session.commit()

    return{"Usuário criado com sucesso!"}
