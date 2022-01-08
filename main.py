from typing import List
from fastapi import FastAPI, status, HTTPException, Depends
from fastapi.responses import StreamingResponse
import io
from database import Base, engine, SessionLocal
from sqlalchemy.orm import Session
import models
import schemas

# Create the database
Base.metadata.create_all(engine)

# Initialize app
app = FastAPI()

# Helper function to get database session
def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

@app.get("/")
def root():
    return "item"

@app.post("/Item", response_model=schemas.Item, status_code=status.HTTP_201_CREATED)
def create_Item(Item: schemas.ItemCreate, session: Session = Depends(get_session)):

    # create an instance of the Item database model
    Itemdb = models.Item(name = Item.name)

    # add it to the session and commit it
    session.add(Itemdb)
    session.commit()
    session.refresh(Itemdb)

    # return the Item object
    return Itemdb

@app.get("/Item/{id}", response_model=schemas.Item)
def read_Item(id: int, session: Session = Depends(get_session)):

    # get the Item item with the given id
    Item = session.query(models.Item).get(id)

    # check if Item item with given id exists. If not, raise exception and return 404 not found response
    if not Item:
        raise HTTPException(status_code=404, detail=f"Item item with id {id} not found")

    return Item

@app.put("/Item/{id}", response_model=schemas.Item)
def update_Item(id: int, name: str, session: Session = Depends(get_session)):

    # get the Item item with the given id
    Item = session.query(models.Item).get(id)

    # update Item item with the given name (if an item with the given id was found)
    if Item:
        Item.name = name
        
        session.commit()

    # check if Item item with given id exists. If not, raise exception and return 404 not found response
    if not Item:
        raise HTTPException(status_code=404, detail=f"Item item with id {id} not found")

    return Item

@app.delete("/Item/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_Item(id: int, session: Session = Depends(get_session)):

    # get the Item item with the given id
    Item = session.query(models.Item).get(id)

    # if Item item with given id exists, delete it from the database. Otherwise raise 404 error
    if Item:
        try:
            session.delete(Item)
            session.commit()
        except:
            return None
    else:
        raise HTTPException(status_code=404, detail=f"Item item with id {id} not found")

    return "Deleted"

@app.get("/Item_csv", response_model = List[schemas.Item])
def read_Item_list(session: Session = Depends(get_session)):

    # get all Item items
    

    Item_list = session.query(models.Item).all()
    stream = io.StringIO()
    response = StreamingResponse(iter([stream.getvalue()]),
                            media_type="text/csv"
       )
    response.headers["Content-Disposition"] = "attachment; filename=export.csv"
    
    return response



