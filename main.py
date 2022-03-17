import os, sys, datetime, pymysql, random

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
        self.s1Status = 0
        self.s2Status = 0
        self.s3Status = 0
        self.currentQzId = None
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


    def start(self):
        name, pressed = QtWidgets.QInputDialog.getText(self, "Please Enter Agent Name", "Full Name : ",
                                             QtWidgets.QLineEdit.Normal, "")
        if pressed:
            if name:
                self.agentName = name

                cnx = conn()
                cur = cnx.cursor()
                cur.execute(f"select count(id) from Agents where fullName like '{name}';")

                if not int(cur.fetchone()[0]):
                    cur.execute(f"insert into Agents (fullName) value('{name}');")
                    cnx.commit()
                    cur.execute('select max(id) from Agents;')
                    self.startedTime = datetime.datetime.now()
                    self.label.setText(
                        f'The Quiz for {name} Started at {self.startedTime.strftime("%d-%m-%Y %H:%M:%S")}.')
                    cur.execute(f"insert into Quiz (agent, startTime) values({cur.fetchone()[0]}, '{self.startedTime.strftime("%d-%m-%Y %H:%M:%S")}');")
                    cnx.commit()
                    cur.execute('select max(id) from Quiz;')
                    self.currentQzId = cur.fetchone()[0]
                    self.Quiz.setEnabled(True)
                    self.strsbtn.setEnabled(False)
                    self.q1.setText(self.qts1[self.s1Status][1])
                    self.q2.setText(self.qts2[self.s2Status][1])
                    self.q3.setText(self.qts3[self.s3Status][1])
                else :
                    QtWidgets.QMessageBox.warning(self, "Can't Continue with this Name", "the Name that you're trying to use is already used please try again .")


                cnx.close()
            else:
                self.label.setText(f'To Start The Quiz You Have To Write a Name.')
        else:
            print("canceled")
            self.label.setText(f'The Quiz Not Started.')

    def end(self):
        self.endTime = datetime.datetime.now()
        duration = str(divmod((self.endTime - self.startedTime).total_seconds() , 60)[0]).replace(".", ":")
        cnx = conn()
        cur = cnx.cursor()
        cur.execute(f"""update Quiz set endTime """)

        self.label.setText(f'The Quiz for {self.agentName} Stopped at {endTime}.')
        self.Quiz.setEnabled(False)
        self.strsbtn.setEnabled(True)
        cnx.close()

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


