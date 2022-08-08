from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

SQLALCHEMY_DATABASE_URL = "postgresql://mustafa:hasanat123@localhost/store"

engine = create_engine(SQLALCHEMY_DATABASE_URL, convert_unicode=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

Base = declarative_base()
# Base.query = SessionLocal.query_property()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()