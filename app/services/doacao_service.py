from app.services.base_service import BaseService
from app.managers.doacao_manager import DoacaoManager
from app.managers.usuario_manager import UsuarioManager
from app.managers.unidade_manager import UnidadeManager

class DoacaoService(BaseService):
    def __init__(self):
        super().__init__(DoacaoManager())
        self.unidade_manager = UnidadeManager()
    
    manager: DoacaoManager
    usuario_manager: UsuarioManager

    def create(self, data: dict):
        if "descricao" not in data:
            raise ValueError("Descrição é obrigatória")
        if "doador_id" not in data:
            raise ValueError("Doador_id é obrigatório")

        nome_unidade = data.get("unidade") 
        
        if nome_unidade:
            # Busca ignorando espaços extras
            unidade_existente = self.unidade_manager.find_first_by(nome=nome_unidade.strip())
            
            if unidade_existente:
                unidade_id = unidade_existente.id_unidade
            else:
                # Cria a nova unidade
                nova_unidade = self.unidade_manager.create(nome=nome_unidade.strip())
                # Após o refresh no manager, o id_unidade estará disponível aqui
                unidade_id = nova_unidade.id_unidade
            
            data.pop("unidade", None)
            data["unidade_id"] = unidade_id

        doacao = self.manager.create(**data)
        return doacao

    # READ por ID
    def get_by_id(self, doacao_id: int, usuario_id: int):
        # usuario = self.usuario_manager.find_by_id(usuario_id)
        # if not usuario:
        #     raise ValueError("Usuário não encontrado")
        
        # doacao_doador = self.manager.find_first_by(id_doacao=doacao_id, doador_id=usuario_id)
        # doacao_receptor = self.manager.find_first_by(id_doacao=doacao_id, receptor_id=usuario_id)
        # doacao = doacao_doador or doacao_receptor
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