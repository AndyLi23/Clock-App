from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
from alarm import Timer
import time


class App(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(App, self).__init__(*args, **kwargs)
        self.setWindowTitle("AlarmClock")
        self.setGeometry(0, 0, 400, 300)
        self.timer = Timer()
        self.setStylesheet()
        self.stflag = False
        self.curC = 0
        self.initUI()

    def initUI(self):
        # tabs
        self.tabs = QTabWidget()

        # clock
        self.tab1 = QWidget()
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        self.todayTime = QLabel("")
        self.todayTime.setWordWrap(True)
        self.updateClock()
        layout.addWidget(self.todayTime)
        self.tab1.setLayout(layout)

        self.tab1.setStyleSheet("""
        QLabel {
            max-width: 300px;
            font-size: 40px;
        }
        """)

        # stopwatch
        layout = QVBoxLayout()

        layout.setAlignment(Qt.AlignCenter)

        self.stbutton = QPushButton("Start")
        self.stbutton.clicked.connect(self.setStopwatchTime)
        layout.addWidget(self.stbutton)

        self.stebutton = QPushButton("Stop")
        self.stebutton.clicked.connect(self.stopStopwatchTime)
        layout.addWidget(self.stebutton)

        self.strbutton = QPushButton("Restart")
        self.strbutton.clicked.connect(self.restartStopwatchTime)
        layout.addWidget(self.strbutton)

        self.sttimeLabel = QLabel("")
        self.sttimeLabel.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.sttimeLabel)

        self.tab2 = QWidget()
        self.tab2.setLayout(layout)
        self.tab2.setStyleSheet("""
        QLabel {
            width: 200px;
            max-width: 300px;
        }
        QPushButton {
            width: 200px;
            max-width: 300px;
        }
        """)

        # timer
        self.tab3 = QWidget()
        layout = QHBoxLayout()

        # layout.setAlignment(Qt.AlignCenter)
        self.textbox = QPlainTextEdit(self.tab3)
        self.textbox.setLineWrapMode(False)
        self.textbox.verticalScrollBar().hide()
        self.textbox1 = QPlainTextEdit(self.tab3)
        self.textbox1.setLineWrapMode(False)
        self.textbox1.verticalScrollBar().hide()
        self.textbox2 = QPlainTextEdit(self.tab3)
        self.textbox2.setLineWrapMode(False)
        self.textbox2.verticalScrollBar().hide()

        self.h = QLabel("h")
        self.m = QLabel("m")
        self.s = QLabel("s")
        self.h.setStyleSheet(
            "QLabel {width: 5px; background:#222222; padding:0;margin:0;}")
        self.m.setStyleSheet(
            "QLabel {width: 5px; background:#222222; padding:0;margin:0;}")
        self.s.setStyleSheet(
            "QLabel {width: 5px; background:#222222; padding:0;margin:0;}")
        layout.addWidget(self.textbox)
        layout.addWidget(self.h)
        layout.addWidget(self.textbox1)
        layout.addWidget(self.m)
        layout.addWidget(self.textbox2)
        layout.addWidget(self.s)

        layout2 = QVBoxLayout()

        self.timerStartB = QPushButton("Start")
        self.timerStartB.clicked.connect(self.startTimer)
        layout2.addWidget(self.timerStartB)

        self.timerStopB = QPushButton("Stop")
        self.timerStopB.clicked.connect(self.stopTimer)
        layout2.addWidget(self.timerStopB)

        self.timerRestartB = QPushButton("Restart")
        self.timerRestartB.clicked.connect(self.restartTimer)
        layout2.addWidget(self.timerRestartB)

        self.timerLabel = QLabel("")
        self.timerLabel.setAlignment(Qt.AlignCenter)
        layout2.addWidget(self.timerLabel)

        layout3 = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout2.setAlignment(Qt.AlignCenter)
        layout3.setAlignment(Qt.AlignCenter)
        layout3.addLayout(layout)
        layout3.addLayout(layout2)

        self.tab3.setLayout(layout3)
        self.tab3.setStyleSheet("""
        QPlainTextEdit {
            background: #333333;
            padding: 3px;
            color: white;
            border: none;
            font-size: 20px;
            min-height: 30px;
            max-height: 30px;
            margin: 0;
        }
        QPushButton {
            width: 200px;
            max-width: 300px;
        }
        """)

        # alarm
        self.tab4 = QWidget()

        # set tabs
        self.tabs.addTab(self.tab1, "Clock")
        self.tabs.addTab(self.tab2, "Stopwatch")
        self.tabs.addTab(self.tab3, "Timer")
        self.tabs.addTab(self.tab4, "Alarm")

        self.setCentralWidget(self.tabs)

        # update timer
        timer = QTimer(self)

        timer.timeout.connect(self.updateAll)

        # update the timer every hundredth second
        timer.start(10)
        self.count = 0

        self.show()

    def updateAll(self):
        self.updateStopwatch()
        self.updateClock()
        self.updateTimer()
        '''self.count = (self.count + 1) % 4
        if self.count == 0:
            self.clockUpdateColor()'''

    def updateClock(self):
        temp = self.timer.getTime()
        month = self.timer.getRn().strftime("%B")
        temp = temp.split(" ")
        day = str(int(temp[0].split("-")[2]))
        daytext = self.timer.getDay()
        self.todayTime.setText(daytext + "\n" + month +
                               " " + day + "\n" + temp[1])

    def clockUpdateColor(self):
        colors = ("red", "orange", "yellow", "lime", "white")
        self.curC = (self.curC + 1) % 5
        self.tab1.setStyleSheet(
            "QLabel {max-width: 300px; font-size: 40px; color: %s;}" % colors[self.curC])

    def startTimer(self):
        sum_ = 0
        t1, t2, t3 = self.textbox.toPlainText(
        ), self.textbox1.toPlainText(), self.textbox2.toPlainText()
        if t1:
            if all(i.isdigit() for i in t1):
                sum_ += int(t1)*3600
        if t2:
            if all(i.isdigit() for i in t2):
                sum_ += int(t2)*60
        if t3:
            if all(i.isdigit() for i in t3):
                sum_ += int(t3)
        if sum_ > 0:
            self.timer.startTimer(sum_)

    def updateTimer(self):
        if self.timer.getTimer() != True:
            self.timerLabel.setText(self.timer.getTimer())
        else:
            self.timerLabel.setText("0.00s")

    def stopTimer(self):
        self.timer.stopTimer()

    def restartTimer(self):
        self.timer.restartTimer()

    def setStopwatchTime(self):
        self.timer.startStopwatch()
        self.stflag = True
        self.stbutton = QPushButton("Lap")

    def stopStopwatchTime(self):
        self.timer.stopStopwatch()

    def updateStopwatch(self):
        if self.stflag:
            self.sttimeLabel.setText(self.timer.getStopwatch())
        else:
            self.sttimeLabel.setText("0.00s")

    def restartStopwatchTime(self):
        self.timer.restartStopwatch()

    def setStylesheet(self):
        self.setStyleSheet("""
        QWidget {
            background: #222222;
        }
        QLabel {
            color: white;
            font-size: 20px;
            font-family: Arial;
            padding: 5px 20px 5px 20px;
            background: #333333;
            border-radius: 10px;
            border: none;
            text-align: center;
        }
        QPushButton {
            color: white;
            font-size: 20px;
            border: 2px solid white;
            self.padding: 20px;
        }
        QTabBar {
            font-size: 20px;
        }
        QTabBar::tab:selected {
            padding: 5px 20px 5px 20px;
            color: white;
            background: #777777;
        }
        QTabBar::tab {
            padding: 5px 20px 5px 20px;
            color: black;
            background: #555555;
        }
        QPushButton:pressed {
            background: #333333;
        }
        """)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
