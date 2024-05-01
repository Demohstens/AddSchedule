import datetime
from webuntis.objects import PeriodObject

from ..utils.untis import get_day
# the untis api should return a list of PeriodObject obejct
class Day():
    def __init__(self, date : datetime.date) -> None:
        self.date : datetime.date =  date
        self.periods : list[PeriodObject] = get_day(day=date)
        self.times = set(p.start for p in self.periods)
        
    def to_html(self):
        ret = []
        for t in self.times:
            ret.append(f"<p>{t.strftime('%H:%M')}</p>")  # Format time as HH:MM
        for p in self.periods:
            ret.append(p.lstext)
        return "".join(ret)
