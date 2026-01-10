from flask import Blueprint, request, jsonify
from app.services.usuario_service import UsuarioService

usuario_bp = Blueprint("usuario", __name__, url_prefix="/usuario")
service = UsuarioService()

# CREATE
@usuario_bp.route("/", methods=["POST"])
def create_usuario():
    try:
        data = request.get_json()
        usuario = service.create(data)
        return jsonify(usuario.to_dict()), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

# READ por ID
@usuario_bp.route("/<int:usuario_id>", methods=["GET"])
def get_usuario(usuario_id):
    try:
        usuario = service.get_by_id(usuario_id)
        return jsonify(usuario.to_dict())
    except ValueError as e:
        return jsonify({"error": str(e)}), 404

# UPDATE por ID
@usuario_bp.route("/<int:usuario_id>", methods=["PUT"])
def update_usuario(usuario_id):
    try:
        data = request.get_json()
        usuario = service.update(usuario_id, data)
        return jsonify(usuario.to_dict())
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

# DELETE por ID
@usuario_bp.route("/<int:usuario_id>", methods=["DELETE"])
def delete_usuario(usuario_id):
    try:
        service.delete(usuario_id)
        return jsonify({"message": "Usuário deletado com sucesso"}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
