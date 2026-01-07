from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import Config

db = SQLAlchemy()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(app)  # habilita acesso do Next.js

    db.init_app(app)

    from app.endpoints.usuario_endpoint import usuario_bp
    from app.endpoints.login_endpoint import auth_bp
    app.register_blueprint(usuario_bp)
    app.register_blueprint(auth_bp)

    jwt.init_app(app)

    return app
