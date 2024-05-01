import webuntis
import datetime
from unidecode import unidecode
import webuntis.session
from webuntis.objects import PeriodObject
from flask_login import current_user
from flask import session as flask_session

from .untis_login import login as login_untis_session

def check_holidays(session, start=datetime.datetime.now().date(), end=datetime.datetime.now().date()):
    holidays_in_range = []
    days_in_range = [start + datetime.timedelta(days=i) for i in range(datetime.timedelta(end-start or 1))]
    # holidays_in_week = [h.start.date().weekday() for h in holidays if h.start.date() in days_in_week]
    for h in session.holidays():
        if h.start.date() == h.end.date() and h.start.date() in holidays_in_range:
            holidays_in_range.append(h.start.date().weekday())
        else: 
            for d in [d for d in range((h.end.date()-h.start.date()).days)]:
                day_of_holiday = (h.start.date() + datetime.timedelta(days=d)) 
                if day_of_holiday in days_in_range:
                    holidays_in_range.append(day_of_holiday)  
    return holidays_in_range


def get_day(day : datetime.date = datetime.datetime.today()):
    if current_user.is_authenticated:
        session = login_untis_session()
    else:
        raise Exception("Could not find untis Session")
    table = session.my_timetable(start=day, end=day).to_table()
    periods : list = []
    #Will be set
    for time, row in table:
        for _, cell in (row):
            #Empty variables to get the data from the period and add it to HTML classes later
            # period_type = ""
            # subject_name = ""
            # period_code = "" 
            for period in cell:
                # period_code = period.code or "regular"
                # period_type = period.type
                # try:
                periods.append(period)   
                # except IndexError:
                #     pass
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
    return "".join(return_doc)