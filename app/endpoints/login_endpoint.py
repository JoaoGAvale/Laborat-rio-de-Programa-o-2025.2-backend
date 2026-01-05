from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from app.models.usuario_model import Usuario 
from app import db

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")