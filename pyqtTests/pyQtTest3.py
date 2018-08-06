# -*- coding: utf-8 -*-
"""
Created on Tue Jul 31 12:25:15 2018

@author: Iddo
"""

import sys
from PyQt5.QtWidgets import QMainWindow, QAction, qApp, QApplication,QMenu,QTextEdit
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QCoreApplication


class Example(QMainWindow):
    
    def __init__(self):
        super().__init__()
        
        self.initUI()
        
        
    def initUI(self):               
        
        
        
        exitAct = QAction(QIcon('exit.png'), '&Exit', self)        
        exitAct.setShortcut('Ctrl+Q')
        exitAct.triggered.connect(self.safeQuit)

        #menubar -> menu  (-> menu) -> action
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAct)
         
        addMenu = QMenu("&Directory",self)
        addAction = QAction('Add Directory',self)
        rem = QAction("Remove Directory",self)
        addMenu.addAction(addAction)
        addMenu.addAction(rem)
        menubar.addMenu(addMenu)

        
        view = menubar.addMenu("&View")
        viewAction = QAction("Check me",self,checkable = True)
        viewAction.setChecked(True)
        viewAction.triggered.connect(self.toggleMenu)
        view.addAction(viewAction)
        
        
        #end menu stuff

        exitAct = QAction( 'Exit', self)
        exitAct.setShortcut('Ctrl+Q')
        exitAct.triggered.connect(self.safeQuit)
        
        fakeAct = QAction( QIcon('yes.jpg'),'Yes', self)
        

        self.toolbar = self.addToolBar('Exit')
        self.toolbar.addAction(exitAct)
        self.toolbar.addAction(fakeAct)
        
        #end toolbar stuff
        

        self.statusBar()

        textEdit = QTextEdit()
        self.setCentralWidget(textEdit)

        
        self.setGeometry(300, 300, 350, 250)
        self.setWindowTitle('Simple menu')    
        self.show()
        
         
    def contextMenuEvent(self, event):
       
           cmenu = QMenu(self)
           
           newAct = cmenu.addAction("New")
           opnAct = cmenu.addAction("Open")
           quitAct = cmenu.addAction("Quit")
           action = cmenu.exec_(self.mapToGlobal(event.pos()))
           
           if action == quitAct:
               self.safeQuit()
       
   
        
    def safeQuit(self):
        """exit the application gently so Spyder IDE will not hang"""
        self.deleteLater()
        self.close()
        self.destroy()

    def toggleMenu(self, state):
        if state:
            pass
        else:
            pass

        
        
if __name__ == '__main__':
    app = QCoreApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    ex = Example()
    try:
        sys.exit(app.exec_())
    except:
        pass