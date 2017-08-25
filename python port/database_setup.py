from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class Admin(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(150), nullable=False)
    email = Column(String(150), nullable=False)
    password = Column(String(150), nullable=False)
    power = Column(String(150), server_default="User", nullable=False)

class Data(Base):
    __tablename__ = 'Data'

    id = Column(Integer, primary_key=True)
    Title = Column(String(100), nullable=False)
    name = Column(String(100), nullable=False)
    website = Column(String(100), nullable=True)
    phoneno = Column(String(100), nullable=True)
    description = Column(String(300), nullable=True)
    address = Column(String(100), nullable=True)

engine = create_engine('sqlite:///Database.db')
Base.metadata.create_all(engine)
