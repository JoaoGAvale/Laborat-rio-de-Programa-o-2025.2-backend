from sqlalchemy import BigInteger, Identity, PrimaryKeyConstraint, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models import base_model

class UnidadeMedida(base_model.Base):
    __tablename__ = 'UnidadeMedida'
    __table_args__ = (
        PrimaryKeyConstraint('id_unidade', name='UnidadeMedida_pkey'),
    )

    id_unidade: Mapped[int] = mapped_column(BigInteger, Identity(start=1, increment=1, minvalue=1, maxvalue=9223372036854775807, cycle=False, cache=1), primary_key=True)
    nome: Mapped[str] = mapped_column(Text, nullable=False)

    #Doacao: Mapped[list['Doacao']] = relationship('Doacao', back_populates='unidade')