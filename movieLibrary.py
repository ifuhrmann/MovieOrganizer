# -*- coding: utf-8 -*-
"""
Created on Sun Jul 15 13:13:14 2018

@author: Iddo
"""

import os.path
import time
import sqlalchemy
import movieClassInfo

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

movieObjList[2].scrapeImdb()
