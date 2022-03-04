from typing import Optional
from datetime import datetime, timedelta

from jose import JWTError, jwt

SECRET_KEY = "bfa71874041e8e720954f455bf8734c283747f1040622ab7949577a8cc983f9f"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def createToken(id: int, expiresDelta: Optional[timedelta] = None):
    toEncode = {"id": id}
    if expiresDelta:
        expire = datetime.utcnow() + expiresDelta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    toEncode.update({"exp": expire})
    encodedJwt = jwt.encode(toEncode, SECRET_KEY, algorithm=ALGORITHM)
    return encodedJwt
