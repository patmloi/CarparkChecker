from sqlalchemy.orm import Session
from . import models, schemas

def createUser(db: Session, user: schemas.UserCreateInternal): 
    dbUser = models.User(
        email = user.email,
        hashedPw = user.hashedPw,
        fName = user.fName, 
        lName = user.lName, 
        contactNo = user.contactNo
    )
    db.add(dbUser)
    db.commit()
    db.refresh(dbUser)

    return dbUser
    
def getUserById(db: Session, id: int):
    return db.query(models.User).filter(models.User.id == id).first()

def getUserByEmail(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

