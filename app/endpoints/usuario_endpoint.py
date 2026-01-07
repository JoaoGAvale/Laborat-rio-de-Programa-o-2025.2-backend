from flask import Blueprint, request, jsonify
from app.services.usuario_service import UsuarioService

usuario_bp = Blueprint("usuario", __name__, url_prefix="/usuario")
service = UsuarioService()

@usuario_bp.route("/", methods=["POST"])
def create_usuario():
    try:
        data = request.get_json()
        usuario = service.create(data)
        return jsonify(usuario.to_dict()), 201

    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@usuario_bp.route("/<int:usuario_id>", methods=["GET"])
def get_usuario(usuario_id):
    try:
        usuario = service.get_by_id(usuario_id)
        return jsonify(usuario.to_dict())

    except ValueError as e:
        return jsonify({"error": str(e)}), 404
