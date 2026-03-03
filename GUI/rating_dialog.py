from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QRadioButton, QPushButton


class RatingDialog(QDialog):

    def __init__(self,prev_rating=-1):
        self.rating = None
        self.buttons = []
        super(RatingDialog, self).__init__(None)
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
        for i in range(0, 11):
            b = QRadioButton(str(i))
            buttons.addWidget(b)
            self.buttons.append(b)
            b.toggled.connect(self.buttonState)
        if prev_rating in range(10):
            self.buttons[prev_rating].setChecked(True)

        # layout.addWidget(QLabel("Filename: "+movie.filename))
        layout.addLayout(buttons)
        l = QHBoxLayout()
        l.addStretch(1)
        okB = QPushButton("&OK")
        okB.clicked.connect(self.okClicked)
        l.addWidget(okB)
        l.addStretch(1)
        layout.addLayout(l)

        l.addStretch(1)
        okB = QPushButton("&Cancel")
        okB.clicked.connect(self.cancelClicked)
        l.addWidget(okB)
        l.addStretch(1)

        self.setLayout(layout)

    def buttonState(self):
        for i in range(0, 11):
            if self.buttons[i].isChecked():
                self.rating = int(self.buttons[i].text())
                break
        # self.rating = int(b.text())

    def okClicked(self):
        self.accept()

    def cancelClicked(self):
        self.reject()
