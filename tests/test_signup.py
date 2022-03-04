from auth.signup import *

# 1. Check email

# 1.1 Missing domain
def test_Email1():
    email = "johndoe"
    result = False

    emailCheck, emailError = checkEmail(email)
    assert emailCheck == result
    assert type(emailError) == str


# 1.2 Missing top-level domain
def test_Email2():
    email = "johndoe@gmail"
    result = False

    emailCheck, emailError = checkEmail(email)
    assert emailCheck == result
    assert type(emailError) == str


# 1.3 Missing user
def test_Email3():
    email = "@gmail.com"
    result = False

    emailCheck, emailError = checkEmail(email)
    assert emailCheck == result
    assert type(emailError) == str


# 1.4 Correct email
def test_Email4():
    email = "johndoe@gmail.com"
    result = True

    emailCheck, emailError = checkEmail(email)
    assert emailCheck == result
    assert type(emailError) == str


# 2. Check password

# 2.1 Password too short
def test_Pw1():
    pw = "Pw1"
    result = False
    errorList = ["Password must be at least 8 characters long."]

    pwCheck, pwErrorList = checkPw(pw)
    assert pwCheck == result
    assert pwErrorList == errorList


# 2.2. Password has no numbers
def test_Pw2():
    pw = "Password"
    result = False
    errorList = ["Password must contain at least 1 number."]

    pwCheck, pwErrorList = checkPw(pw)
    assert pwCheck == result
    assert pwErrorList == errorList


# 2.3. Password has no uppercase
def test_Pw3():
    pw = "password3"
    result = False
    errorList = ["Password must contain at least 1 uppercase letter."]

    pwCheck, pwErrorList = checkPw(pw)
    assert pwCheck == result
    assert pwErrorList == errorList


# 2.4 Password has no lowercase
def test_Pw4():
    pw = "PASSWORD4"
    result = False
    errorList = ["Password must contain at least 1 lowercase letter."]

    pwCheck, pwErrorList = checkPw(pw)
    assert pwCheck == result
    assert pwErrorList == errorList


# 2.5 Correct password
def test_Pw5():
    pw = "Password5"
    result = True
    errorList = []

    pwCheck, pwErrorList = checkPw(pw)
    assert pwCheck == result
    assert pwErrorList == errorList


# 3. Test name
# 3.1 Name too short
def test_Name1():
    name = ""
    nameType = "First"
    result = False
    errorList = [
        "First name must be at least 1 character long.",
        "First name must only contain letters.",
    ]

    nameCheck, nameErrorList = checkName(name, nameType)
    assert nameCheck == result
    assert nameErrorList == errorList


# 3.2 Name contains numbers
def test_Name2():
    name = "John2"
    nameType = "First"
    result = False
    errorList = ["First name must only contain letters."]

    nameCheck, nameErrorList = checkName(name, nameType)
    assert nameCheck == result
    assert nameErrorList == errorList


# 3.3 Correct name
def test_Name3():
    name = "John"
    nameType = "First"
    result = True
    errorList = []

    nameCheck, nameErrorList = checkName(name, nameType)
    assert nameCheck == result
    assert nameErrorList == errorList


# 4. Contact number

# 4.1 Empty string
def test_contactNo1():
    contactNo = ""
    result = True
    errorMsg = ""

    contactNoCheck, contactNoStr = checkContactNo(contactNo)
    assert contactNoCheck == result
    assert contactNoStr == errorMsg


# 4.2 Contains letters
def test_contactNo2():
    contactNo = "87654321a"
    result = False
    errorMsg = "Contact number must only contain digits."

    contactNoCheck, contactNoStr = checkContactNo(contactNo)
    assert contactNoCheck == result
    assert contactNoStr == errorMsg


# 4.3.1 Correct contact no: Contains spaces
def test_contactNo3():
    contactNo = "8765 4321"
    result = True
    errorMsg = ""

    contactNoCheck, contactNoStr = checkContactNo(contactNo)
    assert contactNoCheck == result
    assert contactNoStr == errorMsg


# 4.3.2 Correct contact no: No spaces
def test_contactNo4():
    contactNo = "87654321"
    result = True
    errorMsg = ""

    contactNoCheck, contactNoStr = checkContactNo(contactNo)
    assert contactNoCheck == result
    assert contactNoStr == errorMsg
