from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker 

# Database URL: SQL Lite 
# PostgreSQL: "postgresql://user:password@postgresserver/db"
DbUrl = "sqlite:///./sql_app.db"

# SQLALchemy engine 
engine = create_engine(
    DbUrl, connect_args={"check_same_thread": False} # check_same_thread not needed for PostgreSQL
)


