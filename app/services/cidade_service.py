from app.services.base_service import BaseService
from app.managers.cidade_manager import CidadeManager

class CidadeService(BaseService):
    def __init__(self):
        super().__init__(CidadeManager())

    # CREATE
    def create(self, data: dict):
        if "nome" not in data:
            raise ValueError("Nome da cidade é obrigatório")
        cidade = self.manager.create(**data)
        return cidade

    # READ por ID
    def get_by_id(self, cidade_id: int):
        cidade = self.manager.find_by_id(cidade_id)
        if not cidade:
            raise ValueError("Cidade não encontrada")
        return cidade

    # LIST (com filtros opcionais)
    def list(self, **filters):
        return self.manager.find_all(**filters)

    # UPDATE por ID
    def update(self, cidade_id: int, data: dict):
        cidade = self.get_by_id(cidade_id)
        cidade = self.manager.update(cidade, **data)
        return cidade

    # DELETE por ID
    def delete(self, cidade_id: int):
        cidade = self.get_by_id(cidade_id)
        self.manager.delete(cidade)
        return True
