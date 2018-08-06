# -*- coding: utf-8 -*-
"""
Created on Tue Jul 31 12:25:15 2018

@author: Iddo
"""

import sys
from PyQt5.QtWidgets import (QWidget,QMainWindow, QAction, qApp, QApplication,
                             QMenu,QTextEdit,QPushButton, QHBoxLayout, QVBoxLayout)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QCoreApplication


class Example(QWidget):
    
    def __init__(self):
        super().__init__()
        
        self.initUI()
        
        
    def initUI(self):               
        #textEdit = QTextEdit()
        #self.setCentralWidget(textEdit)

        okButton = QPushButton("OK")
        cancelButton = QPushButton("Cancel")

        hbox = QHBoxLayout()
        
        hbox.addStretch(1)
        hbox.addWidget(okButton)
        hbox.addStretch(1)
        hbox.addWidget(cancelButton)
        hbox.addStretch(1)

        vbox = QVBoxLayout()
        vbox.addLayout(hbox)
        
        self.setLayout(vbox)    
        
        
        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('Buttons')    
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