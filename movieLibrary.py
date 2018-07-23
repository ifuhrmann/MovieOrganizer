# -*- coding: utf-8 -*-
"""
Created on Sun Jul 15 13:13:14 2018

@author: Iddo
"""

import os.path
import time
import sqlalchemy as sq
import movieClassInfo
from sqlalchemy import Column, ForeignKey, Integer, String, Text, DateTime, func, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Table,MetaData
import sys

print('File         :', __file__)
print('Access time  :', time.ctime(os.path.getatime(__file__)))
print('Modified time:', time.ctime(os.path.getmtime(__file__)))
print('Change time  :', time.ctime(os.path.getctime(__file__)))
print('Size         :', os.path.getsize(__file__))

fstat = os.stat("F:/Wolf.Warrior.2.2017.1080p.BluRay.x264.DTS-WiKi.mkv")
print(fstat.st_size, "bytes")
print(fstat.st_size/(2**30),"gigabytes")


directory = os.scandir("F:/")
movieList = []

for d in directory:
    if(d.is_dir() and 'System Volume Information' not in d.name):
        levelTwoDir = os.scandir(d.path)
        for d2 in levelTwoDir:
            if ".mkv" in d2.name and "sample" not in d2.name.lower():
                movieList.append(d2)
    else:
        if "sample" not in d.name.lower() and 'System Volume Information' not in d.name and ('mkv' in d.name or 'mp4' in d.name):
            movieList.append(d)

print(len(movieList))

movieObjList=[]

for x in movieList:
    movieObjList.append( movieClassInfo.MovieInfo(x.name,x.path, time.ctime(os.path.getmtime(x.path)) , os.path.getsize(x.path) ) )

for x in movieObjList:
    break
    x.scrapeImdb()

print("")








Base = declarative_base()
db_path = "movieLibrary.db"
engine = create_engine('sqlite:///' + db_path)
    # Bind the engine to the metadata of the Base class so that the
    # declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine
metadata = MetaData(engine)

DBSession = sessionmaker(bind=engine)
    # A DBSession() instance establishes all conversations with the database
    # and represents a "staging zone" for all the objects loaded into the
    # database session object. Any change made against the objects in the
    # session won't be persisted into the database until you call
    # session.commit(). If you're not happy about the changes, you can
    # revert all of them back to the last commit by calling
    # session.rollback()
session = DBSession()

    
Base.metadata.create_all(engine)
   

try:
    movies = Table('movies', metadata, autoload=True)
except:
    movies = Table('movies',metadata,
                  Column('id',Integer, primary_key=True),
                  Column('filename',String),
                  Column('path',String),
                  Column('modifiedTime',String),
                  Column('size',Integer),
                  Column('actualName',String),
                  Column('hasSeen',Boolean),
                  Column('imdb',String),
                  Column('personalRating',Integer),

                  )
    movies.create()
    
"""
        self.filename = filename
        self.path = path
        self.modifiedTime = modifiedTime
        self.size = size
        self.actualName = actualName
        self.hasSeen = hasSeen
        self.imdb = imdb
        self.personalRating = personalRating
"""

for t in metadata.sorted_tables:
    print ("Table name: ", t.name)
    
s = movies.select()
rs = s.execute()
row = rs.fetchall()

for x in movieObjList:
    inDatabase = False
    for y in row:
        yinfo = movieClassInfo.MovieInfo(y["filename"],y["path"],y["modifiedTime"],
                                         y["size"],y["actualName"],y["hasSeen"],y["imdb"],y["personalRating"])
        if x == yinfo :
            inDatabase = True
    if inDatabase == False:
        x.scrapeImdb()
        i=movies.insert()
        i.execute({"filename":x.filename,"path":x.path,"modifiedTime":x.modifiedTime,
                   "size":x.size,"actualName":x.actualName,"hasSeen":x.hasSeen,
                   "imdb":x.imdb,"personalRating":x.personalRating})
    

s = movies.select()
rs = s.execute()
row = rs.fetchall()
for r in row:
    print(movieClassInfo.MovieInfo(r["filename"],r["path"],r["modifiedTime"],
                                   r["size"],r["actualName"],r["hasSeen"],r["imdb"],r["personalRating"])
    )
    print(r.imdb)

session.close()






