from flask import Blueprint, request, jsonify
from app.services.endereco_service import EnderecoService

endereco_bp = Blueprint("endereco", __name__, url_prefix="/endereco")
service = EnderecoService()

# CREATE
@endereco_bp.route("/", methods=["POST"])
def create_endereco():
    try:
        data = request.get_json()
        endereco = service.create(data)
        return jsonify(endereco.to_dict()), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

# READ por ID
@endereco_bp.route("/<int:endereco_id>", methods=["GET"])
def get_endereco(endereco_id):
    try:
        endereco = service.get_by_id(endereco_id)
        return jsonify(endereco.to_dict())
    except ValueError as e:
        return jsonify({"error": str(e)}), 404

# LIST (opcionalmente com filtros)
@endereco_bp.route("/", methods=["GET"])
def list_enderecos():
    filters = request.args.to_dict()  # pega filtros da query string
    enderecos = service.list(**filters)
    return jsonify([e.to_dict() for e in enderecos])

# UPDATE sempre por ID
@endereco_bp.route("/<int:endereco_id>", methods=["PUT"])
def update_endereco(endereco_id):
    try:
        data = request.get_json()
        endereco = service.update(endereco_id, data)
        return jsonify(endereco.to_dict())
    except ValueError as e:
        return jsonify({"error": str(e)}), 404

# DELETE sempre por ID
@endereco_bp.route("/<int:endereco_id>", methods=["DELETE"])
def delete_endereco(endereco_id):
    try:
        service.delete(endereco_id)
        return jsonify({"message": "Endereço deletado com sucesso"})
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
