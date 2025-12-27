from typing import Optional
import datetime

from sqlalchemy import BigInteger, Boolean, Column, DateTime, Double, Enum, ForeignKeyConstraint, Identity, Numeric, PrimaryKeyConstraint, Table, Text, UniqueConstraint, text
from sqlalchemy.dialects.postgresql import OID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass


class Estado(Base):
    __tablename__ = 'Estado'
    __table_args__ = (
        PrimaryKeyConstraint('id_estado', name='Estado_pkey'),
    )

    id_estado: Mapped[int] = mapped_column(BigInteger, Identity(start=1, increment=1, minvalue=1, maxvalue=9223372036854775807, cycle=False, cache=1), primary_key=True)
    nome: Mapped[Optional[str]] = mapped_column(Text)
    sigla: Mapped[Optional[str]] = mapped_column(Text)

    Cidade: Mapped[list['Cidade']] = relationship('Cidade', back_populates='estado')


class UnidadeMedida(Base):
    __tablename__ = 'UnidadeMedida'
    __table_args__ = (
        PrimaryKeyConstraint('id_unidade', name='UnidadeMedida_pkey'),
    )

    id_unidade: Mapped[int] = mapped_column(BigInteger, Identity(start=1, increment=1, minvalue=1, maxvalue=9223372036854775807, cycle=False, cache=1), primary_key=True)
    nome: Mapped[str] = mapped_column(Text, nullable=False)

    Doacao: Mapped[list['Doacao']] = relationship('Doacao', back_populates='unidade')


t_pg_stat_statements = Table(
    'pg_stat_statements', Base.metadata,
    Column('userid', OID),
    Column('dbid', OID),
    Column('toplevel', Boolean),
    Column('queryid', BigInteger),
    Column('query', Text),
    Column('plans', BigInteger),
    Column('total_plan_time', Double(53)),
    Column('min_plan_time', Double(53)),
    Column('max_plan_time', Double(53)),
    Column('mean_plan_time', Double(53)),
    Column('stddev_plan_time', Double(53)),
    Column('calls', BigInteger),
    Column('total_exec_time', Double(53)),
    Column('min_exec_time', Double(53)),
    Column('max_exec_time', Double(53)),
    Column('mean_exec_time', Double(53)),
    Column('stddev_exec_time', Double(53)),
    Column('rows', BigInteger),
    Column('shared_blks_hit', BigInteger),
    Column('shared_blks_read', BigInteger),
    Column('shared_blks_dirtied', BigInteger),
    Column('shared_blks_written', BigInteger),
    Column('local_blks_hit', BigInteger),
    Column('local_blks_read', BigInteger),
    Column('local_blks_dirtied', BigInteger),
    Column('local_blks_written', BigInteger),
    Column('temp_blks_read', BigInteger),
    Column('temp_blks_written', BigInteger),
    Column('shared_blk_read_time', Double(53)),
    Column('shared_blk_write_time', Double(53)),
    Column('local_blk_read_time', Double(53)),
    Column('local_blk_write_time', Double(53)),
    Column('temp_blk_read_time', Double(53)),
    Column('temp_blk_write_time', Double(53)),
    Column('wal_records', BigInteger),
    Column('wal_fpi', BigInteger),
    Column('wal_bytes', Numeric),
    Column('jit_functions', BigInteger),
    Column('jit_generation_time', Double(53)),
    Column('jit_inlining_count', BigInteger),
    Column('jit_inlining_time', Double(53)),
    Column('jit_optimization_count', BigInteger),
    Column('jit_optimization_time', Double(53)),
    Column('jit_emission_count', BigInteger),
    Column('jit_emission_time', Double(53)),
    Column('jit_deform_count', BigInteger),
    Column('jit_deform_time', Double(53)),
    Column('stats_since', DateTime(True)),
    Column('minmax_stats_since', DateTime(True))
)


t_pg_stat_statements_info = Table(
    'pg_stat_statements_info', Base.metadata,
    Column('dealloc', BigInteger),
    Column('stats_reset', DateTime(True))
)


class Cidade(Base):
    __tablename__ = 'Cidade'
    __table_args__ = (
        ForeignKeyConstraint(['estado_id'], ['Estado.id_estado'], name='Cidade_estado_id_fkey'),
        PrimaryKeyConstraint('id_cidade', name='Cidade_pkey')
    )

    id_cidade: Mapped[int] = mapped_column(BigInteger, Identity(start=1, increment=1, minvalue=1, maxvalue=9223372036854775807, cycle=False, cache=1), primary_key=True)
    nome: Mapped[str] = mapped_column(Text, nullable=False)
    estado_id: Mapped[Optional[int]] = mapped_column(BigInteger)

    estado: Mapped[Optional['Estado']] = relationship('Estado', back_populates='Cidade')
    Endereco: Mapped[list['Endereco']] = relationship('Endereco', back_populates='cidade')


class Endereco(Base):
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

    cidade: Mapped[Optional['Cidade']] = relationship('Cidade', back_populates='Endereco')
    Usuario: Mapped[list['Usuario']] = relationship('Usuario', back_populates='endereco')
    Doacao: Mapped[list['Doacao']] = relationship('Doacao', back_populates='endereco')


class Usuario(Base):
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
    Doacao: Mapped[list['Doacao']] = relationship('Doacao', foreign_keys='[Doacao.doador_id]', back_populates='doador')
    Doacao_: Mapped[list['Doacao']] = relationship('Doacao', foreign_keys='[Doacao.receptor_id]', back_populates='receptor')
    Notificacao: Mapped[list['Notificacao']] = relationship('Notificacao', back_populates='usuario')


class Doacao(Base):
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

    doador: Mapped[Optional['Usuario']] = relationship('Usuario', foreign_keys=[doador_id], back_populates='Doacao')
    endereco: Mapped[Optional['Endereco']] = relationship('Endereco', back_populates='Doacao')
    receptor: Mapped[Optional['Usuario']] = relationship('Usuario', foreign_keys=[receptor_id], back_populates='Doacao_')
    unidade: Mapped[Optional['UnidadeMedida']] = relationship('UnidadeMedida', back_populates='Doacao')


class Notificacao(Base):
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

    usuario: Mapped[Optional['Usuario']] = relationship('Usuario', back_populates='Notificacao')
