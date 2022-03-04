from email_validator import validate_email, EmailNotValidError
from typing import Tuple, Union

from db.schemas import UserCreate, UserCreateInternal
from auth.password import getHashedPw

def addError(errorList: list, errorPass: bool, errorMsg: Union[str, list]) -> list:
    ''' Adds new error messages to an error list. '''
    if errorPass == False:

        if type(errorMsg) == str:
            errorList.append(errorMsg)
        elif type(errorMsg) == list:
            errorList += errorMsg

    return errorList

def checkEmail(email: str) -> Tuple[bool, str]:
    ''' Checks for errors in the entered email. '''

    try: 
        valid = validate_email(email)
        emailCheck = True 
        errorMsg = ""

    except EmailNotValidError as e: 
        emailCheck = False 
        errorMsg = str(e)
        
    return emailCheck, errorMsg


def checkPw(pw: str) -> Tuple[bool, list]:
    ''' Checks for errors in the entered password.'''
    pwErrorList = []

    # 1. Minimum password length = 8
    checkLength = len(pw) >= 8
    checkLengthErrorMsg = "Password must be at least 8 characters long."
    pwErrorList = addError(pwErrorList, checkLength, checkLengthErrorMsg)

    # 2. Minimum no. of numbers = 1 
    checkNum = any([char.isdigit() for char in pw])
    checkNumErrorMsg = "Password must contain at least 1 number."
    pwErrorList = addError(pwErrorList, checkNum, checkNumErrorMsg)

    # 2. Minimum no. of uppercase letters = 1 
    checkUpper = any([char.isupper() for char in pw])
    checkUpperErrorMsg = "Password must contain at least 1 uppercase letter."
    pwErrorList = addError(pwErrorList, checkUpper, checkUpperErrorMsg)

    # 2. Minimum no. of lowercase letters = 1
    checkLower = any([char.islower() for char in pw])
    checkLowerErrorMsg = "Password must contain at least 1 lowercase letter."
    pwErrorList = addError(pwErrorList, checkLower, checkLowerErrorMsg)

    pwCheck = False if len(pwErrorList) > 0 else True 

    return pwCheck, pwErrorList

def checkName(name: str, nameType: str) -> Tuple[bool, list]:
    ''' Checks for errors in an entered name. '''
    nameErrorList = []
    
    checkLength = len(name) >= 1
    checkLengthErrorMsg = f"{nameType} name must be at least 1 character long."
    nameErrorList = addError(nameErrorList, checkLength, checkLengthErrorMsg)
    
    checkAlpha = name.isalpha() 
    checkAlphaErrorMsg = f"{nameType} name must only contain letters."
    nameErrorList = addError(nameErrorList, checkAlpha, checkAlphaErrorMsg)

    nameCheck = False if len(nameErrorList) > 0 else True 

    return nameCheck, nameErrorList

def checkContactNo(contactNo: str) -> Tuple[bool, str]:
    ''' Checks for errors in the entered contact number. '''

    if contactNo != "": 
        contactNoSpacing = contactNo.replace(" ", "")
        checkNum = contactNoSpacing.isdigit() 

        checkNumErrorMsg = "Contact number must only contain digits."
        checkNumMsg = "" if checkNum else checkNumErrorMsg

        return checkNum, checkNumMsg

    return True, ""

def checkUser(user: UserCreate) -> Tuple[bool, list]:
    ''' Checks for errors in the entered information. '''
    errorList = []

    # 1. Email
    emailCheck, emailError = checkEmail(user.email)
    errorList = addError(errorList, emailCheck, emailError)
    
    # 2. Password
    pwCheck, pwError = checkPw(user.password)
    errorList = addError(errorList, pwCheck, pwError)

    # 3.1 First name
    fNameCheck, fNameError = checkName(user.fName, "First")
    errorList = addError(errorList, fNameCheck, fNameError)

    # 3.2. Last name 
    lNameCheck, lNameError = checkName(user.lName, "Last")
    errorList = addError(errorList, lNameCheck, lNameError)
    
    # 4. Contact no
    checkNum, checkNumError = checkContactNo(user.contactNo)
    errorList = addError(errorList, checkNum, checkNumError)

    success = False if errorList == [] else True 
    errorStr = "" if errorList == [] else " ".join(errorList)

    return success, errorStr

def updateUser(user: UserCreate) -> UserCreateInternal:
    ''' Standardises user registration inputs. '''
    user = UserCreateInternal(
        email = validate_email(user.email).email,
        hashedPw = getHashedPw(user.password),
        fName = user.fName.capitalize(),
        lName = user.lName.capitalize(),
        contactNo = user.contactNo.replace(" ", "")
    )
    return user 