import os, sys, datetime, pymysql

from PyQt5 import QtGui, QtWidgets, uic

qtsDone = []

conn = lambda : pymysql.connect(host="127.0.0.1", user="", password="", database="", port=3306)

class Main(QtWidgets.QWidget):
    def __init__(self):
        super(Main, self).__init__()
        uic.loadUi(os.path.join(os.getcwd(), "ui", "main.ui"), self)
        self.strsbtn.clicked.connect(self.start)
        self.agentName = ""
        self.qts = []



    def loadQts(self):



    def start(self):
        text, pressed = QtWidgets.QInputDialog.getText(self, "Input Text", "Text: ",
                                             QtWidgets.QLineEdit.Normal, "")
        if pressed:
            if text:
                self.agentName = text
                self.label.setText(f'The Quiz for {text} Started at {datetime.datetime.now().strftime("%H:%M:%S")}.')
                self.Quiz.setEnabled(True)
                self.strsbtn.setEnabled(False)
            else:
                self.label.setText(f'To Start The Quiz You Have To Write a Name.')
        else:
            print("canceled")
            self.label.setText(f'The Quiz Not Started.')

    def end(self):
        self.label.setText(f'The Quiz for {self.agentName} Stopped at {datetime.datetime.now().strftime("%H:%M:%S")}.')
        self.Quiz.setEnabled(False)
        self.strsbtn.setEnabled(True)

    def send1(self):
        ...

    def send2(self):
        ...

    def send3(self):
        ...







if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main = Main()
    main.show()
    sys.exit(app.exec_())


