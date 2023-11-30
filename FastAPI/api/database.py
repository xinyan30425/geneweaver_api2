# database.py

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker



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

# In the declarative system, the base class maintains a catalog of classes and tables
# relating to that base
Base = declarative_base()

# Create the tables
Base.metadata.create_all(bind=engine)
print("Tables created successfully.")


# Dependency to use in FastAPI endpoints to get a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
