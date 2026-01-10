from app.services.base_service import BaseService
from app.managers.usuario_manager import UsuarioManager

class UsuarioService(BaseService):
    def __init__(self):
        super().__init__(UsuarioManager())

    # CREATE (não tem id ainda)
    def create(self, data: dict):
        if "password" not in data:
            raise ValueError("Senha é obrigatória")

        password = data.pop("password")

        usuario = self.manager.create(**data)
        usuario.set_password(password)

        # precisa commitar de novo pq alterou o objeto após o create
        self.manager.update(usuario)
        return usuario

    # READ por ID
    def get_by_id(self, usuario_id: int):
        usuario = self.manager.find_by_id(usuario_id)
        if not usuario:
            raise ValueError("Usuário não encontrado")
        return usuario

    # LIST (opcionalmente com filtros)
    def list(self, **filters):
        return self.manager.find_all(**filters)

    # UPDATE sempre por ID
    def update(self, usuario_id: int, data: dict):
        usuario = self.get_by_id(usuario_id)

        if "password" in data:
            usuario.set_password(data.pop("password"))

        usuario = self.manager.update(usuario, **data)
        return usuario

    # DELETE sempre por ID
    def delete(self, usuario_id: int):
        usuario = self.get_by_id(usuario_id)
        self.manager.delete(usuario)
        return True
