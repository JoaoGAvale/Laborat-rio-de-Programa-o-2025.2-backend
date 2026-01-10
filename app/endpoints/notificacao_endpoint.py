from flask import Blueprint, request, jsonify
from app.services.notificacao_service import NotificacaoService

notificacao_bp = Blueprint("notificacao", __name__, url_prefix="/notificacao")
service = NotificacaoService()

# CREATE
@notificacao_bp.route("/", methods=["POST"])
def create_notificacao():
    try:
        data = request.get_json()
        notificacao = service.create(data)
        return jsonify(notificacao.to_dict()), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

# READ por ID
@notificacao_bp.route("/<int:notificacao_id>", methods=["GET"])
def get_notificacao(notificacao_id):
    try:
        notificacao = service.get_by_id(notificacao_id)
        return jsonify(notificacao.to_dict())
    except ValueError as e:
        return jsonify({"error": str(e)}), 404

# LIST com filtros opcionais
@notificacao_bp.route("/", methods=["GET"])
def list_notificacoes():
    filters = request.args.to_dict()
    notificacoes = service.list(**filters)
    return jsonify([n.to_dict() for n in notificacoes])

# UPDATE por ID
@notificacao_bp.route("/<int:notificacao_id>", methods=["PUT"])
def update_notificacao(notificacao_id):
    try:
        data = request.get_json()
        notificacao = service.update(notificacao_id, data)
        return jsonify(notificacao.to_dict())
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

# DELETE por ID
@notificacao_bp.route("/<int:notificacao_id>", methods=["DELETE"])
def delete_notificacao(notificacao_id):
    try:
        service.delete(notificacao_id)
        return jsonify({"message": "Notificação deletada com sucesso"}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
