from typing import Optional
import datetime

from sqlalchemy import BigInteger, DateTime, Enum, ForeignKeyConstraint, Identity, PrimaryKeyConstraint, Text, UniqueConstraint, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models import base_model
from app.models.endereco_model import Endereco

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

    endereco: Mapped[Optional['Endereco']] = relationship('Endereco', back_populates='Usuario')
    #Doacao: Mapped[list['Doacao']] = relationship('Doacao', foreign_keys='[Doacao.doador_id]', back_populates='doador')
    #Doacao_: Mapped[list['Doacao']] = relationship('Doacao', foreign_keys='[Doacao.receptor_id]', back_populates='receptor')
    #Notificacao: Mapped[list['Notificacao']] = relationship('Notificacao', back_populates='usuario')