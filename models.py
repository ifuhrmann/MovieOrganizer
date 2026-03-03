from db_manager import Base
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Float


class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True)
    filename = Column(String)
    path = Column(String)
    modifiedTime = Column(DateTime)
    size = Column(Integer)
    actualName = Column(String)
    hasSeen = Column(Boolean)
    imdb = Column(String)
    personalRating = Column(Integer)
    imdbRating = Column(Float)
    year = Column(Integer)

    def __init__(self, filename=None,path=None):
        self.hasSeen = False
        self.filename=filename
        self.path=path


    def __str__(self):
        if self.actualName is None or self.actualName == "":
            return self.filename
        else:
            return self.actualName

class Directory(Base):
    __tablename__ = "directories"

    id = Column(Integer, primary_key=True)
    path = Column(String)
    updateTime = Column(DateTime)

    def __str__(self):
        return self.path
