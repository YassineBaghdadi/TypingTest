import os, sys, datetime, pymysql, random
import time

from PyQt5 import QtGui, QtWidgets, uic

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

        # self.q1.textChanged.connect(lambda : self.timeChange(1))
        # self.q2.textChanged.connect(lambda : self.timeChange(2))
        # self.q3.textChanged.connect(lambda : self.timeChange(3))

        self.currentQzId = None
        # cnx = conn()
        # cur = cnx.cursor()
        # cur.execute(f"select subjct from Qts;")
        # sbjcts = [i[0] for i in set(cur.fetchall())]
        # s1 = random.choice(sbjcts)
        # sbjcts.pop(sbjcts.index(s1))
        # cur.execute(f'select id, qt from Qts where subjct like "{s1}"')
        # self.qts1 = [[j for j in i] for i in cur.fetchall()]
        # s2 = random.choice(sbjcts)
        # sbjcts.pop(sbjcts.index(s2))
        # cur.execute(f'select id, qt from Qts where subjct like "{s2}"')
        # self.qts2 = [[j for j in i] for i in cur.fetchall()]
        #
        # s3 = random.choice(sbjcts)
        # sbjcts.pop(sbjcts.index(s3))
        # cur.execute(f'select id, qt from Qts where subjct like "{s3}"')
        # self.qts3 = [[j for j in i] for i in cur.fetchall()]
        #
        # cnx.close()
        print(self.qts1)
        print(self.qts2)
        print(self.qts3)
        self.s1.clicked.connect(self.send1)
        self.s2.clicked.connect(self.send2)
        self.s3.clicked.connect(self.send3)


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

                self.q1.setText(self.qts1[self.s1Status][1])
                self.s1showedTime = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
                self.a1.setPlainText("")
            else:
                self.q1.setText("Scenario 1 finished .")
                self.a1.setPlainText("")
                self.s1.setEnabled(False)
                self.a1.setEnabled(False)
                self.s1finished = True

        if q == 2:
            if self.s2Status < len(self.qts2) -1:
                self.s2Status += 1

                self.q2.setText(self.qts2[self.s2Status][1])
                self.s2showedTime = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
                self.a2.setPlainText("")
            else:
                self.q2.setText("Scenario 2 finished .")
                self.a2.setPlainText("")
                self.s2.setEnabled(False)
                self.a2.setEnabled(False)
                self.s2finished = True
        if q == 3:
            if self.s3Status < len(self.qts3) -1:
                self.s3Status += 1

                self.q3.setText(self.qts3[self.s3Status][1])
                self.s3showedTime = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
                self.a3.setPlainText("")
            else:
                self.q3.setText("Scenario 3 finished .")
                self.a3.setPlainText("")
                self.s3.setEnabled(False)
                self.a3.setEnabled(False)
                self.s3finished = True

    def timeChange(self, q):
        if q == 1:
            self.s1showedTime = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        if q == 2:
            self.s2showedTime = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        if q == 3:
            self.s3showedTime = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    def start(self):
        name, pressed = QtWidgets.QInputDialog.getText(self, "Please Enter Agent Name", "Full Name : ",
                                             QtWidgets.QLineEdit.Normal, "")
        if pressed:
            if name:
                self.agentName = name
                self.s1.setEnabled(True)
                self.s2.setEnabled(True)
                self.s3.setEnabled(True)
                self.a1.setEnabled(True)
                self.a2.setEnabled(True)
                self.a3.setEnabled(True)
                cnx = conn()
                cur = cnx.cursor()
                cur.execute(f"select count(id) from Agents where fullName like '{name}';")

                if not int(cur.fetchone()[0]):
                    cur.execute(f"insert into Agents (fullName) value('{name}');")
                    cnx.commit()
                    cur.execute('select max(id) from Agents;')
                    self.startedTime = datetime.datetime.now()
                    self.label.setText(
                        f'The Quiz for {name} Started at {self.startedTime.strftime("%d-%m-%Y %H:%M:%S")} .')
                    cur.execute(f"""insert into Quiz (agent, startTime) values({cur.fetchone()[0]}, '{self.startedTime.strftime("%d-%m-%Y %H:%M:%S")}');""")
                    cnx.commit()
                    cur.execute('select max(id) from Quiz;')
                    self.currentQzId = cur.fetchone()[0]
                    self.Quiz.setEnabled(True)
                    self.strsbtn.setEnabled(False)
                    # [self.changeQts(i)for i in range(1, 4)]
                    self.q1.setText(self.qts1[self.s1Status][1])
                    self.s1showedTime = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
                    self.q2.setText(self.qts2[self.s2Status][1])
                    self.s2showedTime = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
                    self.q3.setText(self.qts3[self.s3Status][1])
                    # self.s1Status += 1
                    # self.s2Status += 1
                    # self.s3Status += 1
                    self.s3showedTime = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
                else :
                    QtWidgets.QMessageBox.warning(self, "Can't Continue with this Name", "the Name that you're trying to use is already used please try again .")


                cnx.close()
            else:
                self.label.setText(f'To Start The Quiz You Have To Write a Name.')
        else:
            print("canceled")
            self.label.setText(f'The Quiz Not Started.')

    def end(self):
        if  self.s1finished and  self.s2finished and  self.s3finished :
            self.endTime = datetime.datetime.now()

            duration = time.strftime('%H:%M:%S', time.gmtime(int(time.mktime(self.endTime.timetuple()) - time.mktime(self.startedTime.timetuple()))))
            print(f'{self.endTime} - {self.startedTime} == {duration}')

            cnx = conn()
            cur = cnx.cursor()
            cur.execute(f"""update Quiz set endTime = '{self.endTime.strftime("%d-%m-%Y %H:%M:%S")}', duration = '{duration}' where id = {self.currentQzId}""")
            cnx.commit()
            self.label.setText(f'The Quiz for {self.agentName} Stopped at {self.endTime.strftime("%d-%m-%Y %H:%M:%S")}.')
            self.Quiz.setEnabled(False)
            self.strsbtn.setEnabled(True)
            self.s1.setEnabled(True)
            self.s2.setEnabled(True)
            self.s3.setEnabled(True)
            self.a1.setPlainText("")
            self.a2.setPlainText("")
            self.a3.setPlainText("")
            self.q1.setText("Qts")
            self.q2.setText("Qts")
            self.q3.setText("Qts")
            cnx.close()
            self.loadQ()
            self.s1finished = False
            self.s2finished = False
            self.s3finished = False

    def send1(self):
        cnx = conn()
        cur = cnx.cursor()
        # print(self.self.qts1[self.s1Status][0])
        print(self.s1Status)
        cur.execute(f'''insert into ansewrs(qz, qt, qtTime, ansr, ansrTime) values (
                {self.currentQzId},
                {self.qts1[self.s1Status][0]},
                "{self.s1showedTime}",
                "{self.a1.toPlainText()}",
                "{datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")}"
        )''')
        cnx.commit()
        cnx.close()
        # self.s1Status =+ 1
        # self.q1.setText(self.qts1[self.s1Status][1])
        # self.a1.setPlainText("")
        self.changeQts(1)
        self.end()

    def send2(self):
        cnx = conn()
        cur = cnx.cursor()

        cur.execute(f'''insert into ansewrs(qz, qt, qtTime, ansr, ansrTime) values (
                {self.currentQzId},
                {self.qts2[self.s2Status][0]},
                "{self.s2showedTime}",
                "{self.a2.toPlainText()}",
                "{datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")}"
        )''')
        cnx.commit()
        cnx.close()
        # self.s2Status =+ 1
        # self.q2.setText(self.qts2[self.s2Status][1])
        # self.a2.setPlainText("")
        self.changeQts(2)
        self.end()

    def send3(self):
        cnx = conn()
        cur = cnx.cursor()

        cur.execute(f'''insert into ansewrs(qz, qt, qtTime, ansr, ansrTime) values (
                {self.currentQzId},
                {self.qts3[self.s3Status][0]},
                "{self.s3showedTime}",
                "{self.a3.toPlainText()}",
                "{datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")}"
        )''')
        cnx.commit()
        cnx.close()
        # self.s3Status =+ 1
        # self.q3.setText(self.qts3[self.s3Status][1])
        # self.a3.setPlainText("")
        self.changeQts(3)
        self.end()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main = Main()
    main.show()
    sys.exit(app.exec_())


