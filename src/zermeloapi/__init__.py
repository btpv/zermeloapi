import os.path
import requests
import json
import time
import base64
from datetime import datetime
class zermelo:
    expires_in = 0
    school = ''
    username = ''
    teacher = False
    debug = False
    TimeToAddToUtc = 0
    access_token = ''

    def __init__(self, school, username, teacher=False, version=3,debug=False,linkcode=None):
        self.school = school
        self.username = username
        self.teacher = teacher
        self.debug = debug
        self.version = 'v'+str(version)
        self.TimeToAddToUtc = self.get_date()[2]
        self.token = self.gettokenfromfile(linkcode=linkcode)

    def updatetoken(self, linkcode):
        self.token = self.gettokenfromfile(linkcode=linkcode)
    def gettokenfromlinkcode(self, linkcode=None):
        if linkcode == None:
            linkcode = input("apitoken: ").replace(" ",'')
        else:
            linkcode = linkcode.replace(" ",'')
        return json.loads(requests.post(f"https://ozhw.zportal.nl/api/v3/oauth/token?grant_type=authorization_code&code={linkcode}").text)["access_token"]

    def gettokenfromfile(self, file="./token", linkcode=None):
        if not os.path.exists(file):
            self.settokentofile(linkcode=linkcode)
        with open(file) as f:
            filevalue = f.read()
        return base64.b64decode(filevalue)
    def settokentofile(self,token=None,file="./token",linkcode=None):
        if token == None:
            token = self.gettokenfromlinkcode(linkcode=linkcode)
        file = (base64.b64encode(bytes(token, "utf-8")))[2:-1]
        with open("./token", "w") as f:
            f.write(str(file))
    def get_date(self):
        timezoneinforeq = requests.get("http://worldtimeapi.org/api/ip").text
        if self.debug:
            print(timezoneinforeq)
        timezoneinfo = json.loads(str(timezoneinforeq))
        localtime = time.localtime(timezoneinfo["unixtime"]-946728000)
        offset_h = int(str(timezoneinfo["utc_offset"]).split(":")[0].replace("+", ""))
        year, week = localtime[0], timezoneinfo["week_number"]
        if localtime[4] > 4:
            week = int(week)+1
        return year, week, offset_h
    

    def get_raw_schedule(self, year:int=None, week:int=None) -> dict:
        time = self.get_date()
        if year == None:
            year = time[0]
        if week == None:
            week = time[1]
            ("teacher" if (self.teacher) else "student")+'='+self.username+'&week='+str(year)+str(week)
        rawr = requests.get(f"https://ozhw.zportal.nl/api/v3/liveschedule?access_token={self.token}&{'teacher' if (self.teacher) else 'student'}={self.username}&week={year}{week}")
        if self.debug:
            print(rawr)
        rl = json.loads(rawr.text)
        return rl
    def get_schedule(self,rawschedule:dict=None,year=None, week=None):
        if rawschedule == None:
            rawschedule = self.get_raw_schedule(year=year,week=week)
        response = rawschedule["response"]
        data = response["data"][0]
        appointments = data["appointments"]
        return(appointments)

    def sort_schedule(self, schedule=None, year=None, week=None):
        if(schedule == None):
            schedule = self.get_schedule(year=year, week=week)
        pdate = 0
        days = [[[], []]]
        for les in schedule:
            date = datetime.utcfromtimestamp(les["start"]).strftime('%Y%m%d')
            hour = str(int(datetime.utcfromtimestamp(
                les["start"]).strftime('%H')) + self.TimeToAddToUtc)
            time = datetime.utcfromtimestamp(les["start"]).strftime('%Y-%m-%d ') + (hour if int(
                hour) > 9 else ('0'+hour)) + datetime.utcfromtimestamp(les["start"]).strftime(':%M')
            ehour = str(int(datetime.utcfromtimestamp(
                les["end"]).strftime('%H')) + self.TimeToAddToUtc)
            etime = datetime.utcfromtimestamp(les["end"]).strftime('%Y-%m-%d ') + (ehour if int(
                ehour) > 9 else ('0'+ehour)) + datetime.utcfromtimestamp(les["end"]).strftime(':%M')
            # print(les["status"])
            if date != pdate:
                days.append([[], []])
            if (les["status"][0]["code"] < 3000 and les["status"][0]["code"] >= 2000):
                days[-1][0].append([les["subjects"][0], time, etime,
                                    str(les["locations"]), les["status"], les["online"]])
            else:
                days[-1][1].append([les["subjects"][0], time, etime,
                                    str(les["locations"]), les["status"], les["online"]])
            pdate = date
        days.pop(0)
        return(days)

    def readable_schedule(self, days=None, year=None, week=None):
        result = ''
        if(days == None):
            days = self.sort_schedule(year=year, week=week)
        daysofweek = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        for i,day in enumerate(days):
            if len(day[0]) > 0:
                result += (daysofweek[i]+"\nstart: "+day[0][0][1]+"\tend: "+day[0][-1][2]+'\n')
            else:
                result += (f"{daysofweek[i]}\n")
            for les in day[0]:
                if (les[4][0]["code"] < 3000 and les[4][0]["code"] >= 2000):
                    result += ("les: "+les[0].ljust(10, " ")+"lokaal: "+("📷"if(les[5])else (les[3][2:-2]if(
                        len(les[3][2:-2]) > 0)else "----")).ljust(10, " ")+"\tstart: "+les[1]+"\tend: "+les[2]+'\n')
                    pass
            result += ("\n\n")
        return result

    def print_schedule(self, readable=None, days=None, year=None, week=None):
        if(readable == None):
            readable = self.readable_schedule(days=days, year=year, week=week)
        print(readable)
