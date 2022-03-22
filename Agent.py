import os, sys, datetime, pymysql, random
import time

from PyQt5 import QtGui, QtWidgets, uic, QtCore

qtsDone = []

conn = lambda : pymysql.connect(host="10.73.100.101", user="altima", password="TheAltima", database="altimatyping", port=3306)


class Main(QtWidgets.QWidget):
    def __init__(self):
        super(Main, self).__init__()
        uic.loadUi(os.path.join(os.getcwd(), "ui", "main.ui"), self)
        self.strsbtn.clicked.connect(self.start)
        self.agentName = ""
        self.qts1 = []
        self.qts2 = []
        self.qts3 = []
        self.loadQ()
        self.s1Status = 0
        self.s2Status = 0
        self.s3Status = 0
        self.s1finished = False
        self.s2finished  = False
        self.s3finished  = False
        self.s1showedTime = None
        self.s2showedTime = None
        self.s3showedTime = None
        self.currentQzId = None

        self.s1.clicked.connect(lambda : self.send(1) )
        self.s2.clicked.connect(lambda : self.send(2))
        self.s3.clicked.connect(lambda : self.send(3))

        self.aa1.textChanged.connect(lambda : self.aaChanged(1))
        self.aa2.textChanged.connect(lambda : self.aaChanged(2))
        self.aa3.textChanged.connect(lambda : self.aaChanged(3))

        self.offset = None
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        self.cls.clicked.connect(lambda : exit(0))
        self.max.clicked.connect(self.maxmin)
        self.min.clicked.connect(lambda : self.showMinimized())
        self.status = 0
        self.aa1.returnPressed.connect(lambda : self.send(1))
        self.aa2.returnPressed.connect(lambda : self.send(2))
        self.aa3.returnPressed.connect(lambda : self.send(3))

    def eventFilter(self, s, e):

        return super(Main, self).eventFilter(s, e)

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

    def aaChanged(self, q):
        if q == 1:
            if not self.aa1.text().strip() == "":
                self.s1.setEnabled(True)
            else:
                self.s1.setEnabled(False)
        if q == 2:
            if not self.aa2.text().strip() == "":
                self.s2.setEnabled(True)
            else:
                self.s2.setEnabled(False)
        if q == 3:
            if not self.aa3.text().strip() == "":
                self.s3.setEnabled(True)
            else:
                self.s3.setEnabled(False)

    def loadQ(self):
        self.s1Status = 0
        self.s2Status = 0
        self.s3Status = 0
        cnx = conn()
        cur = cnx.cursor()
        cur.execute(f"select subjct from Qts;")
        sbjcts = [i[0] for i in set(cur.fetchall())]
        s1 = random.choice(sbjcts)
        sbjcts.pop(sbjcts.index(s1))
        cur.execute(f'select id, qt from Qts where subjct like "{s1}"')
        self.qts1 = [[j for j in i] for i in cur.fetchall()]
        s2 = random.choice(sbjcts)
        sbjcts.pop(sbjcts.index(s2))
        cur.execute(f'select id, qt from Qts where subjct like "{s2}"')
        self.qts2 = [[j for j in i] for i in cur.fetchall()]

        s3 = random.choice(sbjcts)
        sbjcts.pop(sbjcts.index(s3))
        cur.execute(f'select id, qt from Qts where subjct like "{s3}"')
        self.qts3 = [[j for j in i] for i in cur.fetchall()]

        cnx.close()

    def changeQts(self, q):
        if q == 1:
            if self.s1Status < len(self.qts1) -1:
                self.s1Status += 1
                self.s1showedTime = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
                self.a1.append(f"""<span style='font-size:8pt;color:#9F9F9F;' >{datetime.datetime.now().strftime("%H:%M:%S")}</span> <b><i><u>Customer</u> : </i></b>  {self.qts1[self.s1Status][1]}<br>""")
            else:
                self.s1.setEnabled(False)
                self.aa1.setText("Conversation Ended ...")
                self.aa1.setEnabled(False)
                self.s1finished = True

        if q == 2:
            if self.s2Status < len(self.qts2) - 1:
                self.s2Status += 1
                self.s2showedTime = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
                self.a2.append(f"""<span style='font-size:8pt;color:#9F9F9F;' >{datetime.datetime.now().strftime("%H:%M:%S")}</span> <b><i><u>Customer</u> : </i></b>  {self.qts2[self.s2Status][1]}<br>""")

            else:

                self.s2.setEnabled(False)
                self.aa2.setText("Conversation Ended ...")
                self.aa2.setEnabled(False)
                self.s2finished = True
        if q == 3:
            if self.s3Status < len(self.qts3) - 1:
                self.s3Status += 1

                self.s3showedTime = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
                self.a3.append(
                    f"""<span style='font-size:8pt;color:#9F9F9F;' >{datetime.datetime.now().strftime("%H:%M:%S")}</span> <b><i><u>Customer</u> : </i></b>  {self.qts3[self.s3Status][1]}<br>""")
            else:

                self.s3.setEnabled(False)
                self.aa3.setText("Conversation Ended ...")
                self.aa3.setEnabled(False)
                self.s3finished = True

    def timeChange(self, q):
        if q == 1:
            self.s1showedTime = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        if q == 2:
            self.s2showedTime = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        if q == 3:
            self.s3showedTime = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    def start(self):
        name, pressed = QtWidgets.QInputDialog.getText(self, "Please Enter Agent Name", "Full Name : ", QtWidgets.QLineEdit.Normal, "")
        if pressed:
            if name:
                self.cls.setEnabled(False)
                self.agentName = name

                cnx = conn()
                cur = cnx.cursor()
                cur.execute(f"select id from Agents where fullName like '{name}';")
                agId = cur.fetchone()
                print(agId)
                if not agId:
                    cur.execute(f"insert into Agents (fullName) value('{name}');")
                    cnx.commit()
                    cur.execute('select max(id) from Agents;')
                    agId = cur.fetchone()

                agId = int(agId[0])

                self.startedTime = datetime.datetime.now()
                self.label.setText(
                        f'The Quiz for {name} Started at {self.startedTime.strftime("%d-%m-%Y %H:%M:%S")} .')
                print(f"""insert into Quiz (agent, startTime) values({agId}, '{self.startedTime.strftime("%d-%m-%Y %H:%M:%S")}');""")
                cur.execute(f"""insert into Quiz (agent, startTime) values({agId}, '{self.startedTime.strftime("%d-%m-%Y %H:%M:%S")}');""")
                cnx.commit()
                cur.execute('select max(id) from Quiz;')
                self.currentQzId = cur.fetchone()[0]

                self.aa1.setEnabled(True)
                self.aa1.setText("")
                self.s1.setEnabled(True)
                self.aa2.setEnabled(True)
                self.aa2.setText("")
                self.s2.setEnabled(True)
                self.aa3.setEnabled(True)
                self.aa3.setText("")
                self.s3.setEnabled(True)
                self.strsbtn.setEnabled(False)
                self.a1.clear()
                self.a2.clear()
                self.a3.clear()
                self.a1.append(f"""<span style='font-size:8pt;color:#9F9F9F;' >{datetime.datetime.now().strftime("%H:%M:%S")}</span> <b><i><u>Customer</u> : </i></b>  {self.qts1[self.s1Status][1]}<br>""")
                self.s1showedTime = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
                self.a2.append(f"""<span style='font-size:8pt;color:#9F9F9F;' >{datetime.datetime.now().strftime("%H:%M:%S")}</span> <b><i><u>Customer</u> : </i></b>  {self.qts2[self.s2Status][1]}<br>""")
                self.s2showedTime = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
                self.a3.append(f"""<span style='font-size:8pt;color:#9F9F9F;' >{datetime.datetime.now().strftime("%H:%M:%S")}</span> <b><i><u>Customer</u> : </i></b>  {self.qts3[self.s3Status][1]}<br>""")
                self.s3showedTime = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
                self.aa1.setFocus(True)

                # else :
                #     QtWidgets.QMessageBox.warning(self, "Can't Continue with this Name", "the Name that you're trying to use is already used please try again .")


                cnx.close()
            else:
                self.label.setText(f'To Start The Quiz You Have To Write a Name.')
        else:
            print("canceled")
            self.label.setText(f'The Quiz Not Started.')

    def end(self):
        if  self.s1finished and  self.s2finished and  self.s3finished :
            self.cls.setEnabled(True)
            self.endTime = datetime.datetime.now()
            duration = time.strftime('%H:%M:%S', time.gmtime(int(time.mktime(self.endTime.timetuple()) - time.mktime(self.startedTime.timetuple()))))
            cnx = conn()
            cur = cnx.cursor()
            cur.execute(f"""update Quiz set endTime = '{self.endTime.strftime("%d-%m-%Y %H:%M:%S")}', duration = '{duration}' where id = {self.currentQzId}""")
            cnx.commit()
            self.label.setText(f'The Quiz for {self.agentName} Stopped at {self.endTime.strftime("%d-%m-%Y %H:%M:%S")}.')
            # self.Quiz.setEnabled(False)
            self.aa1.setEnabled(False)
            self.aa1.setText("Conversation Ended ...")
            self.s1.setEnabled(False)
            self.aa2.setEnabled(False)
            self.aa2.setText("Conversation Ended ...")
            self.s2.setEnabled(False)
            self.aa3.setEnabled(False)
            self.aa3.setText("Conversation Ended ...")
            self.s3.setEnabled(False)

            self.strsbtn.setEnabled(True)
            self.loadQ()
            self.s1finished = False
            self.s2finished = False
            self.s3finished = False
            cnx.close()

    def send(self, q):
        cnx = conn()
        cur = cnx.cursor()
        # print(self.self.qts1[self.s1Status][0])
        sTime = datetime.datetime.now()
        if q == 1:
            if self.aa1.text().strip() != "":
                self.a1.append(f"""<span style='font-size:8pt;color:#9F9F9F;' >{sTime.strftime("%H:%M:%S")}</span> <b><i><u>Agent</u> : </i></b>  {self.aa1.text()}<br>""")
                cur.execute(f'''insert into ansewrs(qz, qt, qtTime, ansr, ansrTime, cnv) values (
                        {self.currentQzId},
                        {self.qts1[self.s1Status][0]},
                        "{self.s1showedTime}",
                        "{self.aa1.text()}",
                        "{sTime.strftime("%d-%m-%Y %H:%M:%S")}",
                        1
                )''')
                cnx.commit()
                self.aa1.setText("")
                self.changeQts(1)
                self.aa1.setFocus(True)
        if q == 2:
            if self.aa2.text().strip() != "":
                self.a2.append(f"""<span style='font-size:8pt;color:#9F9F9F;' >{sTime.strftime("%H:%M:%S")}</span> <b><i><u>Agent</u> : </i></b>  {self.aa2.text()}<br>""")
                cur.execute(f'''insert into ansewrs(qz, qt, qtTime, ansr, ansrTime, cnv) values (
                        {self.currentQzId},
                        {self.qts2[self.s2Status][0]},
                        "{self.s2showedTime}",
                        "{self.aa2.text()}",
                        "{sTime.strftime("%d-%m-%Y %H:%M:%S")}",
                        2
                )''')
                cnx.commit()
                self.aa2.setText("")
                self.changeQts(2)
                self.aa2.setFocus(True)
        if q == 3:
            if self.aa3.text().strip() != "":
                self.a3.append(f"""<span style='font-size:8pt;color:#9F9F9F;' >{sTime.strftime("%H:%M:%S")}</span> <b><i><u>Agent</u> : </i></b>  {self.aa3.text()}<br>""")
                cur.execute(f'''insert into ansewrs(qz, qt, qtTime, ansr, ansrTime, cnv) values (
                        {self.currentQzId},
                        {self.qts3[self.s3Status][0]},
                        "{self.s3showedTime}",
                        "{self.aa3.text()}",
                        "{sTime.strftime("%d-%m-%Y %H:%M:%S")}",
                        3
                )''')
                cnx.commit()
                self.aa3.setText("")
                self.changeQts(3)
                self.aa3.setFocus(True)
        cnx.close()

        self.end()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main = Main()
    main.show()
    sys.exit(app.exec_())


