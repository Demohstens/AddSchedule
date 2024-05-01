import datetime

from ..utils.untis import get_day
# the untis api should return a list of PeriodObject obejct
class Day():
    def __init__(self, date : datetime.date) -> None:
        self.date : datetime.date =  date
        self.periods = get_day(day=date)
        self.times = set(p.start for p in self.periods)