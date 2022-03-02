from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session 

from . import crud, models, schemas
from .db.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
'''
- Independent database session/connection per request
- Use the same session through all the request
- Close session after all requests are completed 
'''

def getDb():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/users/", response_model=schemas.User)
def createUser(user: schemas.UserCreate, db: Session = Depends(getDb)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

@app.get("/users/{user_id}", response_model=schemas.User)
def readUser(id: int, db: Session = Depends(getDb)):
    db_user = crud.get_user(db, id=id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


