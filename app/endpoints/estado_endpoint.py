from flask import Blueprint, request, jsonify
from app.services.estado_service import EstadoService

estado_bp = Blueprint("estado", __name__, url_prefix="/estado")
service = EstadoService()

# CREATE
@estado_bp.route("/", methods=["POST"])
def create_estado():
    try:
        data = request.get_json()
        estado = service.create(data)
        return jsonify(estado.to_dict()), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

# READ por ID
@estado_bp.route("/<int:estado_id>", methods=["GET"])
def get_estado(estado_id):
    try:
        estado = service.get_by_id(estado_id)
        return jsonify(estado.to_dict())
    except ValueError as e:
        return jsonify({"error": str(e)}), 404

# LIST com filtros opcionais
@estado_bp.route("/", methods=["GET"])
def list_estados():
    filters = request.args.to_dict()
    estados = service.list(**filters)
    return jsonify([e.to_dict() for e in estados])

# UPDATE por ID
@estado_bp.route("/<int:estado_id>", methods=["PUT"])
def update_estado(estado_id):
    try:
        data = request.get_json()
        estado = service.update(estado_id, data)
        return jsonify(estado.to_dict())
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

# DELETE por ID
@estado_bp.route("/<int:estado_id>", methods=["DELETE"])
def delete_estado(estado_id):
    try:
        service.delete(estado_id)
        return jsonify({"message": "Estado deletado com sucesso"}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
