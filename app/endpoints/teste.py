from app import db
from app.models.cidade_model import Cidade

novo = Cidade(nome="Models Separados",estado_id = 1)
db.session.add(novo)
db.session.commit()