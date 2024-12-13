from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import scoped_session, sessionmaker, declarative_base

engine = create_engine('sqlite:///nome.sqlite3')
db_session = scoped_session(sessionmaker(bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()


class Clientes(Base):
    __tablename__ = ('TAB_CLIENTES')
    Nome = Column(String)
    Sobrenome = Column(String)
    id_cliente = Column(Integer, primary_key=True)
    CPF = Column(Integer, nullable=False, unique=True)
    telefone = Column(Integer, nullable=False, unique=True)

    def save(self):
        db_session.add(self)
        db_session.commit()

    def delete(self):
        db_session.delete(self)
        db_session.commit()

    def serialize_cliente(self):
        dados_cliente = {
            "Nome": self.Nome,
            "Sobrenome": self.Sobrenome,
            "id_cliente": self.id_cliente,
            "CPF": self.CPF,
            "telefone": self.telefone


        }

        return dados_cliente


class Produtos(Base):
    __tablename__ = 'TAB_PRODUTOS'
    Nome_produto = Column(String, nullable=False)
    tipo = Column(String, nullable=False)
    cor = Column(String, nullable=False)
    id_produto = Column(Integer, primary_key=True, unique=True)
    preco = Column(Float, nullable=False)



    def save(self):
        db_session.add(self)
        db_session.commit()

    def delete(self):
        db_session.delete(self)
        db_session.commit()

    def serialize_produto(self):
        dados_produtos = {
            "Nome_produto": self.Nome_produto,
            "tipo": self.tipo,
            "cor": self.cor,
            "id_produto": self.id_produto,
            "preco": self.preco


        }

        return dados_produtos


class Vendas(Base):
    __tablename__ = 'TAB_VENDAS'
    Nome = Column(String, nullable=False)
    tipo = Column(String, nullable=False)
    cor = Column(String, nullable=False)
    preco = Column(Float, nullable=False)
    id_vendas = Column(Integer, primary_key=True, unique=True)
    id_cliente = Column(Integer, ForeignKey('TAB_CLIENTES.id_cliente'), nullable=False)
    id_produto = Column(Integer, ForeignKey('TAB_PRODUTOS.id_produto'), nullable=False)

    def save(self):
        db_session.add(self)
        db_session.commit()

    def delete(self):
        db_session.delete(self)
        db_session.commit()

    def serialize_vendas(self):
        dados_vendas = {
            "Nome": self.Nome,
            "cor": self.cor,
            "tipo": self.tipo,
            "preco": self.preco,
            "id_vendas": self.id_vendas,
            "id_cliente": self.id_cliente,
            "id_produto": self.id_produto

        }

        return dados_vendas


def init_db():
    Base.metadata.create_all(bind=engine)


if __name__ == '__main__':
    init_db()