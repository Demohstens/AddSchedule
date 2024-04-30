PRIOTITY = {0: "High", 1: "Medium", 2: "Low"}
from datetime import datetime

class Task:
    def __init__(self, name, tags = "", due_date : datetime.date = datetime.now(), priority = 1, estimate = 45) -> None:
        self.name = name
        self.due_date = due_date
        self.priority = priority
        self._sort_score = self.time_left()["days"] + self.priority * 2
        self.is_completed = 0
        self.tags = tags.strip("#").split(" ")
        self.estimate = estimate
    
    def __repr__(self) -> str:
        return f"{self.name} due on {self.due_date} with {PRIOTITY[self.priority]} priority"

    def get_estimate(self):
        return self.estimate

    def _time_left(self):
        return self.due_date - datetime.now()
    def time_left(self):    
        time_difference = self.due_date-datetime.now()
        days = time_difference.days
        hours, remainder = divmod(time_difference.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return {"days": days, "hours":hours, "minutes":minutes}
    def __dict__(self):
        return {"name": self.name, "due_date": self.due_date, "priority": self.priority, "tags": self.tags, "estimate": self.estimate}

new = Task("Deutsch", "Deutsch", datetime(2024, 4, 23), 0, 45)
print(new)