from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False, index=True)
    senha_hash = Column(String(255), nullable=False)
    criado_em = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relacionamento com Medico (1 para 1 opcional)
    medico = relationship("Medico", back_populates="usuario", uselist=False)

class Medico(Base):
    __tablename__ = "medicos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(150), nullable=False)
    crm = Column(String(10), unique=True, nullable=False, index=True)
    especialidade = Column(String(100), nullable=False)
    ativo = Column(Boolean, default=True)
    criado_em = Column(DateTime(timezone=True), server_default=func.now())
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=True)
    
    # Relacionamentos
    usuario = relationship("Usuario", back_populates="medico")
    consultas = relationship("Consulta", back_populates="medico")

class Paciente(Base):
    __tablename__ = "pacientes"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(150), nullable=False)
    cpf = Column(String(11), unique=True, nullable=False, index=True)
    data_nascimento = Column(String(10), nullable=False)  # DD/MM/YYYY
    telefone = Column(String(20), nullable=True)
    ativo = Column(Boolean, default=True)
    criado_em = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relacionamento
    consultas = relationship("Consulta", back_populates="paciente")

class Consulta(Base):
    __tablename__ = "consultas"

    id = Column(Integer, primary_key=True, index=True)
    data_consulta = Column(String(10), nullable=False)  # DD/MM/YYYY
    motivo = Column(String(300), nullable=False)
    status = Column(String(20), default='agendada')
    criado_em = Column(DateTime(timezone=True), server_default=func.now())
    medico_id = Column(Integer, ForeignKey("medicos.id"), nullable=False)
    paciente_id = Column(Integer, ForeignKey("pacientes.id"), nullable=False)
    
    # Relacionamentos
    medico = relationship("Medico", back_populates="consultas")
    paciente = relationship("Paciente", back_populates="consultas")