#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
ZetCode PyQt5 tutorial 

In this example, we create a simple
window in PyQt5.

Author: Jan Bodnar
Website: zetcode.com 
Last edited: August 2017
"""

import sys
from PyQt5.QtWidgets import (QWidget,QMainWindow, QTextEdit, 
    QAction, QFileDialog, QApplication,QPushButton, QHBoxLayout, QVBoxLayout,QGridLayout,QFrame,QLabel)
from PyQt5.QtCore import QCoreApplication,Qt,QSize
from PyQt5.QtGui import QIcon,QFont

import movieLibrary as ml
import movieClassInfo

from PyQt5.QtGui import QIcon



#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
ZetCode PyQt5 tutorial 

In this example, we select a file with a
QFileDialog and display its contents
in a QTextEdit.

Author: Jan Bodnar
Website: zetcode.com 
Last edited: August 2017
"""
class MovieWidget(QFrame):
    def __init__(self,movie):
        super().__init__()
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
        
        vbox = QVBoxLayout()
        vbox.addWidget(self.text)
        vbox.addWidget(year)
        self.setLayout(vbox)





class Example(QMainWindow):
    
    def __init__(self):
        super().__init__()
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
            self.widget = QWidget()
            self.widget.setLayout(self.makeLayout())    
            self.setCentralWidget( self.widget )
    
    def nextPageFunc(self):
        if self.pagenum*50+49<len(self.movieList):
            self.pagenum+=1
            del(self.widget)
            self.widget = QWidget()
            self.widget.setLayout(self.makeLayout())    
            self.setCentralWidget( self.widget )
    
    def setMovieList(self):
        self.movieList = []
        f = open("directoryList.txt","r") 
        data = f.read()
        dlist = data.split(" ")
        for d in dlist :
            if d == "":
                dlist.remove(d)
        m = ml.MovieLibrary(dlist)
        m.updateAll()
        self.movieList = m.sortBy("")


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
        if  (self.pagenum+1)*50-1 < len(self.movieList):
            moviesShown = QLabel( str(self.pagenum*50)+"-"+str((self.pagenum+1)*50-1)+" out of "+str(len(self.movieList))   )
        else:
            moviesShown = QLabel( str(self.pagenum*50)+"-"+str(len(self.movieList))+" out of "+str(len(self.movieList))   )
        
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
        return layout

        
    def initUI(self):      
        fh = open("directoryList.txt", "r")
        s = fh.read()
        if(s is ""):
            self.setInitDir()
        
        self.statusBar()
        
        openFile = QAction(QIcon('open.png'), 'Add Directory', self)
        openFile.setShortcut('Ctrl+D')

        openFile.setStatusTip('Open new File')
        openFile.triggered.connect(self.showDialog)
        
        quitAction= QAction(QIcon('open.png'), 'Quit', self)
        quitAction.triggered.connect(self.safeQuit)
        quitAction.setShortcut('Ctrl+Q')
        


        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(openFile)
        fileMenu.addAction(quitAction)

        self.setMovieList()
        self.pagenum = 0
        self.widget = QWidget()
        self.widget.setLayout(self.makeLayout())    
        self.setCentralWidget( self.widget )
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

        
if __name__ == '__main__':
    
    app = QCoreApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    ex = Example()
    try:
        sys.exit(app.exec_())
    except:
        pass
