from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker 

# Database URL: SQL Lite 
DbUrl = "sqlite:///./sql_app.db"

# SQLALchemy engine 
engine = create_engine(
    DbUrl, connect_args={"check_same_thread": False}
)


