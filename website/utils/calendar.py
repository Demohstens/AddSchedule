from calendar import *
import datetime

def update():
    cal = HTMLCalendar()
    now =datetime.datetime.now()
    f = open("./website/templates/calendar.html", "w")
    f.write(formatmonth(cal=cal, theyear=now.year, themonth=now.month, now=now))
    f.close


def formatmonth(cal, theyear, themonth, withyear=True, now=datetime.datetime.now()):
    """
    Return a formatted month as a table.
    """
    v = []
    a = v.append
    a('<table class="%s draggable calendar" draggable="true">' % (
        cal.cssclass_month))
    a('\n')
    a(cal.formatmonthname(theyear, themonth, withyear=withyear))
    a('\n')
    a(cal.formatweekheader())
    a('\n')
    for week in cal.monthdays2calendar(theyear, themonth):
        a(formatweek(cal, week, now=now))
        a('\n')
    a('</table>')
    a('\n')
    return ''.join(v)

def formatday(cal, day, weekday, now=datetime.datetime.now()):
    """
    Return a day as a table cell.
    """
    if day == 0:
        # day outside month
        return '<td class="%s">&nbsp;</td>' % cal.cssclass_noday
    else:
        try:
            month = now.month
        except AttributeError:
            print(type(now))
        if len(str(now.month)) < 2:
            month = f"0{now.month}"
        if len(str(day)) < 2:
            day = f"0{day}"
        if now.date().day == day:
            return f'<td class="%s today"><a href="/d/{now.year}-{month}-{day}">%d</a></td>' % (cal.cssclasses[weekday], day)
        else:
            return f'<td class="%s"><a href="/d/{now.year}-{month}-{day}">%d</a></td>' % (cal.cssclasses[weekday], int(day))
    
def formatweek(cal, theweek, now=datetime.datetime.now()):
    """
    Return a complete week as a table row.
    """
    s = ''.join(formatday(cal,d, wd, now=now) for (d, wd) in theweek)
    return '<tr>%s </tr>' % s

if __name__ == "__main__":
    update()