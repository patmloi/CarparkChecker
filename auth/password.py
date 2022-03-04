from passlib.context import CryptContext

pwdContext = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verifyPw(plainPw, hashedPw):
    return pwdContext.verify(plainPw, hashedPw)


def getHashedPw(plainPw: str) -> str:
    return pwdContext.hash(plainPw)
