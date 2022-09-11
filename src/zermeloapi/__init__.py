# from calendar import weekday
import os.path
import requests
import json
import time
import base64
# from datetime import datetime
import datetime
class zermelo:
    expires_in = 0
    school = ''
    username = ''
    teacher = False
    debug = False
    TimeToAddToUtc = 0

    def __init__(self, school, username,password=None, teacher=False, version=3,debug=False,linkcode=None):
        self.school = school
        self.username = username
        self.teacher = teacher
        self.debug = debug
        self.version = 'v'+str(version)
        self.TimeToAddToUtc = self.get_date()[2]
        if linkcode == None and password != None:
            self.token = self.get_tokenfromusrpsw(school=school,username=username,password=password)
        else:
            self.token = self.gettokenfromfile(linkcode=linkcode)

    def updatetoken(self, linkcode):
        self.token = self.gettokenfromfile(linkcode=linkcode)
    def gettokenfromlinkcode(self, linkcode=None):
        if linkcode == None:
            linkcode = input("apitoken: ").replace(" ",'')
        else:
            linkcode = str(linkcode).replace(" ",'')
        return json.loads(requests.post(f"https://ozhw.zportal.nl/api/v3/oauth/token?grant_type=authorization_code&code={linkcode}").text)["access_token"]
    def get_tokenfromusrpsw(self, school=None, username=None, password=None):
        if(school == None):
            school = self.school
        if (username == None):
            username = self.username
        if(password == None):
            password = self.password
        url = 'https://'+school+'.zportal.nl/api/'+self.version+'/oauth'
        myobj = {'username': username, 'password': password, 'client_id': 'OAuthPage', 'redirect_uri': '/main/',
                 'scope': '', 'state': '4E252A', 'response_type': 'code', 'tenant': school}
        x = requests.post(url, data=myobj)
        respons = x.text
        if self.debug:
            print(x.text)
        start = respons.find("code=") + len("code=")
        end = respons.find("&", start)
        token = respons[start:end]
        start = respons.find("tenant=") + len("tenant=")
        end = respons.find("&", start)
        school = respons[start:end]
        start = respons.find("expires_in=") + len("expires_in=")
        end = respons.find("&", start)
        self.expires_in = respons[start:end]
        start = respons.find("loginMethod=") + len("loginMethod=")
        end = respons.find("&", start)
        self.loginMethod = respons[start:end]
        start = respons.find("interfaceVersion=") + len("interfaceVersion=")
        end = respons.find("&", start)
        self.interfaceVersion = respons[start:end]
        if(school == None):
            school = self.school
        if(token == None):
            token = self.get_token()
        url = 'https://' + school+'.zportal.nl/api/'+self.version+'/oauth/token'
        myobj = {'code': token, 'client_id': 'ZermeloPortal', 'client_secret': 42,
                 'grant_type': 'authorization_code', 'rememberMe': False}
        l = requests.post(url, data=myobj)
        if self.debug:
            print(l.text)
        jl = json.loads(l.text)
        token = jl['access_token']
        return(token)

    def gettokenfromfile(self, file="./token", linkcode=None):
        if not os.path.exists(file):
            self.settokentofile(linkcode=linkcode)
        with open(file) as f:
            filevalue = f.read()
        return str(base64.b64decode(filevalue))[2:-1]
    def settokentofile(self,token=None,file="./token",linkcode=None):
        if token == None:
            token = self.gettokenfromlinkcode(linkcode=linkcode)
        file = str(base64.b64encode(bytes(token, "utf-8")))[2:-1]
        with open("./token", "w") as f:
            f.write(str(file))
    def get_date(self):
        timezoneinforeq = requests.get("http://worldtimeapi.org/api/ip").text
        if self.debug:
            print(timezoneinforeq)
        timezoneinfo = json.loads(str(timezoneinforeq))
        localtime = time.localtime(timezoneinfo["unixtime"])
        day = datetime.datetime.strptime(time.strftime("%y%d%m",localtime),"%y%d%m").weekday()
        offset_h = int(str(timezoneinfo["utc_offset"]).split(":")[0].replace("+", ""))
        year, week = localtime[0], timezoneinfo["week_number"]
        if day > 4:
            week = int(week)+1
        return year, week, offset_h
    

    def get_raw_schedule(self, year:int=None, week:int=None) -> dict:
        time = self.get_date()
        if year == None:
            year = time[0]
        if week == None:
            week = time[1]
        url = f"https://{self.school}.zportal.nl/api/v3/liveschedule?access_token={self.token}&{'teacher' if (self.teacher) else 'student'}={self.username}&week={year}{week}"
        if self.debug:
            print(url)
        rawr = requests.get(url)
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
            date = datetime.datetime.utcfromtimestamp(les["start"]).strftime('%Y%m%d')
            hour = str(int(datetime.datetime.utcfromtimestamp(
                les["start"]).strftime('%H')) + self.TimeToAddToUtc)
            time = datetime.datetime.utcfromtimestamp(les["start"]).strftime('%Y-%m-%d ') + (hour if int(
                hour) > 9 else ('0'+hour)) + datetime.datetime.utcfromtimestamp(les["start"]).strftime(':%M')
            ehour = str(int(datetime.datetime.utcfromtimestamp(
                les["end"]).strftime('%H')) + self.TimeToAddToUtc)
            etime = datetime.datetime.utcfromtimestamp(les["end"]).strftime('%Y-%m-%d ') + (ehour if int(
                ehour) > 9 else ('0'+ehour)) + datetime.datetime.utcfromtimestamp(les["end"]).strftime(':%M')
            # print(les["status"])
            if date != pdate:
                days.append([[], []])
            if self.debug:
                print(les)
            if not (les == None or len(les["status"]) < 1):
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
