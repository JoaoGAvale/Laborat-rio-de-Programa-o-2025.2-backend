from typing import Optional
import datetime

from sqlalchemy import BigInteger, DateTime, Enum, ForeignKeyConstraint, Identity, PrimaryKeyConstraint, Text, UniqueConstraint, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models import base_model
from app.models.endereco_model import Endereco

from werkzeug.security import generate_password_hash, check_password_hash

class Usuario(base_model.Base):
    __tablename__ = 'Usuario'
    __table_args__ = (
        ForeignKeyConstraint(['endereco_id'], ['Endereco.id_endereco'], name='Usuario_endereco_id_fkey'),
        PrimaryKeyConstraint('id_usuario', name='Usuario_pkey'),
        UniqueConstraint('cnpj', name='Usuario_cnpj_key')
    )

    id_usuario: Mapped[int] = mapped_column(BigInteger, Identity(start=1, increment=1, minvalue=1, maxvalue=9223372036854775807, cycle=False, cache=1), primary_key=True)
    data_cadastro: Mapped[datetime.datetime] = mapped_column(DateTime(True), nullable=False, server_default=text('now()'))
    cnpj: Mapped[str] = mapped_column(Text, nullable=False)
    nome: Mapped[Optional[str]] = mapped_column(Text)
    endereco_id: Mapped[Optional[int]] = mapped_column(BigInteger)
    perfil: Mapped[Optional[str]] = mapped_column(Enum('Doador', 'Receptor', 'Admin', name='Perfil'))
    email: Mapped[Optional[str]] = mapped_column(Text)
    password_hash: Mapped[Optional[str]] = mapped_column(Text)
    telefone: Mapped[Optional[str]] = mapped_column(Text)

    endereco: Mapped[Optional['Endereco']] = relationship('Endereco')
    #Doacao: Mapped[list['Doacao']] = relationship('Doacao', foreign_keys='[Doacao.doador_id]', back_populates='doador')
    #Doacao_: Mapped[list['Doacao']] = relationship('Doacao', foreign_keys='[Doacao.receptor_id]', back_populates='receptor')
    #Notificacao: Mapped[list['Notificacao']] = relationship('Notificacao', back_populates='usuario')

    def __init__(self, nome = None, cnpj = None, endereco_id = None, perfil=None, email = None, telefone = None):
        self.nome = nome
        self.cnpj = cnpj
        self.endereco_id = endereco_id
        self.perfil = perfil
        self.data_cadastro = datetime.datetime.now()
        self.email = email
        self.telefone = telefone

    def __repr__(self):
        return f"<Usuario {self.id_usuario} - {self.nome}>"

    def to_dict(self):
        return {
            "id_usuario":self.id_usuario,
            "nome":self.nome,
            "cnpj": self.cnpj,
            "endereco_id":self.endereco_id,
            "perfil":self.perfil,
            "data_cadastro":self.data_cadastro,
            "email":self.email,
            "password_hash":self.password_hash,
            "telefone": self.telefone
        }
    
    def set_password(self, password: str):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)