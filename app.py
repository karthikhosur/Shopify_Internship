import databases
import sqlalchemy

from pydantic import BaseModel
from fastapi import FastAPI
from fastapi_crudrouter import DatabasesCRUDRouter


DATABASE_URL = "sqlite:///./inventory.db"

database = databases.Database(DATABASE_URL)
engine = sqlalchemy.create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

metadata = sqlalchemy.MetaData()
items = sqlalchemy.Table(
    "inventory",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String),
    sqlalchemy.Column("quantity", sqlalchemy.Integer),
    sqlalchemy.Column("warehouse_location", sqlalchemy.String),
)
metadata.create_all(bind=engine)

class ItemCreate(BaseModel):
    name: str
    quantity: float
    warehouse_location: str
    
class Item(ItemCreate):
    id: int
    
app = FastAPI()

@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


router = DatabasesCRUDRouter(
    schema=Item,
    create_schema=ItemCreate,
    table=items,
    database=database,
)

# @app.get('/_generate_csv',response_model = Item)
# def generate_csv():
#     print(Item)
#     return True

app.include_router(router)
    