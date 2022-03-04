from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session 

from jose import JWTError, jwt

from datetime import datetime, timedelta 

from db import crud, models, schemas
from db.database import engine, getDb
from db.schemas import User

from auth.signup import checkUser, updateUser 
from auth.user import authUser, getUserById

from domain.token import Token, TokenData
from auth.token import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, createToken

from fastapi import FastAPI, Form
from typing import Optional
from datetime import datetime
import requests
import urllib.parse


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

oauth2Scheme = OAuth2PasswordBearer(tokenUrl="token")

async def getCarparkAvail(dateTime: datetime):

    if dateTime == None or dateTime == '': 
        queryUrl = "https://api.data.gov.sg/v1/transport/carpark-availability"
    else: 
        carparkUrl = "https://api.data.gov.sg/v1/transport/carpark-availability?date_time="
        queryUrl = carparkUrl + urllib.parse.quote(str(dateTime).encode())

    response = requests.get(queryUrl)
    carparkAvail = response.json()
    return carparkAvail

async def getCurrentUser(token:str = Depends(oauth2Scheme), db: Session = Depends(getDb)) -> User:
    ''' Checks whether the current user is a valid user. '''
    credentialsException = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    # Decoding token -> ID 
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: int = payload.get("id")
        if id is None:
            raise credentialsException

        # tokenData = TokenData()
        user = getUserById(id, db)
        if user is None:
            raise credentialsException

    except JWTError:
        raise credentialsException

    return user

async def getCurrentActiveUser(currentUser: User=Depends(getCurrentUser)) -> User:
    if currentUser.isActive == 0:
        raise HTTPException(status_code=400, detail="Inactive user")
    return currentUser

@app.get("/")
async def root():
    return {"message": "Hello World"}


# 1. Registration
@app.post("/register", response_model=schemas.User)
def createUser(user: schemas.UserCreate, db: Session = Depends(getDb)):

    # Check for existing users with the same email
    dbUser = crud.getUserByEmail(db, email=user.email)
    if dbUser:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Registration parameters checks 
    success, errorStr = checkUser(user)
    if success:
         raise HTTPException(status_code=400, detail=errorStr)

    # Add new user to database 
    updatedUser = updateUser(user)
    
    return crud.createUser(db=db, user=updatedUser)

# 2. Login
@app.post("/token", response_model=Token)
async def login(formData: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(getDb)):
    # Autheticate user: Password check 
    user = authUser(formData.username, formData.password, db)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Generate a token for the user who logged in.
    tokenExpires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    token = createToken(
        id=user.id, 
        expiresDelta=tokenExpires
    )

    return {"access_token": token, "token_type": "bearer"}

# 3. View member details
@app.get("/me", response_model= User)
async def readUserMe(currentUser: User = Depends(getCurrentActiveUser)): 
    return currentUser


# 4.Carpark avaialability 
@app.post("/availability")
async def readCarparkAvail(currentUser: User = Depends(getCurrentActiveUser), dateTime: Optional[datetime] = Form(None)):
    print(bool(currentUser))
    if currentUser:
        carparkAvail = await getCarparkAvail(dateTime)
    return carparkAvail
