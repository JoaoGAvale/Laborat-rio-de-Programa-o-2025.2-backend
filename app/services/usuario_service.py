from app.services.base_service import BaseService
from app.managers.usuario_manager import UsuarioManager

# TODO: Adicionar as verificações (permissão, tratamento de erro, etc...)

class UsuarioService(BaseService):
    def __init__(self):
        super().__init__(UsuarioManager())

    def create(self, data: dict):
        return self.manager.create(**data)

    def get_by_id(self, _id):
        obj = self.manager.find_by_id(_id)
        if not obj:
            raise ValueError("Registro não encontrado")
        return obj

    def list(self, **filters):
        return self.manager.find_all(**filters)

    def update(self, _id, data: dict):
        obj = self.get_by_id(_id)
        return self.manager.update(obj, **data)

    def delete(self, _id):
        obj = self.get_by_id(_id)
        self.manager.delete(obj)
        return True
