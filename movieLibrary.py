# -*- coding: utf-8 -*-
"""
Created on Sun Jul 15 13:13:14 2018

@author: Iddo
"""

import os.path
import time
import sqlalchemy as sq
import movieClassInfo
from sqlalchemy import Column, ForeignKey, Integer, String, Text, DateTime, func, Boolean,Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Table,MetaData
import sys
from datetime import datetime

class MovieLibrary():
    
    def __init__(self, directories,ignoreList=[]):
        self.directories=directories
        self.ignoreList = ignoreList
        self.scrapeAll()

    
    def printAll(self):
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
           
        movies = Table('movies', metadata, autoload=True)
        
        s = movies.select()
        rs = s.execute()
        row = rs.fetchall()
        for r in row:
            print( movieClassInfo.MovieInfo(r["filename"],r["path"],r["modifiedTime"],
                                           r["size"],r["actualName"],r["hasSeen"],r["imdb"],r["personalRating"],r["imdbRating"],r["year"]))
        print("\n"+str(len(row)))
        session.close()

        
    
    
    def scrapeFolder(self,direct):
        directory = os.scandir(direct)
        movieList = []
        
        for d in directory:
            if(d.is_dir() and 'System Volume Information' not in d.name):
                levelTwoDir = os.scandir(d.path)
                for d2 in levelTwoDir:
                    if ((not d2.is_dir()) and (d2.path.endswith(".mkv") or d2.path.endswith(".mp4")) and
                        "sample" not in d2.name.lower() and os.path.getsize(d2) > 500000000 and
                        "S0" not in d2.path):
                        ignore = False
                        for i in self.ignoreList:
                            if(d2.path.startswith(i)):
                                ignore = True
                        if not ignore:
                            movieList.append(d2)
            else:
                if ("sample" not in d.name.lower() and 'System Volume Information' not in d.name and
                    'DVD' not in d.name and (d.path.endswith(".mkv") or d.path.endswith(".mp4")) and
                    os.path.getsize(d)  > 500000000 and "S0" not in d.path):
                    ignore = False
                    for i in self.ignoreList:
                        if(d.path.startswith(i)):
                            ignore = True
                    if not ignore:
                        movieList.append(d)

        
        print(len(movieList))
        
        movieObjList=[]
        
        for x in movieList:
            movieObjList.append( movieClassInfo.MovieInfo(x.name,x.path, time.ctime(os.path.getmtime(x.path)) , os.path.getsize(x.path) ) )
        
        for x in movieObjList:
            datetime_object = datetime.strptime(x.modifiedTime,"%a %b %d %H:%M:%S %Y")
            x.modifiedTime=datetime_object
        
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
                          Column('modifiedTime',DateTime),
                          Column('size',Integer),
                          Column('actualName',String),
                          Column('hasSeen',Boolean),
                          Column('imdb',String),
                          Column('personalRating',Integer),
                          Column('imdbRating',Float),
                          Column('year',Integer)
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
                                                 y["size"],y["actualName"],y["hasSeen"],y["imdb"],
                                                 y["personalRating"],y["imdbRating"],y["year"])
                if x == yinfo :
                    inDatabase = True
            if inDatabase == False:
                try:
                    x.scrapeImdb()
                except:
                    print("stupid ratshit imdb search is down for some reason")
                i=movies.insert()
                i.execute({"filename":x.filename,"path":x.path,"modifiedTime":x.modifiedTime,
                           "size":x.size,"actualName":x.actualName,"hasSeen":x.hasSeen,
                           "imdb":x.imdb,"personalRating":x.personalRating,"imdbRating":x.imdbRating,"year":x.year})
        for y in row:
            #ydatetime = datetime.strptime(y['modifiedTime'],"%Y-%m-%d %H:%M:%S")
            yinfo = movieClassInfo.MovieInfo(y["filename"],y["path"],y['modifiedTime'],
                                             y["size"],y["actualName"],y["hasSeen"],y["imdb"]
                                             ,y["personalRating"],y["imdbRating"],y["year"])
            inFolder = False
            if(direct in y['path']):   
                for x in movieObjList:
                    if x == yinfo:
                        inFolder = True
                if(inFolder== False):
                    d = movies.delete().where(movies.c.id == y['id'])
                    rs = d.execute()
                    print("deleted")
        session.close()


    def scrapeAll(self):
        for f in self.directories:
            self.scrapeFolder(f)
    
    
    def sortBy(self,sort):
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
           
        movies = Table('movies', metadata, autoload=True)
        
        s = movies.select().order_by(sort)
        rs = s.execute()
        row = rs.fetchall()
        mList = []
        for r in row:
            for d in self.directories:
                if(r["path"].startswith(d)):
                    mList.append(movieClassInfo.MovieInfo(r["filename"],r["path"],r["modifiedTime"],
                                           r["size"],r["actualName"],r["hasSeen"],r["imdb"],
                                           r["personalRating"],r["imdbRating"],r["year"]))
                    break
        print("\n"+str(len(row)))
        session.close()
        return mList
            
    
            
    def updateAll(self):
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
           
        movies = Table('movies', metadata, autoload=True)
        
        s = movies.select()
        rs = s.execute()
        row = rs.fetchall()
        for r in row:
            if (r["imdb"]==None):
                mov = movieClassInfo.MovieInfo(r["filename"],r["path"],r["modifiedTime"],
                                           r["size"],r["actualName"],r["hasSeen"],r["imdb"],
                                           r["personalRating"],r["imdbRating"],r['year'])
                try:
                    mov.scrapeImdb()
                    conn = engine.connect()
                    stmt = movies.update().\
                           values(imdb = mov.imdb , actualName = mov.actualName , imdbRating = mov.imdbRating, year = mov.year).\
                           where(movies.c.path == mov.path)
                    conn.execute(stmt)
                    print(mov.filename, "updated with name",mov.actualName,"imdb",mov.imdb)
                except:
                    print("stupid ratshit imdb isn't working")
        session.close()
        
        
    def updateImdb(self,movie,imdb):
        try:
            movie.updateImdb(imdb)
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
               
            movies = Table('movies', metadata, autoload=True)
            conn = engine.connect()
            stmt = movies.update().\
                            values(imdb = movie.imdb , actualName = movie.actualName , imdbRating = movie.imdbRating, year = movie.year).\
                            where(movies.c.path == movie.path)
            conn.execute(stmt)
            print(movie.filename, "updated with name",movie.actualName,"imdb",movie.imdb)
            session.close()
        except:
            print("imdb isn't working right now")


    def updateRating(self,movie,rate):
        movie.updateRating(rate)
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
           
        movies = Table('movies', metadata, autoload=True)
        conn = engine.connect()
        stmt = movies.update().\
                        values(personalRating=movie.personalRating).\
                        where(movies.c.path == movie.path)
        conn.execute(stmt)
        print(movie.filename, "updated with rating ",movie.personalRating)
        session.close()

    def setSeen(movie,seen):
        print(movie,seen)
        movie.setSeen(seen)
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
           
        movies = Table('movies', metadata, autoload=True)
        conn = engine.connect()
        stmt = movies.update().\
                        values(hasSeen=movie.hasSeen).\
                        where(movies.c.path == movie.path)
        conn.execute(stmt)
        print(movie.filename, "updated with seen ",movie.hasSeen)
        session.close()
        
        
        
    def setPersonalRating(movie,rating):
        print(movie,rating)
        movie.updateRating(rating)
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
           
        movies = Table('movies', metadata, autoload=True)
        conn = engine.connect()
        stmt = movies.update().\
                        values(personalRating=movie.personalRating).\
                        where(movies.c.path == movie.path)
        conn.execute(stmt)
        print(movie.filename, "updated with rating ",movie.personalRating)
        session.close()



#if you initialize a movieLibrary with a folder and a folder inside it you're going to hell