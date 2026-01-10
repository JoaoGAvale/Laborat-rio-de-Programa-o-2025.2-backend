from app.services.base_service import BaseService
from app.managers.endereco_manager import EnderecoManager

class EnderecoService(BaseService):
    def __init__(self):
        super().__init__(EnderecoManager())

    # CREATE
    def create(self, data: dict):
        # você pode colocar validações aqui se quiser
        endereco = self.manager.create(**data)
        return endereco

    # READ por ID
    def get_by_id(self, endereco_id: int):
        endereco = self.manager.find_by_id(endereco_id)
        if not endereco:
            raise ValueError("Endereço não encontrado")
        return endereco

    # LIST (opcionalmente com filtros)
    def list(self, **filters):
        return self.manager.find_all(**filters)

    # UPDATE sempre por ID
    def update(self, endereco_id: int, data: dict):
        endereco = self.get_by_id(endereco_id)
        endereco = self.manager.update(endereco, **data)
        return endereco

    # DELETE sempre por ID
    def delete(self, endereco_id: int):
        endereco = self.get_by_id(endereco_id)
        self.manager.delete(endereco)
        return True
