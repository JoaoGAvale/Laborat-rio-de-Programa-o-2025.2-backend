from app import db
from app.models.usuario_model import Usuario

novo = Usuario(nome="Testando",cnpj="123123123",perfil="Receptor")
db.session.add(novo)
db.session.commit()