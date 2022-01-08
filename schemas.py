from pydantic import BaseModel

# Create Item Schema (Pydantic Model)
class ItemCreate(BaseModel):
    name: str
   
    
# Complete Item Schema (Pydantic Model)
class Item(BaseModel):
    id: int
    name: str
    
    
    class Config:
        orm_mode = True