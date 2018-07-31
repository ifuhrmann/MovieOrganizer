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
from PyQt5.QtWidgets import QApplication, QWidget, QToolTip, QPushButton
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtGui import QIcon,QFont

import movieLibrary
import movieClassInfo

from PyQt5.QtGui import QIcon


class Example(QWidget):
    
    def __init__(self):
        super().__init__()
        
        self.initUI()
        
    def safeQuit(self):
        """exit the application gently so Spyder IDE will not hang"""
        self.deleteLater()
        self.close()
        self.destroy()


        
    def initUI(self):
        
        self.setWindowIcon(QIcon('web.png'))        
        QToolTip.setFont(QFont('SansSerif', 10))
        
        self.setToolTip('This is a <b>QWidget</b> widget')
        
        btn = QPushButton('Button', self)
        btn.setToolTip('This is a <b>QPushButton</b> widget <strong>This is deprecated HTML</strong>')
        btn.resize(btn.sizeHint())
        btn.move(50, 50)       
        
        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('Tooltips')    
        
        qbtn = QPushButton('Quit', self)
        qbtn.clicked.connect(self.safeQuit)
        qbtn.resize(qbtn.sizeHint())
        qbtn.move(150, 150)       
        
        self.show()

        
        
if __name__ == '__main__':
    
    app = QCoreApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    ex = Example()
    try:
        sys.exit(app.exec_())
    except:
        pass