from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

engine = create_engine("sqlite:///movieLibrary.db", future=True)
Session = sessionmaker(bind=engine, future=True)
Base = declarative_base()
