from app.services.base_service import BaseService
from app.managers.unidade_manager import UnidadeManager

class UnidadeService(BaseService):
    def __init__(self):
        super().__init__(UnidadeManager())

    # CREATE
    def create(self, data: dict):
        if "nome" not in data or not data["nome"]:
            raise ValueError("O nome da unidade de medida é obrigatório")
        return self.manager.create(**data)

    # READ por ID
    def get_by_id(self, unidade_id: int):
        unidade = self.manager.find_by_id(unidade_id)
        if not unidade:
            raise ValueError("Unidade de medida não encontrada")
        return unidade

    # LIST com filtros opcionais
    def list(self, **filters):
        return self.manager.find_all(**filters)

    # UPDATE por ID
    def update(self, unidade_id: int, data: dict):
        unidade = self.get_by_id(unidade_id)
        unidade = self.manager.update(unidade, **data)
        return unidade

    # DELETE por ID
    def delete(self, unidade_id: int):
        unidade = self.get_by_id(unidade_id)
        self.manager.delete(unidade)
        return True
