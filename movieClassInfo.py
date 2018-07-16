# -*- coding: utf-8 -*-
from imdb import IMDb
import time
import re

def imdbTest():
    ia = IMDb()
    tinit = time.time()
    print( tinit )
    # get a movie and print its director(s)
    m = ia.search_movie("The Matrix")
    print(m)
    ia.update(m[0])
    print(m[0].movieID,m[0].get('directed by'))
    print(time.time()-tinit)

class MovieInfo():
    def __init__(self,filename,path,modifiedTime,size,actualName=None,hasSeen=False,imdb=None,personalRating=None):
        self.filename = filename
        self.path = path
        self.modifiedTime = modifiedTime
        self.size = size
        self.actualName = actualName
        self.hasSeen = hasSeen
        self.imdb = imdb
        self.personalRating = personalRating
    def __eq__(self,other):
        if self.name == other.name and self.path == other.path and self.modifiedTime== other.modifiedTime and self.size == other.size:
            return True
        else:
            return False
    
    def __str__(self):
        if(self.actualName is None):
            return( self.filename )
        else:
            return self.actualName
    def setSeen(self,value = True):
        self.hasSeen = value
    
    def scrapeImdb(self):
        word = re.split('\.| |-',self.filename)
        s=word[0]
        i=1
        if(len(word) is not 1):
            while "2" not in word[i] and "1" not in word[i] and i != len(word) and "=AKA=" not in word[i] and 'mkv' not in word[i] and "Director's" not in word[i]:
                s+=" "+word[i]
                i+=1
        print(s)