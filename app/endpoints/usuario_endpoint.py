from flask import Blueprint, request, jsonify, make_response
from app.services.usuario_service import UsuarioService
from flask_jwt_extended import create_access_token
from flask_jwt_extended import jwt_required, get_jwt_identity
from http import HTTPStatus

usuario_bp = Blueprint("usuario", __name__, url_prefix="/usuario")
service = UsuarioService()

# CREATE
@usuario_bp.route("/", methods=["POST"])
def create_usuario():
    """
    Os dados retornados do front devem ter os campos: nome, cnpj, perfil, email e password
    """
    try:
        data = request.get_json()
        usuario = service.create(data)
        access_token = create_access_token(identity=f"{usuario.id_usuario}")
        response = make_response(jsonify({
            "user": {
                "id_usuario": usuario.id_usuario,
                "email": usuario.email,
                "nome": usuario.nome,
                "perfil":usuario.perfil,
                "cnpj":usuario.cnpj
            }
        }))

        response.set_cookie(
            "access_token_cookie", 
            access_token, 
            httponly=True,
            samesite="Lax",
            secure=False
            )
        return response, HTTPStatus.CREATED
    except ValueError as e:
        return jsonify({"error": str(e)}), HTTPStatus.CONFLICT
    except Exception:
        return jsonify({"error": "Erro interno ao cadastrar usuário."}), HTTPStatus.INTERNAL_SERVER_ERROR

# READ por ID
@usuario_bp.route("/<int:usuario_id>", methods=["GET"])
def get_usuario(usuario_id):
    try:
        usuario = service.get_by_id(usuario_id)
        return jsonify(usuario.to_dict())
    except ValueError as e:
        return jsonify({"error": str(e)}), 404

# UPDATE por ID
@usuario_bp.route("/", methods=["PUT"])
@jwt_required()
def update_usuario():
    try:
        usuario_id_str = get_jwt_identity()
        usuario_id = int(usuario_id_str)
        data = request.get_json()
        usuario = service.update(usuario_id, data)
        access_token = create_access_token(identity=f"{usuario.id_usuario}")
        response = make_response(jsonify({
            "user": {
                "id_usuario": usuario.id_usuario,
                "email": usuario.email,
                "nome": usuario.nome,
                "perfil":usuario.perfil,
                "cnpj":usuario.cnpj
            }
        }))

        response.set_cookie(
            "access_token_cookie", 
            access_token, 
            httponly=True,
            samesite="Lax",
            secure=False
            )
        return response, HTTPStatus.OK
    except ValueError as e:
        return jsonify({"error": str(e)}), HTTPStatus.CONFLICT
    except Exception:
        return jsonify({"error": "Erro interno ao editar usuário."}), HTTPStatus.INTERNAL_SERVER_ERROR

# DELETE por ID
@usuario_bp.route("/<int:usuario_id>", methods=["DELETE"])
def delete_usuario(usuario_id):
    try:
        service.delete(usuario_id)
        return jsonify({"message": "Usuário deletado com sucesso"}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
