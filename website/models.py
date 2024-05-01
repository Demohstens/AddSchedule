from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from json import loads

class Day(db.Model):
    date = db.Column(db.Date, primary_key=True)
    day_HTML = db.Column(db.String, default=None)
    user = db.Column(db.Integer, db.ForeignKey("user.id"))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128), unique=True)
    password = db.Column(db.String(128))
    username = db.Column(db.String(128), unique=True)
    is_private = db.Column(db.Boolean, default=False)
    untis_login = db.Column(db.String, default=None)
    untis_login_valid = db.Column(db.Boolean, default=False)
    days = db.relationship("Day")

    def get_untis_credentials(self):
        print(self.untis_login)
        return loads(self.untis_login.replace("'", '"'))
    
    #A database object for the untis PeriodObject. Do not touch without API. 
# class Period(db.Model):
#     # Dates and time
#     start = db.Column(db.DateTime(timezone=True), primary_key=True)
#     end = db.Column(db.DateTime(timezone=True))
#     # Requires a Converted List AND needs to be parsed.
#     klassen = db.Column(db.String)
#     teachers = db.Column(db.String)
#     rooms = db.Column(db.String)
#     # Subjects go here: TODO: Difficult
    
#     #Single String return values
#     code = db.Column(db.String(9), nullable=True)
#     type = db.Column(db.String(2))
#     lstext = db.Column(db.String)
#     info = db.Column(db.String)
#     activity_type = db.Column(db.String)
#     lsnumber = db.Column(db.String)
#     subst_text = db.Column(db.String)
#     # The Subject in the Lesson
#     subject = db.Column(db.Integer, db.ForeignKey("subject.id"))

#     # Get an attribute as a list by name
#     def get_list(self, arg):
#         return_list = []
#         match arg:
#             case "klassen":
#                 _ = self.klassen.replace("[", "").replace("]", "").replace("'", "").split(",")
#             case "teachers":
#                 _ = self.klassen.replace("[", "").replace("]", "").replace("'", "").split(",")
#             case "rooms":
#                 _ = self.klassen.replace("[", "").replace("]", "").replace("'", "").split(",")
#         for i in _:      
#             return_list.append(i.strip())
#         return return_list
    

# class Subject(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     # The String that the untis api returns for period.name! NOTHING ELSE! Redundency for Id. 
#     name = db.Column(db.String, unique=True)
#     # Start date, lstext, etc should either be called directly from the API or the own database for period or timetable. 
#     periods = db.relationship('Period')