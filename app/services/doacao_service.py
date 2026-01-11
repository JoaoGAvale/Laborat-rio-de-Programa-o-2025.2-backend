from app.services.base_service import BaseService
from app.managers.doacao_manager import DoacaoManager
from app.managers.usuario_manager import UsuarioManager

class DoacaoService(BaseService):
    def __init__(self):
        super().__init__(DoacaoManager())
    
    manager: DoacaoManager
    usuario_manager: UsuarioManager

    # CREATE
    def create(self, data: dict):
        # validações básicas, ex: descrição obrigatória
        if "descricao" not in data:
            raise ValueError("Descrição é obrigatória")
        if "doador_id" not in data:
            raise ValueError("Doador_id é obrigatório")
        
        doacao = self.manager.create(**data)
        return doacao

    # READ por ID
    def get_by_id(self, doacao_id: int):
        doacao = self.manager.find_by_id(doacao_id)
        if not doacao:
            raise ValueError("Doação não encontrada")
        return doacao

    # LIST com filtros opcionais
    def list(self, **filters):
        return self.manager.find_all(**filters)

    # UPDATE por ID
    def update(self, doacao_id: int, data: dict):
        doacao = self.get_by_id(doacao_id)
        doacao = self.manager.update(doacao, **data)
        return doacao

    # DELETE por ID
    def delete(self, doacao_id: int):
        doacao = self.get_by_id(doacao_id)
        self.manager.delete(doacao)
        return True

    def get_user_history(self, user_id: int, status: str = None):
        if not user_id:
            raise ValueError("ID do usuário é obrigatório")

        if status:
            historico = self.manager.find_by_user_and_status(user_id, status)
        else:
            historico = self.manager.find_by_user(user_id)

        return historico
    

    def get_available_donations(self):
        return self.manager.find_all(status="Disponivel")