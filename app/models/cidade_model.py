from typing import Optional

from sqlalchemy import BigInteger, Identity, PrimaryKeyConstraint, Text, ForeignKeyConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models import base_model
from app.models.estado_model import Estado

class Cidade(base_model.Base):
    __tablename__ = 'Cidade'
    __table_args__ = (
        ForeignKeyConstraint(['estado_id'], ['Estado.id_estado'], name='Cidade_estado_id_fkey'),
        PrimaryKeyConstraint('id_cidade', name='Cidade_pkey')
    )

    id_cidade: Mapped[int] = mapped_column(BigInteger, Identity(start=1, increment=1, minvalue=1, maxvalue=9223372036854775807, cycle=False, cache=1), primary_key=True)
    nome: Mapped[str] = mapped_column(Text, nullable=False)
    estado_id: Mapped[Optional[int]] = mapped_column(BigInteger)

    estado: Mapped[Optional['Estado']] = relationship('Estado')
    #Endereco: Mapped[list['Endereco']] = relationship('Endereco', back_populates='cidade')

    def __init__(self, nome, estado_id = None):
        self.nome = nome
        self.estado_id = estado_id

    def __repr__(self):
        return f"<Cidade {self.id_cidade} - {self.nome}>"

    def to_dict(self):
        return {
            "id_cidade": self.id_cidade,
            "nome": self.nome,
            "estado_id": self.estado_id,
        }