from flask import Blueprint, request, jsonify
from app.services.notificacao_service import NotificacaoService
from flask_jwt_extended import jwt_required, get_jwt_identity
from http import HTTPStatus

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
@jwt_required()
def update_notificacao(notificacao_id):
    try:
        data = request.get_json()
        usuario_id_str = get_jwt_identity()
        usuario_id = int(usuario_id_str)
        notificacao = service.update(notificacao_id, usuario_id, data)
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

@notificacao_bp.route("/pagina_notificacoes",methods=["GET"])
@jwt_required()
def pagina_notificacoes():
    try:
        usuario_id_str = get_jwt_identity()
        usuario_id = int(usuario_id_str)
        notificacaoes = service.get_all_notificacoes_by_usuario_id(usuario_id)
        return jsonify({"notificacoes":notificacaoes}), HTTPStatus.OK
    except Exception as e:
        print("erro: ",e)
        return jsonify({"error": "Erro interno ao buscar os dados da página de notificações"}), HTTPStatus.INTERNAL_SERVER_ERROR