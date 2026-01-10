from flask import Blueprint, request, jsonify, make_response
from flask_jwt_extended import create_access_token
from app.models.usuario_model import Usuario 
from app.services.usuario_service import UsuarioService
from flask_jwt_extended import jwt_required, get_jwt_identity

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

usuario_service = UsuarioService()

@auth_bp.post("/login")
def login():
    try:
        data = request.get_json() or {}
        email = data.get("email",None)
        password = data.get("password",None)

        if not email or not password:
            return jsonify({"message": "Credenciais inválidas"}), 400

        usuario : Usuario= usuario_service.get_usuario_by_email(email=email)

        # resposta genérica para evitar brute-force inteligente
        if not usuario or not usuario.check_password(password):
            return jsonify({"message": "Email ou senha incorretos"}), 401

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

        response.set_cookie("access_token_cookie", access_token, httponly=True)

        return response
    except Exception:
        return jsonify({"message": "Erro interno ao realizar login."}), 400

@auth_bp.get("/me")
@jwt_required()
def me():
    try:
        usuario_id_str = get_jwt_identity()
        usuario_id = int(usuario_id_str)
        return {"id_usuario": usuario_id}, 200
    except Exception:
        return jsonify({"message": "Erro interno ao buscar usuário logado."}), 400

@auth_bp.post("/logout")
@jwt_required()
def logout():
    try:
        response = make_response(jsonify({"message": "Logout realizado"}))

        response.delete_cookie("access_token_cookie")

        return response, 200
    except Exception:
        return jsonify({"message": "Erro interno ao realizar logout"}), 400