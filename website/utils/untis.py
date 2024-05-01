import webuntis
import datetime
from unidecode import unidecode
import webuntis.session
from webuntis.objects import PeriodObject
from flask_login import current_user
from .untis_login import login, logout

def get_day(session : webuntis.session = None, day : datetime.date = datetime.datetime.today()):
    logout_required = False
    if session == None and current_user.is_authenticated:
        session = login(current_user)
        logout_required = True
    table = session.my_timetable(start=day, end=day).to_table()
    periods = []
    #Will be set
    for time, row in table:
        for _, cell in (row):
            #Empty variables to get the data from the period and add it to HTML classes later
            period_type = ""
            subject_name = ""
            period_code = "" 
            for period in cell:
                period_code = period.code or "regular"
                period_type = period.type
                try:
                    #periods.append({"sart" : period.start, "end" : period.end, "klassen" : period.klassen, "teachers" : period.teachers })
                    periods.append(PeriodObject)
                except IndexError:
                    pass
    times = set(p.start for p in periods)
    if logout_required:
        logout(session=session)
    return periods

def get_week(session : webuntis.session):
    return_doc = []
    # prefered: with webuntis.Session(...).login() as s:
    today = datetime.date.today()
    if today.weekday() == 5 or today.weekday() == 6:
        day = today
        while day.weekday() == 5 or day.weekday() == 6:
            day += datetime.timedelta(days=1)
    monday = day or today - datetime.timedelta(days=today.weekday())
    friday = monday + datetime.timedelta(days=4)

    table = session.my_timetable(start=monday, end=friday).to_table()
    open("./website/templates/timetable.html", "w").close()
    f = open("./website/templates/timetable.html", "a")

    #Create HTML Table
    return_doc.append(f'<table border="1" class="draggable timetable" start-date="{str(monday)}" end-date="{str(friday)}"  draggable="true"><thead><th>Time</th>')

    for day_index, weekday in enumerate(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']):
        return_doc.append(f'<th class="{weekday} {monday + datetime.timedelta(days=day_index)}">' + str(weekday) + '</th>')

    return_doc.append('</thead><tbody>')
    for time, row in table:
        return_doc.append('<tr>')
        return_doc.append('<td>{}</td>'.format(time.strftime('%H:%M')))
        for date, cell in (row):
            print(str(date))
            #Empty variables to get the data from the period and add it to HTML classes later
            period_type = ""
            subject_name = ""
            period_code = "" 
            for period in cell:
                period_code = period.code or "regular"
                period_type = period.type
                try:
                    subject_name = unidecode(', '.join(su.name for su in period.subjects))
                    sub_name = (f'<p class=lsname>{subject_name}</p>')
                    if period.lstext:
                        sub_name += f'<p class=lstext>{unidecode(period.lstext)}</p>'
                    if period.substText:
                        sub_name += f'<p class=substtext>{unidecode(period.substText)}</p>'
                except IndexError:
                    pass
            return_doc.append(f'<td class="{period_type} {period_code}"><a href="/s/{subject_name.replace(" ", "-").replace("/", "-")}">')
            if sub_name:
                return_doc.append(sub_name)
            return_doc.append('</a></td>')
            sub_name = None
        return_doc.append('</tr>')
    return_doc.append('</tbody></table>')
    
    print("Updated Timetable.html")
    if logout_required:
        logout(session)
    return "".join(return_doc)

if __name__ == "__main__":
    from website.utils.untis_login import login, logout
    s = login()
    get_day(session=s, day=datetime.datetime(2024, 4, 29))
    logout(s)