from app.services.base_service import BaseService
from app.managers.usuario_manager import UsuarioManager

class UsuarioService(BaseService):
    def __init__(self):
        super().__init__(UsuarioManager())

    # CREATE (não tem id ainda)
    def create(self, data: dict):
        email = data.get("email",None)
        exist = self.manager.find_first_by(email = email)
        if exist:
            raise ValueError("Já existe um usuário com o email informado.")
        if "password" not in data:
            raise ValueError("Senha é obrigatória")

        password = data.pop("password")

        # O manager desse servise é o UsuarioManager
        usuario = self.manager.cadastrar_usuario(password,**data)

        return usuario

    # READ por ID
    def get_by_id(self, usuario_id: int):
        usuario = self.manager.find_by_id(usuario_id)
        if not usuario:
            raise ValueError("Usuário não encontrado")
        return usuario

    # LIST (opcionalmente com filtros)
    def list(self, **filters):
        return self.manager.find_all(**filters)

    # UPDATE sempre por ID
    def update(self, usuario_id: int, data: dict):
        usuario = self.get_by_id(usuario_id)

        CAMPOS_PERMITIDOS = {"nome", "cnpj", "email"}
        for campo in data:
            if campo not in CAMPOS_PERMITIDOS:
                data.pop(campo)
            elif not data.get(campo):
                data.pop(campo)

        email = data.get("email",None)
        if email:
            exist = self.manager.find_first_by(email = email)
            if exist and exist.id_usuario != usuario_id:
                raise ValueError("Já existe um usuário com o email informado.")

        ### Sem mudar a senha por enquanto
        # if "password" in data:
        #     usuario.set_password(data.pop("password"))

        usuario = self.manager.update(usuario, **data)
        return usuario

    # DELETE sempre por ID
    def delete(self, usuario_id: int):
        usuario = self.get_by_id(usuario_id)
        self.manager.delete(usuario)
        return True
    
    def get_usuario_by_email(self, email):
        return self.manager.find_first_by(email = email)
