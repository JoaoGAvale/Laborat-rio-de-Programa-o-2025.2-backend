from app.services.base_service import BaseService
from app.managers.estado_manager import EstadoManager

class EstadoService(BaseService):
    def __init__(self):
        super().__init__(EstadoManager())

    # CREATE
    def create(self, data: dict):
        if "nome" not in data or not data["nome"]:
            raise ValueError("Nome do estado é obrigatório")
        if "sigla" not in data or not data["sigla"]:
            raise ValueError("Sigla do estado é obrigatória")

        # opcional: checar duplicidade por sigla
        existente = self.manager.find_first_by(sigla=data["sigla"])
        if existente:
            raise ValueError("Já existe um estado com esta sigla")

        return self.manager.create(**data)

    # READ por ID
    def get_by_id(self, estado_id: int):
        estado = self.manager.find_by_id(estado_id)
        if not estado:
            raise ValueError("Estado não encontrado")
        return estado

    # LIST (opcionalmente com filtros)
    def list(self, **filters):
        return self.manager.find_all(**filters)

    # UPDATE sempre por ID
    def update(self, estado_id: int, data: dict):
        estado = self.get_by_id(estado_id)

        # opcional: checar duplicidade de sigla se estiver alterando
        if "sigla" in data:
            existente = self.manager.find_first_by(sigla=data["sigla"])
            if existente and existente.id_estado != estado.id_estado:
                raise ValueError("Já existe um estado com esta sigla")

        return self.manager.update(estado, **data)

    # DELETE sempre por ID
    def delete(self, estado_id: int):
        estado = self.get_by_id(estado_id)
        self.manager.delete(estado)
        return True
