from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session 

from db import crud
from db.database import getDb
from .password import verifyPw

def getUserById(id: int, db: Session = Depends(getDb)): #, token: str = Depends(oauth2Scheme)
    db_user = crud.getUserById(db, id=id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user 

def getUserByEmail(email: str, db: Session = Depends(getDb)): #, token: str = Depends(oauth2Scheme)
    db_user = crud.getUserByEmail(db, email)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

def authUser(email: str, enteredPw: str, db: Session = Depends(getDb)):
    user = getUserByEmail(email, db)
    if not user:
        return False
    if not verifyPw(enteredPw, user.hashedPw):
        return False
    return user