import os, sys, datetime, pymysql, random
import time

from PyQt5 import QtGui, QtWidgets, uic, QtCore

qtsDone = []

conn = lambda : pymysql.connect(host="10.73.100.101", user="altima", password="TheAltima", database="altimatyping", port=3306)


class Main(QtWidgets.QWidget):
    def __init__(self):
        super(Main, self).__init__()
        uic.loadUi(os.path.join(os.getcwd(), "ui", "admn.ui"), self)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        self.cls.clicked.connect(lambda : exit(0))
        self.max.clicked.connect(self.maxmin)
        self.min.clicked.connect(lambda : self.showMinimized())
        self.status = 0
        self.agntsIDs = {}
        self.refreshAg()
        self.agnts.currentTextChanged.connect(self.refreshQz)

    def show(self):
        if self.qzs.currentText() not in ["Choose Quiz ...", "there are no Quiz to select ..."]:
            cnx = conn()
            cur = cnx.cursor()

            cur.execute(f"""select q.di, a.fullName, q.startTime, q.endTime, q.duration, q.result, q.note from quiz q inner join agents a on q.agent = a.id where agent = {int(self.agntsIDs[self.agnts.currentText()])}""")
            quizInfo = [i for i in cur.fetchone()]

            self.qzinfo.clear()
            self.qzinfo.setRowCount(1)
            self.qzinfo.setColumnCount(len(quizInfo))
            self.qzinfo.setHorizontalHeaderLabels(
                [i for i in "Quiz Id.Full Name.Start Time.End Time.Duration.Result.Note".split('.')])

            [self.qzinfo.horizontalHeader().setSectionResizeMode(i, QtWidgets.QHeaderView.Stretch) for i in self.qzinfo.columnCount()]
            for i in enumerate(quizInfo):
                self.qzinfo.setItem(0, cidx, QtWidgets.QTableWidgetItem(str(v))) #todo contuned 

            cnx.close()

    def refreshAg(self):
        cnx = conn()
        cur = cnx.cursor()
        cur.execute(f"""select * from agents;""")
        agnts = []
        for i in cur.fetchall():
            self.agntsIDs[i[1]] = i[0]
            agnts.append(i[1])
        self.agnts.clear()
        self.agnts.addItems(["Choose Agent ..."] + agnts)

        cnx.close()


    def refreshQz(self):
        if self.agnts.currentText() != "Choose Agent ...":
            cnx = conn()
            cur = cnx.cursor()
            cur.execute(f'select startTime from quiz where agent = {int(self.agntsIDs[self.agnts.currentText()])};')
            self.qzs.clear()
            self.qzs.addItems(["Choose Quiz ..."] + [i[0] for i in cur.fetchall()])
            cnx.close()
        else:
            self.qzs.clear()
            self.qzs.addItems(["there are no Quiz to select ..."] )


    def maxmin(self):
        if self.status:
            self.showNormal()
            self.status = 0
        else:
            self.showMaximized()
            self.status = 1

    def paintEvent(self, event):

        opt = QtWidgets.QStyleOption()
        opt.initFrom(self)
        rect = opt.rect

        p = QtGui.QPainter(self)
        p.setRenderHint(QtGui.QPainter.Antialiasing, True)
        p.setBrush(opt.palette.brush(QtGui.QPalette.Window))
        p.setPen(QtCore.Qt.NoPen)
        p.drawRoundedRect(rect, 40, 40)
        p.end()

    def mousePressEvent(self, event):
            if event.button() == QtCore.Qt.LeftButton:
                self.offset = event.pos()
            else:
                super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
            if self.offset is not None and event.buttons() == QtCore.Qt.LeftButton:
                self.move(self.pos() + event.pos() - self.offset)
            else:
                super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
            self.offset = None
            super().mouseReleaseEvent(event)



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main = Main()
    main.show()
    sys.exit(app.exec_())

