import io

from flask import abort, flash, url_for, redirect, send_file, render_template
from flask_login import current_user, login_required

from utils.crud import (
    reject_user,
    approve_user,
    get_user_by_address,
    get_unverified_users,
)

from . import admin_bp


@admin_bp.route("/admin", methods=["GET"])
@login_required
def _index():
    if not current_user.admin:
        return redirect(url_for("app._index"))

    unverified_users = get_unverified_users()

    return render_template("admin/index.html", unverified_users=unverified_users)


@admin_bp.route("/admin/approve/<address>", methods=["GET"])
@login_required
def _approve(address):
    if not current_user.admin:
        return redirect(url_for("app._index"))

    approve_user(address)
    flash("User approved.", "success")
    return redirect(url_for("admin._index"))


@admin_bp.route("/admin/reject/<address>", methods=["GET"])
@login_required
def _reject(address):
    if not current_user.admin:
        return redirect(url_for("app._index"))

    reject_user(address)
    flash("User rejected.", "error")
    return redirect(url_for("admin._index"))


@admin_bp.route("/admin/render_id/front/<address>", methods=["GET"])
@login_required
def _render_id_front(address):
    if not current_user.admin:
        return redirect(url_for("app._index"))

    user = get_user_by_address(address)

    if user and user.id_front:
        return send_file(
            io.BytesIO(user.id_front),
            mimetype="image/jpeg",
            as_attachment=False,
            download_name=f"{user.username}_id_front.jpg",
        )

    return abort(404)


@admin_bp.route("/admin/render_id/back/<address>", methods=["GET"])
@login_required
def _render_id_back(address):
    if not current_user.admin:
        return redirect(url_for("app._index"))

    user = get_user_by_address(address)

    if user and user.id_back:
        return send_file(
            io.BytesIO(user.id_back),
            mimetype="image/jpeg",
            as_attachment=False,
            download_name=f"{user.username}_id_back.jpg",
        )

    return abort(404)
