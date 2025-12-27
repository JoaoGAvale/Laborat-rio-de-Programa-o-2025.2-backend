from app.managers.base_manager import BaseManager
from app.models.usuario_model import Usuario

class UsuarioManager(BaseManager):
    model = Usuario