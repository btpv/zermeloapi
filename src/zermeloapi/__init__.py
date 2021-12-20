class zermelo:
    expires_in = 0
    school = ''
    username = ''
    password = ''
    teacher = False
    TimeToAddToUtc = 0
    access_token = ''

    def __init__(self, school, username, password, teacher=False, version=3):
        self.school = school
        self.username = username
        self.password = password
        self.teacher = teacher
        self.version = 'v'+str(version)
        self.TimeToAddToUtc = self.get_date()[2]
        self.access_token = self.get_access_token()

    def get_date(self):
        from datetime import date, datetime
        year, week = date.today().strftime("%Y %W").split(" ")
        if date.today().isoweekday() > 6:
            week = str(int(week)+1)
        TimeToAddToUtc = int(
            str(datetime.now().astimezone()).split("+")[1].split(":")[0])
        return year, week, TimeToAddToUtc

    def refresh(self):
        self.access_token = self.get_access_token()
        return(self.expires_in)

    def get_token(self, school=None, username=None, password=None):
        if(school == None):
            school = self.school
        if (username == None):
            username = self.username
        if(password == None):
            password = self.password
        import requests
        url = 'https://'+school+'.zportal.nl/api/'+self.version+'/oauth'
        myobj = {'username': username, 'password': password, 'client_id': 'OAuthPage', 'redirect_uri': '/main/',
                 'scope': '', 'state': '4E252A', 'response_type': 'code', 'tenant': school}
        x = requests.post(url, data=myobj)
        respons = x.text
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
        return(token)

    def get_access_token(self, school=None, token=None):
        if(school == None):
            school = self.school
        if(token == None):
            token = self.get_token()
        import requests
        url = 'https://' + school+'.zportal.nl/api/'+self.version+'/oauth/token'
        myobj = {'code': token, 'client_id': 'ZermeloPortal', 'client_secret': 42,
                 'grant_type': 'authorization_code', 'rememberMe': False}
        l = requests.post(url, data=myobj)
        import json
        jl = json.loads(l.text)
        access_token = jl['access_token']
        return(access_token)

    def get_schedule(self, year=None, week=None):
        time = self.get_date()
        if year == None:
            year = time[0]
        if week == None:
            week = time[1]
        import requests
        import json
        try:
            headers = {"Authorization": "Bearer "+self.access_token}
            rawr = requests.get('https://' + self.school + '.zportal.nl/api/'+self.version+'/liveschedule?'+("teacher" if (self.teacher) else "student")+'='+self.username+'&week='+str(year)+str(week) +
                                '&fields=appointmentInstance,start,end,startTimeSlotName,endTimeSlotName,subjects,groups,locations,teachers,cancelled,changeDescription,schedulerRemark,content,appointmentType', headers=headers)
            rl = json.loads(rawr.text)
            response = rl["response"]
            data = response["data"][0]
            appointments = data["appointments"]
        except:
            self.refresh()
            headers = {"Authorization": "Bearer "+self.access_token}
            rawr = requests.get('https://' + self.school + '.zportal.nl/api/'+self.version+'/liveschedule?'+("teacher" if (self.teacher) else "student")+'='+self.username+'&week='+str(year)+str(week) +
                                '&fields=appointmentInstance,start,end,startTimeSlotName,endTimeSlotName,subjects,groups,locations,teachers,cancelled,changeDescription,schedulerRemark,content,appointmentType', headers=headers)
            rl = json.loads(rawr.text)
            response = rl["response"]
            data = response["data"][0]
            appointments = data["appointments"]
        return(appointments)

    def sort_schedule(self, schedule=None, year=None, week=None):
        if(schedule == None):
            schedule = self.get_schedule(year=year, week=week)
        pdate = 0
        days = [[[], []]]
        for les in schedule:
            from datetime import datetime
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
