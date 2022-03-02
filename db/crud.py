import pwd
from sqlalchemy.orm import Session
from . import models, schemas

def createUser(db: Session, user: schemas.schemaCreate):
    dbUser = models.user(
            email = user.email,
            hashedPw = user.pw,
            fName = user.fName, 
            lName = user.lName, 
            contactNo = user.contactNo
    )
    
def getUserByEmail(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email.first())