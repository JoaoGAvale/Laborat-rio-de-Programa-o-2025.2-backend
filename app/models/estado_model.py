from typing import Optional

from sqlalchemy import BigInteger, Identity, PrimaryKeyConstraint, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models import base_model
#from app.models.cidade_model import Cidade

class Estado(base_model.Base):
    __tablename__ = 'Estado'
    __table_args__ = (
        PrimaryKeyConstraint('id_estado', name='Estado_pkey'),
    )

    id_estado: Mapped[int] = mapped_column(BigInteger, Identity(start=1, increment=1, minvalue=1, maxvalue=9223372036854775807, cycle=False, cache=1), primary_key=True)
    nome: Mapped[Optional[str]] = mapped_column(Text)
    sigla: Mapped[Optional[str]] = mapped_column(Text)

    #Cidade: Mapped[list['Cidade']] = relationship('Cidade', back_populates='estado')

    def __init__(self, nome = None, sigla=None):
            self.nome = nome
            self.sigla = sigla

    def __repr__(self):
        return f"<Estado {self.id_estado} - {self.nome}>"

    def to_dict(self):
        return {
            "id_estado": self.id_estado,
            "nome": self.nome,
            "sigla": self.sigla,
        }