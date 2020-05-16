import time
import datetime


class Timer():
    def __init__(self):
        self.timerStartTime = None
        self.timerGoal = None
        self.timerLeft = "0.00s"
        self.timerP = True
        self.timerPrev = 0

        self.stopwatchStart = None
        self.prev = 0
        self.prevTime = None
        self.stpaused = True

        self.m = {"s": 1, "m": 60, "h": 3600}

    def startTimer(self, t):
        if self.timerP:
            if self.timerPrev:
                self.timerGoal = self.timerPrev
            else:
                self.timerGoal = int(t)
            self.timerStartTime = time.time()
            self.timerP = False

    def getTimer(self):
        if self.timerP:
            return self.timerLeft
        if self.timerStartTime:
            if self.timerGoal <= time.time() - self.timerStartTime:
                return True
            if (self.timerGoal - time.time() + self.timerStartTime) > 3600:
                return "%ih %im %0.2fs" % (int((self.timerGoal - time.time() + self.timerStartTime)//3600), ((self.timerGoal - time.time() + self.timerStartTime) % 3600) // 60, ((self.timerGoal - time.time() + self.timerStartTime) % 60))
            elif (self.timerGoal - time.time() + self.timerStartTime) > 60:
                return "%im %0.2fs" % (int((self.timerGoal - time.time() + self.timerStartTime)//60), ((self.timerGoal - time.time() + self.timerStartTime) % 60))
            else:
                return "%0.2fs" % (self.timerGoal - time.time() + self.timerStartTime)
        else:
            return None

    def stopTimer(self):
        if not self.timerP:
            self.timerLeft = self.getTimer()
            self.timerPrev = self.timerGoal - time.time() + self.timerStartTime
            self.timerP = True

    def restartTimer(self):
        self.timerP = True
        self.timerGoal = None
        self.timerStartTime = None
        self.timerLeft = "0.00s"
        self.timerPrev = 0

    def startStopwatch(self):
        if self.stpaused:
            self.stopwatchStart = time.time()
            self.stpaused = False

    def stopStopwatch(self):
        if not self.stpaused:
            self.prevTime = self.getStopwatch()
            self.prev = time.time() - self.stopwatchStart + self.prev
            self.stopwatchStart = None
            self.stpaused = True

    def restartStopwatch(self):
        self.prev = 0
        self.prevTime = "0.00s"
        self.stopwatchStart = None
        self.stpaused = True

    def getStopwatch(self):
        if self.stpaused:
            return self.prevTime
        if time.time() - self.stopwatchStart + self.prev > 3600:
            return "%ih %im %0.2fs" % ((time.time() - self.stopwatchStart + self.prev)//3600, ((time.time() - self.stopwatchStart + self.prev) % 3600)//60, ((time.time() - self.stopwatchStart + self.prev) % 60))
        elif time.time() - self.stopwatchStart + self.prev > 60:
            return "%im %0.2fs" % ((time.time() - self.stopwatchStart + self.prev)//60, ((time.time() - self.stopwatchStart + self.prev) % 60))
        else:
            return "%0.2fs" % (time.time() - self.stopwatchStart + self.prev)

    def alarm(self, t):
        with open("alarms.txt", "r") as fin:
            cur = set(fin.read().split("\n"))
        with open("alarms.txt", "w") as fout:
            cur.add(t)
            fout.write("\n".join(cur))

    def getAlarms(self):
        with open("alarms.txt", "r") as fin:
            cur = [i for i in fin.read().split("\n") if i]
            cur.sort(key=lambda x: [
                int(x.split(":")[0]), int(x.split(":")[1])])
            ans = ""
            for i in cur:
                if self.getSingleAlarm(i):
                    i = i.split(":")
                    if int(i[0]) > 12:
                        ans += "-- " + str(int(i[0])-12) + \
                            ":" + i[1] + " PM" + " --" + "\n"
                    elif int(i[0]) == 0:
                        ans += "-- " + "12" + \
                            ":" + i[1] + " PM" + " --" + "\n"
                    else:
                        ans += "-- " + str(int(i[0])) + \
                            ":"+i[1] + " AM" + " --" + "\n"
                else:
                    i = i.split(":")
                    if int(i[0]) > 12:
                        ans += str(int(i[0])-12) + \
                            ":" + i[1] + " PM" + "\n"
                    elif int(i[0]) == 0:
                        ans += "12" + ":" + i[1] + " PM" + "\n"
                    else:
                        ans += str(int(i[0])) + \
                            ":"+i[1] + " AM" + "\n"
            return ans.rstrip()

    def cancelAlarm(self, t):
        with open("alarms.txt", "r") as fin:
            cur = fin.read().split("\n")
        with open("alarms.txt", "w") as fout:
            fout.write("\n".join([i for i in cur if i != t]).strip())

    def getAlarm(self):
        with open("alarms.txt", "r") as fin:
            cur = fin.read().split("\n")
        for i in cur:
            if ":".join(str(datetime.datetime.today()).split(
                    ".")[0].split(" ")[1].split(":")[0:2]) == i:
                return True
        return False

    def getSingleAlarm(self, t):
        return ":".join(str(datetime.datetime.today()).split(
            ".")[0].split(" ")[1].split(":")[0:2]) == t

    def getTime(self):
        return str(datetime.datetime.today()).split(".")[0]

    def getAlarmTime(self):
        return ":".join(str(datetime.datetime.today()).split(".")[0].split(":")[:-1])

    def getDay(self):
        weekDays = ("Monday", "Tuesday", "Wednesday",
                    "Thursday", "Friday", "Saturday", "Sunday")
        return weekDays[datetime.datetime.today().weekday()]

    def getRn(self):
        return datetime.datetime.now()


if __name__ == "__main__":
    print(str(datetime.datetime.today()).split(".")[0])
