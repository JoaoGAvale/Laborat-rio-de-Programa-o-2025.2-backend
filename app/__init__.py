from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from config import Config


db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(app)  # habilita acesso do Next.js

    db.init_app(app)

    from app.endpoints.usuario_endpoint import bp_usuario
    app.register_blueprint(bp_usuario)

    return app
