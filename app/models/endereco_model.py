from typing import Optional
import datetime
from sqlalchemy import BigInteger, DateTime, ForeignKeyConstraint, Identity, PrimaryKeyConstraint, Text, text
from sqlalchemy.orm import  Mapped, mapped_column, relationship
from app.models import base_model
from app.models.cidade_model import Cidade

class Endereco(base_model.Base):
    __tablename__ = 'Endereco'
    __table_args__ = (
        ForeignKeyConstraint(['cidade_id'], ['Cidade.id_cidade'], name='Endereco_cidade_id_fkey'),
        PrimaryKeyConstraint('id_endereco', name='Endereco_pkey')
    )

    id_endereco: Mapped[int] = mapped_column(BigInteger, Identity(start=1, increment=1, minvalue=1, maxvalue=9223372036854775807, cycle=False, cache=1), primary_key=True)
    data_cadastro: Mapped[datetime.datetime] = mapped_column(DateTime(True), nullable=False, server_default=text('now()'))
    cidade_id: Mapped[Optional[int]] = mapped_column(BigInteger)
    logradouro: Mapped[Optional[str]] = mapped_column(Text)
    numero: Mapped[Optional[str]] = mapped_column(Text)
    cep: Mapped[Optional[str]] = mapped_column(Text)
    complemento: Mapped[Optional[str]] = mapped_column(Text)

    cidade: Mapped[Optional['Cidade']] = relationship('Cidade')
    #Usuario: Mapped[list['Usuario']] = relationship('Usuario', back_populates='endereco')
    #Doacao: Mapped[list['Doacao']] = relationship('Doacao', back_populates='endereco')

    def __init__(self, cidade_id = None, logradouro =None, numero=None, cep=None, complemento=None):
        self.cidade_id = cidade_id,
        self.logradouro = logradouro
        self.numero = numero,
        self.cep = cep,
        self.complemento = complemento,
        self.data_cadastro = datetime.datetime.now()

    def __repr__(self):
        return f"<Endereco {self.id_endereco} - {self.logradouro} - {self.numero} - {self.cep}>"

    def to_dict(self):
        return {
            "id_endereco": self.id_endereco,
            "logradouro":self.logradouro,
            "cidade_id":self.cidade_id,
            "numero":self.numero,
            "cep":self.cep,
            "complemento":self.complemento,
            "data_cadastro":self.data_cadastro
        }  