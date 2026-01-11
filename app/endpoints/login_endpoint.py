from flask import Blueprint, request, jsonify, make_response
from flask_jwt_extended import create_access_token
from app.models.usuario_model import Usuario 
from app.services.usuario_service import UsuarioService
from flask_jwt_extended import jwt_required, get_jwt_identity
from http import HTTPStatus

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

usuario_service = UsuarioService()

@auth_bp.post("/login")
def login():
    try:
        data = request.get_json() or {}
        email = data.get("email",None)
        password = data.get("password",None)

        if not email or not password:
            return jsonify({"error": "Credenciais inválidas"}), HTTPStatus.INTERNAL_SERVER_ERROR

        usuario : Usuario= usuario_service.get_usuario_by_email(email=email)

        # resposta genérica para evitar brute-force inteligente
        if not usuario or not usuario.check_password(password):
            return jsonify({"error": "Email ou senha incorretos"}), HTTPStatus.UNAUTHORIZED

        access_token = create_access_token(identity=f"{usuario.id_usuario}")

        response = make_response(jsonify({
            "user": {
                "id_usuario": usuario.id_usuario,
                "email": usuario.email,
                "nome": usuario.nome,
                "perfil":usuario.perfil,
                "cnpj":usuario.cnpj
            }
        }))

        response.set_cookie(
            "access_token_cookie", 
            access_token, 
            httponly=True,
            samesite="Lax",
            secure=False
            )

        return response
    except Exception:
        return jsonify({"error": "Erro interno ao realizar login."}), HTTPStatus.INTERNAL_SERVER_ERROR

@auth_bp.get("/me")
@jwt_required()
def me():
    try:
        usuario_id_str = get_jwt_identity()
        usuario_id = int(usuario_id_str)
        return jsonify({"usuario_id": usuario_id}), HTTPStatus.OK
    except Exception:
        return jsonify({"error": "Erro interno ao buscar usuário logado."}), HTTPStatus.INTERNAL_SERVER_ERROR

@auth_bp.post("/logout")
@jwt_required()
def logout():
    try:
        response = make_response(jsonify({"message": "Logout realizado"}))

        response.delete_cookie("access_token_cookie")

        return response, HTTPStatus.OK
    except Exception:
        return jsonify({"error": "Erro interno ao realizar logout"}), HTTPStatus.INTERNAL_SERVER_ERROR