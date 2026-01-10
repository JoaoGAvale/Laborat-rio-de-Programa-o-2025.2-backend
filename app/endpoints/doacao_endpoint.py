from flask import Blueprint, request, jsonify
from app.services.doacao_service import DoacaoService

doacao_bp = Blueprint("doacao", __name__, url_prefix="/doacao")
service = DoacaoService()

# CREATE
@doacao_bp.route("/", methods=["POST"])
def create_doacao():
    try:
        data = request.get_json()
        doacao = service.create(data)
        return jsonify(doacao.to_dict()), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

# READ por ID
@doacao_bp.route("/<int:doacao_id>", methods=["GET"])
def get_doacao(doacao_id):
    try:
        doacao = service.get_by_id(doacao_id)
        return jsonify(doacao.to_dict())
    except ValueError as e:
        return jsonify({"error": str(e)}), 404

# LIST com filtros opcionais
@doacao_bp.route("/", methods=["GET"])
def list_doacoes():
    filters = request.args.to_dict()  # captura query params
    doacoes = service.list(**filters)
    return jsonify([d.to_dict() for d in doacoes])

# UPDATE por ID
@doacao_bp.route("/<int:doacao_id>", methods=["PUT"])
def update_doacao(doacao_id):
    try:
        data = request.get_json()
        doacao = service.update(doacao_id, data)
        return jsonify(doacao.to_dict())
    except ValueError as e:
        return jsonify({"error": str(e)}), 404

# DELETE por ID
@doacao_bp.route("/<int:doacao_id>", methods=["DELETE"])
def delete_doacao(doacao_id):
    try:
        service.delete(doacao_id)
        return jsonify({"success": True})
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
