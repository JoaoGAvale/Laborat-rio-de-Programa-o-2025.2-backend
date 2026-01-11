from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import Config
import os

db = SQLAlchemy()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(
        app,
        supports_credentials=True,
        origins=["http://localhost:3000"]
        #origins=[os.getenv("ORIGINS")]
    )
  # habilita acesso do Next.js

    db.init_app(app)

    from app.endpoints.usuario_endpoint import usuario_bp
    from app.endpoints.login_endpoint import auth_bp
    from app.endpoints.cidade_endpoint import cidade_bp
    from app.endpoints.doacao_endpoint import doacao_bp
    from app.endpoints.endereco_endpoint import endereco_bp
    from app.endpoints.notificacao_endpoint import notificacao_bp
    from app.endpoints.unidade_endpoint import unidade_bp
    from app.endpoints.estado_endpoint import estado_bp

    app.register_blueprint(usuario_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(cidade_bp)
    app.register_blueprint(doacao_bp)
    app.register_blueprint(endereco_bp)
    app.register_blueprint(notificacao_bp)
    app.register_blueprint(unidade_bp)
    app.register_blueprint(estado_bp)

    jwt.init_app(app)

    return app
