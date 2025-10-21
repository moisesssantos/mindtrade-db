from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, Date, Text, ForeignKey, TIMESTAMP
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from datetime import datetime

# 🔗 COLE aqui sua connection string (sem o prefixo psql)
DATABASE_URL = "psql 'postgresql://neondb_owner:npg_xdZKq5FRT8Wn@ep-dry-wind-adh6ysjv-pooler.c-2.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

class PreAnalise(Base):
    __tablename__ = "pre_analise"
    id = Column(Integer, primary_key=True)
    data_jogo = Column(Date)
    jogo = Column(String)
    mercado = Column(String)
    odd_inicial = Column(Float)
    trabalhar = Column(Boolean, default=False)
    observacao = Column(Text)
    entradas = relationship("Entrada", back_populates="pre_analise")

class Entrada(Base):
    __tablename__ = "entradas"
    id = Column(Integer, primary_key=True)
    id_pre_analise = Column(Integer, ForeignKey("pre_analise.id"))
    stake = Column(Float)
    odd_entrada = Column(Float)
    minuto = Column(Integer)
    resultado = Column(String)
    concluida = Column(Boolean, default=False)
    data_criacao = Column(TIMESTAMP, default=datetime.utcnow)
    pre_analise = relationship("PreAnalise", back_populates="entradas")
    historico = relationship("Historico", back_populates="entrada", uselist=False)

class Historico(Base):
    __tablename__ = "historico"
    id = Column(Integer, primary_key=True)
    id_entrada = Column(Integer, ForeignKey("entradas.id"))
    lucro_prejuizo = Column(Float)
    data_conclusao = Column(TIMESTAMP, default=datetime.utcnow)
    observacao = Column(Text)
    entrada = relationship("Entrada", back_populates="historico")

Base.metadata.create_all(engine)
print("✅ Tabelas criadas com sucesso!")
