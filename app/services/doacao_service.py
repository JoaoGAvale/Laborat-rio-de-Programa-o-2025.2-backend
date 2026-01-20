from app.services.base_service import BaseService
from app.managers.doacao_manager import DoacaoManager
from app.managers.usuario_manager import UsuarioManager
from app.managers.unidade_manager import UnidadeManager
from app.models.doacao_model import Doacao
from app.models.usuario_model import Usuario

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
    def get_by_id(self, doacao_id: int):
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
    
    def pagina_detalhes(self, doacao_id: int, usuario_id:int):
        doacao : Doacao = self.manager.find_by_id(doacao_id)
        if not doacao:
            raise ValueError("Doação não encontrada")
        doacao_formatada={
            "id_doacao": doacao.id_doacao,
            "doador": doacao.doador.nome if doacao.doador_id else "Não definido",
            "doador_id": doacao.doador_id if doacao.doador_id else None,
            "receptor": doacao.receptor.nome if doacao.receptor_id else "Não definido",
            "receptor_id": doacao.receptor_id if doacao.receptor_id else None,
            "descricao": doacao.descricao,
            "quantidade": doacao.quantidade,
            "unidade": doacao.unidade.nome if doacao.unidade else "Não definida",
            "validade": doacao.validade.strftime("%d/%m/%Y") if doacao.validade else "Não definida",
            "data_cadastro": doacao.data_cadastro.strftime("%d/%m/%Y") if doacao.data_cadastro else "Não definida",
            "data_entrega": doacao.data_entrega.strftime("%d/%m/%Y") if doacao.data_entrega else "Não definida",
            "fotografia": "",
            "status": doacao.status,
            "confirmacao_entrega": doacao.confirmacao_entrega,
            "confirmacao_recebimento": doacao.confirmacao_recebimento,
            "endereco": {
            "logradouro": doacao.endereco.logradouro if doacao.endereco_id else "Não definido",
            "numero": doacao.endereco.numero if doacao.endereco_id else "Não definido",
            "cep": doacao.endereco.cep if doacao.endereco_id else "Não definido",
            "cidade": doacao.endereco.cidade.nome if doacao.endereco_id and doacao.endereco.cidade_id else "Não definida",
            "estado": doacao.endereco.cidade.estado.nome if doacao.endereco_id and doacao.endereco.cidade_id and doacao.endereco.cidade.estado_id else "Não definido",
            },
            "doador_info": {
            "nome": doacao.doador.nome if doacao.doador_id else "Não definido",
            "telefone": "(11) 99999-9999",
            "email": doacao.doador.email if doacao.doador_id else "Não definido",
            "endereco": "Rua das Flores, 123 - São Paulo/SP"
            },
            "receptor_info": {
            "nome": doacao.receptor.nome if doacao.receptor_id else "Não definido",
            "telefone": "(11) 98888-8888",
            "email": doacao.receptor.email if doacao.receptor_id else "Não definido",
            "endereco": "Av. Principal, 456 - São Paulo/SP"
            }
        }
        return doacao_formatada

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
    
    def acompanhar_doacoes(self, usuario_id: int, perfil: str):
        doacoes = self.manager.acompanhar_doacoes(usuario_id, perfil)
        return doacoes

    def get_available_donations(self):
        return self.manager.find_all(status="Disponivel")