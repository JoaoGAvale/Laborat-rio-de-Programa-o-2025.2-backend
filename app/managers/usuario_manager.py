from app.managers.base_manager import BaseManager
from app.models.usuario_model import Usuario

class UsuarioManager(BaseManager):
    model = Usuario

    def find_by_email(self, email: str):
        return self.find_first_by(email=email)

    def find_by_cnpj(self, cnpj: str):
        return self.find_first_by(cnpj=cnpj)
