from flask import Blueprint, request, jsonify
from app.services.unidade_service import UnidadeService

unidade_bp = Blueprint("unidade", __name__, url_prefix="/unidade")
service = UnidadeService()

# CREATE
@unidade_bp.route("/", methods=["POST"])
def create_unidade():
    try:
        data = request.get_json()
        unidade = service.create(data)
        return jsonify(unidade.to_dict()), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

# READ por ID
@unidade_bp.route("/<int:unidade_id>", methods=["GET"])
def get_unidade(unidade_id):
    try:
        unidade = service.get_by_id(unidade_id)
        return jsonify(unidade.to_dict())
    except ValueError as e:
        return jsonify({"error": str(e)}), 404

# LIST com filtros opcionais
@unidade_bp.route("/", methods=["GET"])
def list_unidades():
    filters = request.args.to_dict()
    unidades = service.list(**filters)
    return jsonify([u.to_dict() for u in unidades])

# UPDATE por ID
@unidade_bp.route("/<int:unidade_id>", methods=["PUT"])
def update_unidade(unidade_id):
    try:
        data = request.get_json()
        unidade = service.update(unidade_id, data)
        return jsonify(unidade.to_dict())
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

# DELETE por ID
@unidade_bp.route("/<int:unidade_id>", methods=["DELETE"])
def delete_unidade(unidade_id):
    try:
        service.delete(unidade_id)
        return jsonify({"message": "Unidade de medida deletada com sucesso"}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
