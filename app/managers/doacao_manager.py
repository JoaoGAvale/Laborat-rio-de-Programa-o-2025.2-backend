from app.managers.base_manager import BaseManager
from app.models.doacao_model import Doacao
from app import db  
from sqlalchemy import or_ , and_

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
    
    def acompanhar_doacoes(self, usuario_id: int, perfil: str):

        query = db.session.query(Doacao).filter(
            or_(
                and_(Doacao.doador_id == usuario_id, perfil == "Doador", Doacao.status != "Finalizada"),
                and_(Doacao.receptor_id == usuario_id, perfil == "Receptor", Doacao.status == "Reservada")
            )
        )

        return query.all()