from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from alarm import Timer
import subprocess
import sys
import playsound


class EditAlarm(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(EditAlarm, self).__init__(*args, **kwargs)
        self.setWindowTitle("Edit Alarm")
        self.setGeometry(400, 20, 300, 200)
        self.timer = Timer()
        self.PMB = False
        self.alarmToBeRemoved = None
        self.initUI()
        self.setStylesheet()

    def initUI(self):
        self.centralWidget = QWidget()

        self.setCentralWidget(self.centralWidget)

        layout = QHBoxLayout()
        layout2 = QVBoxLayout()
        layout3 = QVBoxLayout()

        self.hourBox = QPlainTextEdit(self.centralWidget)
        self.hourBox.setLineWrapMode(False)
        self.hourBox.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.hourBox.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.minuteBox = QPlainTextEdit(self.centralWidget)
        self.minuteBox.setLineWrapMode(False)
        self.minuteBox.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.minuteBox.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.colon = QLabel(":")
        self.colon.setStyleSheet(
            "QLabel {width: 5px; background:#222222; padding:0;margin:0;}")
        self.amPm = QComboBox()
        self.amPm.addItems(["AM", "PM"])
        self.amPm.activated.connect(self.amPmActivated)
        layout.addWidget(self.hourBox)
        layout.addWidget(self.colon)
        layout.addWidget(self.minuteBox)
        layout.addWidget(self.amPm)

        self.addAlarmB = QPushButton("Add")
        self.addAlarmB.clicked.connect(self.startAlarm)
        layout2.addWidget(self.addAlarmB)

        self.removeAlarmCB = QComboBox()
        self.removeAlarmCB.addItems(self.timer.getAlarms().split("\n"))
        self.removeAlarmCB.activated.connect(self.removeAlarmCBActivated)
        layout2.addWidget(self.removeAlarmCB)

        self.removeAlarmB = QPushButton("Remove")
        self.removeAlarmB.clicked.connect(self.removeAlarm)
        layout2.addWidget(self.removeAlarmB)

        layout.setAlignment(Qt.AlignCenter)
        layout2.setAlignment(Qt.AlignCenter)
        layout3.setAlignment(Qt.AlignCenter)
        layout3.addLayout(layout)
        layout3.addLayout(layout2)

        self.centralWidget.setLayout(layout3)
        self.centralWidget.setStyleSheet("""
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
        QComboBox {
            padding-left: 10px;
            font-size: 16px;
            color: white;
            background: #444444;
            min-height: 30px;
            border: none;
            margin: 0;
            min-width: 100px;
        }
        QComboBox:drop-down {
            color: white;
        }
        QLabel {
            background: #222222;
        }
        """)

        timer = QTimer(self)

        timer.timeout.connect(self.updateAll)

        # update the timer every hundredth second
        timer.start(10)

        self.show()

    def startAlarm(self):
        t1, t2 = self.hourBox.toPlainText(), self.minuteBox.toPlainText()
        if t1 and t2:
            if all(i.isdigit() for i in t1) and int(t1) >= 1 and int(t1) <= 12 and all(i.isdigit() for i in t2) and int(t2) >= 0 and int(t2) <= 59:
                self.muted = False
                if self.PMB:
                    t1 = str((int(t1)+12) % 24)
                if len(t2) == 1:
                    t2 = "0" + t2
                if len(t1) == 1:
                    t1 = "0" + t1
                self.timer.alarm(t1+":"+t2)

    def removeAlarmCBActivated(self, index):
        if self.timer.getAlarms():
            self.alarmToBeRemoved = self.timer.getAlarms().split("\n")[index]

    def amPmActivated(self, index):
        if index == 1:
            self.PMB = True
        else:
            self.PMB = False

    def removeAlarm(self):
        if self.alarmToBeRemoved:
            temp = self.alarmToBeRemoved.split(" ")
            pmb = (temp[1] == "PM")
            t1, t2 = temp[0].split(":")
            if pmb:
                t1 = str((int(t1)+12) % 24)
            if len(t2) == 1:
                t2 = "0" + t2
            if len(t1) == 1:
                t1 = "0" + t1
            self.timer.cancelAlarm(t1+":"+t2)
            self.alarmToBeRemoved = None

    def updateAll(self):
        self.removeAlarmCB.clear()
        self.removeAlarmCB.addItems(self.timer.getAlarms().split("\n"))
        if not self.alarmToBeRemoved and self.timer.getAlarms():
            self.alarmToBeRemoved = self.timer.getAlarms().split("\n")[0]

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
            padding: 1px 20px 2px 20px;
        }
        QPushButton:pressed {
            background: #333333;
        }
        """)


class App(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(App, self).__init__(*args, **kwargs)
        self.setWindowTitle("AlarmClock")
        self.setGeometry(0, 0, 400, 300)
        self.timer = Timer()
        self.setStylesheet()
        self.stflag = False
        self.curC = 0
        self.ended = False
        self.PMB = False
        self.muted = False
        self.initUI()

    def initUI(self):

        self.alarmDialog = EditAlarm(self)
        self.alarmDialog.hide()

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
        self.textbox.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.textbox.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.textbox1 = QPlainTextEdit(self.tab3)
        self.textbox1.setLineWrapMode(False)
        self.textbox1.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.textbox1.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.textbox2 = QPlainTextEdit(self.tab3)
        self.textbox2.setLineWrapMode(False)
        self.textbox2.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.textbox2.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

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
        layout2 = QVBoxLayout()

        self.editAlarmB = QPushButton("Edit")
        self.editAlarmB.clicked.connect(self.editAlarm)
        layout2.addWidget(self.editAlarmB)

        self.muteAlarmB = QPushButton("Mute")
        self.muteAlarmB.clicked.connect(self.muteAlarm)
        self.muteAlarmB.hide()
        layout2.addWidget(self.muteAlarmB)
        self.alarmDisplay = QLabel("")
        self.alarmDisplay.setAlignment(Qt.AlignCenter)
        layout2.addWidget(self.alarmDisplay)
        '''self.cancleAlarmB = QPushButton("Cancel")
        self.cancleAlarmB.clicked.connect(self.cancelAlarm)
        layout2.addWidget(self.cancleAlarmB)'''

        layout2.setAlignment(Qt.AlignCenter)

        self.tab4 = QWidget()
        self.tab4.setLayout(layout2)
        self.tab4.setStyleSheet("""
        QPushButton {
            width: 200px;
            max-width: 300px;
        }
        QLabel {
            background: #222222;
        }
        """)

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
        self.updateAlarm()
        self.count = (self.count + 1) % 20

    def updateAlarm(self):
        self.updateAlarmDisplay()
        if self.timer.getAlarm():
            self.muteAlarmB.show()
            if not self.muted:
                if self.count == 0:
                    playsound.playsound("alarm.mp3", False)
        else:
            self.muted = False
            self.muteAlarmB.hide()

    def muteAlarm(self):
        self.muted = True

    def updateAlarmDisplay(self):
        self.alarmDisplay.setText(self.timer.getAlarms())

    def cancelAlarm(self, t):
        self.timer.cancelAlarm(t)
        self.muteAlarmB.hide()
        self.alarmDisplay.setText("")

    def editAlarm(self):
        self.alarmDialog.show()
        self.alarmDialog.raise_()

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
            self.ended = False
            self.timerLabel.setText(self.timer.getTimer())
        else:
            if not self.ended:
                playsound.playsound("alarm.mp3", False)
                self.restartTimer()
                self.ended = True
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
            padding: 1px 20px 2px 20px;
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
