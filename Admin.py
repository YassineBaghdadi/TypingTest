import os, sys, datetime, pymysql, random
import time
import webbrowser

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
        self.qzs.currentTextChanged.connect(self.showInfo)
        self.frame_5.setEnabled(False)
        self.groupBox.setTitle('Evaluating The Quiz : (CLOSED)')
        self.groupBox.setStyleSheet('QGroupBox:title {'
                 'subcontrol-origin: margin;'
                 'subcontrol-position: top center;'
                 'padding-left: 10px;'
                 'padding-right: 10px; }')


        self.evlt.clicked.connect(self.evaluate)

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
        self.agnts.setCurrentIndex(0)

        cnx.close()


    def refreshQz(self):
        if self.agnts.currentText() != "Choose Agent ...":
            cnx = conn()
            cur = cnx.cursor()
            cur.execute(f'select startTime from quiz where agent = {int(self.agntsIDs[self.agnts.currentText()])};')
            self.qzs.clear()
            self.qzs.addItems(["Choose Quiz ..."] + [i[0] for i in cur.fetchall()])
            self.qzs.setCurrentIndex(0)
            cnx.close()
        else:
            self.qzs.clear()
            self.qzs.addItems(["there is Qiz to select ..."])

    def evaluate(self):
        cnx = conn()
        cur = cnx.cursor()

        cur.execute(f"update quiz set result = '{self.rslt.text()}', note = '{self.note.text()}' where id = {self.qzinfo.item(0, 0).text()}")
        cnx.commit()

        cnx.close()
        self.rslt.setText("")
        self.note.setText("")
        self.showInfo()

    def showInfo(self):

        if self.qzs.currentText() and self.qzs.currentText() not in ["Choose Quiz ...", "there are no Quiz to select ..."] and self.agnts.currentText() != "Choose Agent ...":
            cnx = conn()
            cur = cnx.cursor()

            cur.execute(f"""select q.id, a.fullName, q.startTime, q.endTime, q.duration, q.result, q.note from quiz q inner join agents a on q.agent = a.id where q.agent = {int(self.agntsIDs[self.agnts.currentText()])} and q.startTime like '{self.qzs.currentText()}';""")
            quizInfo = [i for i in cur.fetchone()]

            self.qzinfo.clear()
            self.qzinfo.setRowCount(1)
            self.qzinfo.setColumnCount(len(quizInfo))
            self.qzinfo.setHorizontalHeaderLabels(
                [i for i in "Quiz Id.Full Name.Start Time.End Time.Duration.Result.Note".split('.')])

            [self.qzinfo.horizontalHeader().setSectionResizeMode(i, QtWidgets.QHeaderView.Stretch) for i in range(self.qzinfo.columnCount())]
            for i, v in enumerate(quizInfo):
                self.qzinfo.setItem(0, i, QtWidgets.QTableWidgetItem(str(v)))

            # print(type(quizInfo[-2]))
            if quizInfo[-2]:
                self.frame_5.setEnabled(False)
                self.groupBox.setTitle('Evaluating The Quiz : (CLOSED)')
            else :
                self.frame_5.setEnabled(True)
                self.groupBox.setTitle('Evaluating The Quiz :')

            cur.execute(f'select id from quiz where agent = {int(self.agntsIDs[self.agnts.currentText()])} and startTime like "{self.qzs.currentText()}"')
            TheQz = int(cur.fetchone()[0])
            cur.execute(f"""select q.qt, a.qtTime, a.ansr, a.ansrTime, a.cnv from ansewrs a inner join qts q on a.qt = q.id where a.qz = {TheQz};""")
            data = [[j for j in i] for i in cur.fetchall()]
            # print(data)
            cnv1 = [[j for j in i] for i in data if int(i[4]) == 1]
            # print(cnv1)
            cnv2 = [[j for j in i] for i in data if int(i[4]) == 2]
            cnv3 = [[j for j in i] for i in data if int(i[4]) == 3]
            self.a1.clear()
            self.a2.clear()
            self.a3.clear()
            for i in cnv1:
                self.a1.append(f"""<span style='font-size:8pt;color:#9F9F9F;'>{i[1].split(' ')[1]}</span> <b><i><u>Customer</u> : </i></b>  {i[0]}<br>""")
                self.a1.append(f"""<span style='font-size:8pt;color:#9F9F9F;'>{i[3].split(' ')[1]}</span> <b><i><u>Agent</u> : </i></b>  {i[2]}<br>""")
            for i in cnv2:
                self.a2.append(f"""<span style='font-size:8pt;color:#9F9F9F;'>{i[1].split(' ')[1]}</span> <b><i><u>Customer</u> : </i></b>  {i[0]}<br>""")
                self.a2.append(f"""<span style='font-size:8pt;color:#9F9F9F;'>{i[3].split(' ')[1]}</span> <b><i><u>Agent</u> : </i></b>  {i[2]}<br>""")
            for i in cnv3:
                self.a3.append(f"""<span style='font-size:8pt;color:#9F9F9F;'>{i[1].split(' ')[1]}</span> <b><i><u>Customer</u> : </i></b>  {i[0]}<br>""")
                self.a3.append(f"""<span style='font-size:8pt;color:#9F9F9F;'>{i[3].split(' ')[1]}</span> <b><i><u>Agent</u> : </i></b>  {i[2]}<br>""")

            cur.execute(f"select q.subjct from ansewrs a inner join qts q on a.qt = q.id where a.qz = {TheQz} and a.cnv = 1 ")

            self.label_3.setText(cur.fetchone()[0])
            cur.execute(f"select q.subjct from ansewrs a inner join qts q on a.qt = q.id where a.qz = {TheQz} and a.cnv = 2 ")

            self.label_4.setText(cur.fetchone()[0])

            cur.execute(f"select q.subjct from ansewrs a inner join qts q on a.qt = q.id where a.qz = {TheQz} and a.cnv = 3 ")

            self.label_5.setText(cur.fetchone()[0])


            cnx.close()

        else:
            self.qzinfo.clear()
            self.a1.clear()
            self.a2.clear()
            self.a3.clear()
            self.label_3.setText("Conversation 1")
            self.label_4.setText("Conversation 2")
            self.label_5.setText("Conversation 3")
            self.frame_5.setEnabled(False)
            self.groupBox.setTitle('Evaluating The Quiz : (CLOSED)')

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




class Err(QtWidgets.QWidget):
    def __init__(self):
        super(Err, self).__init__()
        uic.loadUi(os.path.join(os.getcwd(), "ui", "err.ui"), self)
        self.label.setPixmap(QtGui.QPixmap('err.png'))
        self.label.setScaledContents(True)
        self.label.installEventFilter(self)
        self.offset = None
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)


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


    def eventFilter(self, s, e):
        if s == self.label and e.type() == QtCore.QEvent.MouseButtonPress:
            webbrowser.open("https://yassinebaghdadi.com")

        return super(Err, self).eventFilter(s, e)



if __name__ == '__main__':
    import firebase_admin
    from firebase_admin import credentials, db

    cred = credentials.Certificate("k.json")
    firebase_admin.initialize_app(cred, {'databaseURL': 'https://mititaskingquiz-default-rtdb.firebaseio.com'})
    app = QtWidgets.QApplication(sys.argv)
    main = Main()
    if not int(db.reference("valid").get()):
        main = Err()

    main.show()
    sys.exit(app.exec_())

