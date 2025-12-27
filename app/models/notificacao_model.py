from typing import Optional
import datetime

from sqlalchemy import BigInteger, DateTime, Enum, ForeignKeyConstraint, Identity, PrimaryKeyConstraint, Text, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models import base_model
from app.models.usuario_model import Usuario

class Notificacao(base_model.Base):
    __tablename__ = 'Notificacao'
    __table_args__ = (
        ForeignKeyConstraint(['usuario_id'], ['Usuario.id_usuario'], name='Notificacao_usuario_id_fkey'),
        PrimaryKeyConstraint('id_notificacao', name='Notificacao_pkey')
    )

    id_notificacao: Mapped[int] = mapped_column(BigInteger, Identity(start=1, increment=1, minvalue=1, maxvalue=9223372036854775807, cycle=False, cache=1), primary_key=True)
    data_cadastro: Mapped[datetime.datetime] = mapped_column(DateTime(True), nullable=False, server_default=text('now()'))
    condicao: Mapped[Optional[str]] = mapped_column(Enum('Lida', 'Nao lida', name='Condicao'))
    texto: Mapped[Optional[str]] = mapped_column(Text)
    usuario_id: Mapped[Optional[int]] = mapped_column(BigInteger)

    usuario: Mapped[Optional['Usuario']] = relationship('Usuario')

    def __init__(self, texto = None, usuario_id = None):
        self.data_cadastro = datetime.datetime.now()
        self.condicao = "Nao lida"
        self.usuario_id = usuario_id
        self.texto = texto

    def __repr__(self):
        return f"<Notificacao {self.id_notificacao} - {self.texto}>"

    def to_dict(self):
        return {
            "id_notificacao": self.id_notificacao,
            "data_cadastro": self.data_cadastro,
            "condicao":self.condicao,
            "texto":self.texto,
            "usuario_id":self.usuario_id
        }