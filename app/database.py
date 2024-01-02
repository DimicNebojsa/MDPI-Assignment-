"""Package for databse engine and session.

Author: Nebojsa Dimic
Date: 1/2/2024
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


SQLALCHEMY_DATABASE_URL = "postgresql://postgres:postgres@localhost/mdpi"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency
def get_db() -> SessionLocal:
    """Generator that provides local session."""
    """
        Args:
            None
                
        Excpetions:
            HTTP exceptions    

        Returns:
            SessionLocal
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
        
        
    

