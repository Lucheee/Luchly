from flask import Blueprint, render_template
from flask_login import current_user

base = Blueprint("base", __name__)


@base.route("/")
def home():
    return render_template("index.html", user=current_user)