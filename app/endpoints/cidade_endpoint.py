from flask import Blueprint, request, jsonify
from app.services.cidade_service import CidadeService

cidade_bp = Blueprint("cidade", __name__, url_prefix="/cidade")
service = CidadeService()

# CREATE
@cidade_bp.route("/", methods=["POST"])
def create_cidade():
    try:
        data = request.get_json()
        cidade = service.create(data)
        return jsonify(cidade.to_dict()), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

# READ por ID
@cidade_bp.route("/<int:cidade_id>", methods=["GET"])
def get_cidade(cidade_id):
    try:
        cidade = service.get_by_id(cidade_id)
        return jsonify(cidade.to_dict())
    except ValueError as e:
        return jsonify({"error": str(e)}), 404

# LIST (com filtros opcionais via query string)
@cidade_bp.route("/", methods=["GET"])
def list_cidades():
    try:
        filters = request.args.to_dict()  # captura filtros como ?nome=São+Paulo
        cidades = service.list(**filters)
        return jsonify([cidade.to_dict() for cidade in cidades])
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# UPDATE por ID
@cidade_bp.route("/<int:cidade_id>", methods=["PUT"])
def update_cidade(cidade_id):
    try:
        data = request.get_json()
        cidade = service.update(cidade_id, data)
        return jsonify(cidade.to_dict())
    except ValueError as e:
        return jsonify({"error": str(e)}), 404

# DELETE por ID
@cidade_bp.route("/<int:cidade_id>", methods=["DELETE"])
def delete_cidade(cidade_id):
    try:
        service.delete(cidade_id)
        return jsonify({"message": "Cidade deletada com sucesso"})
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
