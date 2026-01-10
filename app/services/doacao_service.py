from app.services.base_service import BaseService
from app.managers.doacao_manager import DoacaoManager

class DoacaoService(BaseService):
    def __init__(self):
        super().__init__(DoacaoManager())

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
