import datetime
from unidecode import unidecode
from ..utils.untis_login import login as login_untis_session
from flask import session as flask_session

def update(session=None):
    try:
        session = flask_session["untis_session"]
        print("Session found")
        print(session)
    except KeyError:
        login_untis_session()
        session = session["untis_session"]

    # today = datetime.date(2024, 5, 20)
    today = datetime.date.today()
    day = None

    if today.weekday() == 5 or today.weekday() == 6:
        day = today
        while day.weekday() == 5 or day.weekday() == 6:
            day += datetime.timedelta(days=1)
    if day:
        monday = day
    else:
        monday = today - datetime.timedelta(days=today.weekday())
    friday = monday + datetime.timedelta(days=4)

    # List of all periods in table format.
    table = session.my_timetable(start=monday, end=friday).to_table()

    # List of ALL holidays ("ever")
    holidays = session.holidays()

    # Days in the current week as datetime.date objects in a list
    # list<date>
    days_in_week = [monday + datetime.timedelta(days=i) for i in range(5)]
    # for i in range(5):
    #     days_in_week.append(monday + datetime.timedelta(days=i)) 
    #     #datetime.datetime.date

    # List of datetime.dates WITHIN in the week
    holidays_in_week = []
    # holidays_in_week = [h.start.date().weekday() for h in holidays if h.start.date() in days_in_week]
    for h in holidays:
        if h.start.date() == h.end.date() and h.start.date() in days_in_week:
            holidays_in_week.append(h.start.date().weekday())
        else: 
            for d in [d for d in range((h.end.date()-h.start.date()).days)]:
                day_of_holiday = (h.start.date() + datetime.timedelta(days=d)) 
                if day_of_holiday in days_in_week:
                    holidays_in_week.append(day_of_holiday)

    #Clear and reopen the file. #TODO Could be optmized by using a list and .join at the end?
    ret = []

    #Create HTML Table
    ret.append(f'<table border="1" class="draggable timetable" start-date="{str(monday)}" end-date="{str(friday)}"  draggable="true"><thead><th>Time</th>')


    for day_index, weekday in enumerate(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']):
        ret.append(f'<th class="{weekday} {monday + datetime.timedelta(days=day_index)}">' + str(weekday) + '</th>')

    ret.append('</thead><tbody>')
    for time, row in table:
        ret.append('<tr>')
        ret.append('<td>{}</td>'.format(time.strftime('%H:%M')))
        weekday_index = 0
        for i in range(5):
            if i in holidays_in_week:
                ret.append('<td class="holiday"></td>')
                continue
            try:
                date, cell = row[weekday_index]
                weekday_index += 1
            except IndexError:
                break
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
                        sub_name += f'<p class=substtext>{unidecode(period.substText)} </p>'
                    if period.info:
                        sub_name += f'<p class=periodinfo>{unidecode(period.info)}</p>'
                except IndexError:
                    pass
            ret.append(f'<td class="{period_type} {period_code}"><a href="/s/{subject_name.replace(" ", "-").replace("/", "-")}">')
            if sub_name:
                ret.append(sub_name)
            ret.append('</a></td>\n')
            sub_name = None
        ret.append('</tr>\n')
    ret.append('</tbody></table>')
    return ret
