from typing import Optional
import datetime

from sqlalchemy import BigInteger, Boolean, DateTime, Double, Enum, ForeignKeyConstraint, Identity, PrimaryKeyConstraint, Text, text
from sqlalchemy.orm import  Mapped, mapped_column, relationship
from app.models import base_model
from app.models.usuario_model import Usuario
from app.models.endereco_model import Endereco
from app.models.unidade_model import UnidadeMedida

class Doacao(base_model.Base):
    __tablename__ = 'Doacao'
    __table_args__ = (
        ForeignKeyConstraint(['doador_id'], ['Usuario.id_usuario'], name='Doacao_doador_id_fkey'),
        ForeignKeyConstraint(['endereco_id'], ['Endereco.id_endereco'], name='Doacao_endereco_id_fkey'),
        ForeignKeyConstraint(['receptor_id'], ['Usuario.id_usuario'], name='Doacao_receptor_id_fkey'),
        ForeignKeyConstraint(['unidade_id'], ['UnidadeMedida.id_unidade'], name='Doacao_unidade_id_fkey'),
        PrimaryKeyConstraint('id_doacao', name='Doacao_pkey')
    )

    id_doacao: Mapped[int] = mapped_column(BigInteger, Identity(start=1, increment=1, minvalue=1, maxvalue=9223372036854775807, cycle=False, cache=1), primary_key=True)
    data_cadastro: Mapped[datetime.datetime] = mapped_column(DateTime(True), nullable=False, server_default=text('now()'))
    doador_id: Mapped[Optional[int]] = mapped_column(BigInteger)
    receptor_id: Mapped[Optional[int]] = mapped_column(BigInteger)
    descricao: Mapped[Optional[str]] = mapped_column(Text)
    quantidade: Mapped[Optional[float]] = mapped_column(Double(53))
    unidade_id: Mapped[Optional[int]] = mapped_column(BigInteger)
    validade: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    endereco_id: Mapped[Optional[int]] = mapped_column(BigInteger)
    status: Mapped[Optional[str]] = mapped_column(Enum('Disponivel', 'Reservada', 'Finalizada', name='Status'))
    confirmacao_entrega: Mapped[Optional[bool]] = mapped_column(Boolean)
    confirmacao_recebimento: Mapped[Optional[bool]] = mapped_column(Boolean)
    data_entrega: Mapped[datetime.datetime] = mapped_column(DateTime(True), nullable=False)

    doador: Mapped[Optional['Usuario']] = relationship('Usuario', foreign_keys=[doador_id])
    endereco: Mapped[Optional['Endereco']] = relationship('Endereco')
    receptor: Mapped[Optional['Usuario']] = relationship('Usuario', foreign_keys=[receptor_id])
    unidade: Mapped[Optional['UnidadeMedida']] = relationship('UnidadeMedida')

    def __init__(self, doador_id = None, receptor_id = None, descricao = None, quantidade = None, unidade_id = None, validade = None, endereco_id = None, status = None):
        self.doador_id = doador_id
        self.receptor_id = receptor_id
        self.descricao = descricao
        self.quantidade = quantidade
        self.unidade_id = unidade_id
        self.validade = validade
        self.endereco_id = endereco_id
        self.status = status
        self.data_cadastro = datetime.datetime.now()
        self.confirmacao_entrega = False
        self.confirmacao_recebimento = False

    def __repr__(self):
        return f"<Doacao {self.id_doacao} - {self.descricao}>"

    def to_dict(self):
        return {
            "id_doacao":self.id_doacao,
            "doador_id":self.doador_id,
            "doador":self.doador.nome if self.doador else "N/A",
            "receptor_id":self.receptor_id,
            "receptor":self.receptor.nome if self.receptor else "N/A",
            "descricao":self.descricao,
            "quantidade":self.quantidade,
            "unidade_id":self.unidade_id,
            "unidade": self.unidade.nome if self.unidade else "N/A",
            "validade":self.validade.strftime("%d/%m/%Y") if self.validade else None,
            "endereco_id":self.endereco_id,
            "status":self.status,
            "data_cadastro":self.data_cadastro.strftime("%d/%m/%Y") if self.data_cadastro else None,
            "doador": self.doador.nome if self.doador else "Desconhecido",
            "confirmacao_entrega":self.confirmacao_entrega,
            "confirmacao_recebimento":self.confirmacao_recebimento,
            "data_entrega":self.data_entrega.strftime("%d/%m/%Y") if self.data_entrega else None
        }
