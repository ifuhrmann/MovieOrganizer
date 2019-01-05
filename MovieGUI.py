import sys
from PyQt5.QtWidgets import (QWidget,QMainWindow, QTextEdit,QMenu,QDialog,
    QAction, QFileDialog, QApplication,QPushButton, QHBoxLayout, QVBoxLayout,QGridLayout,
    QFrame,QLabel,QRadioButton)
from PyQt5.QtCore import QCoreApplication,Qt,QSize
from PyQt5.QtGui import QIcon,QFont
from pathlib import Path

import movieLibrary as ml
import subprocess
#subprocess.call()
vlc = 'C:/Program Files (x86)/VideoLAN/VLC/vlc.exe'

#!/usr/bin/python3
# -*- coding: utf-8 -*-

class RatingBox(QDialog):
    
    def __init__(self):
        self.rating = None
        self.buttons = []
        super(RatingBox,self).__init__(None)
        self.setWindowTitle("Rating")
        layout = QVBoxLayout()
        layout.addStretch(1)
        text = QHBoxLayout()
        text.addStretch(1)
        text.addWidget(QLabel("Enter Your Rating "))
        text.addStretch(1)
        layout.addLayout(text)
        layout.addStretch(1)
        buttons = QHBoxLayout()
        for i in range(0,11):
            b = QRadioButton(str(i))
            buttons.addWidget(b)
            self.buttons.append(b)
            b.toggled.connect( self.buttonState )

        #layout.addWidget(QLabel("Filename: "+movie.filename))
        layout.addLayout(buttons)
        l = QHBoxLayout()
        l.addStretch(1)
        okB=QPushButton("&OK")
        okB.clicked.connect(self.okClicked)
        l.addWidget(okB)        
        l.addStretch(1)
        layout.addLayout(l)
        
        l.addStretch(1)
        okB=QPushButton("&Cancel")
        okB.clicked.connect(self.cancelClicked)
        l.addWidget(okB)        
        l.addStretch(1)

        self.setLayout(layout)
        
    def buttonState(self):
        for i in range(0,11):
            if self.buttons[i].isChecked():
                self.rating = int(self.buttons[i].text())
                break
        #self.rating = int(b.text())
        
    def okClicked(self):
        self.accept()
        
    def cancelClicked(self):
        self.reject()

class MovieWindow(QDialog):
    def __init__(self,movie):
        super(MovieWindow,self).__init__(None)
        self.setWindowTitle(str(movie.actualName) + " Info")
        
        layout = QVBoxLayout()
        layout.addStretch(1)
        layout.addWidget(QLabel("Filename: "+movie.filename))
        layout.addStretch(1)
        layout.addWidget(QLabel("Path: "+movie.path))
        layout.addStretch(1)
        layout.addWidget(QLabel("Modified Time: "+str(movie.modifiedTime)))
        layout.addStretch(1)
        layout.addWidget(QLabel("Size: "+str(movie.size/2**30)+" Gigabytes"))
        #layout.addWidget(QLabel("Filename: "+movie.filename))

        l = QHBoxLayout()
        l.addStretch(1)
        okB=QPushButton("&OK")
        okB.clicked.connect(self.okClicked)
        l.addWidget(okB)        
        l.addStretch(1)
        
        layout.addLayout(l)
        self.setLayout(layout)
        
    def okClicked(self):
        self.accept()
        


class MovieWidget(QFrame):
    def __init__(self,movie):
        super().__init__()
        self.movie = movie
        self.setFrameShape(QFrame.Panel)
        self.setFrameShadow(QFrame.Sunken)
        self.setLineWidth(3)
        self.setMidLineWidth(3)

        self.text = QLabel(movie.actualName)
        self.text.setMaximumWidth(150)
        self.text.setWordWrap(True)
        self.text.setAlignment(Qt.AlignCenter)

        year = QLabel( str(movie.year) ) 
        year.setAlignment(Qt.AlignCenter)
        
        
        rate = QLabel( "IMDb Rating: " + str(movie.imdbRating) ) 
        rate.setAlignment(Qt.AlignCenter)
        

        vbox = QVBoxLayout()
        if(movie.hasSeen == True):
            s=""
            if(movie.personalRating is not None):
                s+="Rating: "+str(movie.personalRating)
            else:
                s+="Seen"
            seen = QLabel(s)
            seen.setAlignment(Qt.AlignRight)
            vbox.addWidget(seen)
    
        
        vbox.addStretch(10)
        vbox.addWidget(self.text)
        vbox.addStretch(10)
        vbox.addWidget(year)
        vbox.addStretch(10)
        vbox.addWidget(rate)
        vbox.addStretch(10)
        self.setLayout(vbox)


    def contextMenuEvent(self, event):
       
           cmenu = QMenu(self)
           
           infoAct = cmenu.addAction("More Info")
           seenAct = cmenu.addAction("Toggle Seen")
           ratingAct = cmenu.addAction("Add Rating")
           playAct = cmenu.addAction("Play Movie")
           action = cmenu.exec_(self.mapToGlobal(event.pos()))
           if action == infoAct:
               m = MovieWindow(self.movie)
               m.exec_()
           if action == seenAct:
               ml.MovieLibrary.setSeen(self.movie, not self.movie.hasSeen)
           if action == ratingAct:
               r = RatingBox()
               if r.exec_():
                   if r.rating is not None:
                       ml.MovieLibrary.setPersonalRating(self.movie, r.rating)
           if action == playAct:
               print(self.movie.path)
               
               subprocess.Popen(["vlc.exe",self.movie.path.replace("/","\\")],executable = vlc)




