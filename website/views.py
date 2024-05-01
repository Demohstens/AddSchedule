from flask import redirect, url_for, Blueprint, get_flashed_messages,  render_template, flash, request, session
from flask_login import  login_required, current_user
from datetime import datetime

from website.Objects._Timetable import update as update_untis
from website.utils.calendar import update as update_calendar
import website.utils.untis_login as untis

from .Objects.Day import Day 
from .models import User
from . import db
from .utils.untis_login import check_credentials

views = Blueprint("views", __name__)

@views.route("/@<username>")
def profile(username):
    user = User.query.filter_by(username=username).first()
    try:
        if not user.is_private:
            get_flashed_messages()
            return render_template("profile.html", username = username)
        else:
            flash("User's profile is set to private. Login to view.")
    except AttributeError:
        flash("User does not exist.")
        return redirect(request.origin)

@views.route("/")
def index():
    get_flashed_messages()
    return render_template("index.html")

@views.route("/calendar")
@login_required
def calendar():
    update_calendar()
    return redirect("/")

@views.route("/d/<date>")
@login_required
def day(date):
    # Date var to date obj.:
    year, month, day = map(int, date.split("-"))
    day = Day(datetime(year=2024, month=5, day=2))
    print(day)
    print(day.periods)
    print(day.to_html())
    return day.to_html()
    #return render_template("debug.html", date=date)


@views.route("/s/<subject>")
@login_required
def subject(subject):
    return render_template("subject.html", subject=subject)

@views.route("/timetable")
def timetable():
    return render_template("timetable.html")
  
@views.route("/update-timetable")
@login_required  
def update_timetable():
    if current_user.untis_login_valid:
        try:
            untis_session = session["untis_session"]
        except KeyError:
            untis_session = untis.login(current_user)
        update_untis(untis_session)
        return redirect("/")
    else:
        if untis.check_credentials(user=current_user):
            update_calendar()
        else:
         return redirect(url_for("auth.untis_login"))
         

@views.route("/error")
def error(error, error_code=None):
    return render_template("error.html", error=error, error_code=error_code)