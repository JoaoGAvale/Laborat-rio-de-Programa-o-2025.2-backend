from app.managers.base_manager import BaseManager
from app.models.doacao_model import Doacao
from app import db  
from sqlalchemy import or_  

class DoacaoManager(BaseManager):
    model = Doacao

    def find_by_user(self, user_id: int):
        """Busca básica por usuário (Doador ou Receptor)"""
        return db.session.query(self.model).filter(
            or_(
                self.model.doador_id == user_id,
                self.model.receptor_id == user_id
            )
        ).all()

    def find_by_user_and_status(self, user_id: int, status: str):
        """Busca específica com status obrigatório no parâmetro"""
        return db.session.query(self.model).filter(
            or_(
                self.model.doador_id == user_id,
                self.model.receptor_id == user_id
            )
        ).filter(self.model.status == status).all()