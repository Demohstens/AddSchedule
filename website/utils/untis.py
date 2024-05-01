import webuntis
import datetime
from unidecode import unidecode
import webuntis.session

def get_day(session : webuntis.session, day : datetime.date = datetime.datetime.today(), is_first_or_only_day = False):
    table = session.my_timetable(start=day, end=day).to_table()
    return_doc = []


    #Create HTML Table head
    return_doc.append(f'<table border="1" class="timetable" date="{day}"><thead>')
    #Only add the Time Column if the hour is the first in a sequence (By multiplying string by boolean)
    return_doc.append('<th>Time</th>' * is_first_or_only_day)
    weekday = {0: "Monday", 1:"Tuesday", 2: "Wednesday", 3: "Thursday", 4: "Friday"}
    return_doc.append(f'<th class="{str(day).replace("-", "")}">' + str(weekday.get(day.weekday())) + '</th>')
    return_doc.append('</thead><tbody>\n')

    #HTML Table body
    for time, row in table:
        return_doc.append('<tr class="timetable_row">')
        return_doc.append('<td>{}</td>'.format(time.strftime('%H:%M')) * is_first_or_only_day)
        for _, cell in (row):
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
    
    return "".join(return_doc)

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
    return "".join(return_doc)

if __name__ == "__main__":
    from website.utils.untis_login import login, logout
    s = login()
    get_day(session=s, day=datetime.datetime(2024, 4, 29))
    logout(s)