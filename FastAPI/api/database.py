# database.py
# Here define the database connection and session management. 
# For SQLAlchemy, this would typically include the engine, session, and base declarative class used to define models.

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import GeneSet, AnalysisRun, AnalysisResult,Base

# The database URL for SQLite, it's a local file
DATABASE_URL = "sqlite:///./geneweaver.db"

# An Engine, which the Session will use for connection
# resources, typically just one instance per application
engine = create_engine(
    DATABASE_URL, 
    connect_args={"check_same_thread": False}  # Only needed for SQLite
)

# Each instance of the SessionLocal class will be a database session
# The class itself is not a database session yet
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Dependency to use in FastAPI endpoints to get a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
# Create the tables
# Base.metadata.create_all(bind=engine)
Base.metadata.create_all(bind=engine, tables=[GeneSet.__table__, AnalysisRun.__table__, AnalysisResult.__table__])
print("Tables created successfully.")