class Example(QMainWindow):
    
    def __init__(self):
        super().__init__()
        #the things I'm going to use later for sure go here for understanding
        self.pagenum = 0
        self.sortBy = ""

        self.initUI()
        
            
    def safeQuit(self):
        """exit the application gently so Spyder IDE will not hang"""
        self.deleteLater()
        self.close()
        self.destroy()

    def prevPageFunc(self):
        if self.pagenum>0:
            self.pagenum-=1
            del(self.widget)
            self.makeLayout()  
    
    def nextPageFunc(self):
        if self.pagenum*50+49<len(self.movieList):
            self.pagenum+=1
            del(self.widget)
            self.makeLayout()  
    
    def setMovieList(self):
        self.movieList = []
        f = open("directoryList.txt","r+") 
        data = f.read()
        dlist = data.split(" ")
        for d in dlist :
            if d == "":
                dlist.remove(d)
        f.close()
        try:        
            ignore = open("ignoreList.txt","r") 
        except:
            filename = Path( "ignoreList.txt" )
            filename.touch(exist_ok=True)  # will create file, if it exists will do nothing
            ignore = open(filename,"r")

        data = ignore.read()
        ilist = data.split("becausemovienameshavemanycharactersthiswillsplitmystring")
        for i in ilist :
            if i == "":
                ilist.remove(i)
        ignore.close()
        m = ml.MovieLibrary(dlist,ilist)
        m.updateAll()
        self.movieList = m.sortBy(self.sortBy)
        self.makeLayout()
        
        
    def sortMovieList(self):
        if self.sender().text() =='Year ↑':
            self.sortBy = 'year asc'
            self.sender().setText('Year ↓')
        elif self.sender().text() =='Year ↓':
            self.sortBy = 'year desc'
            self.sender().setText('Year ↑')
            
        if self.sender().text() =='Imdb Rating ↑':
            self.sortBy = 'imdbRating asc'
            self.sender().setText('Imdb Rating ↓')
        elif self.sender().text() =='Imdb Rating ↓':
            self.sortBy = 'imdbRating desc'
            self.sender().setText('Imdb Rating ↑')

        if self.sender().text() =='Personal Rating ↑':
            self.sortBy = 'personalRating asc'
            self.sender().setText('Personal Rating ↓')
        elif self.sender().text() =='Personal Rating ↓':
            self.sortBy = 'personalRating desc'
            self.sender().setText('Personal Rating ↑')
            
        if self.sender().text() =='Has Seen':
            self.sortBy = 'hasSeen asc'
            self.sender().setText("Hasn't Seen")
        elif self.sender().text() =="Hasn't Seen":
            self.sortBy = 'hasSeen desc'
            self.sender().setText('Has Seen')

        if self.sender().text() =='Name ↑':
            self.sortBy = 'actualName asc'
            self.sender().setText('Name ↓')
        elif self.sender().text() =='Name ↓':
            self.sortBy = 'actualName desc'
            self.sender().setText('Name ↑')

        if self.sender().text() =='Modified Time ↑':
            self.sortBy = 'modifiedTime asc'
            self.sender().setText('Modified Time ↓')
        elif self.sender().text() =='Modified Time ↓':
            self.sortBy = 'modifiedTime desc'
            self.sender().setText('Modified Time ↑')
            
        self.movieList = []
        f = open("directoryList.txt","r") 
        data = f.read()
        dlist = data.split(" ")
        for d in dlist :
            if d == "":
                dlist.remove(d)
        f.close()
        
        ignore = open("ignoreList.txt","r") 
        data = ignore.read()
        ilist = data.split(" ")
        for i in ilist :
            if i == "":
                ilist.remove(i)
        ignore.close()
        
        m = ml.MovieLibrary(dlist,ilist)
        m.updateAll()
        self.movieList = m.sortBy(self.sortBy)
        self.makeLayout()



    def makeLayout(self):
        self.mWidgets = []
        layout = QGridLayout()
        layout.setHorizontalSpacing(50)
        layout.setVerticalSpacing(20)
        for i in range(0,5):
            for j in range(0,10):
                if(j+i*10+self.pagenum*50 >= len(self.movieList)):
                    break
                self.mWidgets.append(MovieWidget(self.movieList[j+i*10+self.pagenum*50]))
                layout.addWidget(self.mWidgets[i*10 + j],i,j)
        
        hbox = QHBoxLayout()
        s=""
        if  (self.pagenum+1)*50-1 < len(self.movieList):
            s =  str(self.pagenum*50+1)+"-"+str((self.pagenum+1)*50)+" out of "+str(len(self.movieList)) 
        else:
            s= str(self.pagenum*50+1)+"-"+str(len(self.movieList))+" out of "+str(len(self.movieList))   
        if self.sortBy is not "":
            s+=" ordered by "+self.sortBy
        moviesShown = QLabel( s )
        prevPage = QPushButton("<")
        prevPage.clicked.connect(self.prevPageFunc)
        nextPage = QPushButton(">")
        nextPage.clicked.connect(self.nextPageFunc)
        hbox.addStretch(20)
        hbox.addWidget(moviesShown)
        hbox.addStretch(5)
        hbox.addWidget(prevPage)
        hbox.addStretch(1)
        hbox.addWidget(nextPage)
        hbox.addStretch(20)
        layout.addLayout(hbox,5,0,1,10)
        
        self.widget = QWidget()
        self.widget.setLayout(layout)    
        self.setCentralWidget( self.widget )

        
    def initUI(self):      
        try:        
            fh = open("directoryList.txt","r") 
        except:
            filename = Path( "directoryList.txt" )
            filename.touch(exist_ok=True)  # will create file, if it exists will do nothing
            fh = open(filename,"r")
        s = fh.read()
        if(s is ""):
            self.setInitDir()
        fh.close()
        self.statusBar()
        
        openFile = QAction(QIcon('open.png'), 'Add Directory', self)
        openFile.setShortcut('Ctrl+D')

        openFile.setStatusTip('Open new File')
        openFile.triggered.connect(self.showDialog)
        
        quitAction= QAction(QIcon('open.png'), 'Quit', self)
        quitAction.triggered.connect(self.safeQuit)
        quitAction.setShortcut('Ctrl+Q')
        
        ignoreAction = QAction('Ignore Directory',self)
        ignoreAction.triggered.connect(self.ignoreDirect)
        ignoreAction.setShortcut('Ctrl+I')
        
        ignoreFile = QAction('Ignore File',self)
        ignoreFile.triggered.connect(self.ignoreFile)
        ignoreFile.setShortcut('Ctrl+I')

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(openFile)
        fileMenu.addAction(ignoreAction)
        fileMenu.addAction(ignoreFile)
        fileMenu.addAction(quitAction)
        
        
        updateAct = QAction( 'Update Library', self)
        updateAct.setShortcut('Ctrl+U')
        updateAct.triggered.connect(self.setMovieList)

        sortYear = QAction( 'Year ↑', self)
        sortYear.triggered.connect(self.sortMovieList)

        sortImdb = QAction( 'Imdb Rating ↑', self)
        sortImdb.triggered.connect(self.sortMovieList)
        
        sortRate = QAction( 'Personal Rating ↑', self)
        sortRate.triggered.connect(self.sortMovieList)
        
        seen = QAction( 'Has Seen', self)
        seen.triggered.connect(self.sortMovieList)

        name = QAction( 'Name ↑', self)
        name.triggered.connect(self.sortMovieList)
        
        modified = QAction( 'Modified Time ↑', self)
        modified.triggered.connect(self.sortMovieList)

        self.toolbar = self.addToolBar('')
        self.toolbar.addAction(updateAct)
        self.toolbar.addAction(sortYear)
        self.toolbar.addAction(sortImdb)
        self.toolbar.addAction(sortRate)
        self.toolbar.addAction(seen)
        self.toolbar.addAction(name)
        self.toolbar.addAction(modified)
        self.setMovieList()
        #self.setGeometry(400,400,400,400)
        #self.resize(800,600) 
        self.setWindowTitle('Movie Organizer')
        self.showMaximized()
        
        
    def showDialog(self):
        fname = QFileDialog.getExistingDirectory(self, 'Set Initial Directory', '/home')
        if fname is not "":
            F = open("directoryList.txt","a") 
            F.write(fname+" ")
            F.close()
            
    def setInitDir(self):
        fname = QFileDialog.getExistingDirectory(self, 'Set Initial Directory', '/home')
        if fname is not "":
            F = open("directoryList.txt","a") 
            F.write(fname+" ")
            F.close()
            
    def ignoreDirect(self):
        fname = QFileDialog.getExistingDirectory(self, 'Ignore Directory', '/home')
        if fname is not "":
            print(fname)
            F = open("ignoreList.txt","a") 
            F.write(fname+"becausemovienameshavemanycharactersthiswillsplitmystring")
            F.close()
            
    def ignoreFile(self):
        fname = QFileDialog.getOpenFileName(self, 'Ignore File', '/home')
        if fname is not "":
            print(fname)
            F = open("ignoreList.txt","a") 
            F.write(fname[0]+"becausemovienameshavemanycharactersthiswillsplitmystring")
            F.close()

        
if __name__ == '__main__':
    
    app = QCoreApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    ex = Example()
    try:
        sys.exit(app.exec_())
    except:
        pass
