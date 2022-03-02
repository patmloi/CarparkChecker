from sqlalchemy import VARCHAR, Boolean, Column, ForeignKey, Integer, String, Identity
from sqlalchemy.orm import relationship

from .database import Base

class User(Base):
    __tablename__ = "user"

    # Compulsory fields 
    # Login details
    id = Column('id', Integer, Identity(start=1, cycle=False), 
                primary_key=True, index=True, unique=True, nullable=False)

    email = Column('email', String, index=True, unique=True, nullable=False)
    hashedPw = Column('hashedPw', String, nullable=False)

    # Names
    fName = Column('fName', String, nullable=False)
    lName = Column('lName', String, nullable=False)

    # Optional fields
    contactNo = Column('contactNo', VARCHAR(15), nullable=True) # Follows E.164 format
    is_active = Column(Boolean, default=True)

