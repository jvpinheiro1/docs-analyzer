from sqlalchemy import Column, Integer, String
from database import Base

class Repositorio(Base):
    __tablename__ = "repositorios"
    id = Column(Integer, primary_key=True, index=True)
    github_url = Column(String, unique=True, index=True)
    name = Column(String)
    owner = Column(String)
    stars = Column(Integer)
    language = Column(String, nullable=True)
    description = Column(String, nullable=True)