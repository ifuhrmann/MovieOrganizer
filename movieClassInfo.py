# -*- coding: utf-8 -*-
from imdb import IMDb
import re
import datetime

def imdbTest():
    ia = IMDb()
    # get a movie and print its director(s)
    m = ia.get_movie("2592594")
    print(m.get('year'))


class MovieInfo():
    def __init__(self,filename,path,modifiedTime,size,actualName=None,hasSeen=False,
                 imdb=None,personalRating=None,imdbRating = None,year=None):
        self.filename = filename
        self.path = path
        self.modifiedTime = modifiedTime
        self.size = size
        self.actualName = actualName
        self.hasSeen = hasSeen
        self.imdb = imdb
        self.personalRating = personalRating
        self.imdbRating = imdbRating
        self.year = year
        
    def __eq__(self,other):
        if self.filename == other.filename and self.path == other.path and self.modifiedTime == other.modifiedTime and self.size == other.size:
            return True
        else:
            return False
    
    def __str__(self):
        if(self.actualName is None):
            return( self.filename )
        else:
            return self.actualName
    
    def scrapeImdb(self):
        word = re.split('\.| |-|\(|\)|\[|\]|\{|\}',self.filename)
        s=word[0]
        i=1
        if(len(word) is not 1):
            while ("20" not in word[i] and "19" not in word[i] and i != len(word) and
                   "=aka=" not in word[i].lower() and "mp4" not in word[i] and
                   "mkv" not in word[i] and "Director's" not in word[i] and 
                   'aka' != word[i].lower() and '1080' not in word[i] and 'S01' not in word[i]):
                s+=" "+word[i]
                i+=1
            for x in range(len(word)):
                i = len(word)-x-1
                try:
                    if( datetime.datetime.now().year >= int(word[i]) and int(word[i]) >= 1930):
                        self.year = int(word[i])
                        break
                except:
                    pass
        print(self.year)
        print(s)
        ia = IMDb()
        mov = ia.search_movie(s)
        if(len(mov) is not 0):
            for m in mov:
                if(self.year is not None):
                    if(self.year == m.get('year')):
                        self.actualName = m.get('title')
                        self.imdb = m.movieID
                        ia.update(m,['vote details'])
                        self.imdbRating=m.get("arithmetic mean")
                        break
                else:
                    self.actualName = m.get('title')
                    self.imdb = m.movieID
                    ia.update(m,['vote details'])
                    self.imdbRating=m.get("arithmetic mean")
                    break
        else:
            self.imdb = "Imdb Update Failed"
        if len(mov) is not 0 and self.year is not None and self.imdbRating is None:
                    self.actualName = mov[0].get('title')
                    self.imdb = mov[0].movieID
                    ia.update(mov[0],['vote details'])
                    self.imdbRating=mov[0].get("arithmetic mean")
        print(self.year,self.actualName,self.imdb,self.imdbRating)
        
    def updateName(self,name):
        self.actualName=name
    
    def updateImdb(self,imdb):
        if imdb.startswith("https://www.imdb.com/title/tt"):
            imdb = imdb[len("https://www.imdb.com/title/tt"):]
        if imdb.startswith("tt"):
            imdb = imdb[2:]
        ia = IMDb()
        m = ia.get_movie(imdb)
        self.actualName = m.get('title')
        self.imdb = m.movieID
        ia.update(m,['vote details'])
        self.imdbRating=m.get("arithmetic mean")

    
    def updateRating(self,rate):
        self.personalRating=rate
        
    def setSeen(self,value = True):
        self.hasSeen = value
    
