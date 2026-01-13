from flask import Blueprint, request, jsonify
from app.services.doacao_service import DoacaoService
from flask_jwt_extended import jwt_required, get_jwt_identity
from http import HTTPStatus

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
@jwt_required()
def get_doacao(doacao_id):
    try:
        usuario_id_str = get_jwt_identity()
        usuario_id = int(usuario_id_str)
        doacao = service.get_by_id(doacao_id,usuario_id)
        return jsonify(doacao.to_dict())
    except ValueError as e:
        return jsonify({"error": str(e)}), HTTPStatus.NOT_FOUND
    except Exception:
        return jsonify({"error": "Erro interno ao buscar doação."}), HTTPStatus.INTERNAL_SERVER_ERROR

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

# HISTÓRICO por Usuário (Doador ou Receptor)
@doacao_bp.route("/usuario/<int:user_id>", methods=["GET"])
def get_history(user_id):
    try:
        status = request.args.get("status")
        doacoes = service.get_user_history(user_id, status)      
        return jsonify([d.to_dict() for d in doacoes]), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Erro interno no servidor"}), 500

#Doações disponívels
@doacao_bp.route("/disponiveis", methods=["GET"])
def get_disponiveis():
    doacoes = service.get_available_donations()
    return jsonify([d.to_dict() for d in doacoes]), 200