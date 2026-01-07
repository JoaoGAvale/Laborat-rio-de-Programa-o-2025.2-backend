from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from app.models.usuario_model import Usuario 
from app.services.usuario_service import UsuarioService
from app import db

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

usuario_service = UsuarioService()

@auth_bp.post("/login")
def login():
    data = request.get_json() or {}

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"message": "Credenciais inválidas"}), 400

    usuario : Usuario= usuario_service.get_usuario_by_email(email=email)

    # resposta genérica para evitar brute-force inteligente
    if not usuario or not usuario.check_password(password):
        return jsonify({"message": "Email ou senha incorretos"}), 401

    token = create_access_token(identity=usuario.id_usuario)

    return jsonify({
        "access_token": token,
        "user": {
            "id": usuario.id_usuario,
            "email": usuario.email
        }
    }), 200