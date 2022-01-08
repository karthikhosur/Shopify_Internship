from sqlalchemy import Column, Integer, String
from database import Base

# Define To Do class inheriting from Base
class Item(Base):
    __tablename__ = 'item'
    id = Column(Integer, primary_key=True)
    name = Column(String(256))
    