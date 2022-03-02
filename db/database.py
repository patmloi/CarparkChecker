from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker 

# Database URL: SQL Lite 
# PostgreSQL: "postgresql://user:password@postgresserver/db"
# SQLite: "sqlite:///./sql_app.db"
dbUrl = "postgresql://user:password@postgresserver/db"

# SQLALchemy engine 
engine = create_engine(
    dbUrl, connect_args={} 
    # "check_same_thread": False
    # check_same_thread not needed for PostgreSQL
)

# Session 
sessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base: Returns class 
Base = declarative_base()