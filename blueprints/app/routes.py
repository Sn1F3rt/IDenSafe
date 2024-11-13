from flask import render_template
from flask_login import login_required

from . import app_bp


@app_bp.route("/app", methods=["GET"])
@login_required
def _index():
    return render_template("app/index.html")
