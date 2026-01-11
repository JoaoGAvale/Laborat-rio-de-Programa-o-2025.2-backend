from app.services.base_service import BaseService
from app.managers.notificacao_manager import NotificacaoManager

class NotificacaoService(BaseService):
    def __init__(self):
        super().__init__(NotificacaoManager())

    # CREATE
    def create(self, data: dict):
        if "texto" not in data or not data["texto"]:
            raise ValueError("Texto da notificação é obrigatório")
        if "usuario_id" not in data or not data["usuario_id"]:
            raise ValueError("Usuário da notificação é obrigatório")

        return self.manager.create(**data)

    # READ por ID
    def get_by_id(self, notificacao_id: int):
        estado = self.manager.find_by_id(notificacao_id)
        if not estado:
            raise ValueError("Estado não encontrado")
        return estado

    # LIST (opcionalmente com filtros)
    def list(self, **filters):
        return self.manager.find_all(**filters)

    # UPDATE sempre por ID
    def update(self, notificacao_id: int, usuario_id:int, data: dict):
        notificacao = self.manager.find_first_by(id_notificacao = notificacao_id, usuario_id = usuario_id)

        return self.manager.update(notificacao, **data)

    # DELETE sempre por ID
    def delete(self, notificacao_id: int):
        notificacao = self.get_by_id(notificacao_id)
        self.manager.delete(notificacao)
        return True

    def get_all_notificacoes_by_usuario_id(self, usuario_id:int)->list[dict]:
        notificacoes = self.manager.find_all(usuario_id = usuario_id)
        return [n.to_dict() for n in notificacoes]